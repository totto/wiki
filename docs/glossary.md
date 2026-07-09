---
title: "Glossary"
description: "Plain-language definitions of the terms used across this site — the agentic web, KCP, MCP, A2A, Skill-Driven Development, defendable agents, deterministic planners, temporal pinning, drift, fail-closed policy, and the kcp-* tools. One crisp definition each, linked to where it's explained in full."
image: assets/images/agentic-web-slide-02.webp
---

# Glossary

The work on this site leans on a small, precise vocabulary — and the arguments only hold if the words mean something exact. Here is each term in one or two sentences, linked to where it is explained in full. New here? The [Start Here](/start-here/) page routes you by what you're trying to do.

## The ecosystem

**[Knowledge Context Protocol (KCP)](/topics/knowledge-context-protocol/).** An open standard — a YAML file format — that makes a body of knowledge *navigable* and *trustworthy* for AI agents: topology, intent, freshness, audience, and trust as passive data an agent can traverse without loading everything at once. KCP is to knowledge what MCP is to tools.

**Model Context Protocol (MCP).** The open standard for how an agent *calls tools*. KCP and MCP compose: [MCP provides retrieval, KCP provides structure](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/).

**A2A (Agent-to-Agent).** Protocols and conventions for agents discovering and delegating to one another — e.g. agent cards. How A2A identity meets KCP knowledge is covered in [The Front Door and the Filing Cabinet](/blog/2026/03/08/the-front-door-and-the-filing-cabinet-a2a-agent-cards-meet-kcp/).

**[Synthesis](/topics/synthesis/).** Local-first knowledge infrastructure for AI-augmented development: it indexes a workspace (code, docs, PDFs, media) into a multi-layer knowledge graph and exposes it through a CLI, an MCP server, and an LSP server.

**ExoCortex.** The broader personal-knowledge-infrastructure pattern — an external, queryable memory that stops agents (and people) forgetting. See the [Knowledge Infrastructure](/knowledge-infrastructure/) body of work.

**[Skill-Driven Development (SDD)](/topics/skill-driven-development/).** A method for building software with AI where reusable, encoded *skills* — not one-off prompts — accumulate into compounding capability. The organisational counterpart to defendable agents.

**Whydah.** A production, open-source Single Sign-On / Identity & Access Management platform (Cantara), deployed across Norwegian enterprises. See [Open Source](/open-source/).

**The `kcp-*` tools.** The reference implementations of KCP: **kcp-agent** (the deterministic, fail-closed navigation planner), **kcp-harness** (the knowledge-governance proxy), **kcp-commands** (a Claude Code hook that saves ~33% of the context window), **kcp-memory** (episodic memory for Claude Code), and **kcp-dashboard** (observability). All on the [Open Source](/open-source/) page.

## Agentic-web concepts

**[The agentic web](/topics/agentic-web/).** The internet re-pointed at software agents that read, spend, and act on someone's behalf, rather than at humans clicking links — and the engineering problems that appear once no human is quietly absorbing the gaps.

**Agent identity & delegation.** The provable, scoped, revocable answer to *whose* agent this is and *what* it may do — the front-door problem a login page cannot express. See [The Agentic Web Has No Login Page](/blog/2026/07/04/the-agentic-web-has-no-login-page/).

**Session / semantic / claim memory.** The three distinct memory problems production agents actually have, each needing a different mechanism — not one vector store. See [Three Memory Schemes for Agents That Ship](/blog/2026/07/11/three-memory-schemes-for-agents-that-ship/).

**Swarm.** An uncoordinated multi-agent pile-up that multiplies cost and non-determinism faster than capability. The argument against it — and for pipelines instead — is [Against the Swarm](/blog/2026/07/01/against-the-swarm/).

**llms.txt.** A proposed flat "table of contents" file for AI agents. A real improvement over nothing, but it cannot express topology, freshness, intent, audience, or trust — which is [why agents need maps, not tables of contents](/blog/2026/02/25/beyond-llmstxt-ai-agents-need-maps-not-tables-of-contents/).

**RAG (Retrieval-Augmented Generation).** Retrieving text chunks to condition a model's output. KCP's trust and provenance layers are a response to RAG's blind spot — knowledge that cannot describe or vouch for itself.

## Defendable-agent vocabulary

**[Defendable agent](/topics/defendable-agents/).** An agent whose every consequential decision can be reconstructed, explained, and defended after the fact — declared in advance, reproducible, and evidenced. Defendability is a property of the *system around* the model, not of the model.

**[Deterministic planner](/topics/defendable-agents/architecture/deterministic-planner/).** The part of the stack that decides *what* to do using pure functions — same inputs, same outputs, no sampling — so the binding decision is reproducible rather than improvised.

**[Model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/).** The design principle of confining the language model to the perimeter (extracting signals, drafting narrative) while the deterministic core makes the binding decisions. Determinism guarantees *process*, not *correctness*.

**[Governance harness](/topics/defendable-agents/architecture/governance-harness/).** The runtime wrapper every governed operation passes through, where policy stops being a document and becomes an enforced boundary — fail-closed, audit-all, budget and unit ceilings. A **meta-harness** (e.g. Databricks' Omnigent) governs an agent's *actions*; a knowledge harness like kcp-harness governs what it *knows* — see [Two Halves of the Governance Problem](/blog/2026/07/08/two-halves-of-the-governance-problem/).

**[Decision trace](/topics/defendable-agents/primitives/decision-traces/).** The full input-and-output record of a single decision — every variable and score, the composite, the outcome — that turns a number into an argument you can inspect line by line.

**[Append-only audit trail](/topics/defendable-agents/primitives/audit-trail/).** A JSONL log, one event per line, `fsync`-flushed and never rewritten: you can add to history but never quietly revise it.

**[Temporal pin](/topics/defendable-agents/primitives/temporal-pinning/).** A snapshot taken at decision time — `{scoredAt, dataAsOf, signalDates, modelVersion, modelHash}` — so a decision can be judged against the world as it actually was, not as it is now.

**[Drift](/topics/defendable-agents/primitives/drift-detection/).** The gap between a temporal pin and the present: data drift, model drift, or temporal (age) drift. Detecting staleness — it does not refresh the data for you.

**[Fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/).** When a required check can't be satisfied, the operation *stops* rather than proceeding on a guess. The default is deny — the inverse of bolt-on guardrails.

**[Budget ceilings](/topics/defendable-agents/primitives/budget-and-bounding/).** A hard cap on how much work a session may do, checked *before* each operation is recorded, so the maximum blast radius is a number you can state in advance.

**[Tenant isolation](/topics/defendable-agents/primitives/multi-tenancy/).** Confidential per-tenant state kept in separate directories the harness enforces — a boundary you can `ls`, not a promise in a policy note.

**[Attestation / signing](/topics/defendable-agents/primitives/trust-and-attestation/).** The mechanism (here, ed25519 signatures) by which a party vouches for an artifact so a downstream consumer can verify it is authentic and unaltered — what lets an evidence package travel outside your walls and still be trusted.

**Provenance.** The declared, verifiable origin of a claim — which signed, dated source unit it came from — so an answer can point back to *where it came from* and *whether it's still in force*.

**Skip-reason.** The recorded *why* behind an operation the planner declined to run, making inaction as auditable as action.

---

*Missing a term? The [blog](/blog/) is where each of these was worked out in the open. For the compliance-specific vocabulary in depth, the [Defendable Agents field guide](/topics/defendable-agents/) has its own [glossary](/topics/defendable-agents/orientation/glossary/).*
