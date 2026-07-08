---
title: "The Governance Harness"
description: "Anatomy of the harness: the scaffold that turns a deterministic planner into a governed system through declared domains, fail-closed policy, a budget ceiling and an append-only audit trail."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# The Governance Harness

A deterministic planner decides *what* to do. The harness decides whether it is *allowed* to, records that it happened, and stops it before it costs too much. Everything else in this stack — the [scoring engine](/topics/defendable-agents/decisions/anatomy-of-a-score/), the [audit log](/topics/defendable-agents/primitives/audit-trail/), the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) — is machinery. The harness is the thing that wires them together and refuses to run without them. In the reference implementation this is `kcp-harness`, configured by a single file: `harness.yaml`.

I have watched too many "AI governance" efforts amount to a policy document nobody can execute. The point of the harness is that the policy *is* code, loaded at startup, enforced on every operation. There is no path around it, because the governed session will not construct itself without a valid harness.

## harness.yaml

Here is a working configuration for the Lodestar example, a buyer-scoring system operating in a regulated professional-services market.

```yaml
governance:
  domains:
    - manifest: knowledge/buyer-scoring/knowledge.yaml
      paths: [knowledge/buyer-scoring]
      tools: [kcp_plan, kcp_load]
    - manifest: knowledge/match-scoring/knowledge.yaml
      paths: [knowledge/match-scoring]
      tools: [kcp_plan, kcp_load]

policy:
  fail_closed: true
  audit_all: true
  max_units: 1000
  strict: true
  budget:
    amount: 1000
    currency: units
  context_budget: 200000

audit:
  path: state/audit/session.jsonl

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

Four blocks, four jobs. Read them in order and you have read the whole security model.

## Domains: what the agent is allowed to touch

`governance.domains` is an allow-list, not a suggestion. Each entry names a [KCP manifest](/topics/defendable-agents/kcp/manifest-basics/), the filesystem `paths` it governs, and the `tools` the agent may invoke inside it — here `kcp_plan` and `kcp_load`. The scoring models are [declared as governed KCP units](/topics/defendable-agents/kcp/declaring-governed-units/), which is what lets them be selected deterministically and never silently swapped for a different version mid-session.

Anything outside a declared domain is simply not reachable. The agent does not get told "no" at call time so much as it is never handed the capability in the first place. That distinction matters: a denial you have to remember to write is a denial you will eventually forget. A capability that was never granted cannot be forgotten.

## Policy: the four switches that define "defendable"

The `policy` block is small on purpose. Each field maps to a control you can point an auditor at.

| Field | Effect | Maps to |
|---|---|---|
| `fail_closed` | Any missing dependency, unreadable manifest, or failed check aborts the operation rather than proceeding on a guess | [Fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) |
| `audit_all` | Every governed operation emits an audit event; nothing runs off the record | [Audit trail](/topics/defendable-agents/primitives/audit-trail/) |
| `max_units` | Hard ceiling on the session budget ledger (1000 units here) | [Budget & bounding](/topics/defendable-agents/primitives/budget-and-bounding/) |
| `strict` | Manifest and model-version mismatches are errors, not warnings | [Reproducibility](/topics/defendable-agents/decisions/reproducibility/) |

`fail_closed: true` is the one people push back on, because [it can be over-tuned into blocking legitimate work](/topics/defendable-agents/architecture/fail-closed-behavior/) — a stale manifest and the whole session refuses to start. That is a real cost, and I will not pretend otherwise. But the alternative is an agent that scores a buyer on partial data and emits a confident number with a hole in it. In a regulated market I would rather explain a blocked session than defend a wrong one.

## Budget and context: two independent ceilings

There are two limits, and they bound different things.

The **budget ledger** counts operations against `max_units`. The `costs` table prices each operation — `buyer_scoring` costs 5 units, `firm_analysis` 10, `gtm_plan` 10, and so on. Before an operation runs, the ledger calls `record(op, entity)`, which checks `runningTotal + cost` against the ceiling *first*. If it would exceed, it returns `accepted: false`, the operation throws, and a `budget_exceeded` event lands in the audit log. The spend is refused before it happens, not reconciled after.

The **context budget** (`context_budget: 200000` tokens) bounds what the [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) may consume in a single pass. These are separate ceilings because they fail for separate reasons: you can be cheap on operations and still blow the context window, or vice versa. Collapsing them into one number hides which limit you actually hit.

## How the harness wraps every operation

The harness does not sit beside the work; it encloses it. When you open a [governed session](/topics/defendable-agents/tutorials/03-governed-session/), that session holds exactly one audit log, one budget ledger, and one map of [temporal pins](/topics/defendable-agents/primitives/temporal-pinning/), all constructed from the harness config. Every governed operation then runs the same four steps, in order:

1. **Record budget.** Check the ceiling; throw and emit `budget_exceeded` if the operation would exceed it.
2. **Run the pure score.** The deterministic engine computes the result — same inputs, same outputs, every time.
3. **Pin the data.** Create a temporal pin capturing `scoredAt`, `dataAsOf`, the signal dates, and the model version and hash.
4. **Emit the audit event.** Write one JSONL line carrying the full variable trace — every input, every layer score, the total and the band.

Ending the session emits a summary event and flushes the log with an `fsync`. The result is that no score exists without a receipt, and no receipt exists without a budget line and a data pin behind it. That chain — from domain to receipt — is the whole point of the diagram on this page.

## Honest limits

The harness governs process, not judgement. It guarantees that every operation was priced, recorded, pinned, and confined to a declared domain. It does **not** guarantee the score is *right*: a badly designed variable produces a bad number, applied consistently. The value is that the badness is now visible and reproducible, which is how you catch it — see [determinism vs probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/). Temporal pinning flags stale data; it does not refresh it. And `fail_closed` will occasionally stop work you wanted done. The harness is scaffolding you maintain, not a wall you build once. Wired correctly, though, it means "prove what the agent did" stops being an archaeology project and becomes a `cat` of the audit file.
