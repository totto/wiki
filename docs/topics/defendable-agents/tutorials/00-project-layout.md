---
title: "Tutorial 0: Project Layout"
description: "Set up a defendable-agent project from scratch: the models, data, and state directories, the harness and knowledge manifests, and the CLI-first, file-based, no-SaaS philosophy behind it."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Tutorial 0: Project Layout

Before you write a single scoring function, decide where things live on disk. A defendable agent earns its name from the records it leaves behind, and those records are files: an audit log you can `grep`, a budget ledger you can diff, temporal pins you can replay. If the layout is wrong, the evidence is scattered, and scattered evidence is no evidence at all. So we start here — with directories, not code.

This tutorial builds the skeleton for **Lodestar**, the worked example that runs through the rest of this guide. Lodestar scores buyers in a regulated professional-services market: which buyers a firm should pursue, and how well a given firm matches a given buyer. Every number it produces is deterministic and every decision it takes is logged. None of that is possible without a place to put the artefacts.

## Philosophy: CLI-first, file-based, no SaaS

Three constraints shape everything below.

- **CLI-first.** Every operation is a command you can run from a terminal or a cron entry. There is no dashboard you have to click through to reproduce a score. If an auditor asks "how did you get this number", the answer is a command and a commit hash, not a screenshot.
- **File-based state.** Audit logs, budget ledgers, and temporal pins are plain files — JSONL and YAML — on a filesystem you control. Isolation between tenants is a directory boundary, not a row-level policy you hope the database enforces. See [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/) for why that boundary matters.
- **cron, not SaaS.** Scheduled re-scoring and drift checks run as cron jobs against the same binaries a human would run by hand. Nothing lives behind a vendor API you cannot inspect, version, or take offline.

The trade-off is honest: you own the operations. There is no managed service absorbing upgrades and backups for you. Governance is maintenance, not one-time setup — a theme the [operating and maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/) page returns to.

## Prerequisites

- Node.js 20+ and a package manager (this guide uses `pnpm`, but `npm` is fine).
- `git` — the whole point is that models and manifests are version-controlled.
- A working `kcp-agent` install exposing the MCP tools `kcp_plan`, `kcp_load`, and `kcp_validate`. If those names are unfamiliar, read [manifest basics](/topics/defendable-agents/kcp/manifest-basics/) first.

## The directory layout

Create the project and its top-level directories:

```bash
mkdir lodestar && cd lodestar
git init
mkdir -p models data .state
touch harness.yaml knowledge.yaml
pnpm init
```

You now have the canonical shape:

```
lodestar/
├── harness.yaml        # governance config: policy, budget, audit path
├── knowledge.yaml      # KCP manifest: declared governed units
├── models/             # deterministic scoring models (pure functions)
│   ├── buyer.ts        #   Need + Attractiveness + Winnability
│   └── match.ts        #   4-layer buyer↔firm match
├── data/               # shared, public input data (signals, companies)
│   └── signals/
└── .state/             # generated, append-only run artefacts
    ├── audit.jsonl     #   one event per line, fsync on flush
    ├── ledger.jsonl    #   budget entries {seq, op, cost, runningTotal}
    └── pins/           #   temporal pins, one per score
```

### What each folder holds

| Path | Contents | Committed to git? |
|------|----------|-------------------|
| `models/` | Pure deterministic scoring functions. Same inputs → same outputs. | Yes — this is source. |
| `data/` | Shared, public-data-only inputs: detected signals, company records. Every tenant sees the same events here. | Usually yes, or a pinned snapshot. |
| `.state/` | Generated run artefacts: the audit log, the budget ledger, temporal pins. Append-only, never hand-edited. | No — gitignored. |
| `harness.yaml` | The governance harness config: fail-closed policy, budget ceiling, audit path. | Yes. |
| `knowledge.yaml` | The KCP manifest declaring `models/` as governed units. | Yes. |

The split between `data/` (shared, public) and `.state/` (confidential, per-run) is the same split that later separates tenants. Keep it clean from day one. Add a `.gitignore`:

```bash
echo ".state/" >> .gitignore
```

## The two manifests

`harness.yaml` is the smallest thing you can write that still governs. It names the domains the agent may touch, sets a fail-closed policy, and caps spend and context:

```yaml
governance:
  domains:
    - manifest: knowledge.yaml
      paths: [models/]
      tools: [kcp_plan, kcp_load]
policy:
  fail_closed: true
  audit_all: true
  max_units: 50
  strict: true
  budget:
    amount: 1000
    currency: units
  context_budget: 200000
audit:
  path: .state/audit.jsonl
```

`fail_closed: true` means an operation with no matching rule is refused, not allowed — the subject of [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/). The `budget` ceiling of 1000 units is enforced *before* each operation records; more in [Tutorial 5](/topics/defendable-agents/tutorials/05-budget-ceiling/).

`knowledge.yaml` declares your scoring models as governed KCP units so the harness selects them deterministically and never silently swaps one for another:

```yaml
kind: manifest
metadata:
  name: lodestar
  version: 0.1.0
  domain: professional-services
  description: Buyer and match scoring for a regulated market.
  temporal:
    valid_from: 2026-01-01
    refresh_interval: P30D
units:
  - id: buyer-scoring-model
    path: models/buyer.ts
    tags: [scoring, buyer]
    description: 3-layer weighted buyer score.
  - id: match-scoring-model
    path: models/match.ts
    tags: [scoring, match]
    description: 4-layer buyer↔firm match score.
```

Validate before you go further:

```bash
kcp-agent kcp_validate --manifest knowledge.yaml
```

## Honest limits

This layout guarantees that your evidence is *complete and reproducible*. It does not guarantee it is *correct*. A wrong weight in `models/buyer.ts` will be applied to every buyer, consistently, and logged faithfully — which is exactly how you catch it on review, not something the directory structure prevents. Structure buys you visibility, and visibility is the precondition for everything else.

## Next

The skeleton is ready. Next, wire up the [governance harness](/topics/defendable-agents/tutorials/01-first-harness/) so those two manifests actually gate an operation, then build the [scoring model](/topics/defendable-agents/tutorials/02-scoring-model/) that fills `models/`. If you want the architectural rationale before the code, read the [architecture overview](/topics/defendable-agents/architecture/overview/).
