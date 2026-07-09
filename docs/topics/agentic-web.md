---
title: "The Agentic Web"
description: "The agentic web is the internet rebuilt for software agents that read, spend, and act on your behalf — not for humans clicking links. A map of its hard problems (identity, memory, coordination, determinism, governance, knowledge) and the architecture that makes agents on it defendable rather than merely capable."
image: assets/images/agentic-web-slide-01.webp
---

# The Agentic Web

**The agentic web is the internet re-pointed at software agents instead of human eyeballs** — agents that discover services, read knowledge, spend money, and take consequential actions on someone's behalf. It is not a metaphor for "AI is big now." It is a concrete shift in who the client is: the thing on the other end of the request is increasingly an autonomous agent, and almost none of the web's assumptions — a human reads the page, a person is behind the login, someone will notice if it goes wrong — survive that change.

This page is the map. The [posts below](#reading-guide) are the territory: two years of building agents that run in production and arguing, release by release, about what the agentic web actually requires to be safe.

!!! abstract "The thesis in one line"
    An agent that is capable but not **defendable** is a liability on the agentic web. The fix is architectural, not aspirational: **determinism at the core, the model at the edge**, over knowledge the agent can find and trust. The three pillars of this site — [KCP](/topics/knowledge-context-protocol/), [Skill-Driven Development](/topics/skill-driven-development/), and [Defendable Agents](/topics/defendable-agents/) — are the three faces of that one answer.

---

## What breaks when the client is an agent

The web works because humans quietly absorb its gaps. Take the human out and each gap becomes an engineering problem with no owner:

| The human used to… | On the agentic web, you need… |
|---|---|
| Log in, prove who they are | **Agent identity & delegation** — provable, scoped, revocable |
| Remember what happened last time | **Durable memory** — session, semantic, and claim, not one vector store |
| Read the page and judge the source | **Navigable, signed knowledge** — maps, not tables of contents |
| Notice and stop a bad action | **Deterministic governance** — fail-closed at the boundary, in code |
| Coordinate with other people sensibly | **Agent coordination** — that doesn't collapse into a swarm |

The rest of this page walks each of those, with the one post that makes the case best.

---

## Identity — the agentic web has no login page

A login page assumes a human. An agent acting for you needs to prove *whose* agent it is, *what* it is allowed to do, and have that permission be scoped and revocable — none of which a username-and-password flow expresses. This is the front-door problem of the whole agentic web.

- **The problem, stated:** [The Agentic Web Has No Login Page](/blog/2026/07/04/the-agentic-web-has-no-login-page/)
- **How identity meets knowledge:** [The Front Door and the Filing Cabinet: A2A Agent Cards Meet KCP](/blog/2026/03/08/the-front-door-and-the-filing-cabinet-a2a-agent-cards-meet-kcp/)

---

## Memory — agents that don't forget

"Agent memory" is usually collapsed into one question — vector store or not. Production agents actually have three different memory problems, and conflating them is why so many agents feel amnesiac.

- **The three-way split:** [Three Memory Schemes for Agents That Ship](/blog/2026/07/11/three-memory-schemes-for-agents-that-ship/) — session, semantic, and claim memory, each needing a different mechanism.
- **What enterprise-scale memory demands:** isolation, auditability, continuity, self-maintenance — see the [Knowledge Infrastructure](/knowledge-infrastructure/) body of work.

---

## Coordination — resist the swarm

The reflex answer to a hard task is "spin up more agents." It is usually wrong: uncoordinated multi-agent swarms multiply cost and non-determinism faster than they add capability.

- **The argument:** [Against the Swarm](/blog/2026/07/01/against-the-swarm/)
- **The alternative — pipelines, not swarms:** [The CI Pipeline Is the Agent's Nervous System](/blog/2026/07/02/the-ci-pipeline-is-the-agents-nervous-system/) · [The Third Test Harness](/blog/2026/07/02/the-third-test-harness/)

---

## Determinism — capability is not the bottleneck

The agents shipping today are plenty capable. What they lack is a reason to be *trusted* with a real decision. The move that fixes it is to stop letting the model make the binding call mid-flight and instead make the decision a deterministic function, with the model confined to the edge.

- **The manifesto:** [The Vibes-Based Agent Era Deserves to End](/blog/2026/07/05/the-vibes-based-agent-era-deserves-to-end/)
- **Determinism as a service:** [The Borrowed Leash: Determinism as a Service for the Agentic Web](/blog/2026/07/06/the-borrowed-leash-determinism-as-a-service-for-the-agentic-web/)
- **The full architecture:** the [Defendable Agents](/topics/defendable-agents/) field guide.

---

## Knowledge & economics — how agents find, trust, and pay for what they read

An agent is only as good as what it is allowed to read — and on the open web, it also has to know *who to trust* and, increasingly, *how to pay*. That is the job of a knowledge protocol.

- **Find and trust knowledge:** the [Knowledge Context Protocol](/topics/knowledge-context-protocol/) — maps, not tables of contents.
- **Pay across process boundaries:** [Selling News to Robots](/blog/2026/07/05/selling-news-to-robots/)
- **The whole protocol in one journey:** [One Agent's Journey Through the Whole Protocol](/blog/2026/07/04/one-agents-journey-through-the-whole-protocol/)

---

## Governance — make it defendable, not just capable

Everything above converges here. An agent on the agentic web will read regulations, spend budgets, and brief decision-makers; the dominant architecture cannot answer *"why did you do that?"* with anything better than a transcript. Defendability closes that gap by construction.

- **The field guide:** [Defendable Agents](/topics/defendable-agents/) — the argument, the architecture, the governance primitives, worked examples, and SOC 2 / ISO 27001 / GDPR mapping.
- **Worked examples on real domains:** [A Defendable HR Agent on a Regulatory Knowledge Web](/blog/2026/07/08/hiring-by-the-book-a-defendable-hr-agent-on-a-regulatory-knowledge-web/) · [An Enterprise Documentation Estate the Agent Can Defend](/blog/2026/07/10/the-milky-way-an-enterprise-documentation-estate-the-agent-can-defend/) · [A Family Vacation the Agent Can Defend](/blog/2026/07/09/the-summer-plan-a-family-vacation-the-agent-can-defend/)

---

## Reading guide

- **I have five minutes** → [The Vibes-Based Agent Era Deserves to End](/blog/2026/07/05/the-vibes-based-agent-era-deserves-to-end/)
- **I care about identity/trust** → [The Agentic Web Has No Login Page](/blog/2026/07/04/the-agentic-web-has-no-login-page/)
- **I'm building multi-agent systems** → [Against the Swarm](/blog/2026/07/01/against-the-swarm/)
- **I need this to pass an audit** → the [Defendable Agents](/topics/defendable-agents/) field guide
- **I want the knowledge layer** → [Knowledge Context Protocol](/topics/knowledge-context-protocol/)

---

## Links

- **All agent posts:** [AI Agents & the Agentic Web category](/blog/category/ai-agents--the-agentic-web/)
- **The knowledge layer:** [KCP](/topics/knowledge-context-protocol/) · **The method:** [Skill-Driven Development](/topics/skill-driven-development/) · **The governance:** [Defendable Agents](/topics/defendable-agents/)
- **New here?** [Start here](/start-here/) · **Unsure of a term?** [Glossary](/glossary/)

*The agentic web is being built right now, mostly without the governance it needs. The [blog](/blog/) tracks the argument as it develops; this page is the map.*
