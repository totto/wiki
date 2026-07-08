---
title: "Synthesis: Knowledge Infrastructure for AI Agents"
description: "Synthesis is a local-first knowledge infrastructure platform that indexes code, documents, PDFs, videos, and skills into multi-layer knowledge graphs, and exposes them to AI agents through CLI, MCP, and LSP. Built to fix the comprehension bottleneck: AI creates faster than humans can navigate."
image: assets/images/synthesis-practitioners-journal/slide-01.webp
---

# Synthesis: Knowledge Infrastructure for AI Agents

**Synthesis is a local-first knowledge infrastructure platform that makes a codebase — and everything around it — navigable by AI agents.** It indexes code, documents, PDFs, and even videos into multi-layer knowledge graphs, tracks how that knowledge changes over time, and exposes all of it through a CLI, an [MCP server](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/), and an LSP. Everything runs on your machine; nothing is sent to a cloud service.

It exists because of a problem I did not anticipate.

---

## The problem Synthesis solves

In January 2026 I built [lib-pcb](/blog/2026/01/15/the-surprisingly-hard-problem-of-semiconductor-part-numbers/) — 197,831 lines of Java in eleven days, with an AI agent writing most of it. The methodology worked. And then I couldn't navigate any of it. Nearly 18,000 files. 691 new files per day. I was spending more time *finding* code than *understanding* it.

That is not a lib-pcb problem. It is the [comprehension bottleneck](/blog/2026/02/05/the-comprehension-bottleneck-why-ai-made-creating-easy-but-understanding-harder/): **AI made creating easy but understanding harder.** Output velocity jumped 10–50×; comprehension did not. Every jump in creation speed eventually produces a navigation crisis — monks didn't need a library catalog until the printing press arrived. I had given myself a personal printing press for code, and I was drowning in the output.

Synthesis started as search and became the missing layer. The full story: [The Tool I Didn't Plan to Build: Synthesis, Ten Weeks Later](/blog/2026/04/05/the-tool-i-didnt-plan-to-build-synthesis-ten-weeks-later/).

!!! abstract "At a glance"
    Local-first · indexes at 200–300 files/second · sub-second search · multi-layer knowledge graphs · **60+** CLI commands · **11** MCP tools · **4,300+** tests · Notion as a first-class workspace source · Java 21 · [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

---

## Agents need three kinds of memory

Most AI agents have exactly one kind of memory — the context window — and forget everything the moment the session ends. Synthesis gives them three:

1. **Working memory** — the context window (the model already has this).
2. **Episodic memory** — what happened in past sessions, indexed and searchable.
3. **Semantic memory** — the workspace knowledge graph: what the code *means* and how it connects.

Read [Working Memory, Episodic Memory, Semantic Memory — Your Agent Has One](/blog/2026/03/03/working-memory-episodic-memory-semantic-memory-your-agent-has-one/), then [Your AI Has One Layer. It Needs Four.](/blog/2026/02/28/your-ai-has-one-layer-it-needs-four/) for the retrieval architecture.

And the uncomfortable follow-up: building the layers is the easy part. Memory that is not maintained becomes memory that lies — [Agent Memory Rots. Here's How We Stopped It.](/blog/2026/04/06/agent-memory-rots-heres-how-we-stopped-it/)

---

## What it found by looking at itself

The most convincing evidence for a knowledge tool is what it surfaces when you point it at real, messy history.

| Post | Finding |
|---|---|
| [What Synthesis Found in 31 Seconds](/blog/2026/02/03/what-synthesis-found-in-31-seconds-an-xxe-vulnerability-in-a-production-java-sso-system/) | An XXE vulnerability in a production Java SSO system — in 31 seconds. |
| [The Synthesis Excavation](/blog/2026/02/25/the-synthesis-excavation-recovering-35-years-of-lost-history/) | Text coverage 99.6%, real asset coverage 15.2%. 4,852 binary files recovered from 3.5 years of lost history in one day. |
| [Zero Links: An Engineering Session](/blog/2026/02/26/zero-links-an-engineering-session-with-claude-code-and-opus/) | 777 directories, zero edges → 11,777 edges, 23 new tests, 4 bugs fixed, one day later. |
| [We Gave the AI Better Documentation. It Got Slower.](/blog/2026/02/26/we-gave-the-ai-better-documentation-it-got-slower/) | CLI docs *increased* tool calls 11%; MCP *cut* them 35%. How agents integrate matters more than how much you document. |
| [The Mirror Test](/blog/2026/02/11/the-mirror-test-how-synthesis-benchmarked-itself-into-something-better/) | Using an AI tool to measure whether an AI tool can be trusted — the dogfooding loop. |

---

## Reading guide

- **The problem** → [The Comprehension Bottleneck](/blog/2026/02/05/the-comprehension-bottleneck-why-ai-made-creating-easy-but-understanding-harder/)
- **The story** → [Synthesis, Ten Weeks Later](/blog/2026/04/05/the-tool-i-didnt-plan-to-build-synthesis-ten-weeks-later/)
- **For Java developers** → [Claude Code + Synthesis: Five Superpowers for Java Developers](/blog/2026/02/21/claude-code--synthesis-five-superpowers-for-java-developers/)
- **At organizational scale** → [When Your Agent Can Finally Read the Room](/blog/2026/04/21/when-your-agent-can-finally-read-the-room/)
- **Connecting an agent to it** → [Giving an AI Agent a Brain: Connecting IronClaw to Synthesis via MCP](/blog/2026/02/24/giving-an-ai-agent-a-brain-connecting-ironclaw-to-synthesis-via-mcp/)

---

## Links

- **Source:** [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis) · [release history](../notes/synthesis-releases.md)
- **All Synthesis posts:** [Knowledge Infrastructure category](/blog/category/knowledge-infrastructure/)
- **The wider body of work:** [Knowledge Infrastructure](../knowledge-infrastructure/index.md) · [Knowledge Context Protocol](knowledge-context-protocol.md)

*Synthesis is under active development. The [blog](/blog/) has the latest; this page has the map.*
