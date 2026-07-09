---
description: "Databricks just open-sourced Omnigent, a meta-harness that governs AI agents with deterministic, session-aware policies enforced in code — not prompts. That is the exact bet behind kcp-harness and the Defendable Agents guide, now ratified by Matei Zaharia's team. But Omnigent and KCP govern different halves of the same problem: one governs what an agent does, the other governs what it knows — and lets you prove it later. Why that split matters, and why the two compose instead of compete."
date: 2026-07-08T17:30:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Governance, Trust & Compliance
  - AI Agents & the Agentic Web
  - Knowledge Context Protocol
tags:
  - omnigent
  - databricks
  - kcp-harness
  - governance
  - meta-harness
  - defendable-agents
  - agentic-web
  - compliance
authors:
  - totto
  - claude
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Two Halves of the Governance Problem

A few weeks ago Databricks open-sourced [Omnigent](https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents), and Matei Zaharia's team followed it with a post on [contextual policies using session state](https://www.databricks.com/blog/contextual-policies-omnigent-using-session-state-better-govern-ai-agents). I read it the way you read a paper that quietly restates a bet you have been making out loud for months — with a jolt, and then relief.

<!-- more -->

Because the central claim is one I have written on this blog more times than is polite: **you govern an agent at a deterministic layer between it and its tools, enforced in code, not in a prompt.** Zaharia's framing, as reported, is almost word-for-word the thing [kcp-harness](/open-source/) exists to do — enforce budgets, permissions and risk at the harness layer, *not via prompts*. When the person who gave us Spark and MLflow ships that sentence with Databricks behind it, the argument about *whether* to govern at the boundary is over. Good. It was the right argument to win and I am happy to have company.

So let me do the useful thing rather than the defensive thing: say clearly where Omnigent and the [Defendable Agents](/topics/defendable-agents/) thesis agree, where they genuinely differ, and why I think they are **two halves of the same problem** that compose rather than compete.

## Where we already agree

The overlap is not vague. It is primitive-for-primitive:

| The primitive | Omnigent | kcp-harness / Defendable Agents |
|---|---|---|
| Deterministic layer, **not prompts** | policies at the meta-harness | the [governance harness](/topics/defendable-agents/architecture/governance-harness/) |
| Per-session **budget ceilings** | pause/block at spend caps | [budget & bounding](/topics/defendable-agents/primitives/budget-and-bounding/) |
| **Risk accrues → human approval** | running risk score, threshold gate | [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) |
| **Least privilege / no-write-down** | Bell–LaPadula on Drive | [multi-tenant isolation](/topics/defendable-agents/primitives/multi-tenancy/) |
| **Session state is the record** | contextual policy state | the [append-only audit trail](/topics/defendable-agents/primitives/audit-trail/) |
| Wraps **any** agent | Claude Code, Codex, Pi | an MCP proxy for any agent |

Two teams, no contact, arriving at the same six ideas. In my experience that is the strongest signal you get in this industry that an idea is actually load-bearing and not just fashionable. The convergence *is* the evidence.

And Omnigent brings real things I don't: an OS sandbox that can intercept network egress and inject a secret only on approved requests, so the agent never even sees your GitHub token; the ability to compose multiple frameworks and run several approaches against one problem to pick the best; a sharing model over terminal, app and web. That is serious systems work and it deserves the attention it is getting.

## Where the two halves split

Here is the distinction I want to plant, because it is the whole point.

**Omnigent governs what an agent *does*.** Tool calls, OS access, network egress, dollars. It is a control plane over an agent's *actions* — the output side, the blast radius. It is very good at that.

**KCP governs what an agent *knows*.** Which declared, [signed, temporally-pinned](/topics/defendable-agents/primitives/temporal-pinning/) units of knowledge it is allowed to load, with a provenance chain attached to every claim. It is a control plane over an agent's *inputs* — the knowledge side, the epistemics.

Those are not the same layer, and most real deployments need both. An agent that is perfectly sandboxed on its actions but is reading an unversioned, unsigned, silently-stale pile of "context" is still going to give you a confidently wrong answer about a regulation that changed in February. Governing the blast radius does not govern the *reasoning*. And governing the reasoning without bounding the actions leaves the blast radius open. You want both hands on the wheel.

Three things fall out of the knowledge half that I have not seen Omnigent claim, and that I think matter enormously in regulated work:

**1. Provenance you can replay.** Omnigent governs the *live* session. KCP lets you [reproduce a past decision](/topics/defendable-agents/examples/reproduce-a-decision/) months later — same signed inputs, same pinned model, same number, or a precise explanation of why not. That is the difference between "we had guardrails at the time" and "here is the exact decision, and here is it running again in front of you." Auditors do not want the first sentence. They want the second.

**2. Determinism at the core of the *decision*, not just around it.** This is the deepest difference, and it is philosophical before it is technical. Omnigent wraps deterministic guardrails *around* a model that is still improvising the consequential call. Defendable Agents argues the [improviser should not be making that call at all](/topics/defendable-agents/architecture/overview/): the scoring, the ranking, the "pursue this / not that" is a deterministic pure function, and the model is kept at the [edge](/topics/defendable-agents/architecture/model-at-the-edge/) where it turns messy input into typed input and nothing more. Guardrails on an improviser are a strictly weaker guarantee than an architecture that does not improvise the decision in the first place.

**3. It is aimed at regulated knowledge.** The [control mapping](/topics/defendable-agents/compliance/control-mapping/) is to SOC 2, ISO 27001:2022 and GDPR, and the worked corpus is real EU/Nordic regulation. Omnigent is general enterprise security and cost, which is a larger market and a fair place to aim. But "prove to a regulator why this agent said what it said about Article 28" is a different bar than "keep the agent inside its budget," and it is the bar I keep being asked to clear.

## They compose. That's the headline.

The honest one-liner is this: **Omnigent governs what your agent *does*. KCP governs what it *knows* — and lets you prove it later.**

And these are not rivals fighting for the same slot. They stack. A KCP knowledge-navigation gate — *this agent, in this session, may load these signed units and no others, and every claim carries its provenance* — is exactly the shape of a **contextual policy**. It could run *as* an Omnigent policy inside an Omnigent-wrapped session. The action harness and the knowledge harness are complementary organs, not competing skeletons.

One naming note, since the category is filling up fast: "harness" is now a crowded word — Databricks has staked **"meta-harness,"** and there are agent-harness framings from MongoDB and others. I'm not going to mint a competing suffix for the sake of it. [kcp-harness](/open-source/) is the *knowledge-and-provenance* governance layer — what an agent may read, trust, and later prove. The word I actually want to own is the property, not the plumbing: **defendable**. Omnigent can be the harness over the agent's hands; the point of KCP is that the agent's *sources and reasoning* end up defendable — declared, signed, replayable. Metaphor if it helps: hands and memory, different organs, same body. But the claim that matters isn't "which harness" — it's whether you can put the decision in front of an auditor and run it again.

## The part that actually matters

For two years the loud question was "how do we build a better agent." Omnigent landing where it landed, from where it landed, is the clearest sign yet that the loud question has changed to "how do we *govern the agents already running*" — and that the answer is a deterministic layer at the boundary, not a paragraph of good intentions in a system prompt.

I have been betting on that answer for long enough to have scars from it. It is genuinely good to watch a team with Databricks' reach plant a flag on the same hill. We are describing two halves of one machine. I will take that as validation, keep building the knowledge half in the open, and happily point people at Omnigent for the other half.

The agentic web is going to be governed. The only open question was *where* — in the prompt, or in the harness. That question just got answered twice, by two teams who never spoke. If you are still trying to govern agents by asking them nicely, the field has moved. Come build the boundary.

*The knowledge half is documented end to end in the [Defendable Agents field guide](/topics/defendable-agents/); the tooling is [open source](/open-source/). Omnigent is Apache-2.0 and [on Databricks' blog](https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents). This piece is written from public reporting on Omnigent, not from private knowledge of its internals — corrections welcome.*
