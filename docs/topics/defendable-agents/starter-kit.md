---
title: "Starter Kit — Defendable Agents"
description: "Copyable artifacts for building a defendable agent: a harness.yaml governance skeleton, an append-only audit-log schema, and the controls-mapping table as an adaptable template."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Starter Kit

Three artifacts you can copy and adapt. They are deliberately minimal — the point is the *shape*, not a framework.

---

## 1. `harness.yaml` — governance skeleton

The governance config that wraps every operation. Adjust the domains, costs, and ceilings to your system.

```yaml
# harness.yaml — governance layer for a defendable agent
version: "1.0"

governance:
  domains:
    - manifest: "./knowledge.yaml"   # the KCP manifest that declares your units
      paths:
        - "models/"                  # deterministic scoring / decision models
        - "data/"
      tools:
        - "kcp_plan"                 # deterministic planning
        - "kcp_load"                 # governed content loading

  policy:
    fail_closed: true                # block if governance can't verify — never guess
    audit_all: true                  # log every operation, not just successes
    max_units: 10                    # cap knowledge units per plan
    strict: false                    # list non-eligible units (with reasons) vs hide them
    budget:
      amount: 1000                   # hard ceiling per session
      currency: "units"
    context_budget: 200000           # token ceiling per session

audit:
  path: ".state/audit.jsonl"         # append-only

# Operation cost table — used to enforce the budget ceiling
costs:
  signal_detection: 1
  score_cheap: 5
  analysis_expensive: 10
  plan_generation: 10
  monitoring_check: 1
```

The two decisions that matter most: **`fail_closed: true`** (verification failure blocks, it doesn't proceed) and a **real budget** (so a run is provably bounded).

---

## 2. Audit-log schema — append-only

One JSON object per line, appended and never edited. This is your evidence. The essential fields:

```json
{
  "ts": "2026-07-08T09:14:22Z",
  "session": "run-2026-07-08-0900",
  "op": "buyer_scoring",
  "subject": "buyer:0x8f21",
  "model_id": "buyer-v3",
  "model_valid_from": "2026-07-01",
  "inputs": { "var_01": 0.42, "var_02": 1, "…": "…" },
  "layers": { "fit": 71, "intent": 66, "timing": 80 },
  "score": 73,
  "cost_units": 5,
  "budget_remaining": 812,
  "temporal_pin": { "data_valid_from": "2026-06-30", "stale": false },
  "policy": { "fail_closed": true, "verified": true }
}
```

Why each field earns its place: `model_id` + `model_valid_from` answer *which model, which version*; `inputs`/`layers`/`score` are the **full decision trace** (not just the total); `cost_units`/`budget_remaining` prove the run was bounded; `temporal_pin` makes provenance queryable; `policy.verified` records that fail-closed passed. Together they let you reconstruct *exactly why* a decision came out the way it did, months later.

---

## 3. Controls-mapping — template

Fill the right-hand column with your implementation and the exact clause numbers of whatever frameworks you're assessed against. The primitives don't change; only the citations do.

| Control area | Your implementation | Framework reference |
|---|---|---|
| Audit logging | Append-only log of every operation | ISO 27001 A.12.4 |
| Decision trace | Full variable inputs/outputs per decision | SOC 2 CC7.2 |
| Data provenance | Temporal pinning of input validity | ISO 27001 A.8.1 |
| Reproducibility | Deterministic decision engine | ISO 27001 A.14.2 |
| Access boundaries | Fail-closed trust gating | SOC 2 CC6.1 |
| Processing records | Per-session governed logs | GDPR Art. 30 |
| Data minimization | Declared-audience / minimal-data scoping | GDPR Art. 5(1)(c) |
| Tenant isolation | Per-tenant state separation | ISO 27001 A.9.4 |

---

## Where to go from here

- The reference planner: **`npx kcp-agent`** — [Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)
- The concepts behind these files: [Reference Architecture](reference-architecture.md) · [Governance Patterns](governance-patterns.md)
- A full system using all of it: [Case Study — Lodestar](case-study-lodestar.md)
- The knowledge substrate underneath: [Knowledge Context Protocol](../knowledge-context-protocol.md)

*These artifacts are illustrative skeletons, not a released framework. Adapt them; don't ship them verbatim.*
