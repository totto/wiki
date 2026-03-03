---
date: 2026-02-25
categories:
  - AI-Augmented Development
  - Synthesis
tags:
  - ai
  - agents
  - synthesis
  - knowledge-infrastructure
  - mcp
  - local-first
  - architecture
authors:
  - totto
  - claude
---

# AI Agents Without Knowledge Infrastructure Are Interns With Amnesia

I have been watching the AI agent space closely for the past year. The frameworks are impressive. The orchestration tools are clever. The models are increasingly capable. And yet, most agent deployments I see make the same quiet mistake: they treat the knowledge problem as solved.

It is not solved. It is barely addressed. And until it is, all the reasoning capability in the world will not make your agents reliably useful.

<!-- more -->

![The AI paradox: 10-50x output increase vs 1.5-2x shipping speed improvement](/assets/images/blog/synthesis-ai-agents-paradox-bottleneck.png)

## The problem nobody talks about

When you deploy an AI agent in a real enterprise environment, the agent needs to know things. Not generic things — specific things. Which module owns authentication. What the dependency graph looks like across your forty repositories. What changed in last Tuesday's deployment. Why the data model has that unusual column.

The standard answer to this is RAG: embed your documents, put them in a vector database, retrieve the most "similar" chunks at query time. I have built RAG systems. They work for certain use cases. But for structured technical knowledge — code, dependencies, cross-repo relationships, build history — RAG is the wrong abstraction.

RAG finds text that *sounds like* your query. What you need is a system that finds code that *is structurally related* to your query. Those are fundamentally different problems.

The deeper issue is this: an agent that cannot reliably access the knowledge it needs will fill the gap with confident hallucination. It will tell you the module structure from six months ago. It will cite a dependency version that has since been patched. It will miss the three other places where the pattern you are changing also appears. The problem is not that agents lie — it is that without current, structured knowledge, they have nothing else to work with.

## What Synthesis does differently

We built [Synthesis](/blog/2026/02/25/ai-agents-without-knowledge-infrastructure-are-interns-with-amnesia/) to solve a specific problem: our AI-assisted development was generating output at ten to fifty times the previous rate, but our shipping speed only improved by a factor of two. The bottleneck was not code generation — it was comprehension. Developers were spending forty percent of their time searching for context across thousands of files, understanding how changes would propagate, figuring out what already existed before writing something new.

Synthesis indexes the entire workspace — code, documentation, configuration files, SQL, PDFs, shell scripts — and makes it searchable in under a second. But more importantly, it builds a dependency graph. It tracks which module imports which, what breaks when something changes, how files relate across repository boundaries. This is the structural knowledge that a developer holds in their head after working on a system for months. Synthesis makes it queryable by anyone — or anything — from day one.

![Synthesis as the context engine for high-performance AI agents](/assets/images/blog/synthesis-context-engine-ai-agents.png)

The numbers we have validated: 8,934 files indexed across three workspaces, sub-second retrieval (0.4 seconds measured), 92-95% reduction in context-gathering time, 2.7% storage overhead. The index for 434 MB of content takes 11.6 MB.

For human developers, this was already transformative. For AI agents, it changes the architecture of what is possible.

## The context window problem, properly framed

An AI agent faces a constraint that does not go away: the context window is finite. Claude Opus 4 has a 200K token window. That sounds large until you consider that even a single large Java project can exceed it by an order of magnitude, and most enterprise systems span dozens of repositories.

The naive response is to stuff as much as possible into the context and hope. The sophisticated response is to treat context as a query result, not an upfront payload.

With Synthesis exposed as an MCP server, an agent does not receive a dump of everything that might be relevant. It queries exactly what it needs, when it needs it, in under a second. The context stays focused. The cost per query stays low. The scope of what the agent can reason about becomes effectively unlimited — not because the context window grew, but because the agent can navigate knowledge the same way a librarian navigates a library: by querying, not by memorising.

This is the shift from *fat context* to *thin context plus rich retrieval*. It is the same shift that happened in database design decades ago, from loading entire tables into memory to indexed queries. Synthesis is, in effect, a query engine for the knowledge an agent needs.

![Synthesis MCP Server: connecting agents to structured knowledge](/assets/images/blog/synthesis-mcp-server-overview.png)

## One index, multiple agents

We are currently running two agents in production — one focused on personal assistant tasks and morning briefings, another on DevOps and security monitoring. Both connect to the same Synthesis index via MCP. They share a knowledge substrate but have entirely different system prompts, different skill files, different personas.

This is a pattern worth naming: **shared knowledge, specialised lens**.

Without a shared knowledge layer, deploying multiple agents means maintaining multiple knowledge bases — one per agent. That cost scales linearly with agent count. With Synthesis, the indexing happens once. Adding a new agent means writing a new system prompt and pointing it at the existing MCP endpoint. The marginal cost of a new agent's knowledge is zero.

There is also a subtler benefit. When the DevOps agent patches a dependency and updates a file, the PA agent's next query reflects that change automatically. The agents do not need to communicate with each other. The shared index is the communication channel. They stay consistent without coordination overhead.

## The knowledge priming problem

A contact raised an interesting point recently: AI agents need "knowledge priming" — carefully crafted instruction files that give the agent enough context to be useful. This is true, but it reveals a deeper problem. If you solve the knowledge problem by writing everything into the system prompt, you are creating a maintenance burden that scales with the number of agents and the rate of change in your codebase. Those instruction files become stale. They become incomplete. And they hit context limits long before they cover everything the agent needs.

Synthesis changes what priming needs to cover. The system prompt handles identity, behaviour, and goals — things that are stable and small. Synthesis handles facts, relationships, and current state — things that are large, dynamic, and queryable. This is a clean separation of concerns. The agent knows *how to behave*; Synthesis gives it *something to reason about*.

## Why local-first matters more than it seems

Every cloud-based knowledge solution I have evaluated requires your code to leave your infrastructure. For many organisations — banks, healthcare providers, defence contractors, companies with trade secrets in their codebase — this is not a configuration option. It is a showstopper.

Synthesis processes everything locally. The index lives on your machine or your server. The MCP server runs on your infrastructure. When an agent queries Synthesis, no data leaves your network. This is not a privacy checkbox — it is an architectural constraint that enables deployment in environments where cloud-based alternatives simply cannot go.

![Local-first security architecture: 100% local processing, zero telemetry](/assets/images/blog/synthesis-local-first-security-architecture.png)

The practical consequence: you can give agents access to your most sensitive assets. Proprietary algorithms. Internal security reports. Personnel and skills data. Financial projections. Not because you have accepted a risk — but because the risk was designed away by making the system local in the first place.

## What Synthesis does not solve

Honesty matters more than marketing, so let me be clear about the limits.

Synthesis does not improve the agent's reasoning. Better information does not compensate for a weak model or a poorly written system prompt. Garbage in, garbage out — Synthesis just makes sure what goes in is current and relevant rather than stale and approximate.

Synthesis does not handle real-time events. The index is updated on a schedule, not by a file watcher. There is a freshness gap — minutes to hours depending on your configuration. For most business workflows this is invisible. For real-time incident response, it is not.

Synthesis does not replace semantic similarity search. For unstructured natural language content — documentation written in flowing prose, conversation logs, support tickets — vector search may retrieve relevant material that a keyword-and-structure index would miss. The ideal architecture for a sophisticated agent likely combines both approaches.

And Synthesis does not solve orchestration, memory, or action execution. It is one layer in an agent stack, not the whole stack.

## The layer the ecosystem is missing

The AI agent tooling market has invested heavily in model capability, agent frameworks, and orchestration. The knowledge infrastructure layer — the thing that determines whether agents have access to accurate, current, structured information about the systems they are working with — has been largely neglected.

RAG is not enough. Stuffing context is not enough. Writing elaborate priming documents is not enough and does not scale.

We built Synthesis to solve our own problem. It turned out to solve a broader one. If you are deploying agents against a large codebase, a complex dependency graph, or sensitive enterprise data that cannot leave your network, the knowledge problem is likely your real bottleneck — not the model, not the framework, not the prompt.

Synthesis is the knowledge infrastructure tool described in this series. Sub-second retrieval. Local-first. MCP-native. One index, as many agents as you need.

The agents are only as good as what they know. Give them something to know.
