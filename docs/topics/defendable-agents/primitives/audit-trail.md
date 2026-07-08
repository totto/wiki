---
title: "The Append-Only Audit Trail"
description: "The append-only JSONL audit log and its event schema — the evidence a defendable agent produces as a byproduct of how it works, not as an afterthought."
image: assets/images/kcp-agent-020-04-defeating-prompt-injection.webp
---

# The Append-Only Audit Trail

Most systems bolt logging on afterwards. You ship the feature, an auditor asks how a decision was made, and someone goes spelunking through application logs that were never designed to answer that question. A defendable agent inverts this: the audit trail is not a side effect of running, it is the *product* of running. Every governed operation exists to produce a durable, ordered record of what it decided and why. If the record cannot be written, the operation does not proceed. That is the whole idea.

This page describes the audit trail primitive as it works in Lodestar, my reference system for scoring buyers and firms in a regulated professional-services market. For the wider picture of how this fits together see the [primitives overview](/topics/defendable-agents/primitives/overview/) and the [governance harness](/topics/defendable-agents/architecture/governance-harness/).

## Append-only, and why that word matters

The log is a JSONL file: one JSON object per line, appended, never rewritten. There is no update path, no delete path, no compaction that rewrites history. On flush the writer calls `fsync` so the bytes are on disk before the operation reports success — a crash between the write and the acknowledgement cannot leave you with an event the caller believes was recorded but which is not durable.

Append-only is not a stylistic preference. Evidence that can be edited in place is not evidence. If an auditor, a regulator, or a future version of yourself is going to trust the record, the record has to be structurally incapable of quiet revision. You can *append* a correction — a later event that supersedes an earlier one — but the earlier event stays on its line, with its original timestamp and sequence number. History accumulates; it never gets tidied away. This is what makes the trail hold up under the [evidence-package](/topics/defendable-agents/compliance/evidence-packages/) work later on; in ISO 27001 terms it is the A.12.4 logging control satisfied by a mechanism rather than a promise.

## The event schema

Every line is one event. The schema is deliberately fat: I would rather carry the full decision context on every relevant event than reconstruct it from three tables at audit time. Here is a real `buyer_scored` event:

```json
{
  "timestamp": "2026-07-08T09:14:22.481Z",
  "sessionId": "sess_2026-07-08_a91f",
  "sequence": 42,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_7731", "name": "Buyer 7731" },
  "decision": {
    "action": "score_buyer",
    "inputs": { "signalWindowDays": 90, "modelUnit": "buyer-scoring-v3" },
    "outputs": { "total": 78.6, "band": "High" },
    "justification": "Strong recent signals, moderate winnability"
  },
  "scoring": {
    "model": "buyer-scoring-v3",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "need": 78, "attractiveness": 72, "winnability": 84 },
    "total": 78.6,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-07T00:00:00Z",
    "scoredAt": "2026-07-08T09:14:22.481Z",
    "signalDates": ["2026-07-05", "2026-06-28"]
  },
  "budget": {
    "cost": 5, "currency": "units",
    "runningTotal": 210, "ceiling": 1000, "remaining": 790
  },
  "durationMs": 37
}
```

The fields divide into layers of accountability:

| Field | Answers |
|-------|---------|
| `timestamp`, `sessionId`, `sequence` | when, in which session, in what order |
| `type`, `actor` | what kind of event, which agent produced it |
| `entity` | what was decided about |
| `decision` | the action, its inputs, outputs and a human-readable justification |
| `scoring` | the full variable trace — every 1–5 score, the layer scores, the composite and its band |
| `temporal` | the provenance stamp: what data, as of when |
| `budget` | the cost and where it left the ledger |
| `durationMs` | how long it took |

The `scoring` block is the load-bearing one. Because Lodestar's engine is a set of [pure deterministic functions](/topics/defendable-agents/decisions/reproducibility/), carrying the exact variable inputs on the event means anyone can re-run the model against them and get the identical `total` — the decision-trace evidence a SOC 2 CC7.2 review is looking for. This is also where determinism earns its keep: it guarantees *process*, not *correctness*. If `signal-freshness` was scored 4.5 against a stale signal, the wrong value is applied consistently and it is sitting right there on the line, reproducible, ready to be caught. See [decision traces](/topics/defendable-agents/primitives/decision-traces/) for how that trace is designed, and [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) for the provenance stamp.

Event types across a session include `session_start`, `signal_detected`, `buyer_scored`, `match_scored`, `account_tiered`, `gtm_plan_generated`, `monitoring_check`, `reanalysis_triggered`, `score_delta`, `budget_spend`, `budget_exceeded`, and `session_end`. The `budget_exceeded` event is the one that fires when the [budget ceiling](/topics/defendable-agents/primitives/budget-and-bounding/) is hit and the operation refuses to run — a fail-closed refusal is itself an audited event, not a silent gap.

## Two writers: file and in-memory

There are two implementations behind the same interface.

- **File-based append-only log** for production. It appends to a JSONL file and `fsync`s on flush. This is the writer whose output becomes evidence.
- **In-memory log** for tests. Same interface, events held in an array, nothing touches the disk. Your test suite can assert on the exact sequence of events a governed operation emitted without leaving files around or needing cleanup.

Because the two share an interface, a governed session takes the log as a dependency and never knows which one it holds. The test asserting that a budget overrun emits `budget_exceeded` runs against the in-memory writer; the production session emits the identical event shape to disk.

## Querying the log

JSONL is deliberately boring, which makes it queryable with tools you already have. Filtering by session, entity, or event type is a one-liner:

```bash
# every scoring decision for one buyer, in order
grep '"id": "buyer_7731"' audit.jsonl \
  | jq -c 'select(.type == "buyer_scored")
           | {seq: .sequence, total: .scoring.total, band: .scoring.band}'

# running unit total as of the last buyer scored
jq -s 'map(select(.type == "buyer_scored")) | last | .budget.runningTotal' audit.jsonl
```

For anything heavier — building a customer-facing evidence export, cross-session drift analysis — the same lines load straight into whatever store you like. The point is that the *authoritative* record is a flat, append-only, human-readable file. Downstream indexes are conveniences you can rebuild; they are never the source of truth.

## Honest limits

The audit trail records faithfully; it does not adjudicate. It will capture a wrong justification just as durably as a right one — its job is to make the wrong one *visible and permanent*, not to prevent it. It grows without bound by design, so retention and archival are operational work you own, not something the primitive solves ([operating and maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/)). And an append-only file on a disk you fully control is only as tamper-evident as that control; if your threat model includes a hostile operator, you need external anchoring — periodic hashes shipped somewhere you cannot rewrite — on top of what this primitive gives you. Governance is maintenance, not a one-time setup.
