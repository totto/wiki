---
title: "Tutorial 2: A Deterministic Scoring Model"
description: "Author a compact deterministic scoring model in YAML — two layers, a handful of 1-5 variables with scoring guides and weights, computed by hand and wired as a KCP unit."
image: assets/images/kcp-agent-020-03-model-at-the-edge.webp
---

# Tutorial 2: A Deterministic Scoring Model

In [Tutorial 1](/topics/defendable-agents/tutorials/01-first-harness/) you stood up a governance harness that gates and logs. That harness is worthless without something worth logging: a scoring decision you can reproduce and defend. This tutorial builds the smallest such thing — a two-layer model, authored as plain YAML, computed by hand, then declared as a governed unit so it can never be silently swapped.

The full Lodestar buyer model has three layers and 18 variables. That is too much to hold in your head on a first pass, so we build a compact stand-in with two layers and four variables. The arithmetic is identical; only the count changes. When you understand this, the real thing in [Anatomy of a Score](/topics/defendable-agents/decisions/anatomy-of-a-score/) reads as more of the same.

## The scoring rule, stated plainly

Every layer works the same way. Score each variable 1-5 against a written guide. Take the mean of the variable scores. Multiply by 20. You now have a 0-100 layer score. The overall score is a weighted composite of the layers, and the weights sum to 1.0.

That is the whole engine. It is a pure function: same inputs, same output, forever. There is no sampling, no temperature, no hidden state. This is the property that makes the decision [reproducible](/topics/defendable-agents/decisions/reproducibility/) — and it is the reason the model at the edge is kept *away* from the arithmetic.

## The model manifest

Write this to `models/buyer-lite.yaml`. Notice that each variable carries its own scoring guide inline. The guide is not documentation you keep elsewhere — it *is* the model, and it travels with it.

```yaml
id: buyer-lite
version: 1.0.0
description: Compact two-layer buyer priority model (teaching cut of the full model)
weights:
  need: 0.60
  winnability: 0.40
layers:
  need:
    variables:
      - id: signal-strength
        guide:
          5: Explicit, named mandate in market now
          4: Strong intent signal, unnamed
          3: Recurring soft signal
          2: Weak or inferred signal
          1: No signal
      - id: signal-freshness
        guide:
          5: "<= 3 days old"
          4: "<= 14 days old"
          3: "<= 30 days old"
          2: "<= 60 days old"
          1: "> 60 days old"
  winnability:
    variables:
      - id: relationship-proximity
        guide:
          5: Sitting relationship with the buyer
          4: Warm path via a known contact
          3: One introduction away
          2: Cold, but reachable
          1: No path
      - id: relevant-experience
        guide:
          5: Directly comparable prior engagement
          4: Adjacent, defensible experience
          3: Partial fit
          2: Thin fit
          1: None
bands:
  - { min: 85, label: "Very high" }
  - { min: 70, label: "High" }
  - { min: 55, label: "Interesting but with gaps" }
  - { min: 40, label: "Lower priority" }
  - { min: 0,  label: "Not prioritized now" }
```

The bands here are the real Lodestar buyer bands, unchanged. Keeping them intact matters: the band boundary is a policy decision, and policy lives in the manifest, not in code someone can edit without review.

## Compute a score by hand

Take one buyer. A named mandate is live (`signal-strength = 5`) and the signal is nine days old (`signal-freshness = 4`). You have a warm path in (`relationship-proximity = 4`) but only adjacent experience (`relevant-experience = 4`).

```
Need layer         = mean(5, 4) * 20 = 4.5 * 20 = 90
Winnability layer  = mean(4, 4) * 20 = 4.0 * 20 = 80

Composite = (90 * 0.60) + (80 * 0.40)
          = 54 + 32
          = 86   -> band "Very high"
```

Eighty-six. Very high priority. There is nothing to argue with here that you cannot see: the number is the sum of four judgements and two weights, all of them written down. If a reviewer disputes the outcome, they dispute a specific `1-5` call against a specific guide line — not the machine.

The JSON the harness records for this decision carries the entire trace, which is what makes it a [decision trace](/topics/defendable-agents/primitives/decision-traces/) rather than a bare number:

```json
{
  "model": "buyer-lite@1.0.0",
  "variables": [
    { "id": "signal-strength",        "score": 5 },
    { "id": "signal-freshness",       "score": 4 },
    { "id": "relationship-proximity", "score": 4 },
    { "id": "relevant-experience",    "score": 4 }
  ],
  "layerScores": { "need": 90, "winnability": 80 },
  "total": 86,
  "band": "Very high"
}
```

## Reproducibility, demonstrated

Reproducibility is not a claim you assert; it is a test you can run. Feed the same four scores in tomorrow, next quarter, on another machine — you get 86. Change `signal-freshness` from 4 to 3 and the composite drops to `(mean(5,3)*20*0.6) + 32 = 48 + 32 = 80`, still "High". The relationship between input and output is total and inspectable. A `score_delta` between two runs therefore always has a cause you can name: a variable moved, a weight changed, or the model version changed. Nothing drifts on its own.

## Wire it as a governed KCP unit

The final step is what keeps this honest in production. If the model can be edited or swapped without anyone noticing, none of the above holds. So the manifest is declared as a governed [KCP unit](/topics/defendable-agents/kcp/declaring-governed-units/), selected deterministically by `kcp_plan` rather than picked up from wherever a file happens to sit.

```yaml
kind: manifest
metadata:
  name: lodestar-scoring
  version: 1.0.0
  domain: professional-services-market
  temporal:
    valid_from: "2026-07-01"
    refresh_interval: P90D
units:
  - id: model.buyer-lite
    path: models/buyer-lite.yaml
    tags: [scoring, model, buyer]
    description: Compact two-layer buyer priority model
```

Now the model has an identity — `model.buyer-lite`, version `1.0.0` — that the governed session pins alongside every score. When the version changes, the [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) records model drift, and old decisions are flagged for reanalysis instead of quietly rotting. That linkage between model and record is the entire point of [Versioning Models](/topics/defendable-agents/decisions/versioning-models/).

## Honest limits

Determinism buys you *process*, not *correctness*. If `relationship-proximity` is genuinely a 2 and someone scores it a 4, the model faithfully computes a wrong 86 — every time. That is not a defeat; it is the design. The wrong judgement is applied consistently and recorded in full, so it surfaces in review as a single disputable number rather than hiding inside a probabilistic black box. A defendable model does not stop people being wrong. It stops them being wrong *invisibly*.

When your compact model computes and pins cleanly, move on to [Tutorial 3](/topics/defendable-agents/tutorials/03-governed-session/) and run it inside a full governed session.
