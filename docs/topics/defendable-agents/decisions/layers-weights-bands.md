---
title: "Layers, Weights & Bands"
description: "How the layer/weight/band system turns eighteen small 1-5 judgments into one defensible number: why layers exist, how to document weights honestly, and how to resist tuning the answer."
image: assets/images/kcp-agent-020-03-model-at-the-edge.webp
---

# Layers, Weights & Bands

A single number — "this buyer scores 78, priority High" — is a decision waiting to be challenged. Someone will ask *why 78 and not 55*, and if your only answer is "the model said so", you have no defence. The layer/weight/band system exists so that number decomposes, on demand, back into the small judgements that produced it. This page is about that structure: why we group variables into layers, how we choose and document the weights, where the band thresholds come from, and the one failure mode that quietly poisons the whole thing — tuning weights until you get the answer you already wanted.

## Why layers

In [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/) the buyer score is built from eighteen variables. Feeding eighteen numbers straight into one weighted sum is legal arithmetic, but it is impossible to reason about. Nobody can hold eighteen weights in their head, and a reviewer cannot tell whether a low score came from a weak commercial case or a bad market fit.

Layers are the intermediate abstraction that makes the score *readable*. Each variable is scored 1-5. A layer score is the mean of its variables times twenty, giving a clean 0-100 per layer. The buyer composite is then a weighted sum of just three layer scores:

| Layer | Weight | Variables |
|---|---|---|
| Need | 0.40 | signal-strength, signal-freshness, signal-relevance, signal-velocity, buying-journey-stage, internal-mobilization |
| Attractiveness | 0.25 | mandate-value, strategic-value, growth-potential, sector-fit, reference-value, cross-sell-potential |
| Winnability | 0.35 | competitive-position, relationship-proximity, known-criteria, decision-access, internal-capacity, relevant-experience |

Now a reviewer reads the score at two altitudes: three layer scores tell the *story* (strong need, weak winnability), and eighteen variable scores tell the *evidence*. Layers are how the decision trace stays human-sized. See [Variable Design](/topics/defendable-agents/decisions/variable-design/) for how the leaf variables themselves are kept independent and observable.

## Choosing weights — and documenting them

Weights encode a strategy. Need at 0.40 says *demand comes first*; Winnability at 0.35 says *we would rather chase a winnable mid-fit than an unwinnable perfect fit*; Attractiveness at 0.25 says *how nice the prize is matters least*. Those are business judgements, not mathematical facts, and the honest move is to write them down as such.

The weights live in the [scoring-model manifest](/topics/defendable-agents/decisions/scoring-model-manifest/), version-controlled and hashed, next to a plain-language rationale:

```yaml
model: buyer-score
version: 3.2.0
layers:
  need:
    weight: 0.40
    rationale: >
      A live, fresh buying signal is the single strongest predictor of
      a real opportunity. Weighted highest deliberately: no signal, no deal.
  winnability:
    weight: 0.35
    rationale: >
      We would rather pursue a winnable engagement than an attractive one
      we cannot win. Ranked above attractiveness on purpose.
  attractiveness:
    weight: 0.25
    rationale: >
      Prize size matters, but chasing large unwinnable prizes burns capacity.
constraint: sum(weights) == 1.0
```

Two rules make this defensible. First, weights sum to exactly 1.0 so a composite is always on the same 0-100 scale as its layers — a validator should reject a manifest that violates this. Second, every weight ships with a rationale a non-technical reviewer can read and disagree with. A weight without a written reason is not a decision, it is an accident. Because the model is a declared governed unit (see [Versioning Models](/topics/defendable-agents/decisions/versioning-models/)), changing 0.40 to 0.45 bumps the version, changes the hash, and appears in the [audit trail](/topics/defendable-agents/primitives/audit-trail/) as a distinct model. You cannot alter strategy silently.

## Band thresholds

A 0-100 score is precise but not actionable — nobody works a queue of floating-point numbers. Bands map the continuous score onto a small set of actions:

```json
{
  "bands": [
    { "min": 85, "label": "Very high" },
    { "min": 70, "label": "High" },
    { "min": 55, "label": "Interesting but with gaps" },
    { "min": 40, "label": "Lower priority" },
    { "min": 0,  "label": "Not prioritized now" }
  ]
}
```

Bands are a second, separate policy layer, and putting them in the manifest matters. A score of 69.8 lands in "Interesting but with gaps"; 70.1 lands in "High". That cliff is a real business boundary, so the thresholds deserve the same written rationale and the same versioning as the weights. When a buyer moves band between two runs, the change surfaces in the `band` field of the audit event's scoring block — auditable, not folklore.

## Sensitivity — knowing where the cliffs are

Before you trust a weighting, probe it. Sensitivity analysis asks: how much does the composite move when one variable moves by one point? Because the engine is a set of pure, reproducible functions, you can compute this exactly rather than guess.

A one-point rise in a Need variable (six variables, weight 0.40) shifts the layer by `(1/6)*20 = 3.33` points and the composite by `3.33 * 0.40 = 1.33`. The same one-point rise in Attractiveness moves the composite only `3.33 * 0.25 = 0.83`. So a buyer near the 70 boundary flips to "High" on a single Need point but needs more than one Attractiveness point. Knowing exactly which variables sit near which cliffs tells you where scoring effort and data quality matter most — and where a noisy variable can bounce a buyer across a band for no real reason.

## The real risk: tuning to a desired answer

Here is the failure mode I care most about. Weights are adjustable, scores are visible, and it is trivially easy to nudge weights until a favoured buyer clears the "High" line. Do that and you have inverted the whole exercise: instead of the model producing the answer, the answer produces the model. The arithmetic still looks rigorous. It is now theatre.

Determinism does not save you here — a deterministic engine will apply a rigged weighting perfectly consistently. What saves you is that the rigging is *visible*. The weight change is a version bump with a hash and an audit event; the rationale field is either honest or conspicuously empty; the [reproduce-a-decision](/topics/defendable-agents/examples/reproduce-a-decision/) workflow can replay last quarter's scores under this quarter's weights and show exactly who moved. Defensibility is not "the weights are correct" — it is "the weights are on the record, and any tuning leaves a trace". Guard the process:

- Weights change through review, never in a hot patch. Weight-tuning is on the [anti-patterns](/topics/defendable-agents/reference/anti-patterns/) list for a reason.
- Every weight and every band threshold carries a rationale, or the manifest fails validation.
- Changes go through versioning, so a weight edit is a dated, attributable event.

### Honest limits

This structure guarantees process, not correctness. Well-chosen layers with a badly-chosen weight will still produce a wrong-but-consistent number — the point is that the weight sits in the manifest with a rationale you can argue about, not buried in code. Bands add a hard discontinuity the underlying reality does not have; a buyer at 69 and one at 71 are barely different, yet they land in different queues, so treat band edges as prompts to look, not verdicts. And sensitivity analysis tells you how the score *moves*, never whether the thing it measures is the thing you should care about. Governance keeps the weights honest; it cannot make them wise.

For the arithmetic underneath a single score, see [Anatomy of a Score](/topics/defendable-agents/decisions/anatomy-of-a-score/).
