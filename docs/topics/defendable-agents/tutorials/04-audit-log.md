---
title: "Tutorial 4: The Append-Only Audit Log"
description: "Emit and read append-only JSONL audit events in a governed session, then reconstruct exactly why a decision came out the way it did from its variable trace."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Tutorial 4: The Append-Only Audit Log

By now you have a harness ([Tutorial 1](/topics/defendable-agents/tutorials/01-first-harness/)) and a scoring model ([Tutorial 2](/topics/defendable-agents/tutorials/02-scoring-model/)) running inside a governed session ([Tutorial 3](/topics/defendable-agents/tutorials/03-governed-session/)). This tutorial is about the thing that makes all of it defendable rather than merely automated: the audit log. It is where a decision stops being an opinion the agent asserts and becomes a claim with a receipt.

The rule is simple. Every governed operation emits one event. The log is append-only, one JSON object per line (JSONL), and it is fsync'd on flush so a crash cannot silently swallow the last few decisions. Nothing edits it after the fact. If you want the theory, [Primitives: Audit Trail](/topics/defendable-agents/primitives/audit-trail/) and [Decision Traces](/topics/defendable-agents/primitives/decision-traces/) cover the why. Here we write and read the thing.

## The event shape

An event is a flat-ish JSON record. The load-bearing fields are the `decision` (what happened and why) and, for scoring operations, the `scoring` block that carries the *full variable trace* — every one of the 18 buyer variables with its 1-5 score. That trace is the reconstruction key.

```json
{
  "timestamp": "2026-07-08T09:14:22.481Z",
  "sessionId": "sess_4f1a",
  "sequence": 42,
  "type": "buyer_scored",
  "actor": "buyer-scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_8801", "name": "Meridian Holdings" },
  "decision": {
    "action": "score_buyer",
    "inputs": { "signalWindowDays": 30, "layers": ["need","attractiveness","winnability"] },
    "outputs": { "total": 72.4, "band": "High" },
    "justification": "Strong Need (fresh signals), moderate Winnability"
  },
  "scoring": {
    "model": "buyer-score@1.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "signal-relevance", "score": 4 },
      { "id": "signal-velocity", "score": 3 },
      { "id": "buying-journey-stage", "score": 3 },
      { "id": "internal-mobilization", "score": 3 }
    ],
    "layerScores": { "need": 70, "attractiveness": 66.7, "winnability": 73.3 },
    "total": 72.4,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-08T00:00:00Z",
    "scoredAt": "2026-07-08T09:14:22.481Z",
    "signalDates": ["2026-07-05","2026-07-01","2026-06-20"]
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 218, "ceiling": 1000, "remaining": 782 },
  "durationMs": 34
}
```

(The `variables` array above shows the Need layer only, for brevity; a real `buyer_scored` event carries all 18.) The event types you will see across a session include `session_start`, `signal_detected`, `buyer_scored`, `match_scored`, `account_tiered`, `gtm_plan_generated`, `budget_spend`, `budget_exceeded`, `score_delta`, and `session_end`.

## Writing events: append + fsync

You do not call the writer directly in normal use — the governed session does it for you as step (4) of every operation, after it records budget and runs the deterministic score. But it helps to see the contract. The production writer is a file-based append-only log; tests use an in-memory one with the same interface.

```typescript
import { appendFileSync, openSync, fsyncSync, closeSync } from "node:fs";

export class FileAuditLog {
  private seq = 0;
  constructor(private readonly path: string) {}

  emit(event: Omit<AuditEvent, "sequence">): void {
    const line = JSON.stringify({ ...event, sequence: this.seq++ }) + "\n";
    appendFileSync(this.path, line, { encoding: "utf8" });
  }

  // called on session_end, and periodically
  flush(): void {
    const fd = openSync(this.path, "r+");
    try { fsyncSync(fd); } finally { closeSync(fd); }
  }
}
```

Two properties do the work. **Append-only**: we only ever add lines, never rewrite, so sequence numbers are monotonic and gaps are detectable. **fsync on flush**: when the session ends (or on an interval) the bytes are forced to disk, so the record survives a crash. That is what lets [Fail-Closed Behavior](/topics/defendable-agents/architecture/fail-closed-behavior/) mean something — a blocked operation still leaves a `budget_exceeded` event behind.

## Reading the log: grep and query

Because it is line-delimited JSON, the log is greppable with tools you already have. No database, no console.

```bash
# every event for one buyer, in order
grep '"id":"buyer_8801"' audit.jsonl | jq -c '{seq:.sequence, type, total:.decision.outputs.total}'

# who got scored "High" or better this session
jq -c 'select(.type=="buyer_scored" and (.decision.outputs.band|test("High|Very high")))
       | {id:.entity.id, band:.decision.outputs.band}' audit.jsonl

# did anything get blocked?
grep '"type":"budget_exceeded"' audit.jsonl | jq '.decision.justification'

# reconstruct the running budget over the session
jq -c 'select(.budget) | {seq:.sequence, op:.decision.action, total:.budget.runningTotal}' audit.jsonl
```

For anything heavier — cross-session queries, evidence bundles — see [Tutorial 8: Evidence Export](/topics/defendable-agents/tutorials/08-evidence-export/). For now, `grep` and `jq` are enough to answer real questions.

## Reconstructing a decision from its trace

This is the payoff. Someone asks: *why did buyer_8801 come out at 72.4 and land in "High"?* You do not guess and you do not re-run the agent. You pull the event and replay the arithmetic, because the engine is a pure function ([Reproducibility](/topics/defendable-agents/decisions/reproducibility/)).

From the `scoring` block: the Need layer's six variables average `(4 + 4.5 + 4 + 3 + 3 + 3) / 6 = 3.583`, times 20 = **71.7** — the small difference from the stored `70` would itself be a signal worth chasing (in a real event all six variables and the exact rounding are present). The three layers combine by weight: `Need 0.40 + Attractiveness 0.25 + Winnability 0.35`, giving `70×0.40 + 66.7×0.25 + 73.3×0.35 = 72.4`. That clears the `>= 70` threshold, so the band is **High**. Every number in that sentence is in the event. Nothing is hidden in the model's head.

The `temporal` block tells you *when* — `dataAsOf`, `scoredAt`, and the `signalDates` that fed freshness. That is what a drift check ([Temporal Pinning](/topics/defendable-agents/primitives/temporal-pinning/)) reads later to decide whether this score is still trustworthy.

## Honest limits

The log proves *process*, not *correctness*. If `signal-relevance` was scored 4 when it should have been 2, the audit trail records that mistake faithfully and reproducibly — it does not know it is wrong. That is the point, not a flaw: a consistent, visible error is one you can find by reading the trace and comparing it to reality, whereas an error buried in a black box is one you cannot. The log is also only as complete as the events you emit; an operation that runs outside the governed session leaves no line, which is exactly why the harness gates tool access ([Governance Harness](/topics/defendable-agents/architecture/governance-harness/)). Finally, append-only is a discipline enforced by your storage and permissions, not a law of physics — put the file where the agent's own credentials cannot rewrite it.

Next: [Tutorial 5: The Budget Ceiling](/topics/defendable-agents/tutorials/05-budget-ceiling/), which turns the `budget` block above into a hard stop.
