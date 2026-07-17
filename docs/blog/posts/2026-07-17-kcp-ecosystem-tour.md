---
description: "A practical tour of the KCP toolchain — kcp-commands, kcp-memory, kcp-dashboard, kcp-triage, kcp-agent, kcp-harness, and Synthesis. What each tool does, how they fit together, and exactly where to start."
date: 2026-07-17T12:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - AI Agents & the Agentic Web
  - Knowledge Context Protocol
tags:
  - kcp
  - kcp-commands
  - kcp-memory
  - synthesis
  - tutorial
  - getting-started
authors:
  - totto
---

# The KCP Ecosystem: A Tour for New Arrivals

There are now eight open-source tools in the KCP ecosystem. They were built incrementally over 140 days, each solving one specific problem. If you're arriving for the first time, the map is not obvious.

This is that map.

<!-- more -->

---

## Start here: the problem each tool solves

You are working with Claude Code (or another agent-based IDE). You have a large codebase. You keep burning context window. Your agent keeps rediscovering the same things every session. It issues Bash commands and gets walls of Maven output back. It has no idea what APIs are available or how to navigate the knowledge that already exists.

None of these are model problems. They are knowledge infrastructure problems.

The KCP ecosystem is the infrastructure.

---

## The spec: Knowledge Context Protocol

**Repo**: [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)

The foundation is a YAML file — `knowledge.yaml` — that every other tool in this ecosystem reads, writes, or enforces. It declares:

- **What** the project contains (units: files, directories, URLs)
- **Why** each unit exists (intent, written in natural language)
- **Who** it's for (audience: human, agent, developer)
- **How** to find related units (triggers, dependencies, federation links)
- **Whether** to trust it (ED25519 signature, content hashes)

Think of it as the mirror image of MCP. MCP solved "how does an agent connect to tools?" KCP solves "how does an agent navigate knowledge?" The two standards complement each other — MCP for action, KCP for understanding.

One manifest, per project. Everything else builds on it.

---

## The ecosystem at a glance

```
                    Your project (knowledge.yaml)
                             │
             ┌───────────────┼───────────────┐
             │               │               │
       [kcp-agent]    [kcp-harness]    [kcp-triage]
       load planning  governance       build manifests
       (deterministic) enforcement     for external APIs
             │               │
             └───────┬───────┘
                     │
              Claude Code / Cursor
                     │
           ┌─────────┴─────────┐
           │                   │
    [kcp-commands]       [Synthesis]
    hook: inject +       MCP: search +
    filter + log         index + arch
           │
    ~/.kcp/events.jsonl
           │
    [kcp-memory]
    cross-session
    episodic memory
           │
    [kcp-dashboard]
    TUI: savings +
    compliance view
```

Each box is a separate tool you install independently. You don't need all of them to get started.

---

## The tools, one by one

### kcp-commands — the first thing to install

**Repo**: [github.com/Cantara/kcp-commands](https://github.com/Cantara/kcp-commands)
**Version**: 0.28.0 | 292 bundled CLI manifests

A Claude Code [PreToolUse + PostToolUse hook](https://docs.anthropic.com/en/docs/claude-code/hooks) that intercepts every Bash call in three phases:

**Phase A — before execution**: For recognised commands (`mvn`, `git`, `kubectl`, `terraform`, `docker`, `npm`, …), injects a compact syntax hint — the flags you actually want, not a manpage. 292 manifests cover the most common CLI tools in software development.

**Phase B — after execution**: Strips boilerplate from noisy output. A `mvn clean install` that would return 800 lines of reactor output comes back as the 12 lines that matter. Git diffs, `kubectl get pods`, Docker image lists — all filtered.

**Phase C — event logging**: Every Bash call is appended to `~/.kcp/events.jsonl`. This is the feed that kcp-memory indexes.

Measured result: **33% context window saved** per session. 84% of Bash calls are well-known tools that trigger filtering. The hook runs in Java (12 ms/call) with a Node.js fallback.

```bash
# Install (Java daemon, recommended):
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java

# Node.js only (no JVM required):
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --node
```

---

### kcp-memory — cross-session episodic memory

**Repo**: [github.com/Cantara/kcp-memory](https://github.com/Cantara/kcp-memory)
**Version**: 0.32.0

Agents are amnesiac by default. Every new session starts from zero. kcp-memory fixes this.

It runs as a background daemon and indexes `~/.kcp/events.jsonl` (written by kcp-commands) plus session transcripts from Claude Code. When a new session starts, relevant context from previous sessions is injected automatically — which commands you ran last time, what the agent concluded, what files were modified.

It also indexes subagent transcripts, which means memory is shared across parallel agent sessions in the same project. The storage is SQLite, entirely local, no cloud.

Think of it as the difference between a colleague who was there last week and one who has never heard of your project.

---

### kcp-dashboard — see what's happening

**Repo**: [github.com/Cantara/kcp-dashboard](https://github.com/Cantara/kcp-dashboard)
**Version**: 0.27.0

A [Bubble Tea](https://github.com/charmbracelet/bubbletea) terminal TUI that gives you live visibility into the KCP toolchain:

- Token savings vs. unhooked sessions (rolling average)
- Which commands triggered Phase A injection vs. Phase B filtering
- Session history with guidance quality scores
- kcp-memory recall stats (what got injected, from when)
- Governance compliance metrics if kcp-harness is running

Run it in a split pane while Claude Code is running and you get a live view of what the knowledge layer is doing. Optional — you don't need it for the tools to work — but useful when you're tuning your setup or demonstrating to someone what's happening.

---

### Synthesis — workspace intelligence

**Repo**: [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)
**Version**: 1.43.1

Synthesis is the indexing and search layer. It scans your workspace — code, docs, PDFs, configs — builds a Lucene search index and a relationship graph, and exposes 52 MCP tools to Claude Code, Cursor, Aider, or any MCP-compatible agent.

Where KCP tells an agent *what to load*, Synthesis answers *where is it and how does it relate to everything else*.

What it does:
- **Full-text search** across any file type (code, markdown, PDFs, even video transcripts)
- **Relationship mapping**: bidirectional imports, references, cross-repo dependencies
- **Architecture analysis**: god classes, dead code, circular dependencies, test gaps
- **AI Q&A**: natural language questions answered against your indexed workspace
- **Semantic search** with vector embeddings
- **Real-time daemon** (`synthesis watch`) for live updates as files change

Synthesis is the tool you run across your entire organisation's repos — not just one project. It works independently of KCP but pairs naturally with it: KCP provides the declared intent, Synthesis provides the discovered structure.

```bash
synthesis scan /path/to/workspace
synthesis search "authentication middleware"
synthesis ask "what calls this function?"
```

The MCP server integrates with Claude Code automatically once configured in `.claude/mcp.json`.

---

### kcp-triage — knowledge for external APIs

**Repo**: [github.com/Cantara/kcp-triage](https://github.com/Cantara/kcp-triage)
**Version**: 0.1.0

An LLM-orchestrated CLI that crawls a website, classifies its API surface, audits its security headers, and builds an agent-ready workbench for it — including a signed `knowledge.yaml`.

You give it a URL. It produces a `sites/<domain>/` directory containing:
- `CLAUDE.md` — project context for the agent
- `skills/` — executable workflow patterns
- API inventory (endpoints, schemas, authentication)
- `knowledge.yaml` — a KCP manifest so any KCP-aware agent can navigate the site

It uses a three-tier LLM strategy internally: Opus for orchestration, Sonnet for analysis, Haiku for grunt work. The output is designed to be loaded by kcp-agent, not read by humans.

Use kcp-triage when you're working with a third-party API and want the agent to be properly oriented from session one rather than discovering the API structure through trial and error.

---

### kcp-agent — deterministic load planning

**Repo**: [github.com/Cantara/kcp-agent](https://github.com/Cantara/kcp-agent)
**Version**: 0.13.0

The reference agent that consumes KCP end-to-end. Given a task and a `knowledge.yaml`, it produces an **inspectable load plan** — a deterministic, auditable decision about which units to load, in what order, and why — before it synthesises a response.

The planning step is **LLM-free**. No model is invoked until the load plan is approved. This means you can inspect the plan before the agent reads a single byte of knowledge — a property that matters for compliance and debugging.

The full pipeline:

```
discover manifest
  → verify signature
  → trust-gate
  → score units by task relevance
  → federate (follow links to other manifests)
  → temporal filter (skip stale units)
  → budget (respect token ceiling)
  → emit load plan
  → [load units]
  → [synthesise answer]
```

Each step is deterministic. All decisions are defensible. The agent can explain every unit it loaded and every unit it skipped.

kcp-agent ships with worked examples (`examples/fjordwire/`, `examples/vault/`) that show how to wire it up for real projects.

---

### kcp-harness — governance enforcement

**Repo**: [github.com/Cantara/kcp-harness](https://github.com/Cantara/kcp-harness)
**Version**: 0.4.2

A compliance proxy that sits between an agent and its knowledge tools, enforcing a 13-gate governance cascade on every request:

```
classify → verify → trust → score → federate
→ temporal → budget → permission → audit → execute
```

Every gate either passes or blocks. If the harness can't verify a request, the agent gets nothing. Fail-closed by design.

The key property: the harness emits **content-free audit traces** — logs that prove what governance decisions were made without recording the knowledge content itself. This matters in regulated environments where you need to demonstrate compliance without creating a second copy of sensitive data.

kcp-harness does not require you to modify your agent. It wraps the knowledge layer as an MCP proxy — the agent calls the same MCP tools it always did, the harness intercepts and governs.

Use kcp-harness when auditability and governance matter more than setup simplicity. In practice: production deployments, regulated industries, multi-tenant systems.

---

## Where to start

Not all at once. The ecosystem is layered — each tool adds value independently.

**Day 1 — save context now:**

```bash
# 1. Install kcp-commands (immediate 33% savings)
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java

# 2. Open Claude Code. Start a session. Notice the Phase A hints appearing
#    before Bash calls. Notice the quieter output.
```

**Day 2 — add memory:**

```bash
# Install kcp-memory (episodic cross-session recall)
# See: https://github.com/Cantara/kcp-memory#install
```

**Day 3 — add workspace intelligence:**

```bash
# Configure Synthesis MCP in .claude/mcp.json
# Then: synthesis scan . (from your project root)
# Claude Code can now search, relate, and ask across your entire codebase
```

**When you want governance:**

Add kcp-agent for inspectable load planning, kcp-harness for enforcement. These are for when you're building agents that will run in production or in environments where "the agent read file X because..." needs to be provable.

**When you're working with external APIs:**

Run kcp-triage against the API's documentation site. Get a signed manifest and workbench in minutes rather than spending the first hour of every session re-orienting the agent to the API surface.

---

## The bigger picture

The KCP ecosystem is the knowledge layer for agentic development — the infrastructure that sits between the model and the knowledge it reasons over. It does for knowledge what MCP did for tools: makes it structured, navigable, auditable, and trustworthy.

Every tool is open source (Apache 2.0), maintained by the [Cantara Norwegian Software Development Foundation](https://github.com/Cantara) and [eXOReaction](https://github.com/exoreaction).

The 140-day timeline of how this was built — and why the decisions were made in the order they were — is documented in [The Knowledge Layer: A Record](https://wiki.totto.org/blog/2026/07/16/the-knowledge-layer-a-record/). If you want to understand the reasoning rather than just the tools, that's the place to start.

---

**Links:**

- [Knowledge Context Protocol spec](https://github.com/Cantara/knowledge-context-protocol)
- [kcp-commands](https://github.com/Cantara/kcp-commands) — install first
- [kcp-memory](https://github.com/Cantara/kcp-memory)
- [kcp-dashboard](https://github.com/Cantara/kcp-dashboard)
- [kcp-triage](https://github.com/Cantara/kcp-triage)
- [kcp-agent](https://github.com/Cantara/kcp-agent)
- [kcp-harness](https://github.com/Cantara/kcp-harness)
- [Synthesis](https://github.com/exoreaction/Synthesis)
