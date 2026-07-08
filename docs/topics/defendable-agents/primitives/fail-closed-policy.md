---
title: "Fail-Closed Policy"
description: "The defendable-agent primitive that blocks whenever governance cannot verify a precondition, turning the absence of a block in the audit log into positive evidence that every gate held."
image: assets/images/kcp-agent-020-03-model-at-the-edge.webp
---

# Fail-Closed Policy

Most systems fail open. When a check cannot complete — a service is down, a signature is missing, a provenance record is unreadable — the default behaviour is to shrug and carry on. That is convenient, and it is exactly why guardrails erode: the one time you most need the gate is the one time the gate is unavailable, and an open failure lets the work through anyway.

A defendable agent inverts that default. **Fail-closed** means: if governance cannot positively verify that an operation is permitted, the operation does not run. Not "run and warn". Not "run and log a caveat". Block, emit an audit event, and stop. The burden of proof sits with the action, never with the refusal.

This is the primitive that makes the rest of the stack trustworthy. If you have read [what defendable means](/topics/defendable-agents/argument/what-defendable-means/) and [why guardrails fail](/topics/defendable-agents/argument/why-guardrails-fail/), fail-closed is the mechanism that turns those arguments into behaviour you can observe.

## Verify-or-block

The rule is one sentence: **every governed operation must clear an explicit precondition before it executes, and an unmet or uncheckable precondition is a block.**

The three cases collapse into one outcome:

| Precondition state | Outcome |
| --- | --- |
| Verified true | Proceed, record the decision |
| Verified false | Block, emit audit event |
| Cannot be verified | Block, emit audit event |

The third row is the whole point. A fail-open system treats "cannot verify" as a soft pass. A fail-closed system treats it identically to a hard denial, because from the log's perspective they are indistinguishable — in both cases governance did not get the confirmation it required.

## Worked examples

**Missing attestation.** A tenant asks the agent to score a buyer using a model that must be a declared, governed unit. The [trust-and-attestation](/topics/defendable-agents/primitives/trust-and-attestation/) layer resolves the model through the KCP manifest and checks its hash. If the manifest cannot be loaded, or the resolved model has no attestation, the operation never reaches the scoring engine. No score is produced, so no unverified number can leak into a downstream plan.

**Unverifiable provenance.** Every score carries a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/): `scoredAt`, `dataAsOf`, the signal dates it rests on, and the model version and hash. If the input data arrives without a `dataAsOf`, provenance is unverifiable — you cannot later prove what the agent knew and when. Fail-closed refuses to score rather than mint a pin it cannot stand behind.

**Budget ceiling reached.** The [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) checks the running total *before* recording a cost. If `runningTotal + cost` would exceed the session ceiling, `record()` returns `accepted: false`, the governed operation throws, and a `budget_exceeded` event is written. The expensive `firm_analysis` (10 units) simply does not run.

## Policy configuration

Fail-closed is not an ambient mood; it is a field in `harness.yaml`. The harness reads it once at session start and enforces it on every governed operation.

```yaml
policy:
  fail_closed: true          # uncheckable precondition => block
  audit_all: true            # every decision AND every block is recorded
  strict: true               # unknown tools/units are denied, not ignored
  max_units: 1000            # session budget ceiling
  context_budget: 200000     # token ceiling for the session
  budget:
    amount: 1000
    currency: units
audit:
  path: ./state/audit/session.jsonl
```

When a precondition fails, the block is not silent — it is a first-class audit record with the same schema as a successful decision:

```json
{
  "timestamp": "2026-07-08T09:14:22.517Z",
  "sessionId": "sess_4b2f",
  "sequence": 47,
  "type": "budget_exceeded",
  "actor": "scoring-agent",
  "entity": { "type": "firm", "id": "firm_0912", "name": "—" },
  "decision": {
    "action": "firm_analysis",
    "inputs": { "requestedCost": 10 },
    "outputs": { "accepted": false },
    "justification": "runningTotal 995 + cost 10 > ceiling 1000"
  },
  "budget": {
    "cost": 10, "currency": "units",
    "runningTotal": 995, "ceiling": 1000, "remaining": 5
  },
  "durationMs": 3
}
```

Set `fail_closed: false` and you have a different, weaker system — one where the absence of a block proves nothing. The [fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/) architecture page walks through how the harness threads this flag through each gate.

## The trust it creates in the log

Here is the subtle, valuable part. Because governance blocks on any unverifiable precondition, **the absence of a block becomes evidence.**

In a fail-open system, a clean log tells you nothing — operations could have proceeded despite failed or skipped checks, and the log would look identical. In a fail-closed system with `audit_all: true`, every operation that ran is an operation whose preconditions were positively verified, and every operation that could not verify left a `budget_exceeded`, an attestation failure, or a provenance refusal on its own line in the [append-only audit log](/topics/defendable-agents/primitives/audit-trail/).

So when an auditor reads a session that scored forty buyers with no block events, that is not merely "nothing went wrong". It is a proof: forty times, the model was attested, provenance was pinned, and the budget held. The clean log is the artifact. This is what lets a session feed straight into an [evidence package](/topics/defendable-agents/compliance/evidence-packages/) and satisfy the access-boundary controls in the [control mapping](/topics/defendable-agents/compliance/control-mapping/) (SOC 2 CC6.1).

## Honest limits

Fail-closed is a discipline, not a cure, and it cuts both ways.

- **It can be over-tuned.** A ceiling set too low, or a provenance rule stricter than your data can satisfy, will block legitimate work. Fail-closed that halts the business is a failure of a different kind. Tune ceilings against real session traces, not guesses, and treat a rising rate of blocks as a signal to investigate — sometimes the config is wrong, not the request.
- **It verifies preconditions, not correctness.** Fail-closed confirms that the model was attested and the data was pinned; it cannot confirm the model is *right*. A wrong variable still produces a wrong score — but consistently, visibly, and reproducibly (see [reproducibility](/topics/defendable-agents/decisions/reproducibility/)), which is how you catch it later.
- **It is maintenance, not setup.** Attestations expire, ceilings drift out of date, new tools appear. A fail-closed policy is only as trustworthy as its last review.

The model still sits at the edge, and it is still a model. Fail-closed does not make it honest — it makes every point where honesty is required into a gate you can see, and every gate that held into a line you can cite.
