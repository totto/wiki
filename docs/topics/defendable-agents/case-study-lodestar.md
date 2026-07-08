---
title: "Case Study: Lodestar — a Defendable Scoring System"
description: "Lodestar (anonymized) is a governed competitive-intelligence scoring system for a regulated professional-services market. Deterministic scoring, an append-only audit trail, budget ceilings, and temporal pinning — where every automated score has to justify itself."
image: assets/images/kcp-agent-020-01-plan-is-the-product.webp
---

# Case Study: Lodestar

!!! note "About this case study"
    *Lodestar* is an anonymized composite of a real, shipped system. The domain, client, and specifics have been generalized; what's shown here is the architecture and governance model, which are generic patterns you can apply anywhere. No real names, scores, or client data appear.

## The domain

Lodestar is an automated **competitive-intelligence scoring system** for a regulated professional-services market: thousands of prospective buyers, roughly a hundred competing firms, and a steady stream of public events that signal when a buyer might be in the market. It watches those signals, scores buyers, matches them to firms, and produces go-to-market recommendations that feed the firms' existing CRM systems.

It is deliberately **not a SaaS**. CLI-first, file-based state, cron for scheduling. An intelligence layer, not an interface layer — structured outputs that load into tools people already use.

The reason it is a good case study for defendable agents is simple: **every score drives a commercial decision that someone may later have to justify.** "Why did we prioritize this account?" and "Why did the system rank us behind that competitor?" are questions with real consequences. A number that can't explain itself is worse than no number.

---

## The architecture

```
Public registry events + news sources
          │
          ▼
Signal detection  (typed trigger categories)
          │
          ▼
Buyer scoring     (18 variables · 3 layers · 0–100 composite)
          │
          ▼
Match scoring     (21 variables · 4 layers · buyer ↔ firm)
          │
          ▼
GTM / account strategy  →  CRM export
```

Every stage is **deterministic**. A buyer's 0–100 score is a layered composite of eighteen named variables — not an LLM's impression of the buyer. The match score is twenty-one variables across four layers. When the number changes, you can see *exactly* which variable moved and why.

The model is nowhere in the scoring loop. Where language work is genuinely needed — summarizing a news event into a typed signal, say — it happens at the edge, behind the deterministic gate, and its output is recorded as an input to a scored decision, never as the decision itself.

---

## The governance layer

Every scoring decision routes through a [governance harness](governance-patterns.md) configured in a `harness.yaml`:

- **Fail-closed** — if the harness can't verify a scoring model's provenance, the operation blocks.
- **Audit-all** — every signal detection, buyer score, match score, and tier assignment is written to an append-only log, with the full variable trace, not just the total.
- **Budget ceilings** — each operation costs units (a cheap signal check, a little; a full firm analysis, more); each run has a hard ceiling, so a scheduled job can't run away.
- **Temporal pinning** — every score records the validity window of its inputs; drift detection flags scores whose underlying data has gone stale and schedules re-analysis.

The scoring models themselves are governed knowledge units — declared in a [KCP manifest](../knowledge-context-protocol.md), selected deterministically, never silently swapped. An auditor can ask "which version of the buyer-scoring model produced this number, and when was its input data valid?" and the answer is in the record.

---

## The receipts

Because the governance is mechanical, the compliance story is a mapping, not a promise:

| Control | How Lodestar satisfies it |
|---|---|
| Audit logging (ISO 27001 A.12.4) | Append-only log of every scoring operation |
| Decision trace (SOC 2 CC7.2) | Full 18/21-variable inputs and outputs per score |
| Data provenance (ISO 27001 A.8.1) | Temporal pinning of every input's validity window |
| Reproducibility (ISO 27001 A.14.2) | Deterministic scoring engine — same inputs, same score |
| Processing records (GDPR Art. 30) | Per-session governed logs |
| Data minimization (GDPR Art. 5) | Public data only; declared audience scoping |
| Tenant isolation (ISO 27001 A.9.4) | Per-tenant state; shared signals, confidential scores |
| Budget enforcement (SOC 2 CC6.1) | Operation-cost ceilings per run |

Signal and company data are **shared** across tenants (every firm sees the same public events). Match scores and go-to-market plans are **per-tenant and confidential** — they depend on each firm's own profile — and live in isolated state. The isolation is not a policy; it's a directory boundary the harness enforces.

---

## The organizational angle

Lodestar didn't invent its scoring judgment. It **encodes an expert methodology** — a consultancy's multi-part buyer-and-match model — into roughly thirty discrete, governed units. That has an effect beyond automation: the expertise becomes **infrastructure**. It's auditable, it's reusable across every tenant, and it doesn't walk out the door when the expert who developed it moves on.

This is the seam where *defendable* meets *compound*. The same encoded, governed knowledge that lets an auditor trace a score is what lets the organization apply that expert's judgment consistently, at scale, without the expert in the room. A defendable agent and a [compound organization](../skill-driven-development.md) are built from the same substrate.

---

## What Lodestar is not

- It is not proof the scoring model is *correct* — only that its outputs are reproducible, traceable, and bounded. A flawed variable would be applied consistently and visibly, which is how you'd catch it.
- It is not autonomous in the "let it loose" sense. It runs on a schedule, inside a budget, producing recommendations a human acts on.
- It is not magic. It is boring, governed engineering — which is exactly the point. Boring is what testifies.

*See the [Starter Kit](starter-kit.md) for a `harness.yaml` skeleton and audit schema you can adapt, or start from the [Reference Architecture](reference-architecture.md).*
