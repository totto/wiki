---
title: "Knowledge Context Protocol (KCP)"
description: "The Knowledge Context Protocol (KCP) is an open standard that makes knowledge navigable and trustworthy for AI agents — beyond llms.txt. Topology, intent, freshness, trust, identity, and federation, as passive data an agent can traverse without loading everything at once."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Knowledge Context Protocol (KCP)

**The Knowledge Context Protocol (KCP) is an open standard that makes a body of knowledge navigable and trustworthy for AI agents.** It is a YAML file format — passive data, not executable config — that describes the knowledge units in a project: their topology (`depends_on`, `supersedes`), their intent (what question each unit answers), their freshness (`validated` dates), their audience, and the trust evidence behind them. An agent can traverse a KCP manifest to find exactly what it needs without loading everything into its context window first.

If [Model Context Protocol (MCP)](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/) is how an agent *calls tools*, KCP is how an agent *finds and trusts knowledge*. The two compose: KCP provides structure, MCP provides retrieval.

I have been designing KCP in the open since January 2026. This page is the map; the [posts below](#reading-guide) are the territory.

!!! abstract "At a glance"
    **v0.24** · twenty-four versions in six months (v0.1 shipped January 10, 2026) · six layers — discovery, meaning, trust, time, identity, federation · reference agent shipping on npm · published under [Cantara](https://github.com/Cantara/knowledge-context-protocol) and submitted to the [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) (Linux Foundation).

---

## Why not just llms.txt?

`llms.txt` gives an agent a table of contents — a flat list of files. That is a real improvement over nothing, but a table of contents cannot express **topology** (what depends on what), **freshness** (is this still true?), **intent** (what question does this answer?), **audience** (who is this for?), or **trust** (who signed it, and can I verify that?). Agents need *maps, not tables of contents*.

KCP is that map. It started as a fix for a specific, embarrassing failure — a 33-tool-call bug where an agent kept rediscovering the same context — and grew, one falsifiable release at a time, into a full protocol for the agentic web.

- **Start here:** [Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](/blog/2026/02/25/beyond-llmstxt-ai-agents-need-maps-not-tables-of-contents/)
- **The origin story:** [Down the Rabbit Hole: How a 33-Tool-Call Bug Became a Knowledge Standard](/blog/2026/06/12/down-the-rabbit-hole-how-a-33-tool-call-bug-became-a-knowledge-standard/)
- **KCP and MCP together:** [One Protocol for Structure, One for Retrieval](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/)

---

## Does it actually work?

KCP is an engineering claim, so it ships with numbers. Manifests measurably cut how much an agent has to read and how often it has to guess.

| Evidence | Result |
|---|---|
| [KCP on Two Repos, Two Days](/blog/2026/03/01/kcp-on-two-repos-two-days-what-the-numbers-actually-show/) | 119 → 31 tool calls on application code; 53 → 25 on documentation. A **53–74% reduction** in agent work. |
| [KCP on Three Agent Frameworks](/blog/2026/03/01/kcp-on-three-agent-frameworks-same-pattern-bigger-numbers/) | Same pattern holds across Claude Code, CrewAI, and others — the gain is in the data, not the harness. |
| [We Cancelled a 45-Minute Architecture Review](/blog/2026/04/15/we-cancelled-a-45-minute-architecture-review-a-kcp-query-answered-it-in-12-seconds/) | "What else breaks if we change this API contract?" — a meeting, replaced by a 1.2-second query. |

---

## The protocol, layer by layer

Every layer has one job. Read the tour, or the release that built each one.

- **Discovery** — an agent starts from a domain and finds the manifest: [Pre-Invocation Discovery (v0.10)](/blog/2026/03/13/kcp-v010-pre-invocation-discovery/)
- **Meaning & query** — a standard vocabulary for asking: [Every Agent That Queries a Manifest Reinvents Filtering](/blog/2026/03/25/every-agent-that-queries-a-knowledge-manifest-reinvents-filtering/)
- **Trust** — self-describing, verifiable knowledge: [Beyond RAG: Trustworthy, Self-Describing Knowledge (v0.16–0.17)](/blog/2026/06/12/beyond-rag-how-kcp-016--017-give-agents-trustworthy-self-describing-knowledge/) · [Unit Integrity & Origin Evidence (v0.18)](/blog/2026/06/12/2026-06-12-kcp-018-unit-integrity/)
- **Time** — stale knowledge is worse than none: [Closing the Temporal Gap (v0.19–0.20)](/blog/2026/06/12/stale-knowledge-is-worse-than-no-knowledge-kcp-v019-and-v020-close-the-temporal-gap/)
- **Identity & federation** — the enterprise front door: [One Agent's Journey Through the Whole Protocol (v0.24)](/blog/2026/07/04/one-agents-journey-through-the-whole-protocol/) · [The Agentic Web Has No Login Page](/blog/2026/07/04/the-agentic-web-has-no-login-page/)
- **Economics** — paying for knowledge across process boundaries: [Selling News to Robots](/blog/2026/07/05/selling-news-to-robots/)

**Why passive data matters:** a manifest an agent *reads* cannot inject instructions the way config an agent *executes* can. That single design decision is what makes KCP defensible — see [Why KCP Is Passive Data, Not Executable Config](/blog/2026/05/08/why-kcp-is-passive-data-not-executable-config--and-why-that-matters-now/).

---

## The tooling

KCP is a spec, but it ships with working implementations you can install today.

- **kcp-agent** — the reference agent. Determinism at the core, the model at the edge: [The Vibes-Based Agent Era Deserves to End](/blog/2026/07/05/the-vibes-based-agent-era-deserves-to-end/) · [The Borrowed Leash: Determinism as a Service](/blog/2026/07/06/the-borrowed-leash-determinism-as-a-service-for-the-agentic-web/)
- **kcp-commands** — a Claude Code hook that saves ~33% of the context window: [kcp-commands](/blog/2026/03/02/kcp-commands/)
- **kcp-memory** — episodic memory for Claude Code: [Give Claude Code a Memory](/blog/2026/03/03/kcp-memory-give-claude-code-a-memory/)
- **kcp-dashboard** — observability for the ecosystem: [kcp-dashboard](/blog/2026/03/28/kcp-dashboard-observability-for-the-kcp-ecosystem/)
- **Editor & enterprise reach:** [GitHub Copilot Gets KCP](/blog/2026/03/06/kcp-mcp-v0100-github-copilot-gets-kcp--including-mcp-locked-enterprises/) · [KCP Comes to OpenCode](/blog/2026/03/03/kcp-comes-to-opencode-the-first-ai-coding-tool-plugin/)
- **The whole picture:** [The KCP Ecosystem: Five Tools](/blog/2026/03/31/kcp-ecosystem-five-tools-persistent-intelligence/)

---

## Governance & compliance

Because KCP carries trust and provenance, it turns regulation into something an agent can actually read.

- [From Policy to Practice: Machine-Readable Regulations for AI Agents](/blog/2026/05/30/from-policy-to-practice-how-kcp-makes-regulations-machine-readable-for-ai-agents/)
- [From Capable to Trustworthy: How KCP Evolved from Discovery to Governance](/blog/2026/03/20/from-capable-to-trustworthy-how-kcp-evolved-from-discovery-to-governance/)
- [The Front Door and the Filing Cabinet: A2A Agent Cards Meet KCP](/blog/2026/03/08/the-front-door-and-the-filing-cabinet-a2a-agent-cards-meet-kcp/)

---

## Reading guide

- **I have five minutes** → [Beyond llms.txt](/blog/2026/02/25/beyond-llmstxt-ai-agents-need-maps-not-tables-of-contents/)
- **I want the numbers** → [KCP on Two Repos, Two Days](/blog/2026/03/01/kcp-on-two-repos-two-days-what-the-numbers-actually-show/)
- **I want the full protocol** → [One Agent's Journey Through the Whole Protocol](/blog/2026/07/04/one-agents-journey-through-the-whole-protocol/)
- **I want to build on it** → the [spec and RFCs on GitHub](https://github.com/Cantara/knowledge-context-protocol)
- **I want the six-month retrospective** → [Six Months Down the Rabbit Hole](/blog/2026/07/15/six-months-down-the-rabbit-hole/)

---

## Links

- **Specification & RFCs:** [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)
- **All KCP posts:** [Knowledge Context Protocol category](/blog/category/knowledge-context-protocol/)
- **The wider body of work:** [Knowledge Infrastructure](../knowledge-infrastructure/index.md)

*KCP is developed in the open and still evolving. The [blog](/blog/) has the latest releases; this page has the map.*
