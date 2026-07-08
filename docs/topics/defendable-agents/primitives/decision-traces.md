---
title: "Decision Traces"
description: "How a defendable agent records why a decision came out the way it did — action, inputs, outputs, written justification, plus the full variable-by-variable scoring trace behind every number."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Decision Traces

An [audit trail](/topics/defendable-agents/primitives/audit-trail/) tells you *that* something happened. A decision trace tells you *why it came out the way it did*. Those are different jobs, and conflating them is one of the most common reasons an agent survives its first demo and fails its first review. A log line saying "buyer scored 69" is a claim. A decision trace is the claim *with the receipts attached* — every input, every intermediate score, the model that produced them, and a written justification in the same record.

In [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/), our worked example over a regulated professional-services market, every governed operation emits a decision trace. Nothing produces a number without also producing the paper that explains it.

## The decision block

Every audit event carries a `decision` block with four fields. Keep them honest and keep them small:

| Field | What it holds | Why it matters |
|---|---|---|
| `action` | the operation performed (`buyer_scored`, `match_scored`, `account_tiered`) | names the thing being defended |
| `inputs` | the exact inputs the operation consumed | lets you re-run it |
| `outputs` | what the operation produced | the claim you are standing behind |
| `justification` | a short written rationale | the sentence a reviewer reads first |

The `justification` is not decoration. It is the human-readable bridge between a wall of numbers and a person who has to sign off on the result. Write it as if the reader is a compliance officer with ten minutes, because they are.

## The scoring block

For scored operations the `decision` block is not enough — a reviewer wants to see the arithmetic. That is what the separate `scoring` block is for:

- `model` — which model produced the score, by version
- `variables` — every variable id and its 1–5 score
- `layerScores` — the 0–100 score for each layer
- `total` — the weighted composite
- `band` — the priority band the total falls into

Because the [scoring engine is deterministic](/topics/defendable-agents/decisions/reproducibility/) — pure functions, same inputs to same outputs — the `scoring` block is not a snapshot you have to trust. It is a recipe. Feed the same variables to the same model version and you get the same total, every time. The trace *is* the reproduction instructions.

## Why is this a 69?

Here is the question a decision trace exists to answer. Someone points at a buyer priority of 69 — "Interesting but with gaps", just under the "High" band at 70 — and asks why.

Without a trace you are guessing, or worse, re-scoring and hoping the number lands the same. With a trace you read it straight off the record. The Buyer score is a weighted composite of three layers — Need (weight 0.40), Attractiveness (0.25) and Winnability (0.35) — where each layer score is the mean of its six 1–5 variables times 20. So a 69 decomposes exactly:

```json
{
  "timestamp": "2026-07-08T09:14:22.481Z",
  "sessionId": "sess_4f9c1a",
  "sequence": 42,
  "type": "buyer_scored",
  "actor": "buyer-scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_2201", "name": "Buyer 2201" },
  "decision": {
    "action": "buyer_scored",
    "inputs": { "signalCount": 4, "modelVersion": "buyer-score@1.3.0" },
    "outputs": { "total": 69, "band": "Interesting but with gaps" },
    "justification": "Strong, fresh demand signals lift Need to 82, but a weak competitive position and thin decision access hold Winnability to 47, pulling the composite just under the High band."
  },
  "scoring": {
    "model": "buyer-score@1.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "signal-relevance", "score": 4 },
      { "id": "signal-velocity", "score": 4 },
      { "id": "buying-journey-stage", "score": 4 },
      { "id": "internal-mobilization", "score": 4 },
      { "id": "mandate-value", "score": 4 },
      { "id": "strategic-value", "score": 4 },
      { "id": "growth-potential", "score": 4 },
      { "id": "sector-fit", "score": 4 },
      { "id": "reference-value", "score": 3.5 },
      { "id": "cross-sell-potential", "score": 4.5 },
      { "id": "competitive-position", "score": 2 },
      { "id": "relationship-proximity", "score": 2.5 },
      { "id": "known-criteria", "score": 3 },
      { "id": "decision-access", "score": 2 },
      { "id": "internal-capacity", "score": 2.5 },
      { "id": "relevant-experience", "score": 2 }
    ],
    "layerScores": { "Need": 82, "Attractiveness": 80, "Winnability": 47 },
    "total": 69,
    "band": "Interesting but with gaps"
  },
  "temporal": {
    "dataAsOf": "2026-07-08",
    "scoredAt": "2026-07-08T09:14:22.481Z",
    "signalDates": ["2026-07-02", "2026-07-01", "2026-06-28", "2026-06-20"]
  },
  "durationMs": 12
}
```

Do the arithmetic against the trace and it holds: `0.40 × 82 + 0.25 × 80 + 0.35 × 47 = 32.8 + 20 + 16.45 = 69.25`, rounded to 69. The `justification` names the culprit in one sentence — Winnability at 47 — and the `variables` array shows exactly which two scores dragged it down: `competitive-position` at 2 and `decision-access` at 2. No re-scoring, no guessing. The answer to "why is this a 69?" is a read operation, not an investigation.

Note the `temporal` block riding alongside. The four `signalDates` and the `dataAsOf` are what a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) uses later to tell you whether this 69 is still current or has drifted. A trace is not only a record of the past; it is the anchor future [drift detection](/topics/defendable-agents/primitives/drift-detection/) measures against.

## Honest limits

A decision trace defends *process*, not *correctness*. If a variable is wrong — say `competitive-position` should have been 4, not 2 — the trace does not catch that. What it does is make the mistake **visible and reproducible**: the wrong 2 is right there in the `variables` array, applied consistently, attached to a justification a reviewer can challenge. That is how you find bad variables — by reading the trace, not by hoping. An untraced agent that scored the same buyer at 69 gives you nothing to argue with.

The other limit is discipline. A `justification` that says "scored by model" is worse than useless; it looks like accountability while providing none. The trace is only as defendable as the honesty of the sentence a human writes into it. That is maintenance work, not a one-time setup — see [what defendable means](/topics/defendable-agents/argument/what-defendable-means/).

Decision traces are the mechanism behind the SOC 2 CC7.2 control in our [control mapping](/topics/defendable-agents/compliance/control-mapping/): full variable inputs and outputs, on every operation, on the record. When you want to walk one end-to-end, work through [reproduce a decision](/topics/defendable-agents/examples/reproduce-a-decision/).
