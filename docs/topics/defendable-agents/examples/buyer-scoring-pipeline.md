---
title: "Example: A Buyer-Scoring Pipeline"
description: "The Lodestar pipeline end to end — signal detection, buyer scoring, match scoring, tiering and CRM export — every stage governed, budgeted and audited."
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# Example: A Buyer-Scoring Pipeline

This page walks a single request through Lodestar, the reference system I use throughout this guide. Lodestar serves a regulated professional-services market: it watches public signals about **buyers** (organisations that might need work done), scores them, matches them against **firms** that could win the work, assigns an account tier, and writes the result to the client CRM. Every stage is a governed operation — it costs budget, it produces a decision trace, and it leaves a line in an append-only audit trail.

The pipeline is five stages:

```text
signals → buyer score (18 var) → match score (21 var) → tier → CRM export
```

Nothing here is magic. The scoring is [pure deterministic arithmetic](/topics/defendable-agents/architecture/deterministic-planner/); the model only sits at the edges, extracting variables from messy text. What makes it [defendable](/topics/defendable-agents/argument/what-defendable-means/) is that the arithmetic runs inside a [governed session](/topics/defendable-agents/architecture/governance-harness/) that shares one budget ledger, one audit trail and one set of temporal pins.

## Stage 1 — Signal detection

A signal is a dated public event: a mandate posted, a leadership change, a regulatory filing. Detection costs **1 unit** and emits a `signal_detected` event. Each signal carries a date, and that date matters later — freshness decays with a roughly 30-day half-life, so a signal three days old scores 5 while one ninety days old scores 1.5.

## Stage 2 — Buyer score (18 variables, 3 layers)

The buyer score is a weighted composite of three layers. Each layer score is the mean of its six 1-5 variable scores, times 20, giving a 0-100 layer score. The composite weights are fixed in the [scoring-model manifest](/topics/defendable-agents/decisions/scoring-model-manifest/):

| Layer | Weight | Variables |
|---|---|---|
| Need | 0.40 | signal-strength, signal-freshness, signal-relevance, signal-velocity, buying-journey-stage, internal-mobilization |
| Attractiveness | 0.25 | mandate-value, strategic-value, growth-potential, sector-fit, reference-value, cross-sell-potential |
| Winnability | 0.35 | competitive-position, relationship-proximity, known-criteria, decision-access, internal-capacity, relevant-experience |

Buyer scoring costs **5 units**. Suppose the Need layer averages 4.2 (→ 84), Attractiveness 3.5 (→ 70), Winnability 3.8 (→ 76). The composite is `0.40·84 + 0.25·70 + 0.35·76 = 33.6 + 17.5 + 26.6 = 77.7`, which lands in the **High** band (≥70). The bands are: ≥85 Very high, ≥70 High, ≥55 Interesting but with gaps, ≥40 Lower priority, else Not prioritized now.

The `buyer_scored` audit event carries the full variable trace — not just the total, but every input that produced it:

```json
{
  "timestamp": "2026-07-08T09:14:22.031Z",
  "sessionId": "sess_4f21",
  "sequence": 7,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_8830", "name": "Buyer 8830" },
  "scoring": {
    "model": "buyer-score@2.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "signal-relevance", "score": 4 }
    ],
    "layerScores": { "need": 84, "attractiveness": 70, "winnability": 76 },
    "total": 77.7,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-08",
    "scoredAt": "2026-07-08T09:14:22.031Z",
    "signalDates": ["2026-07-05", "2026-06-28"]
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 11, "ceiling": 1000, "remaining": 989 },
  "durationMs": 42
}
```

Because the total, the layer scores and every variable are recorded, anyone can [reproduce the decision](/topics/defendable-agents/examples/reproduce-a-decision/) from the audit trail alone. That is the whole point of a [decision trace](/topics/defendable-agents/primitives/decision-traces/).

## Stage 3 — Match score (21 variables, 4 layers)

A buyer worth pursuing still needs the right firm. The match score composites four layers — Need-match (0.25), Market-match (0.20), Commercial-match (0.25) and Winnability-priority (0.30) — across 21 variables. It costs **5 units** and emits `match_scored`. Same arithmetic shape, same trace discipline.

## Stage 4 — Account tiering

Tiering rolls the buyer score, the best match and business rules into a coarse label: `tier_1`, `tier_2`, `tier_3` or `out_of_scope`. It costs **2 units** and emits `account_tiered`. A buyer at 77.7 with a strong match typically lands `tier_1`; a low buyer score with no viable firm falls to `out_of_scope`, and the harness records *why*.

## Stage 5 — CRM export

The final stage writes tier, score, band and a provenance reference into the client CRM. Export is the moment the governance work pays off: the CRM record links back to the exact audit sequence, so a reviewer months later can pull the trace without touching Lodestar at all. This feeds the [evidence packages](/topics/defendable-agents/compliance/evidence-packages/) used at audit time.

## The run as one ledger

Across the run, the budget ledger accumulates every spend against the session ceiling (1000 units in the reference `harness.yaml`). Before each operation the ledger checks `runningTotal + cost` against the ceiling; if it would exceed, the operation throws and emits `budget_exceeded` instead of running — a [fail-closed](/topics/defendable-agents/primitives/fail-closed-policy/) stop, not a warning.

```text
seq  operation         entity       cost  runningTotal
1    signal_detection  buyer_8830   1     1
7    buyer_scoring     buyer_8830   5     11
12   match_scoring     match_2201   5     18
14   account_tiering   buyer_8830   2     20
```

Every score also creates a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) `{scoredAt, dataAsOf, signalDates, modelVersion, modelHash}`, so a later [drift check](/topics/defendable-agents/primitives/drift-detection/) can tell you the score is 40 days old — past its 30-day maximum age — and flag it for review before anyone acts on it.

## Honest limits

Determinism here buys you **process, not correctness**. If `signal-relevance` was scored 4 when a human would say 2, the pipeline applies that mistake consistently — but visibly, in the trace, which is exactly how you catch and correct it. Temporal pinning tells you data is stale; it does not refresh the data. And the model at the edge, extracting those 1-5 variable scores from public text, is still a model — the arithmetic downstream is only as good as the reading upstream. The governance is what makes those failures legible rather than silent; see [why guardrails fail](/topics/defendable-agents/argument/why-guardrails-fail/) for the alternative.

For the full production write-up of this system, see the [Lodestar case study](/topics/defendable-agents/reference/case-study-lodestar/).
