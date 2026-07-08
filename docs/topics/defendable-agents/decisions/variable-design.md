---
title: "Designing 1-5 Variables"
description: "How to design scoring variables on a 1-5 scale with explicit scoring guides, so two analysts or an agent score the same input the same way, reproducibly."
image: assets/images/kcp-agent-020-04-defeating-prompt-injection.webp
---

# Designing 1-5 Variables

A deterministic scoring engine is only as defendable as the variables it feeds on. The engine in Lodestar is a set of pure functions: a layer score is the mean of its 1-5 variable scores times 20, and a composite is a fixed weighting of layer scores. Given the same inputs it returns the same outputs, every time. That property is worth nothing if the *inputs* are guesswork. If two analysts look at the same buyer and one writes `4` where the other writes `2`, the machinery downstream is immaculate and the answer is still noise.

So the real design work is not in the arithmetic. It is in defining each variable tightly enough that a human and an agent, scoring the same evidence, land on the same number. This page is about that discipline.

## Anatomy of a variable

A variable is not a label with a number stapled to it. In Lodestar every scoring variable carries five design fields beyond its `layer` and `scale`:

```yaml
- id: signal-freshness
  layer: need
  question: "How recently did the observable buying signal occur?"
  scale: 1-5
  scoring_guide:
    5: "Signal observed within the last 3 days"
    4.5: "Within 7 days"
    4: "Within 14 days"
    3: "Within 30 days"
    2: "Within 60 days"
    1.5: "Within 90 days"
    1: "Older than 90 days, or no dated signal"
  evidence: "URL and publication date of the source event"
  independence: "Measures recency only; not relevance, not strength"
```

The `id` is stable and machine-referenced — it appears verbatim in the audit trail's `scoring.variables[]` array, so it must never be renamed casually. The `question` is the single thing being measured, phrased so it has one answer. The `scoring_guide` is the load-bearing part, covered below. The `evidence` field says what an analyst must point at to justify the score — this is what makes a score a *decision* rather than an opinion, and it is what the [decision trace](/topics/defendable-agents/primitives/decision-traces/) captures. The `independence` note is a standing reminder of what this variable does *not* measure.

Eighteen such variables define a buyer across three layers — Need, Attractiveness, Winnability. Twenty-one define a match. Each one is small on purpose.

## The scoring_guide as inter-rater calibration

The single most valuable field is `scoring_guide`. It is a rubric: for each point on the scale, a concrete, checkable description of what earns that score. Its purpose is inter-rater reliability — the boring statistical property that two raters, working independently, agree.

Compare a variable without a guide:

> **buying-journey-stage** (1-5): how far along is the buyer?

Two analysts will disagree constantly, and neither can say the other is wrong. Now the same variable with a guide:

| Score | The buyer... |
|------|-------------|
| 5 | has a named, funded initiative with a stated timeline |
| 4 | has publicly committed to acting this period |
| 3 | is actively researching; discovery-stage behaviour observed |
| 2 | shows early, unfunded interest |
| 1 | no observable movement |

Now disagreement is a *finding*. If one rater says `4` and the other `2`, they can point at the evidence and the rubric and resolve it. The rubric turns a matter of taste into a matter of fact. It is also exactly what you hand the model at the edge: the same guide that calibrates two humans calibrates the agent, because the agent is scoring against the same enumerated conditions rather than a vibe. See [the model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) for where that boundary sits.

There is an honest limit here. A rubric enforces *consistency*, not *truth*. If the rubric's definition of "5" is wrong, everyone applies the wrong definition identically. The value of determinism is that the error is applied visibly and reproducibly — you can find it, argue about it, and fix it in one place — not that it cannot occur. [Reproducibility](/topics/defendable-agents/decisions/reproducibility/) buys you auditability, not correctness.

## Good variables vs bad variables

A well-designed variable is **atomic, observable, and monotonic**.

- **Atomic** — it measures one thing. `signal-strength` measures how strong a signal is; `signal-relevance` measures how relevant it is to the offering; `signal-freshness` measures how recent it is. Three variables, not one blurred "signal quality" score.
- **Observable** — its evidence field can be filled from public data. If scoring it requires a guess about someone's private intent, it is not a variable, it is a rumour with a number.
- **Monotonic** — higher is unambiguously "more" of the thing. `5` should always be the strong end.

Bad variables fail one of these. "Overall fit" is not atomic — it silently bundles sector, value, and winnability, which is why Lodestar keeps `sector-fit`, `mandate-value`, and `competitive-position` as *separate* variables in *separate* layers. "Likelihood to close" is not observable — it is an outcome, not an input, and folding outcomes back into inputs is how you build a model that flatters itself. See [variable-level anti-patterns](/topics/defendable-agents/reference/anti-patterns/) for the full list.

## Freshness and decay

Some variables measure the *age* of evidence, and here the scoring guide encodes a decay curve. `signal-freshness` uses a roughly 30-day half-life: 5 at three days, dropping through 4.5, 4, 3, 2, 1.5 and bottoming at 1 past ninety days. The curve is baked into the `scoring_guide` as day thresholds, so scoring it is a lookup, not a judgement.

```typescript
export function freshnessScore(ageDays: number): number {
  if (ageDays <= 3) return 5;
  if (ageDays <= 7) return 4.5;
  if (ageDays <= 14) return 4;
  if (ageDays <= 30) return 3;
  if (ageDays <= 60) return 2;
  if (ageDays <= 90) return 1.5;
  return 1;
}
```

Decay variables interact with [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/): the pin records the `signalDates[]` that fed the score, so a later drift check can tell that a score of `4` has silently aged into what should now be a `2`. The variable measures freshness at scoring time; the pin lets you detect that scoring time is now in the past. Neither refreshes the underlying data — that is still a job you have to schedule.

## Keeping variables independent

The composite maths assumes variables are independent. If two variables secretly measure the same thing, that thing is double-weighted and the composite lies. When `signal-strength` and `signal-relevance` both quietly reward "big public event", every splashy announcement is counted twice and the Need layer inflates.

Independence is a design constraint you enforce by construction: give each variable a distinct `question`, a distinct `evidence` requirement, and an explicit `independence` note stating what it excludes. Then check it empirically — score a sample and look at the correlations. Two variables that always move together are one variable wearing two hats; collapse them, or sharpen the boundary. How the independent variables then roll up is covered in [layers, weights, and bands](/topics/defendable-agents/decisions/layers-weights-bands/), and the full walk-through of a single score lives in [anatomy of a score](/topics/defendable-agents/decisions/anatomy-of-a-score/).

Get the variables right and the rest of the engine is just arithmetic you can trust. Get them wrong and no amount of determinism will save you — it will only make your mistake perfectly repeatable.
