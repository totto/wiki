---
title: "The Governance Primitives"
description: "The four mechanical primitives every governed operation routes through — fail-closed policy, audit-all, budget ceilings and temporal pinning — at a glance."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# The Governance Primitives

Guardrails fail because they are advice. A primitive is not advice — it is a piece of mechanism that an operation cannot get around, because the operation is routed *through* it by construction. In the defendable-agent stack there are four such primitives, and every governed operation in the example system, Lodestar, passes through all four before it returns a result. This page is the map: one paragraph on each, then how they compose inside a single governed session, then where to go for depth.

Lodestar scores buyers and firms in a regulated professional-services market. The scoring itself is a set of [pure deterministic functions](/topics/defendable-agents/architecture/deterministic-planner/) — same inputs, same outputs. The four primitives are what wrap that engine so a decision is not just computed but *defendable*: gated, recorded, bounded and pinned to a moment in time.

## Fail-closed policy

The default answer is no. Before any governed operation runs, the harness checks whether the domain it touches is declared, whether the tools it wants are permitted, and whether policy allows the call at all. If any check is missing or ambiguous, the operation does not proceed — it is denied and the denial is recorded. This is the inverse of the guardrail posture, where anything not explicitly forbidden is allowed. Here, anything not explicitly *permitted* is refused. It is the mechanical form of "access boundaries", and it is the one primitive most easily over-tuned: crank it too tight and you block legitimate work, so fail-closed is a dial you calibrate, not a switch you flip once. Depth: [Fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) and the architecture view, [Fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/).

## Audit-all

Every governed operation emits one append-only event. Not a log line summarising what happened — the full decision, including the inputs, the outputs, the justification and, for a score, the complete variable trace: all 18 or 21 variables, their 1-5 scores, the per-layer roll-ups, the composite total and the resulting band. Events are written as JSONL, one per line, fsync on flush, never mutated. If it wasn't recorded, it didn't happen — and if it was recorded, you can reconstruct exactly what the agent saw and decided. Depth: [Audit trail](/topics/defendable-agents/primitives/audit-trail/) and [Decision traces](/topics/defendable-agents/primitives/decision-traces/).

## Budget and bounding

An agent that can spend without limit is an agent you cannot bound. Every operation has a fixed unit cost, and the session carries a ledger with a ceiling. The ledger checks the cost *before* recording it: if the running total plus the new cost would exceed the ceiling, the spend is refused, the operation throws, and a `budget_exceeded` event is emitted. This bounds cost, blast radius and runaway loops in one mechanism. Depth: [Budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/).

## Temporal pinning

A score is only true as of the data it was computed from. Every score creates a *pin* recording when it was scored, the as-of date of its data, the dates of the signals it consumed, and the version and hash of the model used. Later, a drift check compares that pin against current state: newer data than the pin is DATA drift, a changed model version is MODEL drift, and a pin older than the maximum age (default 30 days) is TEMPORAL drift. Pinning tells you a decision has gone stale; it does *not* refresh the data for you — detection is not remediation. Depth: [Temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) and [Drift detection](/topics/defendable-agents/primitives/drift-detection/).

## How they compose in a governed session

A [governed session](/topics/defendable-agents/architecture/governance-harness/) shares one audit log, one budget ledger and one map of temporal pins. The four primitives are not independent add-ons — they are the fixed sequence every governed operation walks:

```typescript
async function governedBuyerScore(session, buyer) {
  // 1. FAIL-CLOSED: gate the operation; deny if not permitted
  session.policy.assertPermitted("buyer_scoring", buyer.domain);

  // 2. BUDGET: check ceiling BEFORE recording; throws + emits
  //    budget_exceeded if runningTotal + cost > ceiling
  session.ledger.record("buyer_scoring", buyer.id, 5);

  // 3. Run the pure, deterministic score (same in -> same out)
  const result = scoreBuyer(buyer);   // Need 0.40 / Attractiveness 0.25 / Winnability 0.35

  // 4. TEMPORAL PIN: capture the moment this score is true for
  session.pins.set(buyer.id, {
    scoredAt: now(),
    dataAsOf: buyer.dataAsOf,
    signalDates: buyer.signals.map(s => s.date),
    modelVersion: result.model.version,
    modelHash: result.model.hash,
  });

  // 5. AUDIT-ALL: one append-only event carrying the full variable trace
  session.audit.emit({
    type: "buyer_scored",
    entity: { type: "buyer", id: buyer.id, name: buyer.name },
    scoring: {
      model: result.model.id,
      variables: result.variables,   // all 18, each { id, score }
      layerScores: result.layers,
      total: result.total,
      band: result.band,             // e.g. ">=70 => High"
    },
  });

  return result;
}
```

The harness is configured declaratively, so the ceilings and switches above are not buried in code:

```yaml
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000            # session budget ceiling, in units
  context_budget: 200000     # tokens
  budget:
    amount: 1000
    currency: units
audit:
  path: ./state/audit.jsonl
```

Read the sequence back and the composition is the point. Fail-closed decides *whether* the operation runs. The budget ledger decides whether it can *afford* to. The deterministic engine computes the answer. The pin records *when* that answer is valid. The audit event records *that it happened and why*. Skip any one and the decision stops being defendable: no gate and you can't bound access, no budget and you can't bound cost, no pin and you can't tell staleness from truth, no audit and you can't reconstruct anything. Ending the session emits a summary event and flushes the log to disk.

## Honest limits

None of this makes the answer *correct*. The model at the edge is still a model, and a badly-designed variable produces a wrong score — the primitives just guarantee it produces the *same* wrong score every time, visibly, with a full trace, which is precisely how you catch and fix it. Determinism buys process, not truth. And the primitives are maintenance, not a one-time install: ceilings drift out of date, models get re-versioned, fail-closed rules need re-tuning as the domain grows. Budget for the upkeep.

## Where next

- Each primitive in depth via the pointer links above.
- The [architecture overview](/topics/defendable-agents/architecture/overview/) for how a session, harness and engine fit together.
- The [Lodestar case study](/topics/defendable-agents/reference/case-study-lodestar/) for the full worked system.
- [Control mapping](/topics/defendable-agents/compliance/control-mapping/) for how each primitive satisfies a named compliance control.
- The [glossary](/topics/defendable-agents/orientation/glossary/) if any term above was unfamiliar.
