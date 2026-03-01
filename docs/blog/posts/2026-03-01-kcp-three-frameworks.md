---
date: 2026-03-01
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - benchmark
  - knowledge-infrastructure
  - standards
authors:
  - totto
  - claude
---

# KCP on Three Agent Frameworks: Same Pattern, Bigger Numbers

Today we applied KCP to three of the most widely-used AI agent frameworks — smolagents (HuggingFace, 25K stars), AutoGen (Microsoft, 55K stars), and CrewAI (44K stars). All three got the same treatment: a `knowledge.yaml` manifest, pre-built TL;DR summary files for the highest-traffic sections, and a before/after benchmark using the same model and methodology.

The results: 73%, 80%, and 76% reductions in agent tool calls. Open PRs are live on all three repositories.

<!-- more -->

## Why frameworks specifically

The [previous post in this series](./2026-03-01-kcp-two-repos-two-days.md) benchmarked two smaller repos — one application codebase (74%) and one documentation repository (53%). The documentation repo produced a lower result, which made sense: a flat 13-chapter guide is navigable without a manifest if the README is well-organised.

AI agent frameworks are a harder problem. They have multiple APIs, dozens of notebooks and concept guides, integration sections, design pattern galleries, and reference material spread across different directories. A baseline agent exploring one of these repos to answer "how do I add memory to my agent?" has no structural signal about which of several plausible directories to look in first.

That is exactly what KCP is designed for.

---

## Repo 1: smolagents (HuggingFace)

**15 units. 8 queries. 73% reduction.**

| Query | Baseline | KCP | Saved |
|-------|----------|-----|-------|
| CodeAgent vs ToolCallingAgent? | 22 | 2 | 20 |
| How do I create a custom tool? | 7 | 3 | 4 |
| Sandboxed code execution? | 24 | 8 | 16 |
| Multi-agent system with manager + subagents? | 11 | 6 | 5 |
| Which LLM models are supported? | 19 | 2 | 17 |
| How do I implement RAG? | 6 | 6 | 0 |
| How do I debug or inspect an agent run? | 22 | 3 | 19 |
| Best practices for reliable production agents? | 10 | 3 | 7 |
| **Total** | **121** | **33** | **88** |

smolagents has a clear architecture split — CodeAgent (writes Python) vs ToolCallingAgent (writes JSON) — that every new user needs to understand. The baseline agent answered this in 22 tool calls: it read the README, explored the full docs tree, read several source files, and eventually found `guided_tour.md`. With KCP, the agent matched the `getting-started-tldr` unit in one read and found the answer there: 2 calls.

The RAG query (6→6) was the only flat result. The answer genuinely requires reading an example file alongside a conceptual guide — KCP correctly routed to the right section, but the depth of reading was the same either way. This is the expected ceiling: KCP eliminates exploration overhead, not reading time.

The sandboxed execution query stayed relatively expensive at 8 KCP calls because the answer spans two files — the guided tour covers the default local executor, and `secure_code_execution.md` covers the sandbox options. The agent read both. That is correct behaviour, not a failure.

---

## Repo 2: AutoGen (Microsoft)

**18 units. 8 queries. 80% reduction.**

| Query | Baseline | KCP | Saved |
|-------|----------|-----|-------|
| AutoGen Core vs AgentChat difference? | 7 | 2 | 5 |
| Build first multi-agent chat? | 9 | 2 | 7 |
| Add tools to an agent? | 23 | 2 | 21 |
| What design patterns are available? | 32 | 4 | 28 |
| Implement group chat? | 12 | 3 | 9 |
| Add memory to an agent? | 24 | 2 | 22 |
| LLM providers and model clients? | 36 | 16 | 20 |
| Human-in-the-loop approval? | 25 | 2 | 23 |
| **Total** | **168** | **33** | **135** |

AutoGen has two distinct Python APIs — Core (low-level, actor model, pub/sub) and AgentChat (high-level, rapid prototyping) — plus design patterns, component guides, and a growing extensions ecosystem. The navigation space is wide.

The design patterns query shows this most clearly: 32 baseline tool calls. The agent read the README, explored the Python docs structure, read the user guide index, found the core concepts section, read architecture docs, browsed the design patterns directory, and only then read the pattern notebooks one by one. With KCP: read `knowledge.yaml`, match to `design-patterns-tldr`, read the TL;DR. 4 calls — a one-line description of each pattern and pointers to the notebooks that go deeper.

The model clients query had the smallest gain (36→16): the full provider list required reading a large notebook with many sections, and KCP directed the agent correctly but could not compress the content itself. It still saved 20 calls.

80% is the best result across all repositories benchmarked so far.

---

## Repo 3: CrewAI

**16 units. 8 queries. 76% reduction.**

| Query | Baseline | KCP | Saved |
|-------|----------|-----|-------|
| Flows vs Crews — what's the difference? | 14 | 2 | 12 |
| Create first agent and assign a task? | 7 | 3 | 4 |
| Create a custom tool? | 8 | 3 | 5 |
| Add memory to a crew? | 7 | 3 | 4 |
| Which LLM providers are supported? | 17 | 5 | 12 |
| Build a flow that triggers a crew? | 15 | 2 | 13 |
| Hierarchical crew with manager agent? | 22 | 9 | 13 |
| Add knowledge (RAG) to a crew? | **33** | **3** | **30** |
| **Total** | **123** | **30** | **93** |

CrewAI's architecture — Flows (event-driven control) + Crews (agent teams) — is conceptually clean but spread across multiple large concept files. The docs are well-written; the problem is navigation, not content.

The RAG query is the standout: 33 baseline calls, 3 with KCP. The baseline agent traversed the entire docs tree — concepts, guides, enterprise integrations, MCP, observability — before finding `knowledge.mdx`. The KCP agent matched `tools-memory-tldr` via the `rag crew` trigger and found a complete quickstart in ~500 tokens.

The hierarchical crew query had the smallest relative improvement (22→9) because it genuinely requires reading two large reference files — `crews.mdx` and `tasks.mdx` — to understand the manager agent configuration. KCP removed the exploration overhead but could not reduce the inherent reading depth.

---

## Five repos, one pattern

Across all five benchmarks now:

| Repo | Type | Queries | Baseline | KCP | Reduction |
|------|------|---------|----------|-----|-----------|
| Plugin wizard (application code) | app codebase | 10 | 119 | 31 | 74% |
| Infrastructure agents guide | pure documentation | 7 | 53 | 25 | 53% |
| smolagents | Python framework | 8 | 121 | 33 | 73% |
| AutoGen | Python framework | 8 | 168 | 33 | 80% |
| CrewAI | Python framework | 8 | 123 | 30 | 76% |

The documentation repository (53%) is the outlier. It is also the simplest navigation case: 13 chapters with clear titles, well-organised README. A baseline agent with no guidance can narrow to the right chapter in 3–4 reads.

Everything else lands between 73% and 80%. The application codebase, despite being small, has wide answer distribution — a question about "how to add a tool" could live in a guide, a type definition, or the source. The frameworks have that problem at scale.

The pattern is consistent enough to state a hypothesis: **KCP adds more value where the navigation problem is harder.** The improvement is not primarily about how much documentation exists — it is about how unpredictable the answer location is without guidance.

---

## What did not change

The methodology was identical across all five repos: Haiku agents, 7–10 queries per repo, tool counts from the Anthropic API `usage.tool_uses` field. Not self-reported. Not estimated. Every `read_file`, `glob_files`, and `grep_content` call counted.

Baseline agents were given no structural guidance — they explored as any agent would without a manifest. KCP agents were told to read `knowledge.yaml` first and match their query to the trigger fields.

No query was designed to favour KCP. The queries are the questions developers actually ask when they start using these frameworks.

---

## Open PRs

All three implementations are submitted to the upstream repositories:

- **smolagents**: [huggingface/smolagents #2026](https://github.com/huggingface/smolagents/pull/2026)
- **AutoGen**: [microsoft/autogen #7329](https://github.com/microsoft/autogen/pull/7329)
- **CrewAI**: [crewAIInc/crewAI #4658](https://github.com/crewAIInc/crewAI/pull/4658)

Each PR includes the `knowledge.yaml` manifest, TL;DR files, `BENCHMARK.md`, and the benchmark runner script so maintainers can reproduce the numbers.

The benchmark methodology is now documented at [github.com/cantara/knowledge-context-protocol/CONTRIBUTING.md](https://github.com/cantara/knowledge-context-protocol/blob/main/CONTRIBUTING.md) — same model, same tool-counting approach, same system prompts. Anyone applying KCP to a new repo can produce results that are directly comparable to the ones here.

---

*The KCP specification is at [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol). The previous post in this series covered the first two repos: [KCP on Two Repos, Two Days](./2026-03-01-kcp-two-repos-two-days.md).*
