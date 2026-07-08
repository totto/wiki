---
title: "Tutorial 1: Your First harness.yaml"
description: "Build a minimal governance harness from scratch — declare a governed domain, turn on fail-closed policy, set a budget ceiling with a cost table, wire an audit path, and verify it loads."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# Tutorial 1: Your First harness.yaml

The harness is the file that turns a pile of clever code into a [defendable agent](/topics/defendable-agents/argument/what-defendable-means/). It is the boundary. Everything the agent is allowed to touch, spend, or record passes through it. In this tutorial we write one from scratch, key by key, and then confirm it loads.

I will use the running example from this guide — **Lodestar**, an agent that scores buyers and firms in a regulated professional-services market. You do not need Lodestar's code to follow along; the harness shape is the same whatever your domain. If you have not yet set up a project directory, do [Tutorial 0: Project Layout](/topics/defendable-agents/tutorials/00-project-layout/) first. For the wider picture of what this file is doing in the architecture, see the [governance harness](/topics/defendable-agents/architecture/governance-harness/) page.

## What the harness is for

A harness is not configuration in the decorative sense. It is an enforced contract. When the session starts, the runtime reads `harness.yaml` and refuses to run anything the file does not permit. That is the whole point of [fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/): the default is *no*, and every *yes* is written down.

There are four things a minimal harness must nail down:

1. **Domains** — which governed units the agent may plan and load.
2. **Policy** — the rules that gate every operation (fail-closed, audit-all, ceilings).
3. **Budget and costs** — a hard ceiling and a price list so spend cannot run away.
4. **Audit** — where the append-only record is written.

Let us build each one.

## Step 1 — Declare a governed domain

A domain points at a [KCP manifest](/topics/defendable-agents/kcp/manifest-basics/) and lists the tools the agent may use against it. Here we grant only `kcp_plan` and `kcp_load` — the agent may work out what to load and load it, nothing more.

```yaml
governance:
  domains:
    - manifest: ./knowledge/knowledge.yaml
      paths:
        - ./knowledge/models
      tools:
        - kcp_plan
        - kcp_load
```

The `manifest` is the single source of truth for which scoring models exist. Because the models are declared as [governed units](/topics/defendable-agents/kcp/declaring-governed-units/), the runtime selects them deterministically and can never silently swap one version for another. `paths` scopes what those units may read from disk.

## Step 2 — Set the policy

```yaml
policy:
  fail_closed: true
  audit_all: true
  strict: true
  max_units: 12
  budget:
    amount: 1000
    currency: units
  context_budget: 200000
```

Take these one at a time.

- **`fail_closed: true`** — if a check cannot be evaluated, the operation is refused. Non-negotiable for a defendable agent. An honest caveat before you copy it: fail-closed can be over-tuned into blocking legitimate work. If your agent starts refusing valid operations, the fix is a narrower, well-tested condition — not turning this off.
- **`audit_all: true`** — every governed operation emits an event. No exceptions, no "quiet" paths.
- **`strict: true`** — unknown fields and undeclared tools are errors, not warnings.
- **`max_units: 12`** — a cap on how many governed units one plan may pull, so a runaway plan cannot load the world.
- **`budget`** — the session ceiling. Here 1000 *units* (an abstract cost, not currency; more below).
- **`context_budget: 200000`** — a token ceiling for the working context, so a session cannot balloon past what the model can defensibly reason over.

## Step 3 — Price the operations

The budget ceiling is only meaningful with a cost table. Each governed operation has a fixed price; the ledger checks `runningTotal + cost` against the ceiling *before* it records, and refuses — emitting a `budget_exceeded` event — if the spend would break through.

```yaml
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

With a 1000-unit ceiling and buyer scoring at 5 units, one session can score roughly 200 buyers before the harness stops it — and every one of those spends lands in the ledger as a `budget_spend` entry `{seq, timestamp, operation, entityId, cost, currency, runningTotal}`. See [budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/) for how the ledger enforces this, and [Tutorial 5](/topics/defendable-agents/tutorials/05-budget-ceiling/) to watch a ceiling trip in practice.

## Step 4 — Wire the audit path

```yaml
audit:
  path: ./state/audit.jsonl
```

That is one line, and it is the line auditors care about most. The log is append-only JSONL — one event per line, fsync on flush — so it is tamper-evident and replayable. Each event carries the full decision, including the [variable-level trace](/topics/defendable-agents/primitives/decision-traces/) behind every score. The [audit trail](/topics/defendable-agents/primitives/audit-trail/) primitive covers the event schema in full.

## The complete file

Assembled, `harness.yaml` reads:

```yaml
governance:
  domains:
    - manifest: ./knowledge/knowledge.yaml
      paths:
        - ./knowledge/models
      tools:
        - kcp_plan
        - kcp_load

policy:
  fail_closed: true
  audit_all: true
  strict: true
  max_units: 12
  budget:
    amount: 1000
    currency: units
  context_budget: 200000

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

audit:
  path: ./state/audit.jsonl
```

## Verify it loads

A harness that does not load cleanly is worse than none — you would be running ungoverned while believing you were safe. Validate before you ever start a session:

```bash
# Ensure the state directory exists for the audit log
mkdir -p ./state

# Validate the manifest the harness depends on
kcp-agent kcp_validate --manifest ./knowledge/knowledge.yaml

# Load the harness and print the resolved policy
kcp-harness verify ./harness.yaml
```

A clean run echoes back the resolved domains, the effective policy with `fail_closed: true`, the ceiling, and the audit path — and exits `0`. Because `strict: true` is set, a typo'd key or an undeclared tool fails the verify step here, at your desk, rather than mid-session in front of a customer.

## Honest limits

This file governs *process*, not correctness. It guarantees that every operation is priced, bounded, and recorded — not that the numbers underneath are right. A wrong weight in a scoring model will be applied consistently and logged faithfully; the harness makes that mistake *visible and reproducible*, which is how you catch it, but it will not catch it for you. And a harness is not a one-time setup: budgets, costs, and domains drift as the system grows, so treat this file as something you [operate and maintain](/topics/defendable-agents/compliance/operating-and-maintenance/).

With the harness in place, the next step is to declare a real scoring model as a governed unit. Continue to [Tutorial 2: A Scoring Model](/topics/defendable-agents/tutorials/02-scoring-model/).
