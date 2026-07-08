---
title: "Tutorial 5: Enforcing a Budget Ceiling"
description: "Add operation costs and a session ceiling so a governed run is provably bounded, then watch a budget_exceeded block get recorded and thrown before any spend happens."
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Tutorial 5: Enforcing a Budget Ceiling

An agent left to its own devices will do as much work as its prompt implies — and sometimes far more, because a model that is uncertain will happily re-score, re-plan, and re-check "to be safe". That is fine when the work is free. It is not fine when each operation costs money, burns a rate limit, or touches a downstream system. In this tutorial we give the Lodestar session a hard spending ceiling and make it *provable* that a run never exceeded it.

This builds directly on the [governed session](/topics/defendable-agents/tutorials/03-governed-session/) and its [audit log](/topics/defendable-agents/tutorials/04-audit-log/). If you have not wired those, start there. The primitive behind this page is [budget ceilings](/topics/defendable-agents/primitives/budget-and-bounding/).

## The cost table

Every operation the agent can perform has a fixed cost in abstract units. Units are deliberately not currency — they are a proxy you can map to tokens, API calls, or money later. The table is a plain constant, checked into version control alongside the governance harness:

```typescript
export const OPERATION_COSTS = {
  signal_detection:     1,
  buyer_scoring:        5,
  firm_analysis:       10,
  match_scoring:        5,
  account_tiering:      2,
  gtm_plan:            10,
  playbook_generation:  5,
  monitoring_check:     1,
  reanalysis:           5,
} as const;

export type Operation = keyof typeof OPERATION_COSTS;
```

The ceiling lives in `harness.yaml`, not in code, so an operator can tighten it without a redeploy:

```yaml
policy:
  fail_closed: true
  audit_all: true
  budget:
    amount: 40          # 1000 in production; kept low here so the demo can hit it
    currency: units
  context_budget: 200000
```

Here `budget.amount` is the session ceiling. In production this is 1000 units; I keep it at 40 for the demo so we can actually reach it.

## record() — check before you spend

The ledger's one rule: **it checks the ceiling _before_ recording, never after.** A post-hoc check would let the expensive operation run and only then complain, which defeats the purpose. `record()` is a pure gate.

```typescript
interface LedgerEntry {
  seq: number;
  timestamp: string;
  operation: Operation;
  entityId: string;
  cost: number;
  currency: string;
  runningTotal: number;
}

class BudgetLedger {
  private entries: LedgerEntry[] = [];
  private runningTotal = 0;

  constructor(readonly ceiling: number, private currency = "units") {}

  record(operation: Operation, entityId: string, cost = OPERATION_COSTS[operation]) {
    if (this.runningTotal + cost > this.ceiling) {
      return {
        accepted: false,
        reason: `ceiling ${this.ceiling} would be exceeded: ` +
                `${this.runningTotal} + ${cost} = ${this.runningTotal + cost}`,
        runningTotal: this.runningTotal,
      };
    }
    this.runningTotal += cost;
    this.entries.push({
      seq: this.entries.length,
      timestamp: new Date().toISOString(),
      operation, entityId, cost,
      currency: this.currency,
      runningTotal: this.runningTotal,
    });
    return { accepted: true, runningTotal: this.runningTotal };
  }
}
```

Note what `record()` does *not* do: it does not throw, log, or know anything about the agent. It returns a verdict. The governed operation decides what to do with a rejection — and because [fail-closed](/topics/defendable-agents/primitives/fail-closed-policy/) is the house rule, a rejection stops the work.

## Hitting the ceiling

Wire the ledger into the session so every governed operation records first. With a ceiling of 40 units and the demo cost table, a run of buyer scores (5 units each) plus a couple of firm analyses (10 each) climbs quickly:

```typescript
function governedBuyerScore(session, buyerId: string, inputs) {
  const verdict = session.ledger.record("buyer_scoring", buyerId);
  if (!verdict.accepted) {
    session.audit.emit({
      type: "budget_exceeded",
      actor: "scoring-agent",
      entity: { type: "buyer", id: buyerId },
      decision: { action: "buyer_scoring", justification: verdict.reason },
      budget: {
        cost: OPERATION_COSTS.buyer_scoring,
        currency: "units",
        runningTotal: verdict.runningTotal,
        ceiling: session.ledger.ceiling,
        remaining: session.ledger.ceiling - verdict.runningTotal,
      },
    });
    throw new BudgetExceededError(verdict.reason);
  }
  const score = scoreBuyer(inputs);   // pure, deterministic
  session.pin(buyerId, score);
  session.audit.emit({ type: "buyer_scored", /* full variable trace */ });
  return score;
}
```

The order is the whole point: **record and gate, then score, then pin, then audit.** The deterministic score — the weighted composite of the Need (0.40), Attractiveness (0.25) and Winnability (0.35) layers — never runs if the budget verdict is negative.

## The budget_exceeded event

When the ceiling is reached, two things happen: an audit event is written, and the operation throws. Here are the relevant JSONL lines from a run that hit the wall on its eighth operation:

```json
{"timestamp":"2026-07-08T09:14:02.113Z","sessionId":"s-4f1c","sequence":11,"type":"budget_spend","actor":"scoring-agent","entity":{"type":"buyer","id":"buyer-7731","name":"redacted"},"budget":{"cost":5,"currency":"units","runningTotal":38,"ceiling":40,"remaining":2}}
{"timestamp":"2026-07-08T09:14:02.240Z","sessionId":"s-4f1c","sequence":12,"type":"budget_exceeded","actor":"scoring-agent","entity":{"type":"firm","id":"firm-0042"},"decision":{"action":"firm_analysis","justification":"ceiling 40 would be exceeded: 38 + 10 = 48"},"budget":{"cost":10,"currency":"units","runningTotal":38,"ceiling":40,"remaining":2}}
{"timestamp":"2026-07-08T09:14:02.244Z","sessionId":"s-4f1c","sequence":13,"type":"session_end","actor":"harness","budget":{"runningTotal":38,"ceiling":40,"remaining":2}}
```

Read sequence 12 carefully. The `runningTotal` is still 38, not 48 — the rejected operation was *never charged*, because the check happens before the spend. The session then ends fail-closed. Nothing partial was committed, and the audit trail records exactly why.

## Proving the run was bounded

This is where the ceremony pays off. To prove a run stayed within budget, you do not trust the agent's word — you replay the append-only log and assert two invariants:

```bash
# every recorded runningTotal must be <= the ceiling
jq -e 'select(.budget.runningTotal != null)
       | .budget.runningTotal <= .budget.ceiling' audit.jsonl \
  && echo "BOUNDED: no entry exceeded the ceiling"

# and every attempt over budget must have been blocked, not charged
jq 'select(.type=="budget_exceeded")
    | {seq:.sequence, tried:.decision.action, held_at:.budget.runningTotal}' audit.jsonl
```

Because the ledger is monotonic and the audit log is append-only with `fsync` on flush, these two checks are sufficient evidence for a control reviewer. That evidence is what flows into an [evidence package](/topics/defendable-agents/compliance/evidence-packages/); budget enforcement maps to SOC 2 CC6.1 in the [control mapping](/topics/defendable-agents/compliance/control-mapping/).

## Honest limits

A ceiling bounds *effort*, not *correctness*. A run that stops at 38 units is not thereby a good run — it is merely a run that did no more than 40 units of work. If the cost table is wrong, or an operation is under-priced, you will bound the wrong thing, consistently and provably. Review the table when you add operations.

The other trap is over-tuning. A ceiling set too low turns fail-closed into a nuisance: legitimate multi-entity runs die halfway, and operators learn to raise the limit reflexively until it means nothing. Pick a ceiling from real percentiles of past sessions, not from fear, and treat it as [maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/), not a one-time setting.

Next, tutorial 6 adds [temporal drift detection](/topics/defendable-agents/tutorials/06-temporal-drift/) so a bounded run also knows when its inputs have gone stale.
