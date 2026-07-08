---
title: "Tutorial 3: The Governed Session"
description: "Wrap scoring in a governed session that shares one audit log, one budget ledger, and one map of temporal pins across every operation, then end and flush."
image: assets/images/kcp-agent-020-04-defeating-prompt-injection.webp
---

# Tutorial 3: The Governed Session

By now you have a harness ([Tutorial 1](/topics/defendable-agents/tutorials/01-first-harness/)) and a scoring model ([Tutorial 2](/topics/defendable-agents/tutorials/02-scoring-model/)). Both are useful in isolation, but neither is defendable on its own. A pure score tells you _what_ was decided; it does not tell you what it cost, whether the inputs were stale, or leave a record anyone can audit six months later. The **governed session** is the object that ties those concerns together.

A session is deliberately narrow: one unit of work, one actor, one shared context. Everything that happens inside it writes to the **same** append-only [audit log](/topics/defendable-agents/primitives/audit-trail/), draws down the **same** [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/), and registers pins in the **same** map of [temporal pins](/topics/defendable-agents/primitives/temporal-pinning/). That sharing is the whole point. If each operation kept its own log, you would have fragments; the session is what makes the trace continuous.

## Creating a session

`createGovernedSession` takes the loaded harness policy and returns an object that owns the three shared resources. Nothing is emitted yet beyond the opening event.

```typescript
import { createGovernedSession } from "./governance/session";
import { loadHarness } from "./governance/harness";

const harness = await loadHarness("harness.yaml");

const session = createGovernedSession({
  sessionId: "sess-2026-07-08-0042",
  actor: "buyer-scoring-agent",
  policy: harness.policy,          // fail_closed, audit_all, max_units, budget
  auditPath: harness.audit.path,   // append-only JSONL, fsync on flush
});
// emits: { type: "session_start", sessionId, actor, timestamp }
```

The `policy` here is not decoration. It carries `fail_closed: true`, `audit_all: true`, the `max_units` ceiling (1000 in the example harness), and the `budget` block. The session enforces these; it does not merely record them. That distinction is the subject of [fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/) — a session that cannot write its audit log refuses to score, it does not score quietly.

## Running a governed score

Here is the sequence every governed operation follows, in order. It is worth reading the steps as a contract, because the order is what makes the record trustworthy.

```typescript
const result = await session.scoreBuyer({
  entity: { type: "buyer", id: "buyer-8814", name: "Acme Holdings" },
  variables: needAttractivenessWinnabilityScores, // 18 vars, each 1-5
  dataAsOf: "2026-07-06",
  signalDates: ["2026-07-01", "2026-07-05"],
});
```

Internally, `scoreBuyer` does four things, and it does them in this order:

1. **Record budget first.** `ledger.record("buyer_scoring", "buyer-8814", 5)` checks the ceiling _before_ recording. If `runningTotal + 5 > 1000` it returns `accepted: false`, and the operation throws and emits a `budget_exceeded` event. Nothing is scored. See [Tutorial 5](/topics/defendable-agents/tutorials/05-budget-ceiling/) for the ceiling in anger.
2. **Run the pure score.** The deterministic engine computes each layer as the mean of its 1–5 variables × 20, then the weighted composite: Need 0.40, Attractiveness 0.25, Winnability 0.35. Same inputs, same output, every time — that is [reproducibility](/topics/defendable-agents/decisions/reproducibility/).
3. **Create a temporal pin.** `{ scoredAt, dataAsOf, signalDates, modelVersion, modelHash }` so drift can be detected later ([Tutorial 6](/topics/defendable-agents/tutorials/06-temporal-drift/)).
4. **Emit the audit event** carrying the full variable trace.

## What gets emitted

The `buyer_scored` event is not a summary line — it is the whole decision, replayable. One JSONL line, fsync'd on flush:

```json
{
  "timestamp": "2026-07-08T09:14:02.331Z",
  "sessionId": "sess-2026-07-08-0042",
  "sequence": 3,
  "type": "buyer_scored",
  "actor": "buyer-scoring-agent",
  "entity": { "type": "buyer", "id": "buyer-8814", "name": "Acme Holdings" },
  "decision": {
    "action": "score_buyer",
    "inputs": { "variables": 18, "dataAsOf": "2026-07-06" },
    "outputs": { "total": 78, "band": "High" },
    "justification": "weighted composite of 3 layers"
  },
  "scoring": {
    "model": "buyer-scoring@2.1.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "need": 74, "attractiveness": 80, "winnability": 79 },
    "total": 78,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-06",
    "scoredAt": "2026-07-08T09:14:02.331Z",
    "signalDates": ["2026-07-01", "2026-07-05"]
  },
  "budget": {
    "cost": 5, "currency": "units",
    "runningTotal": 15, "ceiling": 1000, "remaining": 985
  },
  "durationMs": 12
}
```

Note that the band `High` follows from the fixed thresholds (`>=85` Very high, `>=70` High, `>=55` Interesting but with gaps, `>=40` Lower priority, else Not prioritized now). Anyone can recompute it from the `total`; nothing is hidden in the agent. This is what a [decision trace](/topics/defendable-agents/primitives/decision-traces/) looks like when it is a first-class artefact rather than a log statement bolted on afterwards.

## Ending and flushing

Closing the session emits a summary and, critically, **flushes** the log with `fsync`. Until the flush returns, you have no durability guarantee; do not report a session as complete before it does.

```typescript
await session.end();
// emits: { type: "session_end", sessionId,
//          summary: { operations: 3, unitsSpent: 15, entitiesScored: 3 } }
// then fsyncs the JSONL log to disk
```

The `session_end` event gives an auditor the totals to reconcile against the individual events: three operations, fifteen units, and a running total that must match the last `budget.runningTotal` seen. Reconciliation that closes is a good sign the trace is intact.

## Honest limits

A session guarantees **process, not correctness**. If one of your 18 variables is mis-scored — say `signal-freshness` reads a wrong date — the session will apply that error consistently, pin it, and log it. The determinism does not fix the mistake; it makes the mistake _visible and reproducible_, which is how you catch it in review. Likewise, the temporal pin records that data was `dataAsOf 2026-07-06`; it does not go and fetch fresher data. And the budget ceiling is a blunt instrument — set it too low and a legitimate batch of scores fails closed mid-run. Governance here is maintenance, not a one-time wiring job.

Next, [Tutorial 4](/topics/defendable-agents/tutorials/04-audit-log/) reads these events back and shows how to reconcile a full session. For the architectural picture of how the session sits between the deterministic engine and the model at the edge, see the [architecture overview](/topics/defendable-agents/architecture/overview/).
