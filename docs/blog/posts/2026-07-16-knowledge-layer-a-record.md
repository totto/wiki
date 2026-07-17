---
description: "February 25 to July 16, 2026: what the Knowledge Context Protocol built, when, and what the field confirmed. A timestamped record for anyone working in this space."
date: 2026-07-16T14:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Knowledge Infrastructure
  - AI Agents
  - Architecture
tags:
  - kcp
  - prior-art
  - agent-governance
  - knowledge-layer
  - determinism
---

# The Knowledge Layer: A Record

*February 25 – July 16, 2026*

---

![KCP: The 140-Day Evolution of Knowledge Governance](/assets/images/kcp-record-2026/kcp-140-day-evolution-timeline.png)

---

![The Knowledge Layer: A Record — overview](/assets/images/kcp-record-2026/kcp-record-01-title.png)

The first version of the Knowledge Context Protocol shipped on February 25, 2026. This is a record of what it was, what it became, and why the decisions made in the first week turned out to still be the right ones 140 days later.

<!-- more -->

I'm writing it now because the field has caught up enough to make comparison possible.

## The Problem Was Empirical

In January 2026, we deployed AI agents against a production codebase of 8,934 files. The agents failed — not because the models were weak, but because the knowledge they consumed was stale, unstructured, and had no way to signal its own limitations. Agents produced confident answers from documents that had been superseded months earlier.

We wrote about this as [the Mirror Test](https://wiki.totto.org/blog/2026/02/11/the-mirror-test/): the agent reflects back what the knowledge base contains, not what is true. High confidence, low accuracy.

![The Mirror Test: High Confidence, Low Accuracy](/assets/images/kcp-record-2026/kcp-record-02-mirror-test.png)

No existing format addressed it. `llms.txt` tells crawlers what files exist. It doesn't tell agents what the files mean, when they expire, what they depend on, or which one supersedes which. That gap is structural, not accidental — llms.txt was designed for browse-and-discover. Agents navigate differently.

![Why llms.txt Is Structurally Insufficient](/assets/images/kcp-record-2026/kcp-record-03-llmstxt-gap.png)

## The Decisions We Made in Week One

v0.1.0 shipped 23 days after the production failure. Six design decisions, made in that first week, have not changed through v0.26:

![From Flat Lists to Navigable Topologies](/assets/images/kcp-record-2026/kcp-record-04-navigable-topology.png)

**Topology over lists.** Every knowledge unit declares what it `depends_on`, what it `supersedes`, what it `relates_to`. The result is a navigable graph, not a directory. An agent that understands topology can skip safely; an agent navigating a flat list cannot.

**Intent-first.** Every unit declares what question it answers — not a title, a question. Agents load by intent. This is why the tool-call reduction numbers are what they are: agents stop exploring and start querying.

**Freshness as first-class.** Every unit carries a `validated` timestamp and optional `valid_until`. An agent that loads a unit past its validity window is loading something it knows is stale. The protocol makes stale knowledge visible, not invisible.

**Selective loading.** Query by task, not by crawling. Tested across five frameworks (AutoGen, CrewAI, smolagents, LangChain, OpenCode): 53–80% fewer tool calls versus unguided exploration.

**Adoption gradient.** Three fields (`id`, `intent`, `validated`) constitute a valid Level 1 manifest. The full field set is available for Level 3 enterprise deployments. No all-or-nothing requirement. A single `knowledge.yaml` in five minutes is a valid first step.

**No runtime required.** Static file format. Any compliant parser can read it. No server, no SDK, no vendor lock-in.

![The Protocol Foundation Blueprint (v0.1.0 to v0.26)](/assets/images/kcp-record-2026/kcp-record-05-foundation-blueprint.png)

## The Arc: 140 Days, 26 Versions, 24 RFCs

The release train moved fast:

**February 25**: v0.1.0 — core spec, Python + Java parsers, Apache 2.0 licence. First blog post: [Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](https://wiki.totto.org/blog/2026/02/25/beyond-llms-txt-knowledge-context-protocol/).

**February 28**: v0.2–v0.3 — six alignment fixes, six new fields. RFC-0002 through RFC-0005 published (auth/delegation, federation, trust/compliance, payment/rate-limits).

**March 1**: First empirical benchmarks published. [Two repos, two days](https://wiki.totto.org/blog/2026/03/01/kcp-two-repos-two-days/): 74% and 53% tool-call reduction. [Three agent frameworks](https://wiki.totto.org/blog/2026/03/01/kcp-three-frameworks/): AutoGen 80%, CrewAI 76%, smolagents 73%.

![Empirical Impact: Guided Querying Reduces Tool Calls](/assets/images/kcp-record-2026/kcp-record-06-tool-call-reduction.png)

**March 8**: v0.7 — delegation and compliance blocks. A2A composability proven against 150 adversarial tests; 8 spec gaps found and closed.

**March 9–19**: v0.8–v0.12 — rate limits, federation DAG, visibility and authority, capability discovery provenance.

**June 11–13**: v0.16–v0.21 — the trust and integrity expansion. Forty-eight hours, six versions, six RFCs promoted: per-unit content hashes, temporal validity (`valid_from` / `valid_until` / `recorded_at` / `superseded_by`), manifest composition with integrity pinning, federation-temporal window awareness. Three threat models formally addressed (T9: manifest relocation; T10: composition substitution; T11: rogue representative — the last closed in v0.26).

**July 4**: v0.22–v0.25 — trust attestation gates, org-federation discovery, HTTP 402 economic metadata. An agent can now read the price of a knowledge unit the same way it reads its expiry date, before spending anything.

**July 14**: v0.26 — serving endpoint binding (closes T11), unit aliases. Submitted to the Agentic AI Foundation for neutral-governance consideration alongside MCP and AGENTS.md.

![140 Days. 26 Versions. 24 RFCs.](/assets/images/kcp-record-2026/kcp-record-07-140-days-timeline.png)

Twenty-four published RFCs. Eleven conformance vectors. Three reference parsers (TypeScript, Python, Java). A CLI, MCP bridges, a reference agent, an episodic memory daemon, and a browser-based thought graph simulator.

## What the Field Confirmed

Three independent convergences arrived in 2026.

![Three Independent Discoveries. One Architecture.](/assets/images/kcp-record-2026/v2-three-independent-discoveries.png)

![The Split-Brain Reality of Agent Governance](/assets/images/kcp-record-2026/kcp-record-11-split-brain-governance.png)

**Databricks Omnigent (June 2026)** confirmed the action/knowledge split. Omnigent governs what an agent *does* — tool calls, OS access, cost budgets, human-in-the-loop gates. Six independently-derived primitives. Four overlap precisely with KCP's core design: deterministic layer, per-session budget ceilings, least privilege, wraps any agent.

What Omnigent doesn't govern is what the agent *knows*. This was the design claim KCP made in February 2026: knowledge governance and action governance are two different layers; you need both. Omnigent confirmed the split from the action side. We wrote about the composition on [July 9](https://wiki.totto.org/blog/2026/07/08/two-halves-of-agent-governance/).

![Governing the 'Do' vs. Governing the 'Know'](/assets/images/kcp-record-2026/kcp-record-12-do-vs-know-comparison.png)

**ContextNest** (arxiv:2607.02116, June 2026) arrived at the same architecture independently: typed documents with structured metadata, deterministic URI schemes with version pinning, SHA-256 hash-chained version histories, graph-level checkpoints, and a governance layer beneath retrieval. This is a research paper, not a deployed system. But two teams, different contexts, same shape — that's not coincidence. It means the problem is real and the architecture is load-bearing.

Where KCP goes further: content-free audit traces, the HTTP 402 economic metadata layer, and production deployment at enterprise scale.

**Knowit** (July 14, 2026): Pål de Vibe, Databricks MVP and Principal Engineer at Knowit, on the Two Halves post: *"We have started using KCP internally at Knowit, and it has significant impact in improving AI coding."* This is the first confirmed enterprise adoption outside our own environment.

## What Still Doesn't Exist Elsewhere

After surveying every governance and observability tool we could find (July 2026), three things remain specific to KCP:

![The Knowledge Governance Harness (kcp-harness)](/assets/images/kcp-record-2026/kcp-record-08-kcp-harness-cascade.png)

**Content-free reproducible audit traces.** kcp-harness emits a trace of every gate verdict — which documents were handed, which were skipped, and why — without emitting the documents themselves. The trace is content-free, privacy-safe, and fully reproducible: same inputs, same trace. This is not observability of behavior (what Arize, LangSmith, and Guardrails AI do). It's observability of the information environment the agent was operating in. You're not reading the agent's reasoning — you're reading what it was given to reason with.

![Unique Capability: Reproducible Audit Traces](/assets/images/kcp-record-2026/kcp-record-09-reproducible-audit-traces.png)

The [kcp-dashboard](https://cantara.github.io/kcp-dashboard/) makes this concrete: five scenarios, three complexity levels, each showing the 13-gate cascade verdict-by-verdict in your browser. The thought graph: not what the model was thinking — what it was given to think with.

![Unique Capability: HTTP 402 Economic Metadata](/assets/images/kcp-record-2026/kcp-record-10-http402-economic-metadata.png)

**HTTP 402 economic metadata at the knowledge governance layer.** Publishers can declare, per knowledge unit, what access costs — free, x402 micropayment, metered, subscription — in the same manifest that already declares freshness, provenance, and trust requirements. The protocol declares prices; the agent's own payment stack moves money; KCP executes nothing. HTTP 402 has been reserved since 1997. KCP v0.25 is the first production use of it in a knowledge governance context.

**A deterministic harness with a published spec.** kcp-harness runs a fixed 13-gate cascade. The gates in order: `audience`, `not_for`, `temporal`, `deprecated`, `supersession`, `relevance`, `attestation`, `payment`, `access`, `strict`, `max_units`, `money_budget`, `context_budget`. The cascade is deterministic: same inputs produce the same verdict, always. You can test against it, build conformant implementations, and verify your agent is behaving correctly. The spec is public and versioned. There is no equivalent for the knowledge layer anywhere else.

## An Honest Limit

This architecture works because kcp-harness runs a fixed, deterministic governance cascade and emits a content-free trace of every verdict. If your agent doesn't have a deterministic governance layer, there's nothing faithful to reconstruct. You're back to reading what the model said it was thinking — which is an unreliable narrator.

That's not a caveat. It's the point. Determinism is the prerequisite, not the feature.

## Where to Start

![The Adoption Gradient: Five Minutes to Level 1](/assets/images/kcp-record-2026/v2-adoption-gradient-three-levels.png)

The spec is open source (Apache 2.0): [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol).

If you're building with AI agents and you're not governing what they know — not just what they can do — start with a `knowledge.yaml`. Three fields. Five minutes. The [adoption guide](https://wiki.totto.org/blog/2026/02/28/add-knowledge-yaml-to-your-project-in-five-minutes/) handles the rest.

If you're researching knowledge governance for agents, the [full spec](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md) and [all 24 RFCs](https://github.com/Cantara/knowledge-context-protocol) are timestamped on GitHub from February 25, 2026 forward. ContextNest (2607.02116) is the closest parallel in the literature; the comparison is direct.

If you're working on the action layer — Omnigent, Microsoft Agent Governance Toolkit, similar — these compose with KCP. They're not competing layers. The split is real: governing the blast radius does not govern the reasoning.

![Where to Start: For Builders, Researchers, and Architects](/assets/images/kcp-record-2026/v2-where-to-start-builders-researchers-architects.png)

---

*KCP is proposed by eXOReaction AS under Apache 2.0 and submitted to the Agentic AI Foundation for neutral-governance consideration alongside MCP and AGENTS.md. The repository, all RFCs, and the full commit history are publicly timestamped at [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol).*
