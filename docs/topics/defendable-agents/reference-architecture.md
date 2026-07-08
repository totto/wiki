---
title: "Reference Architecture — Defendable Agents"
description: "The defendable-agent reference architecture: a deterministic planner at the core, a governance harness around it, and the LLM restricted to the edge. Navigation is an algorithm, not a language problem."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Reference Architecture

The whole architecture is one inversion of the industry default:

> **Determinism at the core. The model at the edge — on a leash.**

In the vibes-based agent, the model sits in the middle and decides everything. In a defendable agent, a deterministic planner sits in the middle, and the model is pushed to the two jobs only a model can do — and nothing else.

---

## Three components

### 1. The deterministic planner

The planner reads declared metadata — a [KCP manifest](../knowledge-context-protocol.md) describing intent, dependencies, freshness, trust requirements, audience, and price — and produces an **inspectable plan before any content is fetched and before any model is called.**

This is the part the industry keeps skipping: **navigation is not a language problem.** Scoring declared metadata, gating on trust, filtering by time, budgeting spend — that is an *algorithm*. Handing it to an LLM doesn't add intelligence; it subtracts accountability. A pure function over metadata gives you reproducibility for free, and reproducibility is the first property of a defendable decision.

Skipped units get **reasons, not silence**: superseded, untrusted, over budget, out of audience. The plan is the product — a written, inspectable record of what will happen and why, generated at zero token cost.

### 2. The governance harness

The planner decides *what is eligible*. The harness enforces *the rules of the session*. It wraps every operation with:

- **Fail-closed policy** — if governance can't verify something, it blocks rather than guesses.
- **Audit-all** — every operation is logged, not just the ones that succeeded.
- **Budget ceilings** — each operation costs units; a session has a hard limit; nothing is committed until the plan fits the budget.
- **Temporal pinning** — every decision records the validity window of the data it used, so staleness is detectable later.

The harness is what turns a deterministic *planner* into a governed *system*. It is the difference between "this agent is reproducible" and "this agent is reproducible, bounded, logged, and pinned to a point in time." The [governance patterns](governance-patterns.md) page covers each primitive in detail.

### 3. The model, at the edge

Once the plan says what to load, a model may **synthesize** the answer. That's what they're for. And when there is a genuine lexical gap — the task says "infrastructure," the manifest says "power grid" — a model may act as a **vocabulary critic**, proposing search terms *between* deterministic plans, never above them.

The critical constraint: the model sees plan **metadata only**, never governed content, and its proposals pass through a deterministic gate before the planner re-plans from scratch. So when a document the model reads contains an injection — `IGNORE ALL INSTRUCTIONS` — it has nothing to act on. **The injection bounces off a deterministic gate that only passes vocabulary, by construction.** The model was never holding anything an injection could take.

> The model proposes. The plan disposes. That is not a safety feature bolted on afterward — it is the constitutional arrangement.

---

## Why this is defendable and the alternative isn't

| Question an auditor will ask | Vibes-based agent | Defendable agent |
|---|---|---|
| Why did it read that? | Attention weights, presumably | A scored, written reason in the plan |
| Why did it *not* read this? | Nobody knew it existed | A written skip-reason |
| Same inputs tomorrow? | Different answer | Same decision, byte-for-byte |
| What did it spend, and why? | A token bill | A budget commit log |
| What if a source contained instructions? | The whole context window is exposed | The model never touches navigation |
| When was the data valid? | Unknown | Pinned, with drift detection |

Every row on the right is a piece of evidence. That is the entire point: a defendable agent produces an audit trail as a *byproduct of how it works*, not as an afterthought someone has to reconstruct.

---

## The reference implementations

This isn't a thought experiment. The deterministic planner ships as **kcp-agent** (`npx kcp-agent`), and the governance harness pattern is **kcp-harness** — both open, both under [Cantara](https://github.com/Cantara/knowledge-context-protocol). The [Lodestar case study](case-study-lodestar.md) shows the whole stack running in a regulated domain, and the [starter kit](starter-kit.md) gives you the config to try it.

*Next: [Governance Patterns](governance-patterns.md) — the four primitives, in detail.*
