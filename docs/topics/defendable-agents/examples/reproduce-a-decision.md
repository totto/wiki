---
title: "Example: Reproducing a Decision"
description: "Take an old buyer score from the append-only audit log and reproduce it exactly from its pinned inputs, model version and temporal pin — the proof an audit needs."
image: assets/images/kcp-agent-020-03-model-at-the-edge.webp
---

# Example: Reproducing a Decision

Three months after Lodestar scored a buyer, someone asks: "why did this account get 'High' priority in April?" In most agent systems that question has no answer. The score was a side effect of a prompt, the prompt is gone, the data behind it has moved on, and the model has been updated twice since. You are reduced to guessing.

In a defendable agent the answer is a lookup followed by a re-run that returns the identical number. This page walks through that end to end: pull the event, rebuild the exact inputs, pin the model version and `dataAsOf`, re-score, and compare. It is the concrete payoff of everything in [Reproducibility](/topics/defendable-agents/decisions/reproducibility/) and [Temporal Pinning](/topics/defendable-agents/primitives/temporal-pinning/).

## Step 1 — Pull the event from the audit log

Every governed score writes one line to an append-only JSONL log (see [Audit Trail](/topics/defendable-agents/primitives/audit-trail/)). We want the `buyer_scored` event for this entity. Each line is a self-contained record, so a single `grep` finds it.

```bash
grep '"type":"buyer_scored"' audit/session-2026-04-11.jsonl \
  | grep '"id":"buyer-4821"'
```

The event carries the full decision trace — not a summary, the actual variable-by-variable inputs:

```json
{
  "timestamp": "2026-04-11T09:22:14.006Z",
  "sessionId": "sess-2026-04-11-a7",
  "sequence": 41,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer-4821", "name": "Meridian Holdings" },
  "scoring": {
    "model": "buyer-score@2.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "signal-relevance", "score": 4 },
      { "id": "signal-velocity", "score": 3 },
      { "id": "buying-journey-stage", "score": 3 },
      { "id": "internal-mobilization", "score": 2 },
      { "id": "mandate-value", "score": 4 },
      { "id": "strategic-value", "score": 5 },
      { "id": "growth-potential", "score": 4 },
      { "id": "sector-fit", "score": 4 },
      { "id": "reference-value", "score": 3 },
      { "id": "cross-sell-potential", "score": 3 },
      { "id": "competitive-position", "score": 4 },
      { "id": "relationship-proximity", "score": 3 },
      { "id": "known-criteria", "score": 4 },
      { "id": "decision-access", "score": 3 },
      { "id": "internal-capacity", "score": 4 },
      { "id": "relevant-experience", "score": 5 }
    ],
    "layerScores": { "need": 68.33, "attractiveness": 76.67, "winnability": 76.67 },
    "total": 73.33,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-04-10T23:59:59.000Z",
    "scoredAt": "2026-04-11T09:22:14.006Z",
    "signalDates": ["2026-04-08", "2026-04-05", "2026-03-29"]
  }
}
```

## Step 2 — Rebuild the inputs and pin the model

There is nothing to reconstruct from external state. The 18 variable scores are in the record, the model identity is `buyer-score@2.3.0`, and the temporal pin fixes `dataAsOf` to the end of 10 April. The scoring model is a governed [KCP](/topics/defendable-agents/kcp/declaring-governed-units/) unit, so we load *that version* deterministically rather than whatever is current today.

```typescript
import { loadModel } from "./kcp";
import { scoreBuyer } from "./engine";

// The exact event, read back from the JSONL line.
const ev = readEvent("audit/session-2026-04-11.jsonl", 41);

// Pin the model by version — loadModel resolves the exact release, never "latest".
const model = await loadModel(ev.scoring.model); // resolves "buyer-score@2.3.0", never "latest"

// Feed the recorded variables straight back in.
const inputs = Object.fromEntries(
  ev.scoring.variables.map(v => [v.id, v.score])
);

const result = scoreBuyer(model, inputs);
```

## Step 3 — Re-run the deterministic engine

The engine is a pure function: a layer score is the mean of its 1-5 variables times 20, and the buyer total is the weighted composite Need 0.40, Attractiveness 0.25, Winnability 0.35. Same inputs, same model, same output — no clock, no network, no prompt. You can check the arithmetic by hand:

| Layer | Mean of variables | ×20 | Weight | Contribution |
|---|---|---|---|---|
| Need | 3.4167 | 68.33 | 0.40 | 27.33 |
| Attractiveness | 3.8333 | 76.67 | 0.25 | 19.17 |
| Winnability | 3.8333 | 76.67 | 0.35 | 26.83 |
| **Total** | | | | **73.33** |

```typescript
console.log(result.total);          // 73.33
console.log(result.band);           // "High"
console.log(result.layerScores);    // { need: 68.33, attractiveness: 76.67, winnability: 76.67 }

assert.deepEqual(result.total, ev.scoring.total);
assert.deepEqual(result.band, ev.scoring.band);
```

The reproduced score equals the recorded score to the decimal. The band comes straight from the fixed thresholds (`>=70` is "High"), so it reproduces too. If you want the arithmetic itself explained, see [Anatomy of a Score](/topics/defendable-agents/decisions/anatomy-of-a-score/).

## What this proves for an audit

An auditor is not asking "is 73.33 the *right* number?" They are asking "can you show that this decision was made the way you say it was, and would it come out the same if we checked?" Reproducibility answers exactly that:

- **The inputs are the record.** The 18 variables that produced the score are in the log, not inferred afterwards. That is the decision-trace control (SOC 2 PI1.5).
- **The model is pinned.** `buyer-score@2.3.0` is resolved by version, so a later model change cannot rewrite April's decision. Version and hash both live in the temporal pin.
- **The data window is fixed.** `dataAsOf` and `signalDates` show precisely which signals were in scope, which is the data-provenance control (ISO 27001 A.5.12).
- **The re-run is mechanical.** Anyone with the log and the model can repeat it and get 73.33. That is the reproducibility evidence behind the ISO 27001 A.8.32 change-management control, and it is what turns a claim into evidence you can package (see [Evidence Packages](/topics/defendable-agents/compliance/evidence-packages/)).

## Honest limits

Reproducibility guarantees **process, not correctness**. If `internal-mobilization` was scored 2 when the honest reading of the evidence was 4, the engine will reproduce the wrong 2 forever — consistently and visibly. That is the point: the mistake is pinned in the open where a reviewer can find it and argue with it, instead of dissolving into a lost prompt. Determinism makes errors *auditable*, not absent.

Two related caveats. The temporal pin tells you the data was current to 10 April; it does **not** refresh that data, and re-running today with the same pin deliberately ignores anything newer — that separation is what [Drift Detection](/topics/defendable-agents/primitives/drift-detection/) exists to flag. And the variable scores themselves came from the model at the edge; reproducing them faithfully does not upgrade a judgement call into a fact. What you get is the ability to see, exactly, what was decided and on what basis — which is the whole argument in [What Defendable Means](/topics/defendable-agents/argument/what-defendable-means/).
