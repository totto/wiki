---
title: "Starter Kit & Reference Configs"
description: "Copyable reference artifacts for a defendable agent: a full harness.yaml, a KCP knowledge.yaml, the append-only audit-event schema, and a controls-mapping template."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Starter Kit & Reference Configs

This is the reference desk. Everything below is copyable and grounded in the [Lodestar case study](/topics/defendable-agents/reference/case-study-lodestar/) — the example system I use throughout this guide to score buyers in a regulated professional-services market. Nothing here is a screenshot of prose; each block is a real artifact you can drop into a repository and adapt. If you have read the [architecture overview](/topics/defendable-agents/architecture/overview/), these are the files that make that architecture concrete.

Four artifacts carry most of the weight: the governance harness, the KCP manifest, the audit-event schema, and the controls table. Get those right and the rest of the system has somewhere defendable to stand.

## 1. The governance harness — `harness.yaml`

The harness is the outer boundary. It declares which knowledge domains exist, which tools may touch them, and the policy that gates every operation. Fail-closed is the default: if a domain, a budget, or a manifest is missing, the session refuses to run rather than guessing. See [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) for why that default is load-bearing.

```yaml
# harness.yaml — governance boundary for a single Lodestar session
governance:
  domains:
    - manifest: ./knowledge/knowledge.yaml
      paths:
        - ./knowledge/**
      tools: [kcp_plan, kcp_load]

policy:
  fail_closed: true          # missing domain/budget/manifest => refuse, do not guess
  audit_all: true            # every governed operation emits an audit event
  max_units: 50              # cap on governed units loaded into one session
  strict: true               # unknown manifest fields are errors, not warnings
  budget:
    amount: 1000             # session ceiling, in operation units (not money)
    currency: units
  context_budget: 200000     # token ceiling for the whole session

audit:
  path: ./state/audit/session.jsonl   # append-only JSONL, fsync on flush

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

The `costs` block is the price list the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) reads. Every governed operation calls `record(op, entity)` which checks `runningTotal + cost` against the ceiling *before* recording. Over the ceiling and the operation throws, emitting a `budget_exceeded` event. This is not advisory accounting — it is a hard stop.

## 2. The knowledge manifest — `knowledge.yaml`

KCP declares the governed units of the session. The scoring models themselves are declared units, so the deterministic engine selects them by identity, never by silent fallback. If a model is missing or its hash changes, that is visible in the plan, not discovered later in a wrong score. The mechanics of this live in [declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/).

```yaml
# knowledge/knowledge.yaml — KCP manifest for the Lodestar scoring domain
kind: manifest
metadata:
  name: lodestar-scoring
  version: 3.2.0
  domain: professional-services-market
  description: Deterministic buyer and match scoring models plus signal decay.
  temporal:
    valid_from: "2026-01-01"
    refresh_interval: P30D        # 30-day refresh, matching signal half-life

units:
  - id: model.buyer
    path: models/buyer.v3.json
    tags: [scoring, buyer]
    description: 3-layer buyer score (Need 0.40, Attractiveness 0.25, Winnability 0.35).
  - id: model.match
    path: models/match.v2.json
    tags: [scoring, match]
    description: 4-layer match score across 21 variables.
    depends_on: [model.buyer]
  - id: model.signal-decay
    path: models/signal-decay.json
    tags: [temporal, signal]
    description: Linear freshness decay, ~30-day half-life.
```

`kcp-agent` exposes `kcp_plan`, `kcp_load`, and `kcp_validate` as MCP tools; the harness above only grants `kcp_plan` and `kcp_load` to the domain, keeping validation a separate, deliberate step. Wiring this to the agent runtime is covered in [wiring KCP, the agent, and MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/).

## 3. The audit-event schema

Every governed operation writes one JSON object per line. The schema below is the contract; the [audit trail](/topics/defendable-agents/primitives/audit-trail/) and [decision traces](/topics/defendable-agents/primitives/decision-traces/) pages explain how it is read back. Note the `scoring` block carries the full variable trace — the 18 buyer variables, their raw 1-5 scores, the three layer scores, the total, and the band — so a decision reproduces from its own record.

```json
{
  "timestamp": "2026-07-08T09:14:22.041Z",
  "sessionId": "sess_7f3a",
  "sequence": 42,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buy_1183", "name": "Buyer 1183" },
  "decision": {
    "action": "score_buyer",
    "inputs": { "signals": 6, "dataAsOf": "2026-07-07" },
    "outputs": { "total": 78, "band": "High" },
    "justification": "Weighted composite: Need 0.40, Attractiveness 0.25, Winnability 0.35."
  },
  "scoring": {
    "model": "model.buyer@3.2.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "Need": 82, "Attractiveness": 70, "Winnability": 78 },
    "total": 78,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-07",
    "scoredAt": "2026-07-08T09:14:22.041Z",
    "signalDates": ["2026-07-01", "2026-07-05", "2026-07-07"]
  },
  "budget": {
    "cost": 5, "currency": "units",
    "runningTotal": 210, "ceiling": 1000, "remaining": 790
  },
  "durationMs": 34
}
```

Event `type` values you will see across a session: `session_start`, `signal_detected`, `buyer_scored`, `match_scored`, `account_tiered`, `gtm_plan_generated`, `monitoring_check`, `reanalysis_triggered`, `score_delta`, `budget_spend`, `budget_exceeded`, and `session_end`. Use the file-based append-only writer in production and the in-memory writer in tests — same schema, different durability.

## 4. The controls-mapping template

Each control is satisfied by a *mechanism* and evidenced by a *record*. That pairing is the whole game: a claim with no record is marketing. The [control mapping](/topics/defendable-agents/compliance/control-mapping/) and [evidence packages](/topics/defendable-agents/compliance/evidence-packages/) pages turn this table into an exportable pack.

| Control | Mechanism | Record | Framework |
|---|---|---|---|
| Audit logging | Append-only JSONL | `session.jsonl` | ISO 27001 A.12.4 |
| Decision trace | Full variable inputs/outputs | `scoring` block | SOC 2 CC7.2 |
| Data provenance | Temporal pinning | `temporal` block | ISO 27001 A.8.1 |
| Reproducibility | Deterministic engine | Re-run == same total | ISO 27001 A.14.2 |
| Access boundaries | Fail-closed gating | Refused-session events | SOC 2 CC6.1 |
| Processing records | Per-session governed logs | Session summary | GDPR Art. 30 |
| Data minimization | Public-data-only + declared audience | Manifest `metadata` | GDPR Art. 5(1)(c) |
| Tenant isolation | Per-tenant state directory | Path boundary | ISO 27001 A.9.4 |
| Budget enforcement | Operation cost ceiling | `budget` block | SOC 2 CC6.1 |

## Honest limits

These artifacts make a system *defendable*, not *correct*. The deterministic engine guarantees that the same inputs yield the same score — so a badly designed variable is applied consistently and visibly, which is how you catch it, but the engine will not tell you the weight is wrong. Temporal pinning detects staleness; it does not refresh data. And `fail_closed: true` can be over-tuned until it blocks legitimate work — tune the ceiling and the refresh interval to your real cadence, then revisit them. Governance is maintenance, not one-time setup.

## Where to go next

- Build the harness from scratch in [tutorial 01: first harness](/topics/defendable-agents/tutorials/01-first-harness/).
- Assemble the scoring model in [tutorial 02: scoring model](/topics/defendable-agents/tutorials/02-scoring-model/).
- Export an evidence pack in [tutorial 08: evidence export](/topics/defendable-agents/tutorials/08-evidence-export/).
- Cross-check names against the [glossary](/topics/defendable-agents/orientation/glossary/) and avoid the traps in [anti-patterns](/topics/defendable-agents/reference/anti-patterns/).
