---
description: "The agentic web has a governance-shaped hole. Agents are about to read our regulations, spend our money, and brief our boards — and the dominant architecture can't answer 'why did you do that?' with anything better than a chat log. Defendable agents can. Determinism at the core, the model at the edge, every decision evidenced."
date: 2026-07-08T18:00:00
slug: defendable-agents
categories:
  - Governance, Trust & Compliance
  - AI Agents & the Agentic Web
  - Knowledge Context Protocol
tags:
  - defendable-agents
  - ai-governance
  - compliance
  - kcp
  - kcp-agent
  - determinism
  - audit
  - prompt-injection
authors:
  - totto
  - claude
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Defendable Agents

Every serious conversation about deploying an AI agent into real work — not a demo, real work, with money or regulation or reputation attached — eventually hits the same wall. Someone from compliance, or procurement, or security, or the board, asks a version of one question:

**"Why did it do that?"**

And in the dominant way we build agents today, the honest answer is a shrug and a chat log.

<!-- more -->

![A defendable agent workflow: a deterministic plan produced before any action, every step declared, evidenced, and reproducible](/assets/images/summer-plan-00-defendable-agent-workflow.webp)

The agentic web everyone is racing to build has a governance-shaped hole in it. Agents are about to read our regulations, spend our money, and brief our boards. And the architecture almost everyone is using — stuff the context window, let the model decide what to read and trust and spend, applaud the output — produces decisions that cannot be reproduced, cannot be audited, and cannot be defended in front of anyone who signs things for a living.

I've started calling the alternative **defendable agents**, and I mean the word in both of its senses at once.

## Two kinds of defense

There's the **legal** sense: you can defend the decision. To a regulator, an auditor, a court, a board. "Here is exactly why the agent scored this account a 73, which model version produced it, what data it used, when that data was valid, and the append-only log entry that recorded all of it." That's a sentence you can say in a deposition.

And there's the **engineering** sense: the architecture is defensible. It holds up when someone pushes on it. A prompt injection buried in a document the agent reads has nothing to grab, because the model was never the thing deciding what to read.

You don't get the first without the second. Defendability isn't a policy you write or a review meeting you hold. It's a property of how the agent is built.

## Improvisation doesn't testify well

Here's the core problem with the vibes-based agent, stated plainly: **when the model decides everything, there is nothing left to govern.** By the time the model has chosen what to load, what to believe, and what to spend, the decision has already happened inside a probability distribution nobody can re-run. You can log what it did afterward, but a reconstructed narrative isn't evidence. It's a story.

A defendable agent inverts the stack. **Determinism at the core; the model at the edge, on a leash.** A deterministic planner — a pure function over declared metadata — decides what's eligible: scoring, trust-gating, time-filtering, budgeting. That produces an inspectable *plan* before any content is loaded or any model is called. The model only shows up at the edges, to synthesize an answer once the plan says what to load, or to bridge a vocabulary gap — and even then it works behind a deterministic gate, seeing metadata only, never holding anything an injection could take.

The model proposes. The plan disposes. Every decision comes with a written reason, and every *skipped* option comes with a reason too — superseded, untrusted, over budget, out of audience. Not silence. Reasons.

## From toy to till

You can watch this idea climb a ladder of stakes.

At the low end, I've written about [a family vacation an agent can defend](/blog/2026/07/09/the-summer-plan-a-family-vacation-the-agent-can-defend/) and [a hiring agent that stays inside the rules](/blog/2026/07/08/hiring-by-the-book-a-defendable-hr-agent-on-a-regulatory-knowledge-web/) — relatable, low-blast-radius examples where "defend this decision" is easy to picture. Then [an enterprise documentation estate the agent can defend](/blog/2026/07/10/the-milky-way-an-enterprise-documentation-estate-the-agent-can-defend/), where the stakes get real. Same architecture, rising consequences.

But the example that convinced me this is a category, not a trick, is a production system I'll call **Lodestar** — anonymized, because it's real and it has clients. Lodestar is a governed competitive-intelligence scoring engine for a regulated professional-services market: thousands of buyers, a hundred-odd competing firms, and a score attached to every one of them that drives a commercial decision someone may later have to justify.

Every score is deterministic — eighteen named variables for a buyer, twenty-one for a match, layered into a 0–100 composite. No model guessing in the scoring loop. Every operation routes through a governance harness that is *fail-closed* (can't verify it? block it), *audit-all* (append-only log of every decision, with the full variable trace, not just the total), *budget-bounded* (each run has a hard ceiling), and *temporally pinned* (every score records when its data was valid, and flags itself when that goes stale).

The payoff is a table I keep coming back to — governance primitives mapped straight onto the controls that gate enterprise deployment: audit logging to ISO 27001 A.12.4, decision trace to SOC 2 CC7.2, processing records to GDPR Article 30, reproducibility to ISO 27001 A.14.2. Not a claim of compliance. A *mapping* — each control satisfied by a mechanism you can point at in the code and a record you can pull from the log.

That's what "defendable" cashes out to. A deterministic decision, fully traced, temporally pinned, in an append-only log, mapped to a named control — **that testifies.**

## And it's the same substrate as everything else

Here's the part I didn't expect. Lodestar didn't invent its judgment; it *encodes* an expert methodology — a consultancy's buyer-and-match model — into about thirty governed, reusable units. Which means the same infrastructure that makes each score auditable also makes the expertise *portable*: it applies consistently across every client, and it doesn't walk out the door when the expert who built it leaves.

That's the [compound developer](/blog/2026/06/02/the-compound-developer/) thesis at organizational scale. Defendable and compound turn out to be the same substrate seen from two angles — [navigable, governed knowledge](/topics/knowledge-context-protocol/). The thing that makes an agent smart is the thing that makes it accountable.

## The reference material

The narrative is the easy part. If you want to actually build one of these, I've written up the architecture, the governance patterns, the anonymized Lodestar case study, and a copyable starter kit (a `harness.yaml` skeleton, an audit-log schema, the controls table as a template) as a proper reference section:

**→ [Defendable Agents](/topics/defendable-agents/)**

It's the first section of this site published as a KCP-navigable knowledge unit, discoverable by an agent through the site's own manifest — because it would be a little embarrassing to write all this about navigable, governed knowledge and not practice it.

The era of vibes-based agents won't end because someone writes a stern blog post. It ends when the deterministic, defendable alternative is right there — one command away, with receipts.
