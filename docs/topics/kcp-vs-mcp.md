---
title: "KCP vs MCP"
description: "KCP vs MCP, settled: they are not competitors. MCP is how an agent calls tools (retrieval); KCP is how an agent finds and trusts knowledge (structure). A side-by-side comparison, the failure modes each prevents, and a decision rule for when you need one, the other, or both."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# KCP vs MCP

Short answer: **it's not a versus.** The Model Context Protocol and the Knowledge Context Protocol solve different halves of the same problem, and the best agent stacks run both. MCP is how an agent *calls tools*. KCP is how an agent *finds and trusts knowledge*. One provides **retrieval**, the other provides **structure** — and structure is what tells the agent which retrieval is even worth doing.

The confusion is understandable — both are "context protocols" with three-letter names in the agent space. But they operate at different layers, and treating them as rivals is a category error that leaves a real gap in your architecture.

## Side by side

| | **MCP** (Model Context Protocol) | **KCP** (Knowledge Context Protocol) |
|---|---|---|
| **Question it answers** | "What tools can I call, and how?" | "What knowledge exists, and can I trust it?" |
| **Nature** | An RPC/tool-invocation protocol — *executable* | A YAML manifest format — *passive data* |
| **Verb** | **Do** — call a function, fetch a result | **Know** — navigate, select, trust before loading |
| **Unit** | A tool with a schema | A knowledge unit with intent, topology, freshness, trust |
| **When it runs** | At invocation time (the agent acts) | Before invocation (the agent orients) |
| **Failure it leaves open** | The agent can call tools but doesn't know *which knowledge is authoritative or current* | The agent knows what's true but has *no way to act on it* |
| **Injection surface** | Larger — executable config can carry instructions | Smaller — [passive data an agent reads can't inject](/blog/2026/05/08/why-kcp-is-passive-data-not-executable-config--and-why-that-matters-now/) the way config it executes can |

## They compose — that's the whole point

The two are designed to stack. KCP tells the agent *what knowledge exists, how fresh it is, and whether it's signed*; MCP is one of the ways the agent then *retrieves* it. In practice you expose a KCP manifest **and** an MCP bridge, and the agent uses the manifest to plan and the bridge to fetch. The reference implementation ships exactly this pairing — `kcp-agent` runs as an MCP server (`kcp_plan`, `kcp_load`, `kcp_validate`), so KCP navigation *is* available as MCP tools.

- **The full argument:** [KCP and MCP: One Protocol for Structure, One for Retrieval](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/)
- **How the bridge is wired:** [The Borrowed Leash: Determinism as a Service for the Agentic Web](/blog/2026/07/06/the-borrowed-leash-determinism-as-a-service-for-the-agentic-web/)

## Three failure modes KCP prevents that MCP alone doesn't

MCP gives an agent hands. It does not give it judgement about what to read:

1. **Rediscovery churn.** Without a map, an agent re-explores the same context every session — the [33-tool-call bug](/blog/2026/06/12/down-the-rabbit-hole-how-a-33-tool-call-bug-became-a-knowledge-standard/) that started KCP. A manifest turns 119 tool calls into 31.
2. **Stale confidence.** MCP will happily fetch a document that stopped being true in February. KCP carries `validated` dates and [temporal validity](/blog/2026/06/12/stale-knowledge-is-worse-than-no-knowledge-kcp-v019-and-v020-close-the-temporal-gap/), so an agent can tell fresh from stale.
3. **Unverifiable sources.** A tool result has no provenance. A KCP unit is signed and can be [attested and verified](/topics/defendable-agents/primitives/trust-and-attestation/), which is what makes an answer defensible to an auditor.

## The decision rule

- **You need MCP** the moment your agent has to *call anything* — a database, an API, a file system. Nearly every agent does.
- **You need KCP** the moment your agent has to *choose what to read or trust* from a non-trivial body of knowledge — docs, regulations, a large codebase, multi-source context.
- **You need both** for any serious agent on the [agentic web](/topics/agentic-web/): MCP to act, KCP to know what acting *on* is authoritative and current. They are complementary organs, not competing skeletons.

## Where to go next

- **The knowledge protocol in full:** [Knowledge Context Protocol](/topics/knowledge-context-protocol/)
- **Why "passive data" is the load-bearing distinction:** [Why KCP Is Passive Data, Not Executable Config](/blog/2026/05/08/why-kcp-is-passive-data-not-executable-config--and-why-that-matters-now/)
- **Unsure of a term?** [Glossary](/glossary/) · **New here?** [Start here](/start-here/)

*MCP is a widely-adopted open standard from Anthropic; KCP is an open standard developed under [Cantara](https://github.com/Cantara/knowledge-context-protocol) and submitted to the Linux Foundation's Agentic AI Foundation. This page is one practitioner's framing of how they fit — corrections welcome.*
