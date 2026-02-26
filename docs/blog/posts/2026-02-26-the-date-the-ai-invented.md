---
date: 2026-02-26T12:00:00
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
  - Benchmarks
tags:
  - kcp
  - mcp
  - synthesis
  - agents
  - hallucination
  - benchmark
  - context
  - knowledge
authors:
  - totto
  - claude
---

# The Date the AI Invented

The agent answered the ROI metrics question with zero tool calls. It reported the indexing speed, the search latency, the file count, the retrieval time improvement, the test count. All correct. Every number accurate.

Then it said the metrics were validated on February 19, 2026.

The actual date was February 17.

<!-- more -->

No such date appeared anywhere in the context. The agent did not retrieve it from a wrong file. It did not misread a number. It confabulated a plausible-sounding date by interpolating from surrounding temporal references — benchmark sessions, PR merge dates, version timestamps — and produced something that sounded exactly right.

That one wrong date is the most important finding from our Phase 5 benchmark. Not because of the date itself, but because of what it reveals about how we load knowledge into AI agents, and what we need to do differently.

## What the benchmark was testing

We ran 9 codebase navigation tasks across 6 conditions on the [Synthesis](https://github.com/exoreaction/Synthesis) codebase. The conditions varied how the agent received knowledge: no Synthesis integration (Baseline), pre-loaded context documents (Knowledge), CLI documentation (CLI), MCP tools (MCP), MCP with a system prompt hint (MCP + Hint), and MCP with rewritten tool descriptions (MCP + Descriptions).

The E1 task asked: *List Synthesis's validated performance metrics — indexing throughput, search latency, validation date.*

| Condition | Tool calls | Correctness | Date |
|-----------|:----------:|:-----------:|:----:|
| Knowledge | 0 | 10/12 | Feb 19 ❌ |
| MCP | 0 | 10/12 | Feb 19 ❌ |
| MCP + Hint | 1 | 12/12 | Feb 17 ✓ |
| MCP + Descriptions | 4 | 12/12 | Feb 17 ✓ |
| Baseline | 6 | — | — |

The Knowledge and MCP conditions both answered from pre-loaded context alone. Same answer, same error. The MCP + Hint condition used one Read call to verify, got the correct date, and stopped.

The difference: the one-line hint told the agent to verify when a precise date mattered. One call, correct. Zero calls, wrong.

## Why the hallucination happened

CLAUDE.md — our pre-loaded context document — contains the validated metrics embedded in narrative prose. Somewhere in that prose it mentioned "Validated (Feb 14, 2026)" in one section, "Phase 5 benchmark session" in another, "v1.3.0-SNAPSHOT, PR #18 merged Feb 16, 2026" in a third.

The agent, processing this narrative, synthesised a date. February 19 appeared nowhere. But it was plausible: later than Feb 16 (the PR merge), earlier than the current date, consistent with the surrounding temporal context. The model generated a plausible continuation rather than extracting a precise fact.

This is not a retrieval error. The model did not find the wrong document. It did not confuse two dates that both appeared in the text. It **invented** a date that fit the narrative pattern — and it did so with complete confidence.

This failure mode has a name: confabulation of temporal references from narrative context. LLMs process prose, and prose temporal references are inherently ambiguous. "The metrics were validated in mid-February" is a human sentence. A machine needs an ISO date.

## The structural problem

CLAUDE.md has no machine-readable freshness signal. Dates appear as natural language embedded in prose alongside other dates. When an agent needs a specific date, it must parse temporal references from surrounding narrative and disambiguate between them. LLMs do this probabilistically — and sometimes incorrectly.

This is not a problem with CLAUDE.md specifically. It is a problem with any knowledge format that embeds facts in prose without structured metadata. The format that works for human reading creates ambiguity for machine extraction.

The fix is not a better model. The same failure will occur on any capable model that processes unstructured text. The fix is a better input format.

## What KCP's `validated` field provides

The [Knowledge Context Protocol](https://github.com/cantara/knowledge-context-protocol) represents the same information differently:

```yaml
units:
  - id: synthesis-metrics
    path: docs/METRICS.md
    intent: "What are Synthesis's validated performance metrics?"
    scope: global
    audience: [agent, developer, architect]
    validated: 2026-02-17
    triggers: [performance, metrics, ROI, indexing-speed, search-latency]
```

The `validated` field is an ISO 8601 date — a machine-readable scalar, not a phrase embedded in prose. An agent processing this manifest reads a field value. There is no interpolation, no disambiguation, no ambiguity about which date refers to which fact.

`validated: 2026-02-17` would have provided exactly the date the agent hallucinated. The E1 failure is a representation failure, not a model failure. And representation failures have representation fixes.

## The composability model

The benchmark data makes a stronger argument than a single task can carry. Looking across all 9 tasks and 6 conditions, a pattern emerges: pre-loaded context and runtime tools are not competing strategies. They solve different problems.

**Where pre-loaded context wins:**

| Task | Baseline | Knowledge | MCP | Method |
|------|:--------:|:---------:|:---:|--------|
| E1: ROI metrics | 6 | 0 | 0 | Both answered from CLAUDE.md |
| P4-B1: Flyway migrations | 8 | 1 | 1 | Convention named explicitly in context |

When the answer is stable, explicitly documented, and does not require temporal precision, pre-loaded context eliminates all tool overhead. The agent answers in zero calls because the knowledge is already present.

**Where runtime tools win:**

| Task | Baseline | MCP | Delta |
|------|:--------:|:---:|:-----:|
| P5-R2: Dependency graph | 32 | 10 | -69% |
| P5-R1: SearchIndex callers | 5 | 2 | -60% |
| B3: Cross-repo dependencies | 9 | 3 | -67% |

No static document can enumerate every caller of every method. No snapshot of a dependency graph stays accurate for more than a commit. These are inherently computational queries — answers that must be derived from the current state of the codebase, not retrieved from documentation written last week.

The pattern is clean:

- **Pre-loaded context wins for:** stable facts, architectural decisions, naming conventions, product metrics. Things that change infrequently and are explicitly documented.
- **Runtime tools win for:** computed queries, discovery tasks, currency-critical queries. Things that depend on the current state of the code.

## The three-layer architecture

The benchmark points toward a specific architecture for agent knowledge that addresses each failure mode observed across all six conditions.

**Layer 1: KCP manifest (pre-session)**

Before the agent session starts, load `knowledge.yaml`. The manifest describes what knowledge units exist, which are relevant to this session (via `triggers` and `audience`), what order to load them in (`depends_on`), and — critically — how fresh each one is (`validated`).

The agent loads relevant units into context. For stable factual queries, the answer is now present. For the E1 date specifically: the agent reads `validated: 2026-02-17` as a structured field, not inferred from surrounding narrative.

**Layer 2: Decision heuristic (session configuration)**

A single sentence in the system prompt — equivalent to the Condition 5 hint that produced our best result (-40% vs baseline):

> If the answer is in pre-loaded context and the `validated` date is within 7 days, answer directly. If the answer requires computation or the `validated` date exceeds the freshness threshold, use MCP tools.

The Condition 5 result (5.3 average tool calls) demonstrates that one sentence of decision guidance outperforms every other intervention we tested, including rewriting all 41 tool descriptions. The heuristic tells the agent when to trust its context and when to go looking.

**Layer 3: MCP tools (runtime)**

For discovery tasks, computed queries, and verification when pre-loaded context is stale, MCP tools handle what no static manifest can answer.

Each layer addresses the failure modes the others cannot:

| Failure mode | Observed | Fixed by |
|-------------|---------|----------|
| Temporal hallucination (E1 date) | Knowledge + MCP conditions | KCP `validated` field |
| Over-invocation (18 calls on P4-B1) | MCP + Descriptions | Decision heuristic |
| Can't answer computed queries | Knowledge condition | MCP runtime tools |
| Agent ignores MCP tools | MCP condition, 5/9 tasks | Decision heuristic |
| Stale context trusted | E1, all pre-loaded conditions | KCP freshness threshold |

No single layer addresses all five. The composability model does.

## What this changes about how we build

The E1 finding redirects attention from model capability to knowledge architecture.

The hallucination was not caused by a model limitation. It was caused by a representation limitation — dates embedded in narrative prose, with no structured field an agent can parse deterministically. A better model would still confabulate: all capable LLMs process narrative text and generate plausible continuations.

The right response is not to prompt-engineer around the hallucination, or to require the agent to always verify dates, or to expand the context window. The right response is a format where dates are fields, not phrases.

KCP's `validated` field is one expression of that principle. Any structured metadata format that separates machine-readable fact from human-readable prose would address the same failure mode. The specific format matters less than the discipline: facts the agent needs to extract precisely should be in parseable fields, not embedded in narrative.

The broader implication: when you design knowledge for AI agents, the question is not "is this information correct?" It is "can an agent extract this information correctly from the format I chose?" Those are different questions with different answers.

## Practical guidance

For teams deploying agents against real knowledge bases:

**Use pre-loaded context for stable knowledge.** Metrics, architectural decisions, configuration conventions, API contracts that change quarterly. This eliminates tool overhead entirely for the most common factual queries.

**Add structured metadata for time-sensitive facts.** Any fact where the "when" matters — validation dates, version releases, deployment timestamps — should be in a parseable field, not a prose sentence.

**Use MCP for computed and currency-critical queries.** Dependency graphs, caller analysis, change tracking, anything that depends on the current state of the code. These cannot be pre-loaded; they must be computed from live data.

**Add a decision heuristic to the system prompt.** One sentence mapping task categories to knowledge sources. This is the highest-leverage single intervention in our benchmark.

**Generate `knowledge.yaml` from your existing index.** `synthesis export --format kcp` is on the roadmap. The goal is that KCP becomes a generated artifact, not a hand-maintained file — the same way build metadata is generated, not written.

---

The benchmark data and full results are in the [Synthesis repository](https://github.com/exoreaction/Synthesis) under `/benchmark/`. The KCP draft specification is at [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol).

*Previous in this series: [Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](../2026-02-25-beyond-llms-txt-knowledge-context-protocol/) — introducing the KCP protocol concept. This post provides the benchmark evidence.*
