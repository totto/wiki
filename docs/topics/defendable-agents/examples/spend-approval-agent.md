---
title: "Example: A Spend-Approval Agent"
description: "A governed agent that approves spend within a hard budget ceiling, refusing and recording every request that crosses the line, with the audit log as the approval record."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Example: A Spend-Approval Agent

Most "AI approval" demos put the model in charge of the decision: you ask it politely to stay under budget, and it usually does. Usually is not a control. In Lodestar — the codename I use for the proprietary system behind this guide, an agent operating in a regulated professional-services market — approval is not a thing the model decides. It is a thing the **budget ledger** enforces, before any expensive work runs, and records whether it allowed the spend or refused it.

This page walks a single session end to end: a run that approves several operations and then hits a request that would cross the ceiling. The refusal is the interesting part. Everything the agent does — allowed or denied — becomes a line in an append-only log, and that log *is* the approval record.

## Budget as the core primitive

Every governed operation carries a cost in abstract **units**. The ceiling is set per session in the harness, not negotiated with the model:

```yaml
# harness.yaml (excerpt)
policy:
  fail_closed: true
  audit_all: true
  max_units: 50
  budget:
    amount: 1000       # session ceiling, in units
    currency: units
  context_budget: 200000
audit:
  path: ./state/audit/session.jsonl
```

The cost table is fixed and boring on purpose. Boring is auditable.

| Operation | Cost (units) |
|---|---|
| `signal_detection` | 1 |
| `account_tiering` | 2 |
| `buyer_scoring` | 5 |
| `match_scoring` | 5 |
| `playbook_generation` | 5 |
| `reanalysis` | 5 |
| `firm_analysis` | 10 |
| `gtm_plan` | 10 |
| `monitoring_check` | 1 |

The ledger's `record` call checks the ceiling **before** it commits the cost. This ordering is the whole game — you never let the expensive operation run and then apologise afterwards.

```typescript
record(operation: string, entityId: string, cost?: number): LedgerResult {
  const unit = cost ?? COSTS[operation];
  if (this.runningTotal + unit > this.ceiling) {
    return {
      accepted: false,
      reason: `budget_exceeded: ${this.runningTotal}+${unit} > ${this.ceiling}`,
    };
  }
  this.runningTotal += unit;
  this.entries.push({
    seq: this.entries.length + 1,
    timestamp: new Date().toISOString(),
    operation, entityId, cost: unit,
    currency: this.currency,
    runningTotal: this.runningTotal,
  });
  return { accepted: true, runningTotal: this.runningTotal };
}
```

If `accepted` is `false`, the governed operation **throws** and emits a `budget_exceeded` audit event. It does not silently degrade, retry, or ask the model what to do. That is fail-closed behaviour applied to money — see [/topics/defendable-agents/architecture/fail-closed-behavior/](/topics/defendable-agents/architecture/fail-closed-behavior/) and the [budget-and-bounding primitive](/topics/defendable-agents/primitives/budget-and-bounding/) for the general shape.

## A worked run

Set a deliberately tight ceiling so we hit the wall quickly. Say the session ceiling for this run is **30 units**. The agent works a small set of buyers and firms:

| # | Operation | Entity | Cost | Running total |
|---|---|---|---|---|
| 1 | `signal_detection` | `sig-8842` | 1 | 1 |
| 2 | `buyer_scoring` | `buyer-101` | 5 | 6 |
| 3 | `account_tiering` | `buyer-101` | 2 | 8 |
| 4 | `firm_analysis` | `firm-204` | 10 | 18 |
| 5 | `match_scoring` | `buyer-101×firm-204` | 5 | 23 |
| 6 | `gtm_plan` | `buyer-101` | 10 | **blocked** |

Operations 1–5 are approved and recorded. Each one runs a pure deterministic score, creates a temporal pin, and emits an audit event carrying the full variable trace — the same pipeline described in [buyer-scoring-pipeline](/topics/defendable-agents/examples/buyer-scoring-pipeline/). Operation 6 asks for a go-to-market plan costing 10 units. Running total is 23; `23 + 10 = 33 > 30`. The ledger returns `accepted: false`, the operation throws, and this lands in the log:

```json
{
  "timestamp": "2026-07-08T09:14:52.331Z",
  "sessionId": "sess-7f3a",
  "sequence": 11,
  "type": "budget_exceeded",
  "actor": "gtm-planner",
  "entity": { "type": "buyer", "id": "buyer-101", "name": "Buyer 101" },
  "decision": {
    "action": "gtm_plan",
    "inputs": { "requestedCost": 10 },
    "outputs": { "accepted": false },
    "justification": "budget_exceeded: 23+10 > 30"
  },
  "budget": {
    "cost": 10, "currency": "units",
    "runningTotal": 23, "ceiling": 30, "remaining": 7
  },
  "durationMs": 0
}
```

The plan was never generated. No partial artefact, no half-charged spend. The session continues — cheaper operations under the remaining 7 units still succeed — but the plan is off the table until someone raises the ceiling or ends the session. Ending the session emits a summary event and flushes the log with `fsync`.

## The audit trail is the approval record

There is no separate "approvals database". The question *"was this spend authorised?"* is answered by reading the log:

```bash
jq 'select(.type=="budget_spend" or .type=="budget_exceeded")
    | {seq:.sequence, op:.decision.action, ok:.budget.remaining>=0,
       accepted:.decision.outputs.accepted, total:.budget.runningTotal}' \
  ./state/audit/session.jsonl
```

Every approved operation is a `budget_spend` line with its running total; every refusal is a `budget_exceeded` line with the arithmetic that justified it. Because the log is append-only JSONL with one event per line, you cannot rewrite history to make a blocked spend look approved, or vice versa. That property is what makes it evidence rather than telemetry — see [audit-trail](/topics/defendable-agents/primitives/audit-trail/) and [decision-traces](/topics/defendable-agents/primitives/decision-traces/). For the compliance framing, budget enforcement maps to an operation-cost ceiling under SOC 2 CC6.1 in the [control mapping](/topics/defendable-agents/compliance/control-mapping/).

## Honest limits

The ceiling governs **process, not wisdom**. The ledger guarantees the agent cannot spend beyond 30 units and that every attempt is recorded truthfully; it says nothing about whether 30 was the right number, or whether the operations you approved were worth approving. A cost table that under-prices `firm_analysis` will let the agent burn the budget on the wrong work — consistently, visibly, and reproducibly, which is at least how you notice.

Fail-closed budgeting can also be over-tuned. Set the ceiling too low and you block legitimate work; the operator then raises it, and that raise should itself be a logged, deliberate act, not a quiet edit. Budget governance is maintenance, not a one-time setup — the cost table and ceilings need review as the workload changes, a theme picked up in [operating-and-maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/).

For a full end-to-end build of this pattern, follow the [budget-ceiling tutorial](/topics/defendable-agents/tutorials/05-budget-ceiling/).
