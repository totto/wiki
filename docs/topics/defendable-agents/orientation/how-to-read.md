---
title: "How to Read This Guide"
description: "Who the Defendable Agents field guide is for and four routes through it — paths for CISOs and compliance, for architects, for builders, and for reference."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# How to Read This Guide

This is a field guide, not a manifesto. It exists because I built an agent that makes commercial decisions inside a regulated professional-services market — scoring buyers, ranking firms, drafting go-to-market plans — and the people who had to sign off on it kept asking the same question: *when this thing tells us to chase a buyer, can you show me why, and can you show me it again next month and get the same answer?*

That question is the whole book. Everything here is an answer to it, worked out in code that runs. I refer throughout to a single example system I call **Lodestar**. It is anonymised — the real one is proprietary — but the mechanics are exact: a deterministic scoring engine, a governance harness, an append-only audit log, temporal pinning, a budget ledger, per-tenant isolation. Where I show a number, a weight or an event shape, it is the real shape, just with generic names.

I am Thor Henning Hetland. I have shipped software for four decades. I am not selling you an agent framework. I am showing you a pattern for making a probabilistic model *defendable* to an auditor, and being honest about where the pattern stops.

## Who this is for

Three audiences read this differently, and that is fine.

- **CISOs and compliance leads.** You need to know what evidence exists, what control each mechanism maps to, and where the blast radius is bounded. You care less about the TypeScript and more about the [threat model](/topics/defendable-agents/argument/threat-model/) and the [control mapping](/topics/defendable-agents/compliance/control-mapping/).
- **Architects.** You need to see the seams: what is deterministic and what is a model, where the trust boundary sits, how a session is bounded. Start with the [architecture overview](/topics/defendable-agents/architecture/overview/).
- **Builders.** You want to run something today. The [tutorials](/topics/defendable-agents/tutorials/00-project-layout/) build a working governed session from an empty directory upward, and the [starter kit](/topics/defendable-agents/reference/starter-kit/) gives you the skeleton.

You do not need to be all three. But the argument is written so that a compliance lead can follow the architecture at a conceptual level, and a builder can follow the argument well enough to know *why* the fail-closed check is not optional.

## Four ways through

There is no single correct order. Pick the route that matches why you are here.

### 1. The argument — why this shape at all

Conceptual, prose-heavy, almost no code. This is the case that guardrails bolted onto a model do not survive contact with an auditor, and that you need governance in the control path instead. Read [the governance gap](/topics/defendable-agents/argument/the-governance-gap/), then [what "defendable" means](/topics/defendable-agents/argument/what-defendable-means/), then [determinism vs probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/). If you read nothing else, read these three. They are the load-bearing ideas.

### 2. The architecture — how the pieces fit

Still mostly conceptual, but concrete about structure: the deterministic planner, the harness that gates every operation, the model pushed to the edge, and what happens when a check trips — [fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/). Read this when you need to explain the system to someone else, or decide whether the pattern fits your own stack.

### 3. The tutorials — build it yourself

Step-by-step, every page ends with something that runs. You start with [the project layout](/topics/defendable-agents/tutorials/00-project-layout/) and finish able to export an evidence package. This is the hands-on path. The primitives and decisions sections sit behind the tutorials as reference: when a tutorial uses the [audit trail](/topics/defendable-agents/primitives/audit-trail/) or the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/), the primitive page is the deep dive.

### 4. The reference — look one thing up

The [case study](/topics/defendable-agents/reference/case-study-lodestar/), the [anti-patterns](/topics/defendable-agents/reference/anti-patterns/) and the [FAQ](/topics/defendable-agents/reference/faq/) are for when you already know the shape and need a specific answer. Not meant to be read front to back.

## Conceptual vs step-by-step

A quick map so you know what you are opening:

| Section | Register | Code density |
| --- | --- | --- |
| Argument | conceptual | none to light |
| Architecture | conceptual, structural | light |
| Primitives | reference | moderate, with schemas |
| Decisions | reference | moderate, with manifests |
| Tutorials | step-by-step | heavy, copyable |
| Examples | walkthrough | moderate |
| Compliance | reference | light, tables |

## How Lodestar threads through

Every section uses the same example so you never have to re-learn a domain. Lodestar scores a **buyer** as a weighted composite of three layers — Need (weight 0.40), Attractiveness (0.25) and Winnability (0.35) — each layer the mean of six 1–5 variables scaled to 0–100. A total lands the buyer in a priority band:

```json
{
  "entity": { "type": "buyer", "id": "b-4417" },
  "scoring": {
    "model": "buyer-score@2.1.0",
    "layerScores": { "need": 78, "attractiveness": 62, "winnability": 71 },
    "total": 72.3,
    "band": "High"
  }
}
```

The bands are fixed: `>=85` Very high, `>=70` High, `>=55` Interesting but with gaps, `>=40` Lower priority, otherwise Not prioritized now. When the argument talks about reproducibility, it is *this* score. When the tutorials build a governed session, they score *this* buyer. When compliance maps a decision trace to a control, it is *this* variable list. One example, seen from every angle — which is the fastest way to understand a system.

## An honest limit, up front

The determinism you will read so much about guarantees **process, not correctness**. If a variable is designed badly, the engine applies that bad variable consistently to every buyer — same inputs, same wrong output, every time. That is not a bug in the pattern; it is the point. A consistent, reproducible, fully-traced error is one you can *find*, argue about and fix. A model that is confidently wrong in a different way each run is one you cannot. This guide makes mistakes visible and defensible. It does not make them impossible.

New here? The [glossary](/topics/defendable-agents/orientation/glossary/) defines every term before you meet it in anger. Start wherever your question is loudest.
