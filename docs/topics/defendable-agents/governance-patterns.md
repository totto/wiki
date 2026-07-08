---
title: "Governance Patterns — Defendable Agents"
description: "The four governance primitives behind a defendable agent — fail-closed policy, audit-all, budget ceilings, and temporal pinning — and how they map onto SOC 2, ISO 27001, and GDPR controls."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# Governance Patterns

A defendable agent's governance is not a review meeting or a policy PDF. It is four mechanical primitives, enforced in code, that every operation routes through. Each one produces evidence as a byproduct.

---

## The four primitives

### 1. Fail-closed policy

If governance cannot *verify* something, it **blocks** — it does not proceed on a guess. A manifest that demands an attestation the agent can't provide isn't partially trusted; it's skipped, on the record. This is the inverse of the usual default, where the agent does its best and hopes.

Fail-closed is what makes the audit trail *trustworthy*: an absence of a block is itself evidence, because a block would have been recorded.

### 2. Audit-all

Every operation is written to an **append-only log** — not just the successful ones, not just the interesting ones. And not just totals: the log captures the **full decision trace** — the inputs, the intermediate scores, the outputs. "Why is this a 73?" is answerable because the 73 was never a black box; it was a recorded computation over named variables.

Append-only matters. A log you can edit is not evidence. A log you can only append to is.

### 3. Budget ceilings

Every operation costs **units**, and a session has a hard ceiling. Cheap operations cost a little; expensive analysis costs more; nothing commits until the plan fits the budget. This is not primarily a cost-control feature — it is a **bounding** feature. An agent that cannot exceed a declared budget cannot run away, and "it could only ever have done this much" is a sentence you can say to a risk officer.

### 4. Temporal pinning

Every decision records the **validity window** of the data it used. A score computed from last quarter's data says so. Drift detection then flags decisions whose inputs have gone stale, so they can be recomputed. This closes the gap between "the agent was right when it ran" and "the agent is still right" — and it makes *provenance* a first-class, queryable property rather than an assumption.

> Stale knowledge is worse than no knowledge: no knowledge makes an agent cautious; stale knowledge makes it confidently wrong.

---

## The receipts: mapping primitives to controls

Here is why this matters to anyone who has sat through an audit. Each primitive lands directly on a named control in the frameworks that gate enterprise deployment. This table is the whole argument compressed into one exhibit:

| Control area | Implementation | Framework reference |
|---|---|---|
| Audit logging | Append-only JSONL log of every operation | ISO 27001 A.12.4 |
| Decision trace | Full variable inputs/outputs per decision | SOC 2 CC7.2 |
| Data provenance | Temporal pinning of input validity | ISO 27001 A.8.1 |
| Reproducibility | Deterministic scoring / planning engine | ISO 27001 A.14.2 |
| Access boundaries | Fail-closed trust gating | SOC 2 CC6.1 |
| Processing records | Per-session governed logs | GDPR Art. 30 |
| Data minimization | Declared-audience + public-data-only scoping | GDPR Art. 5(1)(c) |
| Tenant isolation | Per-tenant state separation | ISO 27001 A.9.4 |

The point is not that the agent *claims* compliance. The point is that **each control is satisfied by a mechanism you can point at in the code and a record you can pull from the log.** A deterministic decision, fully traced, temporally pinned, in an append-only log, mapped to a clause — that testifies.

Map the exact clause numbers to whichever frameworks your deployment is assessed against; the primitives don't change, only the citations do.

---

## What this does *not* give you

Honesty is part of defensibility, so: these primitives guarantee **process**, not **correctness**.

- A deterministic engine can encode bad judgment and apply it perfectly consistently. Determinism makes a wrong decision *reproducible and inspectable* — which is how you find and fix it — but it does not make it right.
- Temporal pinning detects staleness; it doesn't refresh the data for you.
- Fail-closed can be over-tuned into a system that blocks legitimate work. The thresholds are a real design decision.
- Governance is **maintenance**, not a one-time setup. A harness you configure once and never revisit drifts, same as any other infrastructure.

Defendability means "here is exactly why, reproducibly, and here is the evidence" — which is a categorical upgrade over a chat log, and worth being precise about rather than overselling.

*Next: [Case Study — Lodestar](case-study-lodestar.md), where these primitives run in a real regulated domain. Or grab the [Starter Kit](starter-kit.md).*
