---
title: "What \"Defendable\" Means"
description: "A defendable decision is declared in advance, reproducible, and evidenced. Here is what each property means, why it differs from explainable AI, and how legal and engineering defensibility meet."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# What "Defendable" Means

I use the word "defendable" deliberately, and I mean it in two senses at once. An engineer defends a decision when they can show it was computed correctly, from known inputs, by a known procedure. A lawyer defends a decision when they can produce the record that proves it — before a regulator, an auditor, or a court. A system that is defendable in the first sense but not the second is a demo. A system that is defendable in the second sense but not the first is theatre. I want both, and I want them to be the same artefact.

A defendable decision has three properties. It is **declared in advance**, it is **reproducible**, and it is **evidenced**. Drop any one and the other two stop being worth much.

## Declared in advance

The procedure that produces a decision exists, in writing, before the decision is made — not reconstructed afterwards to fit the answer. In [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/), the example system I use throughout this guide, a buyer score is a weighted composite of three layers: Need at weight 0.40, Attractiveness at 0.25, Winnability at 0.35. Each layer is the mean of six variables scored 1–5, times twenty. Those weights, those variables, and the priority bands (`>=85` "Very high", `>=70` "High", and so on) are written down and version-pinned as a [scoring model manifest](/topics/defendable-agents/decisions/scoring-model-manifest/) before any buyer is touched.

Declaration is what separates a rule from a rationalisation. If I can change the weights after seeing the output, the weights explain nothing. The [deterministic planner](/topics/defendable-agents/architecture/deterministic-planner/) selects the model version as a governed unit, so the model in force at scoring time is a fact, not a preference.

## Reproducible

Give the engine the same inputs and it returns the same outputs, forever. The scoring functions are pure — no clock reads, no network calls, no hidden state. Anyone holding the input variables and the model version can recompute the total and get the identical number. This is what the [reproducibility](/topics/defendable-agents/decisions/reproducibility/) property buys you: a decision you can re-run in front of a sceptic.

Be honest about what determinism guarantees. It guarantees **process, not correctness**. If `signal-freshness` was scored 4 when the evidence said 2, the engine applies that error consistently — but visibly, and reproducibly, on every run. That is the point. A wrong variable in a deterministic pipeline is a bug you can find, reproduce, and fix. A wrong variable in a probabilistic one is noise. I develop this contrast at length in [determinism vs probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/).

## Evidenced

Every decision leaves a record sufficient to reconstruct it without the running system. Lodestar writes an [append-only audit trail](/topics/defendable-agents/primitives/audit-trail/) — JSONL, one event per line, fsync on flush — and each scoring event carries the full variable trace, not a summary:

```json
{
  "timestamp": "2026-07-08T09:14:02.113Z",
  "sessionId": "sess_4f2a",
  "sequence": 37,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "b_2291", "name": "Buyer 2291" },
  "scoring": {
    "model": "buyer-scoring@2.1.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "need": 76, "attractiveness": 62, "winnability": 68 },
    "total": 69.7,
    "band": "Interesting but with gaps"
  },
  "temporal": {
    "dataAsOf": "2026-07-07",
    "scoredAt": "2026-07-08T09:14:02.113Z",
    "signalDates": ["2026-07-05", "2026-06-30"]
  }
}
```

That single line is the evidence. It names the model version, every input, every layer score, the total, the band, and the [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) fixing what data the score was allowed to see. Hand this to an auditor and they can recompute the total by hand.

## Skip-reasons, not silence

Here is the property that most systems get wrong, and the one I care about most. When a governed operation does **not** run, the record must say why. Silence is not evidence. If the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) ceiling is exceeded, the operation does not quietly fall through — it throws and emits a `budget_exceeded` event. If [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) blocks a tool call, the block is logged as a decision with a justification, exactly like a positive score.

A defendable log is one where every gap is accounted for. "We did not score this buyer" is a claim you must be able to defend as thoroughly as "we scored it 69.7". The absence of an event is itself something a reviewer will ask about, and the honest answer is a recorded skip-reason — not a shrug. This is the difference between a system that can survive an audit and one that merely hopes not to be audited.

## Not the same as explainable AI

Explainable-AI techniques try to reconstruct, after the fact, why a probabilistic model produced an output — attention maps, feature attributions, saliency. They are approximations of an opaque process, and they change when you re-run them. Defendability inverts the arrow. The decision is not opaque and then explained; it is **transparent by construction and then recorded**. There is nothing to reverse-engineer because the arithmetic was legible from the start.

That is why the [model sits at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) in this architecture. A language model is excellent at reading a messy signal and proposing a 1–5 score for `signal-relevance`. It is a poor place to lodge the weighting, the composition, and the banding — those belong in code you can read and re-run. The model at the edge is still a model, with all a model's failure modes; the defence is that its output enters a pipeline that pins, records, and reproduces everything downstream of it.

## The two defensibilities meet

Legal defensibility is not a separate layer bolted on for compliance. It falls out of engineering defensibility done properly. The append-only log satisfies audit-logging controls; the variable trace satisfies decision-trace controls; the temporal pin satisfies data-provenance controls; the deterministic engine satisfies reproducibility controls. One artefact, two audiences. I map each mechanism to its control in [control mapping](/topics/defendable-agents/compliance/control-mapping/).

None of this is free, and none of it is finished once built. Governance is maintenance: models drift, weights need revisiting, and a fail-closed policy tuned too tightly will block legitimate work until someone loosens it. Defendability is a property you keep paying for. But it is the only property that lets you stand behind an agent's decision a year later — and mean it.
