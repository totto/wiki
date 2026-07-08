---
title: "Anatomy of a Defensible Score"
description: "How a 0-100 buyer score is computed deterministically in Lodestar: 1-5 variables averaged and scaled per layer, combined by fixed weights, then bucketed into a priority band."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Anatomy of a Defensible Score

A score you cannot walk by hand is not defensible — it is a rumour with a number attached. In Lodestar, our example agent for a regulated professional-services market, every buyer score is a pure function: the same inputs produce the same output, every time, with no hidden state and no call to a model in the hot path. This page walks the full computation with real numbers so you can reproduce it on paper.

## The three arithmetic steps

There are only three operations, and none of them is clever.

1. **Variable to layer.** Each layer holds six variables, each scored 1-5. A layer score is the mean of its variables, multiplied by 20. That maps `[1,5]` onto `[20,100]`.
2. **Layers to composite.** The buyer score is a weighted sum of three layer scores. The weights are fixed and declared: **Need 0.40, Attractiveness 0.25, Winnability 0.35**. They sum to 1.0, so the composite stays on the 0-100 scale.
3. **Composite to band.** The composite is bucketed into a priority band by fixed thresholds.

That is the whole engine. If you understand those three lines, you can audit any score Lodestar has ever produced — which is the point. Determinism buys you [reproducibility](/topics/defendable-agents/decisions/reproducibility/), and reproducibility is what lets a reviewer disagree with a decision on the merits instead of arguing about whether the machine was having a bad day.

## A worked buyer score

Take a single buyer. Here are the eighteen variable scores an analyst (or the [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/)) assigned, grouped by layer.

| Layer | Variable | Score (1-5) |
|---|---|---|
| **Need** (w=0.40) | signal-strength | 4 |
| | signal-freshness | 4.5 |
| | signal-relevance | 4 |
| | signal-velocity | 3 |
| | buying-journey-stage | 4 |
| | internal-mobilization | 3 |
| **Attractiveness** (w=0.25) | mandate-value | 4 |
| | strategic-value | 3 |
| | growth-potential | 3 |
| | sector-fit | 4 |
| | reference-value | 2 |
| | cross-sell-potential | 3 |
| **Winnability** (w=0.35) | competitive-position | 3 |
| | relationship-proximity | 4 |
| | known-criteria | 3 |
| | decision-access | 4 |
| | internal-capacity | 3 |
| | relevant-experience | 4 |

The `signal-freshness` value of 4.5 is itself deterministic: it is a linear decay with a ~30-day half-life, and this buyer's freshest signal landed within seven days (`<=7d = 4.5`). Nothing here is a judgement call the machine makes twice differently. See [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) for how that date is captured and later checked for drift.

### Step 1 — layer means

```
Need:            (4 + 4.5 + 4 + 3 + 4 + 3) / 6 = 22.5 / 6 = 3.750  -> x20 = 75.00
Attractiveness:  (4 + 3 + 3 + 4 + 2 + 3) / 6   = 19.0 / 6 = 3.167  -> x20 = 63.33
Winnability:     (3 + 4 + 3 + 4 + 3 + 4) / 6   = 21.0 / 6 = 3.500  -> x20 = 70.00
```

### Step 2 — weighted composite

```
composite = 75.00 * 0.40 + 63.33 * 0.25 + 70.00 * 0.35
          = 30.000    + 15.833    + 24.500
          = 70.333
```

### Step 3 — band

The band thresholds are fixed:

| Composite | Band |
|---|---|
| >= 85 | Very high |
| >= 70 | High |
| >= 55 | Interesting but with gaps |
| >= 40 | Lower priority |
| < 40 | Not prioritized now |

A composite of **70.333** clears the 70 threshold, so this buyer lands in **High**. Note how narrow that is: shave two-tenths off `Need` and the buyer drops a band. That fragility is not a flaw to hide — it is exactly the kind of thing a defensible score should make visible, so that a reviewer can see the decision was borderline and weight it accordingly. The [layers, weights and bands](/topics/defendable-agents/decisions/layers-weights-bands/) page covers why we keep the thresholds coarse and public rather than tuning them into the noise.

## What gets recorded

The score is not just returned; it is pinned into the [decision trace](/topics/defendable-agents/primitives/decision-traces/) that the governed session writes to the [audit log](/topics/defendable-agents/primitives/audit-trail/). The `scoring` block of a `buyer_scored` event carries the full trace — every variable, its score, the per-layer results, the composite, and the band:

```json
{
  "type": "buyer_scored",
  "scoring": {
    "model": "buyer-score",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "signal-relevance", "score": 4 },
      { "id": "signal-velocity", "score": 3 },
      { "id": "buying-journey-stage", "score": 4 },
      { "id": "internal-mobilization", "score": 3 },
      { "id": "mandate-value", "score": 4 },
      { "id": "strategic-value", "score": 3 },
      { "id": "growth-potential", "score": 3 },
      { "id": "sector-fit", "score": 4 },
      { "id": "reference-value", "score": 2 },
      { "id": "cross-sell-potential", "score": 3 },
      { "id": "competitive-position", "score": 3 },
      { "id": "relationship-proximity", "score": 4 },
      { "id": "known-criteria", "score": 3 },
      { "id": "decision-access", "score": 4 },
      { "id": "internal-capacity", "score": 3 },
      { "id": "relevant-experience", "score": 4 }
    ],
    "layerScores": { "Need": 75.0, "Attractiveness": 63.33, "Winnability": 70.0 },
    "total": 70.33,
    "band": "High"
  }
}
```

Because the eighteen inputs are all present, anyone can re-run the three steps above and confirm the `70.33`/`High` result without touching Lodestar at all. That is what makes it evidence rather than output. Reproducing a full decision end-to-end is walked in the [reproduce-a-decision example](/topics/defendable-agents/examples/reproduce-a-decision/).

## The same shape, larger

The match score uses the identical machinery — variables to layer means, layers to weighted composite — but over four layers and twenty-one variables: **Need-match 0.25, Market-match 0.20, Commercial-match 0.25, Winnability-priority 0.30**. Nothing about the arithmetic changes; only the weight vector and the variable set do. Both models are declared as governed [KCP units](/topics/defendable-agents/kcp/declaring-governed-units/) so the exact version is selected deterministically and never silently swapped — the full contract lives in the [scoring model manifest](/topics/defendable-agents/decisions/scoring-model-manifest/).

## Honest limits

Determinism guarantees **process, not correctness**. If `reference-value` was assessed as 2 when it should have been 4, the engine will apply that mistake faithfully and identically every time — the score is wrong, consistently and reproducibly. That is not a weakness of the approach; it is how you catch the error. A wrong variable is visible in the trace, attributable to a specific input, and correctable, whereas a wrong number from an opaque model is just a wrong number. The arithmetic is trustworthy. Judging whether a 4 should have been a 2 is still human work — and, upstream, still partly the model at the edge, which is still a model. Defensibility means that when that judgement is contested, the record is complete enough to have the argument.
