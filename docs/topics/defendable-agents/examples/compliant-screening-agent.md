---
title: "Example: A Compliant Screening Agent"
description: "A screening agent that stays inside declared rules and audience scoping, producing a reproducible, defensible decision for a regulated professional-services process."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Example: A Compliant Screening Agent

Screening is the kind of task that looks trivial until a regulator asks you to justify it. Given a buyer in a regulated professional-services market, decide whether the firm may pursue them, and on what evidence. Get it wrong in the permissive direction and you have acted on data you were never allowed to use. Get it wrong the other way and you have quietly discriminated. Either way, the defensible answer is not "the model said so" — it is a decision trace someone can read a year later and agree was made by the rules that were in force at the time.

This page walks the Lodestar screening path end to end. It is deliberately narrow: one buyer, one decision, one audit event. The mechanisms it leans on are covered in depth elsewhere — this is where they meet a worked case.

## Declared rules as governed units

The first defensive move is to stop treating the screening rules as code buried in a function and start treating them as a declared, versioned artifact. In Lodestar the scoring models — and the screening policy that gates on them — are [declared as governed KCP units](/topics/defendable-agents/kcp/declaring-governed-units/). The agent cannot reach into an arbitrary rule file; it can only load the unit the manifest names.

```yaml
# knowledge.yaml (excerpt)
kind: manifest
metadata:
  name: lodestar-screening
  version: 4.2.0
  domain: regulated-professional-services
  temporal:
    valid_from: "2026-06-01"
    refresh_interval: "P30D"
units:
  - id: screening-policy
    path: models/screening.policy.yaml
    tags: [governed, screening, audience-scoped]
    description: >
      Eligibility gate. Public-signal inputs only. Audience: pursue/no-pursue
      decision for tier_1 and tier_2 accounts. NOT for individual profiling.
    depends_on: [buyer-score]
  - id: buyer-score
    path: models/buyer.model.yaml
    tags: [governed, scoring]
    description: BUYER composite — Need 0.40, Attractiveness 0.25, Winnability 0.35.
```

Because the model is a governed unit selected via `kcp_plan` and `kcp_load`, the exact rule version is chosen deterministically and recorded. It is never silently swapped mid-session. That property is the whole point of [wiring KCP to the agent and MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/): the rules the agent used are the rules the manifest pinned.

## Audience and not-for scoping

Notice the `audience-scoped` tag and the blunt `NOT for individual profiling` line in the unit description. This is a declared audience: what the unit is for, and — more usefully in a compliance argument — what it is explicitly not for. The manifest is the place where a reviewer, or a data-protection officer, reads the intended use without reverse-engineering it from the code.

The audience declaration maps directly onto GDPR Art. 5(1)(c) data minimisation: the unit consumes public-signal inputs only, and it is scoped to a pursue / no-pursue decision on `tier_1` and `tier_2` accounts, not to building a profile of a named person. The [control mapping](/topics/defendable-agents/compliance/control-mapping/) treats this pairing — a mechanism plus a record — as the satisfied control. The mechanism is the scoped unit; the record is the audit event below.

## Data minimisation in practice

Minimisation is not a policy note here, it is what the score can physically see. The BUYER composite is built from 18 variables across three layers, and every one of them is fed from public events — signal strength, freshness, relevance, and so on. The screening gate never receives confidential enrichment. Under [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/), the shared signal data every tenant sees is public by construction; the confidential scores and plans live in isolated per-tenant state directories and never cross the boundary into a screening input.

The screening decision itself is a thin band check over the deterministic BUYER score:

| Band | Threshold | Screening action |
|---|---|---|
| Very high | >= 85 | Pursue |
| High | >= 70 | Pursue |
| Interesting but with gaps | >= 55 | Pursue, flag gaps |
| Lower priority | >= 40 | Hold |
| Not prioritized now | < 40 | No pursue |

## The decision trace as the defence

When the governed operation runs, it does four things in order: records the `buyer_scoring` cost of 5 units against the session ceiling, runs the pure score, creates a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/), and emits an [audit event](/topics/defendable-agents/primitives/audit-trail/) carrying the full variable trace. That event is the defence.

```json
{
  "timestamp": "2026-07-08T09:14:22.318Z",
  "sessionId": "sess-3f9a",
  "sequence": 47,
  "type": "buyer_scored",
  "actor": "screening-agent",
  "entity": { "type": "buyer", "id": "buyer-8821", "name": "[redacted]" },
  "decision": {
    "action": "screen",
    "inputs": { "model": "buyer-score@4.2.0", "audience": "pursue-decision" },
    "outputs": { "decision": "pursue", "band": "High" },
    "justification": "BUYER 72 >= 70; public signals only; tier_2 in scope"
  },
  "scoring": {
    "model": "buyer-score@4.2.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "need": 76, "attractiveness": 64, "winnability": 74 },
    "total": 72,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-07",
    "scoredAt": "2026-07-08T09:14:22.318Z",
    "signalDates": ["2026-07-04", "2026-06-28"]
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 235, "ceiling": 1000, "remaining": 765 },
  "durationMs": 12
}
```

Read top to bottom, this line answers the four questions a regulator actually asks. What was decided (`pursue`, band `High`). On what rule version (`buyer-score@4.2.0`, a pinned governed unit). On what data, and how fresh (public signals dated 4 July and 28 June, `dataAsOf` 7 July). And whether the process stayed inside its budget (235 of 1000 units). Because the engine is a pure function, anyone can [reproduce this decision](/topics/defendable-agents/examples/reproduce-a-decision/) from the recorded variables and get 72 again. The trace is not a summary of the reasoning — it *is* the reasoning.

## Honest limits

Three caveats, because a screening agent that oversells itself is a liability.

Determinism guarantees process, not correctness. If `known-criteria` was scored on a bad assumption, the agent applies that mistake to every buyer — consistently, visibly, and reproducibly. That consistency is a feature: a wrong variable shows up as the same wrong number everywhere, which is how you find it in review. It does not make the number right.

Temporal pinning detects staleness; it does not cure it. The pin will tell you the signals are 40 days old and flag them for monitoring via [drift detection](/topics/defendable-agents/primitives/drift-detection/) — a single staleness reason recommends *monitor*, not a full reanalysis. It will not fetch fresher data for you. Acting on a stale pursue decision is still your call, now merely a documented one.

And fail-closed can be over-tuned. A [screening gate wired to block](/topics/defendable-agents/architecture/fail-closed-behavior/) on any ambiguity keeps you compliant right up until it blocks legitimate work and someone routes around it. Governance here is maintenance, not a one-time setup — the [operating guide](/topics/defendable-agents/compliance/operating-and-maintenance/) is where that ongoing cost lives.
