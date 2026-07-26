---
tags:
  - Open Source
  - AI
---

# Open Source

I have been involved in open source for most of my career. The work spans three GitHub organizations and ranges from production IAM systems to AI knowledge infrastructure.

---

## eXOReaction

[github.com/exoreaction](https://github.com/exoreaction)

### Synthesis — Knowledge Infrastructure Platform

**Repository:** [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)
**Language:** Java 21 | **License:** Apache 2.0 | **Current version:** v1.42.0

Local-first knowledge infrastructure for AI-augmented development. Indexes workspaces (code, docs, PDFs, media, Notion), builds multi-layer knowledge graphs, and exposes everything through a CLI, MCP server, and LSP server.

**Key stats:** 76 CLI commands · 52 MCP tools · 4,700+ tests · 200--300 files/second indexing

**Capabilities:**
- Sub-second full-text and semantic search across entire workspaces
- Code knowledge graph (dependency tracking, cross-repo relationships)
- Episodic memory via session indexing (Claude Code session transcripts → searchable SQLite), with `remember`/`recall`/`reflect` MCP tools
- Agent dispatch planner (`synthesis dispatch`) — pre-populates agent spawn prompts
- Full-stack KCP v0.25 support: manifest scaffolding (`kcp init`), refresh, verification against evidence (`kcp verify`), cross-repo federation, read planning (`kcp plan`), and Ed25519 signing
- Security analysis (`code-graph security`) — 21 signals across traditional and agentic attack surfaces
- Notion workspace integration with health signals (W022/W023/W024)
- Executive reporting, research engine, maintain/validate/health commands

[:octicons-arrow-right-24: Release history](notes/synthesis-releases.md) · [:octicons-arrow-right-24: Knowledge Infrastructure](knowledge-infrastructure/index.md)

---

### xorcery-alchemy

**Repository:** [github.com/exoreaction/xorcery-alchemy](https://github.com/exoreaction/xorcery-alchemy)
**Language:** Java | **License:** Apache 2.0

Experimental extensions to the Xorcery framework, exploring temporal analytics and DevSecOps intelligence capabilities.

---

## Cantara

[github.com/Cantara](https://github.com/Cantara)

Cantara builds open-source infrastructure for Java applications: authentication systems, reactive frameworks, messaging abstractions, microservice tooling, and AI knowledge protocols. Most projects are Apache 2.0 licensed and production-ready.

### Knowledge Context Protocol (KCP)

**Repository:** [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)
**Spec:** [cantara.github.io/knowledge-context-protocol](https://cantara.github.io/knowledge-context-protocol)
**License:** Apache 2.0 | **Status:** v0.25.1 — submitted to the Linux Foundation Agentic AI Foundation

A YAML file format specification that makes knowledge navigable — and trustworthy — for AI agents. KCP is to knowledge what MCP is to tools: it adds topology (`depends_on`, `supersedes`), intent (what question each unit answers), freshness (`validated` dates), audience targeting, and context window hints. Twenty-five releases in six months have grown it from a table of contents into a full protocol, with layers for discovery, meaning, trust, time, identity, federation, and economics.

**RFCs:** Auth & Delegation · Federation (Org-Hub) · Trust & Compliance · Unit Content Integrity · Temporal Validity · Payment & Rate Limits (economic metadata) · Context Window Hints

**Reference implementations:** parsers in Python and Java · MCP bridge servers in TypeScript, Python, and Java · the `kcp-agent` reference agent (below)

---

### kcp-commands

**Repository:** [github.com/Cantara/kcp-commands](https://github.com/Cantara/kcp-commands)
**Language:** Java (daemon) + shell | **License:** Apache 2.0 | **Current version:** v0.12.0

A Claude Code hook that applies KCP at the Bash tool boundary. Intercepts every Bash tool call: injects concise flag/syntax guidance before execution (no `--help` round-trips), strips noise after. Also writes every tool call to `~/.kcp/events.jsonl` for kcp-memory ingestion.

**Measured saving:** 67,352 tokens per session — 33.7% of a 200K context window recovered

**283+ bundled manifests** covering git, Linux, Docker, Kubernetes, cloud CLIs, build tools, package managers, and more. Unknown commands auto-generate manifests from `--help`.

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java
```

---

### kcp-memory

**Repository:** [github.com/Cantara/kcp-memory](https://github.com/Cantara/kcp-memory)
**Language:** Java | **License:** Apache 2.0 | **Current version:** v0.32.0

A Java daemon that indexes Claude Code session transcripts and kcp-commands tool events into a local SQLite database with FTS5 full-text search. The episodic memory layer for Claude Code — session history searchable in milliseconds. Ships as both a CLI tool and an MCP server.

**MCP tools:** `kcp_memory_search` · `kcp_memory_events_search` · `kcp_memory_list` · `kcp_memory_stats` · `kcp_memory_session_detail` · `kcp_memory_project_context`

```bash
# Register as MCP server in ~/.claude/settings.json
java -jar ~/.kcp/kcp-memory-daemon.jar mcp
```

---

### kcp-agent

**Repository:** [github.com/Cantara/kcp-agent](https://github.com/Cantara/kcp-agent)
**Language:** TypeScript (npm) + native binaries | **License:** Apache 2.0 | **Current version:** v0.19.0

The reference agent for KCP — a **deterministic, fail-closed navigation planner** plus optional LLM synthesis. It reads a `knowledge.yaml`, scores and gates units against declared trust, freshness, audience, and budget, and produces an inspectable plan *before* any content is loaded or any model is called. Determinism at the core, the model at the edge. Since v0.11 the surface has grown into the full gate triad — *load* (`plan`), *assert* (`ground`), *act* (`assess`) — plus per-unit decision traces (`--trace`), versioned plan JSON with `diff` and `replay`, episodic memory (`remember`/`recall`), serving-endpoint discovery, and 13 published conformance vectors other implementations can test against. Ships as an MCP server (`kcp_plan`, `kcp_load`, `kcp_validate`) and as self-contained native binaries.

```bash
npx kcp-agent plan "your task" --manifest https://example.com/knowledge.yaml
claude mcp add kcp -- npx -y kcp-agent mcp
```

See the [Defendable Agents](topics/defendable-agents/index.md) field guide for the full architecture.

---

### kcp-harness

**Repository:** [github.com/Cantara/kcp-harness](https://github.com/Cantara/kcp-harness)
**Language:** TypeScript | **License:** Apache 2.0 | **Current version:** v0.10.0

Deterministic knowledge governance for any AI agent. An MCP compliance proxy that sits between an agent and its tools, routing every knowledge request through a deterministic multi-gate governance cascade — fail-closed policy, append-only audit trail, budget ledger, and temporal pinning — and emitting the decision traces, audit logs, and budget records that map onto SOC 2 / ISO 27001 / GDPR controls. No model involvement in the governed decision. Recent releases extend governance from knowledge reads to **actions**: human approval workflows for held requests, temporal watch (re-decide a standing plan when time alone changes the outcome), action conformance checking, resolution signatures, and an x402 payment wallet under hard budget ceilings.

---

### pi-kcp

**Repository:** [github.com/Cantara/pi-kcp](https://github.com/Cantara/pi-kcp)
**Language:** TypeScript | **License:** Apache 2.0 | **Current version:** v0.2.0

KCP agent proficiency and ergonomics for the [Pi coding agent](https://github.com/earendil-works/pi) harness. Human-facing `/kcp` commands (plan, validate, recall, health) and agent-facing skills on **stock Pi** — no MCP client required — with kcp-agent invoked as a CLI for deterministic plans and kcp-memory over HTTP for episodic recall. Its runtime-depth milestone added enforcement: a skill declared in `knowledge.yaml` with an `action_scope` becomes enforced authority — native tool calls outside the declared tools/paths/capabilities are blocked by the same deterministic decision the kcp-harness proxy makes, and every governed turn carries one correlation id. Code intelligence (Synthesis or any other provider) stays behind Pi's MCP configuration as an optional, substitutable backend.

Companion post: [The AI Agent That Keeps the Receipts](/blog/2026/07/22/the-agent-that-keeps-the-receipts/) · [interactive demos](https://cantara.github.io/pi-kcp/playground/)

---

### kcp-dashboard

**Repository:** [github.com/Cantara/kcp-dashboard](https://github.com/Cantara/kcp-dashboard)
**Language:** Go | **License:** Apache 2.0 | **Current version:** v0.27.0

A live terminal dashboard (Bubble Tea + Lip Gloss) for the KCP ecosystem — guidance effects, session profiles, token savings, and memory-search activity, auto-refreshing every two seconds.

---

---

### Whydah — SSO / IAM Platform

**Repository:** [github.com/Cantara/Whydah](https://github.com/search?q=org%3ACantara+Whydah&type=repositories) (16 repositories)
**Website:** [getwhydah.com](http://getwhydah.com)
**Language:** Java | **License:** Apache 2.0

A complete Single Sign-On and Identity & Access Management solution. Whydah handles user authentication, token management, role-based access control, and user administration. It is production-deployed across multiple Norwegian enterprise clients.

**Core modules:**
- `Whydah-SecurityTokenService` — Application and user token management
- `Whydah-UserIdentityBackend` — Identity storage with LDAP integration
- `Whydah-SSOLoginWebApp` — SSO login interface
- `Whydah-UserAdminService` — User administration backend
- `Whydah-UserAdminWebApp` — Admin UI
- `Whydah-Java-SDK` — Java integration SDK

**Quick start (Docker):**
```bash
docker pull whydah/whydah-all-in-one-image
docker run -it -p 9997:9997 whydah/whydah-all-in-one-image
# http://localhost:9997/sso/welcome  (admin / whydahadmin)
```

---

### Xorcery — Reactive Java Framework

**Repository:** [github.com/Cantara/xorcery](https://github.com/Cantara/xorcery)
**Language:** Java 21+ | **License:** Apache 2.0

A modular Java library framework built around dependency injection (HK2), composable YAML/JSON configuration, and reactive streams. Designed for building highly performing microservices with strong operational characteristics out of the box.

**Key features:**
- Composable configuration (YAML + JSON Schema)
- Reactive streams over WebSockets
- OpenTelemetry integration
- 30+ extensions: AWS, certificates, DNS, EventStore, JAX-RS/Jersey, Jetty, JWT, OpenSearch, and more
- Used as the foundation for the Xorcery AAA (Alchemy + Aurora) analytics platform

---

### Stingray — Microservice Application Framework

**Repository:** [github.com/Cantara/stingray](https://github.com/Cantara/stingray)
**Language:** Java | **License:** Apache 2.0

A Java application framework with strong conventions for building microservices. Provides structure, configuration, and lifecycle management. Used as the base framework in large-scale deployments (34+ services in production).

---

### Messi — Messaging Abstraction

**Repositories:** [MessiSDK](https://github.com/Cantara/MessiSDK) + provider libraries
**Language:** Java | **License:** Apache 2.0

A messaging and streaming abstraction layer with pluggable providers for different backends. Write once, switch providers without code changes.

**Providers:**
- `MessiS3Provider` — AWS S3
- `MessiSQSProvider` — AWS SQS
- `MessiKinesisProvider` — AWS Kinesis

---

### lib-electronic-components

**Repository:** [github.com/Cantara/lib-electronic-components](https://github.com/Cantara/lib-electronic-components)
**Language:** Java | **License:** Apache 2.0

A Java library for working with electronic components in manufacturing contexts. Provides MPN normalization, component similarity analysis, BOM management, and manufacturer data for 135+ manufacturers.

**Capabilities:**
- MPN normalization and type detection
- 17 specialized similarity calculators (resistors, capacitors, MOSFETs, MCUs, sensors, and more)
- BOM (Bill of Materials) creation and validation
- Alternative component finding
- Component categorization with metadata-driven profiles

---

### Nerthus / Visuale — Service Visualization

**Repositories:** [nerthus](https://github.com/Cantara/nerthus) · [nerthus2](https://github.com/Cantara/nerthus2) · [visuale](https://github.com/Cantara/visuale)
**Language:** Go / Java | **License:** Apache 2.0

Real-time dashboards for visualizing microservice environments. Shows service health, deployment status, and version distribution across a fleet of running services.

---

### Infrastructure & Utilities

**[microservice-baseline](https://github.com/Cantara/microservice-baseline)** — Starting point template for building well-structured microservices.

**[HTTPLoadTest-Baseline](https://github.com/Cantara/HTTPLoadTest-Baseline)** — Load testing tool designed for integration into CD/CD pipelines.

**[ConfigService](https://github.com/Cantara/ConfigService)** — Centralized configuration management service with SDK and dashboard.

**[Valuereporter](https://github.com/Cantara/Valuereporter-Java-SDK)** — Metrics and analytics collection: observations, activities, and reporting.

**[property-config](https://github.com/Cantara/property-config-json)** — Lightweight property-based configuration management.

**[realestate-metasys-cloudconnector-agent](https://github.com/Cantara/realestate-metasys-cloudconnector-agent)** — Reads sensor data from Johnson Controls Metasys building automation systems and distributes to cloud.

