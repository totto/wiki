---
title: "Declaring Governed Units"
description: "Turn scoring models and data into declared KCP units with intent, tags, dependencies and audience, so a governed agent selects them deterministically and never silently swaps them."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Declaring Governed Units

A defendable agent is only as trustworthy as the things it is allowed to pick up. If a scoring model can be swapped for a different file because the two happen to sit in the same folder, or because a retrieval step decided one blob "looked more relevant", then every downstream guarantee — the audit trail, the temporal pin, the reproducible score — is built on sand. The fix is not a smarter retriever. It is declaration: naming the knowledge and the models the agent may use, and pinning what each one is *for*.

In a [Knowledge Context Protocol](/topics/knowledge-context-protocol/) manifest, that declaration is a **governed unit**. This page walks the unit fields, explains why declaring your scoring models as units is what makes selection deterministic, and gives a real `units` block from the Lodestar example — a buyer- and firm-scoring system for a regulated professional-services market.

## The unit fields

A KCP manifest (`knowledge.yaml`) has metadata and a `units` list. Each unit is a small, honest record of one governed thing:

| Field | Purpose |
| --- | --- |
| `id` | Stable, unique handle the agent selects by. Never reused, never silently repointed. |
| `path` | Where the unit's content actually lives on disk. |
| `tags` | Intent and topic labels — how a plan step declares "I need *this kind* of thing". |
| `description` | Human-readable statement of what the unit is and when to use it. |
| `depends_on` | Other unit ids this one requires, so a load pulls the whole coherent set. |
| `audience` | Who the unit may be shown to — the declared-audience half of data minimisation. |

The `id` and `tags` are the load-bearing fields. Selection is a lookup over declared ids and tags, not a similarity search over content. That single design choice is the difference between "the agent used model v3, here is its hash" and "the agent used whatever the vector store returned this morning".

## Scoring models are units too

The instinct is to declare *data* — signal feeds, company records — and leave the scoring logic in code. Resist it. In Lodestar the buyer model (3 layers, 18 variables) and the match model (4 layers, 21 variables) are themselves declared units. The deterministic planner is pure — same inputs, same outputs — but purity only helps if you can prove *which* function ran. Declaring the model as a governed unit means its version and hash are selected explicitly, recorded in the [scoring-model manifest](/topics/defendable-agents/decisions/scoring-model-manifest/), and pinned into every [decision trace](/topics/defendable-agents/primitives/decision-traces/).

```yaml
kind: manifest
metadata:
  name: lodestar-scoring
  version: 3.2.0
  domain: professional-services-gtm
  description: Governed knowledge and scoring models for buyer and firm prioritisation.
  temporal:
    valid_from: 2026-01-01
    refresh_interval: P1D
units:
  - id: model.buyer-score
    path: models/buyer-score.v3.json
    tags: [scoring, model, buyer, deterministic]
    description: >
      Weighted composite of Need (0.40), Attractiveness (0.25), Winnability (0.35).
      18 variables across 3 layers. Emits 0-100 total plus priority band.
    audience: internal
  - id: model.match-score
    path: models/match-score.v3.json
    tags: [scoring, model, firm, deterministic]
    description: >
      Weighted composite of Need-match (0.25), Market-match (0.20),
      Commercial-match (0.25), Winnability-priority (0.30). 21 variables, 4 layers.
    depends_on: [model.buyer-score]
    audience: internal
  - id: data.signal-feed
    path: data/signals/
    tags: [signals, public, temporal]
    description: >
      Public buying-intent events. Freshness decays on a ~30-day half-life;
      feeds signal-freshness in the Need layer.
    audience: shared
  - id: policy.priority-bands
    path: policy/bands.yaml
    tags: [policy, bands, buyer]
    description: >
      Band thresholds: >=85 Very high, >=70 High, >=55 Interesting but with gaps,
      >=40 Lower priority, else Not prioritized now.
    audience: internal
```

## Why declaration makes selection deterministic

When the agent needs to score a buyer, `kcp_plan` resolves a step like "load the buyer scoring model" against declared ids and tags. It returns `model.buyer-score` because that unit *declares* itself as the buyer model — not because a fuzzy match ranked it first. `kcp_load` then reads exactly that `path`, and because `model.match-score` declares `depends_on: [model.buyer-score]`, loading the match model pulls the buyer model with it. No coherent set is ever half-loaded.

This is what lets the [governance harness](/topics/defendable-agents/architecture/governance-harness/) point a domain at a manifest and mean it. The harness only exposes `kcp_plan` and `kcp_load` over the declared units; anything not declared is not selectable, which is the fail-closed default working exactly as intended. Wiring that plumbing end to end is covered in [wiring KCP, the agent and MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/); the manifest shape itself is in [manifest basics](/topics/defendable-agents/kcp/manifest-basics/).

The `audience` field carries its weight at tenant boundaries. `shared` units (public signals, company data) are visible to every tenant; `internal` scores and policies stay in per-tenant state. Declaration is where that line is drawn — see [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/) for how the directory boundary enforces it.

## Honest limits

Declaration governs *selection*, not *content*. If `model.buyer-score` weights a variable wrongly, the manifest will hand the agent that wrong model with perfect consistency — every score reproducibly wrong, which is precisely how you catch it in a [reproduced decision](/topics/defendable-agents/examples/reproduce-a-decision/) rather than never. `depends_on` captures the dependencies you thought to write down; an undeclared coupling between two units is still invisible. And a manifest is not a set-and-forget artefact: versions move, models get revised, `valid_from` ages. Governing units is [maintenance, not one-time setup](/topics/defendable-agents/compliance/operating-and-maintenance/). What declaration buys you is not correctness — it is knowing, on every run, exactly which named thing was used and being able to prove it.
