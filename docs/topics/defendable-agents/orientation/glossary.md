---
title: "Glossary"
description: "Definitions of the core defendable-agent vocabulary: deterministic planner, governance harness, decision trace, temporal pin, drift, fail-closed, budget ceiling, and more."
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# Glossary

This field guide leans on a small, precise vocabulary. The words matter because the whole argument of [what defendable means](/topics/defendable-agents/argument/what-defendable-means/) rests on drawing lines the industry usually blurs — between a plan and a guess, between a log and an audit, between fresh data and stale data that merely looks fresh. Here is each term, one crisp paragraph, grounded in the reference system I call **Lodestar**: an agent that scores buyers and firms in a regulated professional-services market.

**Defendable agent.** An agent whose every consequential action can be reconstructed, explained, and defended after the fact — to a regulator, an auditor, or a customer who disagrees with the outcome. Defendability is a property of the *system around* the model, not of the model itself. It is earned by making the decision boundary deterministic and the record complete, so that "why did it do that?" always has a concrete, replayable answer rather than a shrug.

**Deterministic planner.** The part of the stack that decides *what* to do — which units to load, which operations to run, in what order — using pure functions: same inputs, same outputs, no hidden state, no sampling. In Lodestar the scoring engine is deterministic: a layer score is the mean of its 1-5 variable scores times 20, and a BUYER score is a fixed weighted composite (Need 0.40, Attractiveness 0.25, Winnability 0.35). See the [deterministic planner](/topics/defendable-agents/architecture/deterministic-planner/) chapter for how this couples to the [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/).

**Governance harness.** The runtime wrapper (`harness.yaml`) that every governed operation passes through. It declares the domains, the tools an agent may call, and the policy that binds them — fail-closed, audit-all, unit and budget ceilings, context budget. It is where policy stops being a document and becomes an enforced boundary. The [governance harness](/topics/defendable-agents/architecture/governance-harness/) chapter is the deep dive.

```yaml
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000
  budget: { amount: 1000, currency: units }
  context_budget: 200000
audit: { path: ./state/audit.jsonl }
```

**KCP manifest / unit.** A [Knowledge Context Protocol](/topics/knowledge-context-protocol/) manifest (`knowledge.yaml`) is a versioned declaration of *governed units* — the knowledge, models, and rules an agent is permitted to load. Each unit has an `id`, a `path`, `tags`, and optional `depends_on`. Lodestar's scoring models are themselves declared as units, so they are selected deterministically and never silently swapped. See [declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/).

**Decision trace.** The full input-and-output record of a single scored decision: every one of the 18 buyer variables with its 1-5 score, the three layer scores, the composite total, and the resulting priority band. A trace is what turns a number into an argument you can inspect line by line. This is the heart of [anatomy of a score](/topics/defendable-agents/decisions/anatomy-of-a-score/) and the [decision traces](/topics/defendable-agents/primitives/decision-traces/) primitive.

**Append-only audit log.** A JSONL file, one event per line, `fsync`-flushed, never rewritten. Each event carries a timestamp, session id, monotonic sequence number, type, the acting agent, the entity, the decision (action, inputs, outputs, justification), and — where relevant — the scoring trace, temporal pin, and budget state. Append-only is the point: you can add to history but never quietly revise it. See the [audit trail](/topics/defendable-agents/primitives/audit-trail/) primitive.

**Temporal pin.** A snapshot taken at scoring time: `{ scoredAt, dataAsOf, signalDates[], modelVersion, modelHash }`. It records exactly *when* the data was current and *which* model produced the score, so the decision can be judged against the world as it actually was, not as it is now. Covered in [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/).

**Drift.** The gap between a pin and the present. A drift check reports DATA drift when current `dataAsOf` is newer than the pin's, MODEL drift when the model version changed, and TEMPORAL drift when the score is older than the maximum age (default 30 days). Two or more reasons, or model drift alone, recommend a reanalysis; a single non-model reason recommends monitoring. This is [drift detection](/topics/defendable-agents/primitives/drift-detection/). Honest limit: drift detection tells you a score is *stale*; it does not refresh the data for you.

**Fail-closed policy.** When a required check cannot be satisfied — a manifest is missing, a unit will not validate, a budget is exhausted — the operation *stops* rather than proceeding on a guess. The default is deny. This is the inverse of the guardrail mindset critiqued in [why guardrails fail](/topics/defendable-agents/argument/why-guardrails-fail/). Honest limit: fail-closed can be over-tuned into blocking legitimate work, so tuning the boundary is ongoing operational work, covered in [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/).

**Budget ceiling.** A hard cap on how much work a session may do, denominated in units against an operation cost table (buyer scoring 5, firm analysis 10, GTM plan 10, and so on). The ledger checks `runningTotal + cost` against the ceiling *before* recording; if it would exceed, the operation throws and emits a `budget_exceeded` event. See [budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/).

**Tenant isolation.** Shared, public signal and company data is visible to every tenant, but each tenant's *confidential* scores and plans live in a separate per-tenant state directory. Isolation is a directory boundary the harness enforces, not a promise in a policy note. See [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/).

**Attestation / signing.** The mechanism by which a party vouches for an artifact — a model version, an evidence package, a session log — so a downstream consumer can verify it was produced by whom it claims and has not been altered. It is what lets an [evidence package](/topics/defendable-agents/compliance/evidence-packages/) travel outside your walls and still be trusted. See [trust and attestation](/topics/defendable-agents/primitives/trust-and-attestation/).

**Skip-reason.** When the planner declines to run an operation — because a pin is fresh enough, a budget would be exceeded, or a unit is out of scope — it records *why* it skipped, not merely *that* it skipped. Skip-reasons make inaction as auditable as action, which matters when an auditor asks why a decision was *not* revisited.

**Model at the edge.** The language model is confined to the perimeter — extracting signals, drafting narrative, proposing variable values — while the deterministic core makes the binding decisions. Pushing the model to the edge shrinks the surface where non-determinism can cause harm. Honest limit: the model at the edge is still a model; determinism guarantees *process*, not *correctness*. A wrong variable is applied consistently — but visibly and reproducibly, which is precisely how you catch it. See [reproducibility](/topics/defendable-agents/decisions/reproducibility/) and, if you are just starting, [how to read this guide](/topics/defendable-agents/orientation/how-to-read/).
