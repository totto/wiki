---
title: "Fail-Closed Behavior"
description: "What a defendable agent does when it cannot verify something: it stops and records the block as evidence, rather than proceeding on an unverified guess."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Fail-Closed Behavior

A [defendable agent](/topics/defendable-agents/argument/what-defendable-means/) has one reflex that separates it from a helpful chatbot: when it cannot verify that an action is permitted, it stops. It does not proceed on a plausible guess. It does not degrade gracefully into "best effort". It blocks, writes down why it blocked, and returns control. That reflex is what "fail-closed" means, and in [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/) it is a directory boundary and a budget check and a manifest lookup — not a sentence in a policy document.

## Fail-closed versus fail-open

The two postures answer the same question — *what happens when a precondition cannot be confirmed?* — in opposite directions.

| Posture | On unverifiable state | Failure mode you inherit |
|---|---|---|
| Fail-open | Proceed anyway, log a warning | Silent wrong action, discovered later (or never) |
| Fail-closed | Refuse the action, record the refusal | Blocked legitimate work, discovered immediately |

Most systems fail open by accident. Nobody decides "let the agent run an unbudgeted operation against a tenant it cannot confirm" — it just happens because the happy path was the only path anyone wired. Fail-closed is the opposite: the deny branch is written *first*, and the permit branch is the exception you have to earn. In the harness this is a single flag, `policy.fail_closed: true`, but the flag only matters because every governed operation is built to honour it.

```yaml
# harness.yaml
policy:
  fail_closed: true          # unverifiable => deny, on the record
  audit_all: true            # including the denials
  strict: true
  max_units: 1000            # session budget ceiling
  context_budget: 200000
audit:
  path: ./state/audit/session.jsonl
```

## What counts as a verification failure

A block is not an error and not a crash. It is a *refusal to act on unverified state*. In Lodestar the recurring triggers are concrete:

- **Budget exhausted.** The [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) checks the ceiling *before* recording a cost. If `runningTotal + cost > ceiling`, `record()` returns `accepted: false` and the governed operation throws rather than running the score.
- **Undeclared unit.** The agent asks to load a scoring model that is not a governed unit in the [KCP manifest](/topics/defendable-agents/kcp/declaring-governed-units/). Fail-closed refuses rather than resolving an arbitrary file — no silent model swap.
- **Tenant boundary.** A read or write resolves outside the calling tenant's isolated [state directory](/topics/defendable-agents/primitives/multi-tenancy/). The boundary is a filesystem boundary; crossing it is a block, not a warning.
- **Unpinnable temporal state.** A score cannot form a valid [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) — no `dataAsOf`, no signal dates — so its provenance would be unverifiable. It does not get written as if it were sound.

Each of these is a precondition the agent could not confirm. The model at the edge may still have produced a confident, fluent justification for proceeding. The harness does not care what the model wanted; the [governance harness](/topics/defendable-agents/architecture/governance-harness/) gates the *tool call*, not the model's opinion of it. That is precisely [why guardrails inside the prompt fail](/topics/defendable-agents/argument/why-guardrails-fail/) and a deterministic gate does not.

## What gets recorded on a block

The block is only useful if it leaves a trace. A denied operation emits an audit event to the same append-only [JSONL log](/topics/defendable-agents/primitives/audit-trail/) as a successful one — same shape, same sequence counter, same fsync. A budget block looks like this:

```json
{
  "timestamp": "2026-07-08T09:14:22.771Z",
  "sessionId": "sess_3f9c",
  "sequence": 47,
  "type": "budget_exceeded",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_5521", "name": "redacted" },
  "decision": {
    "action": "buyer_scoring",
    "inputs": { "cost": 5, "currency": "units" },
    "outputs": { "accepted": false },
    "justification": "runningTotal 998 + cost 5 exceeds ceiling 1000"
  },
  "budget": {
    "cost": 5, "currency": "units",
    "runningTotal": 998, "ceiling": 1000, "remaining": 2
  },
  "durationMs": 1
}
```

Notice what is *absent*: there is no `scoring` block, because no score was computed. The entity was not scored, and the record says so unambiguously. Anyone reproducing the session can see the exact ceiling, the exact running total, and the arithmetic that produced the refusal. This is a first-class [decision trace](/topics/defendable-agents/primitives/decision-traces/), just one whose decision was "no".

## A block is itself evidence

This is the point most people miss when they think of blocking as merely defensive. In a fail-open system, the *absence* of an action tells you nothing — maybe it never came up, maybe it was suppressed, maybe it silently failed. In a fail-closed system, a refusal is an affirmative record: *the agent reached this precondition, could not satisfy it, and stopped here.* That record is what you hand an assessor.

The [compliance control mapping](/topics/defendable-agents/compliance/control-mapping/) leans on this directly. "The system enforces a spend ceiling" is a claim. A `budget_exceeded` event with the arithmetic in it is proof the enforcement *fired* — the difference between asserting a control and evidencing it. The same holds for a refused cross-tenant read: the block is the record that the isolation boundary is real and not aspirational — the logical-access control (SOC 2 CC6.1) evidenced, not merely claimed. Blocks belong in your [evidence package](/topics/defendable-agents/compliance/evidence-packages/) alongside the successes.

## Tuning risk: over-blocking is a real failure

Honest limits. Fail-closed is not free, and it is not automatically correct. Tuned too tight, it blocks legitimate work — a ceiling set below a normal session's real cost turns every run into a wall of `budget_exceeded` events, and operators learn to raise the ceiling reflexively until it enforces nothing. An over-eager tenant check can refuse a genuinely shared public signal. The deny branch has the same capacity to be *wrong* as the permit branch; it is just wrong loudly and on the record instead of quietly.

The mitigation is not to loosen the reflex but to calibrate the thresholds against observed sessions and to read the block events as signal. A rising rate of `budget_exceeded` may mean an attack, or it may mean your ceiling no longer matches how the work actually costs out — and because the [determinism](/topics/defendable-agents/architecture/deterministic-planner/) guarantees process, not correctness, a mis-set ceiling is applied consistently and *visibly*, which is exactly how you catch it. Governance here is maintenance, not one-time setup: you revisit ceilings, boundaries, and drift thresholds as the work changes.

A block that never fires is a guardrail nobody has tested. A block that fires constantly is a threshold nobody has tuned. The defendable position is the one in between — and it is a position you hold by watching the log, not by trusting the flag.
