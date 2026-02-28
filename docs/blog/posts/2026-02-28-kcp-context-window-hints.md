---
date: 2026-02-28T13:00:00
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - knowledge-infrastructure
  - standards
  - context-window
authors:
  - totto
  - claude
---

# The Agent Read the Whole Spec. It Didn't Need To.

*Part 6 of the KCP series. Previous: [What Happens When Your Agent Needs Knowledge From Five Teams?](/blog/2026/02/28/what-happens-when-your-agent-needs-knowledge-from-five-teams/)*

<!-- more -->

A 42,000-token specification. An agent with 8,000 tokens of remaining budget. The agent loads
the document. The context overflows. The session fails, truncates, or clears — taking
everything the agent had accumulated with it.

What makes this worse: the knowledge base also contained a 600-token TL;DR that answered
the same question. The agent had no way to know it existed.

RFC-0006 proposes a `hints` block that gives agents the information they need to make
loading decisions *before* fetching content. How large is this unit? Should it be loaded
eagerly or only on demand? Is there a shorter version? If context fills, which units should
be evicted first?

---

## What agents are flying blind on today

KCP manifests tell agents *what* a unit is and *what question it answers*. They do not tell
agents *how expensive it is to load*. An agent navigating a large knowledge base currently
has three bad choices:

- **Load everything** and hope it fits — fails for large corpora
- **Load nothing** and ask the user what to load — defeats the point of a manifest
- **Guess from filenames** — `CHANGELOG.md` is probably large; `README.md` is probably not; `SPEC.md` is anybody's guess

The result is that context overflow is discovered retroactively. The fetch has already
happened. The tokens are already spent.

---

## Two `hints` blocks

RFC-0006 adds a `hints` block at two levels: on individual units, and at the manifest root.

### Unit-level hints

```yaml
units:
  - id: full-specification
    path: SPEC.md
    intent: "What are the normative rules for a knowledge.yaml manifest?"
    scope: global
    audience: [human, agent, developer, architect]
    hints:
      token_estimate: 42000
      token_estimate_method: measured     # measured | estimated
      load_strategy: lazy                 # eager | lazy | never
      priority: supplementary             # critical | supplementary | reference
      density: dense                      # dense | standard | verbose
      summary_available: true
      summary_unit: spec-summary

  - id: spec-summary
    path: SPEC-tldr.md
    intent: "What are the key points of the spec in 500 words?"
    hints:
      token_estimate: 600
      load_strategy: eager
      priority: critical
      summary_of: full-specification
```

The three enum fields do the work.

**`load_strategy`** advises when to load:
- `eager` — load immediately when the manifest is processed. For short, high-signal units: an overview, a schema index, a TL;DR.
- `lazy` — load on demand, when the agent determines the unit is relevant. The default for most content.
- `never` — do not load proactively. Only if explicitly requested. For raw data dumps, full changelogs, large archives where the agent should read the summary instead.

**`priority`** advises what to evict first when context fills:
- `critical` — evict last. Essential facts the agent must retain.
- `supplementary` — standard priority. May be evicted if budget is tight.
- `reference` — evict first. API specs, changelogs, raw data used for spot lookups, not sustained reasoning.

**`density`** advises whether to compress before loading:
- `dense` — nearly every sentence is load-bearing. Compression risks information loss. Load the full text.
- `standard` — normal prose. Some compression acceptable.
- `verbose` — high token count relative to information content. Tutorials, narrative explanations, marketing copy. Summarisation before loading is likely worthwhile.

---

## The summary relationship

The most immediately useful part of RFC-0006 is the summary pairing. When a short summary
of a large unit exists, both sides declare the relationship:

```yaml
  - id: architecture
    path: architecture.md
    intent: "What is the system architecture and how do the components relate?"
    hints:
      token_estimate: 18000
      load_strategy: lazy
      priority: supplementary
      density: dense
      summary_available: true
      summary_unit: architecture-summary    # → points to the short version

  - id: architecture-summary
    path: architecture-tldr.md
    intent: "What are the key architectural decisions in 400 words?"
    hints:
      token_estimate: 500
      load_strategy: eager
      priority: critical
      summary_of: architecture              # ← points back to the full version
```

An agent with a constrained budget loads `architecture-summary` first (`eager`, `critical`,
500 tokens). It reaches for `architecture` only when it needs the normative detail (`lazy`,
18,000 tokens). Without the hints, it would have had to load all 18,000 tokens to find the
400-word answer it actually needed.

---

## Chunked documents

For large documents that have natural sections, RFC-0006 proposes explicit chunk
relationships:

```yaml
  - id: api-reference
    path: api/reference.md
    intent: "What endpoints, parameters, and response schemas does the API expose?"
    hints:
      token_estimate: 62000
      load_strategy: never      # never load the full reference proactively
      priority: reference
      density: dense
      chunked: true
      chunk_count: 5

  - id: api-ref-auth
    path: api/reference-auth.md
    intent: "What are the authentication endpoints and token schemas?"
    hints:
      token_estimate: 9400
      chunk_of: api-reference
      chunk_index: 1
      total_chunks: 5
      chunk_topic: "Authentication and token management"

  - id: api-ref-resources
    path: api/reference-resources.md
    intent: "What are the resource CRUD endpoints and their schemas?"
    hints:
      token_estimate: 18600
      chunk_of: api-reference
      chunk_index: 2
      total_chunks: 5
      chunk_topic: "Resource management endpoints"
```

The agent knows the 62,000-token full reference exists (`never` — do not load it). When it
needs the authentication endpoints specifically, it loads `api-ref-auth` (9,400 tokens)
directly, without touching the rest. The `chunk_topic` field on each chunk is the key: the
agent selects the right section from the manifest without reading any of the content first.

---

## Root-level hints

At the manifest level, a `hints` block provides aggregate information before any unit is
loaded:

```yaml
kcp_version: "0.3"
project: platform-docs
version: 3.0.0

hints:
  total_token_estimate: 128400
  unit_count: 94
  recommended_entry_point: overview
  has_summaries: true
  has_chunks: true
```

`total_token_estimate: 128400` tells an agent with 16,000 tokens of remaining budget that
it cannot load this entire corpus — before it loads a single unit. It can then
plan: load the `recommended_entry_point`, follow the `eager` units, use summaries where
available, and reach for chunks only when needed.

`has_summaries: true` and `has_chunks: true` are flags that signal the corpus is navigable
at lower cost. An agent that knows summaries exist will look for them. An agent that does
not know they exist will not.

---

## The tokenizer problem

One genuinely hard open question: token counts vary across models. A 42,000-token document
by GPT-4's tokenizer may be 38,000 tokens by Claude's tokenizer and 46,000 by Llama's.

RFC-0006 currently proposes model-agnostic estimates — a single integer that approximates
"typical LLM tokenizer." The alternative is a model-keyed map:

```yaml
hints:
  token_estimates:
    cl100k_base: 42000    # GPT-4
    claude: 38500
    llama: 46000
```

Precise, but a maintenance burden that few publishers would actually keep current. The
RFC leaves this open — the model-agnostic single integer is the current proposal, with the
map as a possible extension.

---

## What this changes in practice

The benchmark that motivated the KCP composability work showed a 40% reduction in tool
calls when agents had a structured manifest. Context hints extend that result: agents with
size metadata load the right unit the first time rather than discovering overflow after the
fact, backing out, and retrying.

The more fundamental shift is that `hints` makes context budgeting something the *publisher*
can inform. Today, context management is entirely the agent's problem — it has no data to
work with other than what it discovers by loading. With `hints`, the publisher declares the
cost profile of their knowledge base. Agents can plan. Manifests become navigable not just
by content but by cost.

---

## Open questions

**Token estimate staleness.** `token_estimate` is a snapshot that drifts as content
changes. Is the unit's `validated` date sufficient as a freshness proxy, or should there be
a separate `token_estimate_updated` field?

**`never` and search.** Should units with `load_strategy: never` appear in manifest query
results at all? The agent should know they exist — but returning them in a search result
risks the agent loading them anyway. Should they be returned with a flag, or filtered out
unless explicitly queried by id?

**Chunk navigation.** Chunks are selected by `chunk_topic` today. Should KCP support
topic-based chunk selection server-side — where an agent declares a topic and the publisher
returns the matching chunk id — or is that a query concern beyond the manifest format?

Comment on [Issue #9](https://github.com/Cantara/knowledge-context-protocol/issues/9).

---

Full RFC: [RFC-0006-Context-Window-Hints.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0006-Context-Window-Hints.md)

Spec and all RFCs: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
