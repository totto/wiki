---
title: "Budget & Bounding"
description: "Operation cost ceilings that make an agent run provably bounded — the fixed cost table, an append-only ledger, check-before-record enforcement, and fail-closed budget events."
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Budget & Bounding

Ask a probabilistic agent "how much work will you do?" and the honest answer is "I don't know until I've done it." That is fine for a chat window. It is unacceptable for a governed system that spends money, touches confidential data, and has to answer to an auditor. A [defendable agent](/topics/defendable-agents/argument/what-defendable-means/) needs a property that no amount of prompt engineering gives you: a run that is **provably bounded**. You should be able to say, before the model does anything, "this session could only ever have done this much" — and prove it afterwards from the record.

Bounding is the primitive that delivers that. It is deliberately dumb: a fixed price list, a running total, and a ceiling that is checked before every operation. No cleverness, no estimation. Dumb is the point — it is what makes the guarantee hold.

## The cost table

Every governed operation has a fixed price in abstract **units**. Units are not tokens and not currency; they are a domain-defined measure of "how much of a session's allowance this operation consumes". Pricing operations rather than tokens means the ceiling is legible to the people who set it — a buyer scoring is worth five of a signal detection, and everyone can see why.

| Operation | Cost (units) |
|---|---|
| `signal_detection` | 1 |
| `monitoring_check` | 1 |
| `account_tiering` | 2 |
| `buyer_scoring` | 5 |
| `match_scoring` | 5 |
| `playbook_generation` | 5 |
| `reanalysis` | 5 |
| `firm_analysis` | 10 |
| `gtm_plan` | 10 |

In the Lodestar reference system these costs live in `harness.yaml` under `costs`, alongside the session ceiling. A typical session sets `budget.amount: 1000`, which means at most 200 buyer scorings, or 100 firm analyses, or any mix that sums to a thousand — and not one unit more.

```yaml
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000
  budget:
    amount: 1000
    currency: units
  context_budget: 200000   # token ceiling for context assembly
costs:
  signal_detection: 1
  buyer_scoring: 5
  firm_analysis: 10
  match_scoring: 5
  account_tiering: 2
  gtm_plan: 10
  playbook_generation: 5
  monitoring_check: 1
  reanalysis: 5
```

## The ledger

Spend is tracked in an append-only **budget ledger**. Every accepted operation adds one entry, and entries never mutate. The running total is the sum of everything so far, carried forward so the current position is always one field away.

```json
{ "seq": 1, "timestamp": "2026-07-08T09:14:02.031Z", "operation": "signal_detection", "entityId": "sig-4471", "cost": 1, "currency": "units", "runningTotal": 1 }
{ "seq": 2, "timestamp": "2026-07-08T09:14:02.884Z", "operation": "buyer_scoring", "entityId": "buyer-0192", "cost": 5, "currency": "units", "runningTotal": 6 }
{ "seq": 3, "timestamp": "2026-07-08T09:14:03.510Z", "operation": "firm_analysis", "entityId": "firm-0333", "cost": 10, "currency": "units", "runningTotal": 16 }
```

The ledger is a sibling of the [append-only audit log](/topics/defendable-agents/primitives/audit-trail/), and it should be read as evidence the same way. Given the final `runningTotal` and the ceiling, the bound is arithmetic, not trust.

## Check before you record

Here is the detail that makes bounding a guarantee rather than a report. The ledger checks the ceiling **before** it records, not after. If recording an operation would push the running total past the ceiling, the operation is rejected — it is never charged, never run, never emitted as a real decision.

```typescript
interface LedgerResult {
  accepted: boolean;
  entry?: LedgerEntry;
  reason?: string;
}

record(operation: string, entityId: string, cost = COSTS[operation]): LedgerResult {
  const projected = this.runningTotal + cost;
  if (projected > this.ceiling) {
    return {
      accepted: false,
      reason: `budget_exceeded: ${operation} costs ${cost}, ` +
              `running total ${this.runningTotal} + ${cost} = ${projected} ` +
              `exceeds ceiling ${this.ceiling}`,
    };
  }
  const entry: LedgerEntry = {
    seq: ++this.seq,
    timestamp: new Date().toISOString(),
    operation,
    entityId,
    cost,
    currency: this.currency,
    runningTotal: (this.runningTotal = projected),
  };
  this.entries.push(entry);
  return { accepted: true, entry };
}
```

The ordering matters. Check-after-record leaks: you would have already spent the unit — and possibly already touched the data — before discovering you were over. Check-before-record means the ceiling is a wall, not a warning line.

## Fail-closed on the ceiling

When `record()` returns `accepted: false`, the [governed session](/topics/defendable-agents/architecture/governance-harness/) does not shrug and continue. The operation **throws**, and before it throws it emits a `budget_exceeded` audit event. This is [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) applied to spend: the default outcome when the budget is gone is *stop*, loudly, in the record.

```json
{
  "timestamp": "2026-07-08T09:41:55.204Z",
  "sessionId": "sess-7c1e",
  "sequence": 402,
  "type": "budget_exceeded",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer-2201", "name": "Buyer 2201" },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 998, "ceiling": 1000, "remaining": 2 },
  "decision": {
    "action": "buyer_scoring",
    "justification": "rejected: 998 + 5 = 1003 exceeds ceiling 1000"
  }
}
```

An operator reading the log sees exactly where the session hit its wall and what it was trying to do. There is no half-scored buyer, no partial plan — the throw unwinds before the deterministic score runs. That is the difference between a bounded system and one that merely tracks its own overspend.

## It could only ever have done this much

The payoff is a single defensible sentence. Because operations are priced from a fixed table, tracked in an append-only ledger, and gated by a check-before-record ceiling, the maximum work any session performed is `ceiling ÷ cheapest_operation` operations — hard-capped, with the actual figure sitting in `runningTotal`. Combined with [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) and full decision traces, you can reconstruct not just *what* an agent decided but *how much* it was ever able to do. That maps directly onto the budget-enforcement control (SOC 2 CC6.1) in the [control mapping](/topics/defendable-agents/compliance/control-mapping/).

## Honest limits

Bounding caps volume, not judgement. The ceiling proves a session ran at most a thousand units of work; it says nothing about whether any individual score was *right* — a wrong variable is applied within budget just as consistently as a right one. And the ceiling has a failure mode of its own: set it too low and fail-closed becomes obstruction, blocking legitimate work mid-run and training operators to raise limits without thinking. The unit prices are a governance decision, not a fact of nature — they need review as the workload changes. Bounding is one honest, mechanical guarantee among several. Walk through it hands-on in the [budget-ceiling tutorial](/topics/defendable-agents/tutorials/05-budget-ceiling/), or step back to the [primitives overview](/topics/defendable-agents/primitives/overview/) to see where it sits alongside the other guarantees.
