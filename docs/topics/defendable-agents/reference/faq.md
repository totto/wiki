---
title: "Frequently Asked Questions"
description: "Straight answers on determinism, correctness, performance, where the LLM lives, cost, when a defendable agent is overkill, and how it maps to the EU AI Act."
image: assets/images/kcp-agent-020-03-model-at-the-edge.webp
---

# Frequently Asked Questions

These are the questions I get every time I show someone a defendable agent. I have kept the answers short and honest. Where a full treatment exists elsewhere in this guide, I link to it rather than repeat it.

## Does determinism mean the agent is dumb?

No. It means the part that produces a governed number is a pure function, not a language model improvising. A [deterministic planner](/topics/defendable-agents/architecture/deterministic-planner/) still runs rich logic: eighteen scored variables across three weighted layers, freshness decay, tier thresholds, band cut-offs. Lodestar's buyer score is a weighted composite of Need (0.40), Attractiveness (0.25) and Winnability (0.35) — plenty of nuance, none of it dice-rolling.

The intelligence you keep is the model's. The intelligence you drop is the *unaccountable variance*. See [Determinism vs probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/) for the full argument.

## Does determinism guarantee the answer is correct?

It does not, and anyone who tells you otherwise is selling something. Determinism guarantees **process, not correctness**. If a variable is wrongly designed — say `signal-freshness` decays too fast — the engine applies that error to *every* buyer, identically, on every run.

That is the point. A consistent, visible, reproducible error is one you can find, diff, and fix. A probabilistic error that shows up one run in twenty is one you will argue about for a quarter. [Reproducibility](/topics/defendable-agents/decisions/reproducibility/) is what turns a bug from folklore into a ticket.

## Is a defendable agent slower?

Marginally, and in the places that do not matter. The pure scoring functions are cheap — arithmetic over 18–21 variables. The overhead is the harness: recording a budget entry before each operation, creating a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/), and appending one JSONL line with an `fsync` on flush. That is microseconds of compute plus one durable write per governed decision.

```json
{
  "timestamp": "2026-07-08T09:14:22.881Z",
  "sessionId": "s-4f21",
  "sequence": 42,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "b-9931", "name": "—" },
  "scoring": {
    "model": "buyer@2.3.0",
    "layerScores": { "need": 78, "attractiveness": 64, "winnability": 71 },
    "total": 72.05,
    "band": "High"
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 210, "ceiling": 1000 },
  "durationMs": 3
}
```

The slow part of any agent is the model call at the edge, and that is unchanged. You are adding accounting, not a bottleneck. See [Budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/).

## Where is the LLM, then?

At the edge, and only at the edge. The model reads messy inputs — a news item, an email thread, a filing — and proposes structured variable scores. It never decides the composite, never picks the band, never approves spend. Those are the harness's job. This split is the whole design; read [Model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/).

Honest limit: **the model at the edge is still a model.** It can hallucinate a `signal-relevance` of 5 where a human would say 2. Governance does not stop that — it *records* it, pins the data it saw, and lets a reviewer catch it in the [decision trace](/topics/defendable-agents/primitives/decision-traces/). You are trading invisible error for auditable error, not eliminating error.

## What does it cost to run?

Two kinds of cost. **Compute cost** is dominated by edge model calls, same as any agent. **Governance cost** is one append-only write and a few map insertions per operation — negligible.

The cost you actually manage is the internal **budget ledger**, denominated in units, not currency-until-you-say-so. Each operation has a fixed price:

| Operation | Units |
|---|---|
| signal_detection | 1 |
| buyer_scoring | 5 |
| match_scoring | 5 |
| firm_analysis | 10 |
| account_tiering | 2 |
| gtm_plan | 10 |
| reanalysis | 5 |

The ledger checks the ceiling **before** recording. A session with a 1000-unit ceiling that tries to exceed it gets `accepted:false`, the operation throws, and a `budget_exceeded` event lands in the audit log. That is your runaway-agent circuit breaker and your [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) in one.

## When should I *not* bother?

Be honest with yourself. A defendable agent is overkill when:

- The decision is low-stakes and reversible — a draft, a suggestion, a search rank nobody audits.
- No one will ever ask you to *reproduce* or *justify* the output.
- There is no regulator, auditor, buyer, or angry counterparty in your future.
- The agent touches only your own throwaway data with no [tenant boundary](/topics/defendable-agents/primitives/multi-tenancy/) to defend.

Governance is **maintenance, not one-time setup**. You will version models, re-tune bands, and chase [drift](/topics/defendable-agents/primitives/drift-detection/) for as long as the system lives. If the decision does not warrant that ongoing cost, do not pay it. The [anti-patterns](/topics/defendable-agents/reference/anti-patterns/) page has the failure modes, including fail-closed tuned so tight it blocks legitimate work.

## How does this relate to the EU AI Act?

The defendable-agent primitives are mechanism-and-record pairs, and most of them line up cleanly with what high-risk-system obligations ask for: logging, traceability, human oversight, and record-keeping. Concretely, the append-only [audit trail](/topics/defendable-agents/primitives/audit-trail/) gives you event logging; temporal pinning gives you data provenance; the deterministic engine gives you reproducibility; fail-closed gating gives you access control and an oversight chokepoint.

I map these to specific ISO 27001, SOC 2 and GDPR controls on the [control mapping](/topics/defendable-agents/compliance/control-mapping/) page, and show how to assemble the records into an [evidence package](/topics/defendable-agents/compliance/evidence-packages/).

Honest limit: a control mapping is **evidence you can produce**, not a certificate. It shows a mechanism plus a record for each obligation; it does not conduct your conformity assessment or replace your legal review. The framework makes you *defendable* — able to answer "why did the agent do that?" with a trace — which is necessary for compliance but never the whole of it.

## Where do I start?

Read [How to read this guide](/topics/defendable-agents/orientation/how-to-read/), then build the smallest thing that works: the [first harness tutorial](/topics/defendable-agents/tutorials/01-first-harness/). Everything else layers on top of that one governed session.
