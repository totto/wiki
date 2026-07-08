---
title: "Versioning Decision Models"
description: "How Lodestar versions its scoring models: semantic versions, a content hash, model drift that forces reanalysis, safe migrations, and keeping old scores explainable."
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Versioning Decision Models

A scoring model is not code that sits still. Weights get retuned, a variable gets redefined, a band boundary moves, someone fixes a decay curve. Every one of those edits changes what a score *means*. If you cannot say precisely which version of the model produced a given number, you cannot reproduce it, you cannot defend it, and you cannot explain to a buyer why their priority dropped from "High" to "Interesting but with gaps" overnight. Versioning is the discipline that keeps a score attached to the rules that made it.

This page covers how the Lodestar stack versions its deterministic scoring models: the semantic version, the content hash, how a version change triggers reanalysis through drift detection, and how you migrate without stranding historical decisions.

## Two identifiers, two jobs

Every score in Lodestar carries a `modelVersion` and a `modelHash`. They answer different questions.

- **`modelVersion`** is a human-facing semantic version — `2.3.0`. It communicates intent: did this change break comparability, or is it a safe additive tweak?
- **`modelHash`** is a machine-facing content hash of the resolved model definition — weights, variable list, band boundaries, decay table. It answers "is the running model byte-for-byte the one I think it is?" Two people can both claim to run `2.3.0`; only the hash proves they run the *same* `2.3.0`.

I follow ordinary semantic-versioning rules, but the "public API" is the meaning of the score:

| Bump | When | Comparability with prior scores |
|------|------|-------------------------------|
| **major** | weight change, layer added/removed, band boundary moved, variable redefined | broken — old and new scores are not comparable |
| **minor** | variable added that is optional, new descriptive metadata, decay curve refined | degraded — treat with care |
| **patch** | documentation, non-scoring metadata, comment fixes | preserved |

The rule I hold to: **any change that can move a number is at least a major bump.** A BUYER score is a weighted composite of the Need (0.40), Attractiveness (0.25) and Winnability (0.35) layers; nudge any of those weights and every historical comparison silently lies. Better to burn a major version than to pretend nothing moved.

## Where the version lives

The models are declared as governed [KCP units](/topics/defendable-agents/kcp/declaring-governed-units/), so version selection is deterministic and never a silent swap. The manifest pins both the semantic version and, at load time, the hash is recomputed and checked.

```yaml
kind: manifest
metadata:
  name: lodestar-scoring
  version: 2.3.0
  domain: professional-services-market
  temporal:
    valid_from: 2026-06-01
    refresh_interval: P30D
units:
  - id: buyer-score-model
    path: models/buyer.score.json
    tags: [scoring, buyer, governed]
    description: "3-layer weighted BUYER model (Need/Attractiveness/Winnability)"
  - id: match-score-model
    path: models/match.score.json
    tags: [scoring, match, governed]
    depends_on: [buyer-score-model]
```

The resolved model that actually runs carries the identifiers into every score:

```json
{
  "modelVersion": "2.3.0",
  "modelHash": "sha256:9f2c...b41e",
  "layers": {
    "need":          { "weight": 0.40, "variables": 6 },
    "attractiveness":{ "weight": 0.25, "variables": 6 },
    "winnability":   { "weight": 0.35, "variables": 6 }
  },
  "bands": [
    { "min": 85, "label": "Very high" },
    { "min": 70, "label": "High" },
    { "min": 55, "label": "Interesting but with gaps" },
    { "min": 40, "label": "Lower priority" },
    { "min": 0,  "label": "Not prioritized now" }
  ]
}
```

## Version change is model drift

This is where versioning stops being bookkeeping and starts having teeth. Every Lodestar score creates a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/): `{ scoredAt, dataAsOf, signalDates[], modelVersion, modelHash }`. The drift check compares that pin against current state and classifies the gap:

- **DATA drift** — `currentDataAsOf > pin.dataAsOf`
- **MODEL drift** — the pinned model version (or hash) differs from the live one
- **TEMPORAL drift** — pin age in days exceeds `maxAgeDays` (default 30)

The recommendation logic treats model drift as special:

```typescript
function recommend(reasons: DriftReason[]): "ok" | "monitor" | "reanalyze" {
  const hasModelDrift = reasons.some(r => r.kind === "MODEL");
  if (hasModelDrift) return "reanalyze";       // model drift alone forces it
  if (reasons.length >= 2) return "reanalyze";
  if (reasons.length === 1) return "monitor";  // a single non-model reason
  return "ok";
}
```

Why is model drift alone enough, when a single data or temporal reason only earns "monitor"? Because a version change means the *rules* changed. A stale score under the old rules is still a valid score under the old rules — you can defend it. A score compared against a *new* model's bands is a category error: you are reading a `2.2.0` number against `2.3.0` boundaries. That is not staleness, it is incoherence, and the only honest fix is to recompute. When reanalysis runs it emits a `reanalysis_triggered` and a `score_delta` event into the [audit log](/topics/defendable-agents/primitives/audit-trail/), so the reason the number moved is on the record, not folklore.

## Migration strategy

A major bump is a migration, and I treat it like a database migration — planned, logged, reversible in explanation if not in data.

1. **Freeze and tag.** The outgoing model keeps its version and hash forever. It is never edited in place; you author `2.4.0` alongside `2.3.0`.
2. **Dual-declare.** Keep the old unit resolvable so historical pins still name a model that exists. Deleting `2.3.0` orphans every score that cites it.
3. **Batch reanalyse under budget.** Reanalysis is not free — every recompute is a `reanalysis` operation costing 5 units against the session ceiling. A full re-score of a large book has to be planned against the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/), not fired blindly.
4. **Record deltas.** Each recomputed entity emits a `score_delta` so the before/after and the version transition are auditable.

## Keeping historical scores explainable

The point of never editing a model in place is that an old score stays *reproducible under its own rules*. Because the scoring engine is a pure function — same inputs, same model, same output — pointing the [reproduction path](/topics/defendable-agents/decisions/reproducibility/) at `modelHash: sha256:9f2c...b41e` regenerates the exact `2.2.0` number, variable by variable, years later. The pin tells you which model to load; the hash proves you loaded the right one; the deterministic engine does the rest. An auditor asking "why was this buyer 'High' in Q1?" gets the Q1 model, the Q1 inputs, and the Q1 number — not today's rules retro-fitted onto yesterday's data.

## Honest limits

Versioning guarantees *coherence*, not *correctness*. A wrong weight in `2.3.0` produces wrong scores — but consistently, visibly, and reproducibly, which is precisely how you notice and correct it (see [what defendable means](/topics/defendable-agents/argument/what-defendable-means/)). The hash proves two models are identical; it says nothing about whether either is *good*. And the model at the edge is still a model: versioning disciplines the deterministic scoring layer, not the judgement that fed the variable scores in. Finally, this is maintenance, not setup — every retune is a migration, a budget cost, and an audit event, forever. If you are not willing to pay that ongoing tax, do not put a versioned model into a governed decision.

For the practical version-selection flow through the harness, see [wiring KCP, agent and MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/).
