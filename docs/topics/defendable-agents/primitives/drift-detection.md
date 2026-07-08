---
title: "Drift Detection"
description: "Treating staleness as a first-class signal in Lodestar: data drift, model drift and temporal drift, each yielding a recommendation of reanalyze, monitor or ok."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Drift Detection

A score is a photograph, not a live feed. The moment you compute a buyer score you have frozen three things: the data you scored against, the model you scored with, and the wall-clock instant you did it. The world keeps moving. New signals arrive, the scoring model gets a new version, and the score simply gets older. Drift detection is the discipline of noticing that the photograph and the world have diverged, and of saying so in a way an auditor can read.

Most systems treat staleness as an operational afterthought — a cache TTL, a cron job that re-runs everything nightly whether it needs it or not. In Lodestar staleness is a first-class signal. Every score leaves behind a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/), and drift detection is a pure function over that pin and the current state of the world.

## Three kinds of drift

The pin captures `{scoredAt, dataAsOf, signalDates[], modelVersion, modelHash}`. Comparing it against the present gives us three orthogonal drift signals:

| Drift type | Trigger | What it means |
|------------|---------|---------------|
| **DATA** | `currentDataAsOf > pin.dataAsOf` | Fresher input exists than the score was built on. |
| **MODEL** | current model version differs from `pin.modelVersion` | The scoring rules themselves have changed. |
| **TEMPORAL** | `ageInDays(pin.scoredAt) > maxAgeDays` (default 30) | The score is simply old, regardless of inputs. |

These are independent. A score can be temporally stale but perfectly current on data. It can be built on old data with an unchanged model. The value of separating them is that the *reason* travels with the alert — you never get an undifferentiated "needs refresh" with no explanation.

## The checkDrift logic

The check is deterministic: same pin, same current state, same verdict, every time. That is deliberate — drift detection is itself a governed decision, so it must be [reproducible](/topics/defendable-agents/decisions/reproducibility/) and it lands in the [audit trail](/topics/defendable-agents/primitives/audit-trail/) like any other.

```typescript
type DriftReason = "DATA" | "MODEL" | "TEMPORAL";
type Recommendation = "reanalyze" | "monitor" | "ok";

interface DriftReport {
  entityId: string;
  reasons: DriftReason[];
  recommendation: Recommendation;
  detail: Record<string, unknown>;
}

function checkDrift(
  pin: TemporalPin,
  current: { dataAsOf: string; modelVersion: string },
  maxAgeDays = 30,
): DriftReport {
  const reasons: DriftReason[] = [];

  if (Date.parse(current.dataAsOf) > Date.parse(pin.dataAsOf)) {
    reasons.push("DATA");
  }
  if (current.modelVersion !== pin.modelVersion) {
    reasons.push("MODEL");
  }
  const ageInDays =
    (Date.now() - Date.parse(pin.scoredAt)) / 86_400_000;
  if (ageInDays > maxAgeDays) {
    reasons.push("TEMPORAL");
  }

  return {
    entityId: pin.entityId,
    reasons,
    recommendation: recommend(reasons),
    detail: { ageInDays: Math.round(ageInDays), maxAgeDays },
  };
}
```

## Recommendation rules

The reasons are collected; the recommendation is a small policy on top. The rule is intentionally blunt so that a human can predict it without running the code:

```typescript
function recommend(reasons: DriftReason[]): Recommendation {
  if (reasons.length >= 2) return "reanalyze";
  if (reasons.includes("MODEL")) return "reanalyze";
  if (reasons.length === 1) return "monitor";
  return "ok";
}
```

In words:

- **Two or more reasons ⇒ reanalyze.** Compounding staleness is not worth reasoning about case by case; re-score.
- **Model drift alone ⇒ reanalyze.** If the rules changed, the old number was produced by a model that no longer exists. Comparing it to anything is meaningless, so it must be recomputed. This is the one single-reason case that still forces a re-score.
- **A single non-model reason ⇒ monitor.** Slightly fresher data, or a score that has just crossed the age threshold, is worth watching but not worth spending [budget](/topics/defendable-agents/primitives/budget-and-bounding/) on immediately.
- **No reasons ⇒ ok.** The photograph still matches the world.

## A drift report

Running the check over a buyer whose model was bumped and whose score has aged past the ceiling:

```json
{
  "entityId": "buyer-40219",
  "reasons": ["DATA", "MODEL", "TEMPORAL"],
  "recommendation": "reanalyze",
  "detail": {
    "ageInDays": 44,
    "maxAgeDays": 30,
    "pin": {
      "scoredAt": "2026-05-25T09:12:00Z",
      "dataAsOf": "2026-05-24T00:00:00Z",
      "modelVersion": "buyer-score@2.3.0"
    },
    "current": {
      "dataAsOf": "2026-07-07T00:00:00Z",
      "modelVersion": "buyer-score@2.4.0"
    }
  }
}
```

Every field an operator needs to justify the re-score is present in the object: which entity, why, how stale, and the exact model versions on both sides. When a `reanalysis_triggered` event follows, it points back to this report.

## Nightly re-scan

Drift detection is only useful if something runs it. Lodestar performs a nightly re-scan: for every temporal pin held in the session store, run `checkDrift`, and act on the recommendation. A `monitoring_check` costs 1 budget unit; a `reanalysis` costs 5. The re-scan does *not* blindly re-score everything — that is the whole point. It re-scores only what drift says to re-score, and it emits a `score_delta` when the new number differs from the old one, so you can see not just that a score moved but by how much.

```bash
# nightly, once per tenant state directory
lodestar drift-scan --state ./state/tenant-a \
  --max-age-days 30 \
  --on reanalyze \
  --emit-audit
```

The scan writes one `monitoring_check` audit event per pin and one `reanalysis_triggered` per re-score, all into the same append-only log the rest of the [governed session](/topics/defendable-agents/architecture/governance-harness/) uses. In a [multi-tenant](/topics/defendable-agents/primitives/multi-tenancy/) deployment the scan runs per state directory, so one tenant's drift never triggers work — or spends budget — against another's.

## Honest limits

Drift detection tells you a score is stale. It does not make it fresh. The nightly scan can *recommend* a reanalysis and even schedule one, but the reanalysis is only as good as the data available at that moment — [temporal pinning detects staleness, it does not refresh data](/topics/defendable-agents/primitives/temporal-pinning/). If your upstream signal feed is itself a week behind, drift detection will honestly report "DATA is current" against a `dataAsOf` that is already wrong, and cheerfully mark the score `ok`. Garbage in is still consistent garbage.

The threshold is a knob, and knobs get mis-set. A 30-day ceiling is a default, not a law; a fast-moving buyer signal may deserve seven days and a stable account tier ninety. Set `maxAgeDays` too low and the nightly scan reanalyses everything every night, which is just the dumb cron job wearing a governance costume — and burning budget doing it. Set it too high and you defend decisions built on months-old photographs. Like the rest of this stack, [drift detection is maintenance, not one-time setup](/topics/defendable-agents/compliance/operating-and-maintenance/): the thresholds are part of the model, and the model is versioned, reviewed and tuned over its life.
