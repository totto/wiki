---
title: "Temporal Pinning"
description: "Recording the validity window of every decision — dataAsOf, scoredAt, signalDates, model version and hash — so provenance is queryable and staleness is detectable and reproducible."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# Temporal Pinning

A score is not a fact. It is a fact *as of a moment*, computed from data *as of another moment*, using a model *of a particular version*. Drop those moments and you are left with a number that looks authoritative and cannot be defended. Six weeks later someone asks "why did Lodestar rank this buyer 'Very high'?" and the honest answer is a shrug, because the inputs have moved, the model has been retuned, and nobody wrote down the world the number came from.

Temporal pinning fixes that. Every time a [governed session](/topics/defendable-agents/architecture/governance-harness/) produces a score, it also produces a **pin**: a small immutable record that captures the temporal context of that specific computation. The pin is written alongside the [audit event](/topics/defendable-agents/primitives/audit-trail/) and kept in the session's map of pins. It is what makes provenance a first-class, queryable property of the system rather than a story you reconstruct after the fact.

## The pin fields

A pin has five fields. Each answers a different question about the decision.

```json
{
  "scoredAt": "2026-07-08T09:14:22.418Z",
  "dataAsOf": "2026-07-07T23:59:59.000Z",
  "signalDates": [
    "2026-07-05T08:30:00.000Z",
    "2026-06-28T14:10:00.000Z",
    "2026-05-31T00:00:00.000Z"
  ],
  "modelVersion": "buyer-score@2.3.0",
  "modelHash": "sha256:9f2c1a…e04b"
}
```

| Field | Question it answers |
| --- | --- |
| `scoredAt` | When did we compute this? |
| `dataAsOf` | What was the freshest the underlying data could be? |
| `signalDates` | Which individual events fed the score, and how old is each? |
| `modelVersion` | Which scoring model produced this? |
| `modelHash` | Is that model bit-for-bit the one we think it is? |

## dataAsOf vs scoredAt

The distinction that trips people up is `scoredAt` versus `dataAsOf`, and it matters more than it looks.

`scoredAt` is wall-clock time: the instant the deterministic planner ran. `dataAsOf` is the cut-off of the *input world* — the timestamp beyond which no data was available to the computation. They are almost never equal. You might re-score a buyer at 09:14 today from data that was last refreshed at midnight last night. `scoredAt` is now; `dataAsOf` is last night.

Keeping them separate is what lets you reason about staleness honestly. A score computed a minute ago is "fresh" by `scoredAt` but could be built on a `dataAsOf` from three weeks back — genuinely stale, and only the pin reveals it. Collapse the two into one "timestamp" and you lose the ability to tell a recent computation from recent data.

## signalDates

`signalDates` is the list of timestamps of the individual events that fed the score. In Lodestar the freshness of each signal is not cosmetic — it drives a variable directly. The `signal-freshness` variable is a stepped decay with roughly a 30-day half-life:

```typescript
function signalFreshness(ageDays: number): number {
  if (ageDays <= 3)  return 5;
  if (ageDays <= 7)  return 4.5;
  if (ageDays <= 14) return 4;
  if (ageDays <= 30) return 3;
  if (ageDays <= 60) return 2;
  if (ageDays <= 90) return 1.5;
  return 1; // 1–5 scale, folded into the Need layer
}
```

Because the score already *depends* on these dates, recording them in the pin costs almost nothing and buys a lot: you can look at any past decision and see exactly which events were in play and how tired they were. When someone disputes a ranking, `signalDates` is the receipt.

## modelVersion and modelHash

A score is only reproducible against a specific model. `modelVersion` is the human-readable identity (`buyer-score@2.3.0`); `modelHash` is the content hash of the model definition that the [KCP manifest](/topics/defendable-agents/kcp/declaring-governed-units/) selected. The scoring models are declared as governed KCP units precisely so they are chosen deterministically and never silently swapped underneath a running session — see [versioning models](/topics/defendable-agents/decisions/versioning-models/) for how the manifest pins a model to a decision.

The hash is the belt-and-braces part. Two builds can claim version `2.3.0` and differ; the hash does not lie. If the hash in the pin does not match the hash of the model you are holding today, you are not reproducing the same decision, and the system says so instead of pretending.

## Why pinning makes provenance first-class

Without pins, provenance is an archaeology project. With pins, it is a lookup. The pin travels with the [decision trace](/topics/defendable-agents/primitives/decision-traces/) in the audit log, so any historical score carries its own answer to "what world did this come from?" — no reconstruction, no guessing.

The pin is also the input to drift detection. A drift check compares a pin against current state:

- **DATA drift** — `currentDataAsOf > pin.dataAsOf`. The world moved on; the score was computed against an older cut-off.
- **MODEL drift** — the model version changed since the pin was written.
- **TEMPORAL drift** — the pin's age in days exceeds `maxAgeDays` (default 30).

The recommendation logic is deliberately blunt: two or more drift reasons means *reanalyze*; model drift alone means *reanalyze*; a single non-model reason means *monitor*; otherwise *ok*. That mechanism is covered in full on [drift detection](/topics/defendable-agents/primitives/drift-detection/). Pinning is the half that makes drift *detectable*; without a pin there is no baseline to compare against.

Pins also underwrite [reproducibility](/topics/defendable-agents/decisions/reproducibility/) as a compliance control: data provenance maps to temporal pinning (ISO 27001 A.12.4, Logging and monitoring), and it is the pin — `dataAsOf` plus `signalDates` plus `modelHash` — that lets you re-run a decision and get the same number, or explain precisely why you cannot.

## Honest limits

Pinning records staleness. It does not *fix* it. A pin will tell you the `dataAsOf` is six weeks old and the signals are decayed to 1; it will not go and fetch fresher data. That is a separate job, triggered by the drift recommendation, not by the pin itself. The pin is a smoke detector, not a fire brigade.

Nor does the pin certify that the data was *correct* — only that it was what the system had at that cut-off. If an upstream feed was wrong at `dataAsOf`, the pin faithfully records a decision built on bad input. That is still a strict improvement over the alternative, because the wrongness is now dated, attributable, and reproducible instead of invisible. Determinism here guarantees process, not truth. See [what "defendable" means](/topics/defendable-agents/argument/what-defendable-means/) for why that trade is the whole point.
