---
title: "Tutorial 6: Temporal Pinning & a Drift Report"
description: "Pin every score to the data it was computed from, advance the clock, run checkDrift, and read a recommendation of reanalyze, monitor, or ok — with copyable code and a sample drift report."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# Tutorial 6: Temporal Pinning & a Drift Report

A score is only true as of the moment its inputs were true. By tutorial 4 you had an [audit log](/topics/defendable-agents/tutorials/04-audit-log/) recording every decision; by tutorial 5 a [budget ceiling](/topics/defendable-agents/tutorials/05-budget-ceiling/) bounding the work. Neither tells you when a score has gone stale. That is what temporal pinning is for. This tutorial builds a pin, advances the clock, runs a drift check, and schedules a nightly re-scan so staleness surfaces before someone acts on a number that stopped being true weeks ago.

We are still working in Lodestar, the codename for a scoring stack in a regulated professional-services market: it scores buyers, then matches firms to them. Every buyer score depends on signals that decay — see [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) for the concept, [drift detection](/topics/defendable-agents/primitives/drift-detection/) for the rules, and the [anatomy of a score](/topics/defendable-agents/decisions/anatomy-of-a-score/) for what those 18 variables are.

## Step 1 — Create a pin

Every governed scoring operation already emits a pin. A pin is a small, immutable record attached to a score: when it was computed, what data window it covered, and which model produced it.

```typescript
interface TemporalPin {
  scoredAt: string;      // when the score was computed (ISO 8601)
  dataAsOf: string;      // newest input datum the score reflects
  signalDates: string[]; // dates of the signals that fed the Need layer
  modelVersion: string;  // e.g. "buyer-scoring@2.3.0"
  modelHash: string;     // content hash of the deterministic model
}

function createPin(score: ScoreResult, now: Date): TemporalPin {
  return {
    scoredAt: now.toISOString(),
    dataAsOf: score.inputs.dataAsOf,
    signalDates: score.inputs.signalDates,
    modelVersion: score.model.version,
    modelHash: score.model.hash,
  };
}
```

A concrete pin for one buyer, written the day it was scored:

```json
{
  "scoredAt": "2026-06-01T09:14:02Z",
  "dataAsOf": "2026-05-30T00:00:00Z",
  "signalDates": ["2026-05-28", "2026-05-12", "2026-04-30"],
  "modelVersion": "buyer-scoring@2.3.0",
  "modelHash": "sha256:b41f…9ac2"
}
```

The [governed session](/topics/defendable-agents/tutorials/03-governed-session/) holds one map of pins keyed by entity, alongside the shared audit log and budget ledger, so every score in that session is pinned the moment it is produced.

## Step 2 — Advance the clock, or the data

Nothing has changed yet — the pin is fresh. Two things make a pin stale, and they are different:

- **Time passes.** The signals that drove the Need layer keep decaying. Recall the freshness curve: a 30-day half-life where a signal `<=3d` old scores 5, `<=30d` scores 3, and beyond 90 days scores 1. A score computed on freshness-5 signals is not the same score six weeks later.
- **New data arrives.** A newer signal, or a corrected data window, means `currentDataAsOf` has moved past the pin's `dataAsOf`.

For the tutorial we simulate both: it is now 8 July 2026, 37 days after `scoredAt`, and the signal feed has a newer datum dated 2 July.

## Step 3 — Run checkDrift

`checkDrift` is a pure comparison of a pin against current state. It returns typed reasons, never a silent boolean.

```typescript
type DriftReason = "DATA" | "MODEL" | "TEMPORAL";

interface DriftResult {
  reasons: DriftReason[];
  ageDays: number;
  recommendation: "reanalyze" | "monitor" | "ok";
}

function checkDrift(
  pin: TemporalPin,
  current: { dataAsOf: string; modelVersion: string },
  now: Date,
  maxAgeDays = 30,
): DriftResult {
  const reasons: DriftReason[] = [];
  const ageDays =
    (now.getTime() - Date.parse(pin.scoredAt)) / 86_400_000;

  if (Date.parse(current.dataAsOf) > Date.parse(pin.dataAsOf))
    reasons.push("DATA");
  if (current.modelVersion !== pin.modelVersion)
    reasons.push("MODEL");
  if (ageDays > maxAgeDays)
    reasons.push("TEMPORAL");

  const recommendation =
    reasons.includes("MODEL") || reasons.length >= 2
      ? "reanalyze"
      : reasons.length === 1
        ? "monitor"
        : "ok";

  return { reasons, ageDays: Math.round(ageDays), recommendation };
}
```

## Step 4 — Interpret the recommendation

The recommendation collapses the reasons into one of three actions. The rule is deliberately small so it is auditable:

| Situation | Reasons | Recommendation |
|---|---|---|
| Model version changed | `MODEL` present (alone or with others) | `reanalyze` |
| Two or more reasons | e.g. `DATA` + `TEMPORAL` | `reanalyze` |
| Exactly one non-model reason | `DATA` **or** `TEMPORAL` alone | `monitor` |
| No reasons | none | `ok` |

Model drift always wins because a different model means the old number was never comparable — the pin's `modelHash` no longer matches what you would compute today. Two independent reasons compound, so they escalate together. A single non-model reason is a watch signal, not an alarm.

Running our pin against current state:

```json
{
  "entity": "buyer-3182",
  "pin": {
    "scoredAt": "2026-06-01T09:14:02Z",
    "dataAsOf": "2026-05-30T00:00:00Z",
    "modelVersion": "buyer-scoring@2.3.0"
  },
  "current": {
    "dataAsOf": "2026-07-02T00:00:00Z",
    "modelVersion": "buyer-scoring@2.3.0"
  },
  "drift": {
    "reasons": ["DATA", "TEMPORAL"],
    "ageDays": 37,
    "recommendation": "reanalyze"
  }
}
```

Two reasons — newer data plus an age over the 30-day threshold — so the buyer is flagged for reanalysis. When the session acts on that, it emits a `reanalysis_triggered` event (cost: 5 units) and, once re-scored, a `score_delta` showing how far the band moved.

## Step 5 — Schedule a nightly re-scan

Drift only helps if something checks for it on a schedule. Run `checkDrift` over every pin nightly, act on the recommendations, and let the budget ceiling bound the fan-out.

```bash
#!/usr/bin/env bash
# nightly-drift.sh — cron: 0 2 * * *
set -euo pipefail

lodestar drift scan \
  --pins ./state/${TENANT}/pins.json \
  --max-age-days 30 \
  --emit reanalysis \
  --budget 1000 \
  --audit ./state/${TENANT}/audit.jsonl
```

`--emit reanalysis` re-scores only the pins recommending `reanalyze`; `monitor` pins are logged and left alone. Because each reanalysis costs 5 units against the session ceiling of 1000, a night that flags 300 buyers stops cleanly at 200 and records a `budget_exceeded` event rather than blowing past the ceiling — the [budget ceiling primitive](/topics/defendable-agents/primitives/budget-and-bounding/) at work. In a multi-tenant deployment, run the scan per tenant against its own isolated `state/${TENANT}/` directory so confidential scores never cross the boundary.

## Honest limits

Temporal pinning **detects** staleness; it does not fix it. A `reanalyze` recommendation tells you a number is old — it cannot fetch a fresher signal or correct a bad one. Refreshing the underlying data is a separate job, and if the feed is broken the pin will keep recommending reanalysis on data that never improves.

The 30-day threshold and the two-reason rule are policy, not physics. Set `maxAgeDays` too low and every score reanalyses nightly, burning budget and drowning the audit log; too high and stale numbers sit unflagged. And determinism guarantees process, not correctness: pinning proves *when* a score was true and *what* produced it, not that the score was right. A wrong variable is pinned just as faithfully as a right one — visibly, reproducibly, which is precisely how you catch it.

Next: [Tutorial 7 — multi-tenant isolation](/topics/defendable-agents/tutorials/07-multi-tenant/).
