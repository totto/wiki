---
tags:
  - AI
  - Synthesis
  - Open Source
---

# Synthesis — Release History

Synthesis is a knowledge infrastructure platform for AI-augmented development. It indexes workspaces (code, documentation, PDFs, media), builds a multi-layer knowledge graph, and exposes everything through a CLI, an MCP server for AI agents, and an LSP server for IDEs.

**Repository:** [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

---

## Current Release: v1.21.0 (March 3, 2026)

**55 CLI commands · 8 MCP tools · 4,170 tests · 18 database migrations**

The v1.21.0 release completes the three-layer AI memory model by adding **episodic memory** — indexed access to Claude Code session history. Synthesis has always covered Layer 3 (workspace knowledge graph). It now covers Layer 2 as well.

| Layer | Type | Source | Synthesis command |
|-------|------|--------|-------------------|
| 1 | Working memory | Context window | *(current conversation)* |
| 2 | Episodic memory | Session transcripts | `synthesis sessions` |
| 3 | Semantic memory | Workspace knowledge graph | `synthesis search`, `relate`, `impact` |

### What's new in v1.21.0

**`synthesis sessions`** — a new subcommand backed by a standalone SQLite module that indexes Claude Code session JSONL files from `~/.claude/projects/`. First scan: 2,971 sessions in 109 seconds. Subsequent scans are near-instant (incremental, skips unchanged files).

```bash
synthesis sessions scan                      # index ~/.claude/projects/
synthesis sessions search "authentication"  # full-text search across all sessions
synthesis sessions list --since 7d          # recent sessions
synthesis sessions get <session-id>         # full detail
```

The `sessions` MCP tool extends this to AI agents — Claude Code can now search its own conversation history through the same Synthesis MCP server that already provides workspace knowledge. No second MCP server required.

See the blog post: [Working Memory, Episodic Memory, Semantic Memory. Your Agent Has One.](/blog/2026/03/03/three-layer-ai-memory-episodic-memory-semantic-memory-your-agent-has-one/)

---

## v1.18.2 — Session Lifecycle Integration (February 28, 2026)

Session lifecycle hooks, `synthesis hooks generate` for automated hook scaffolding, `synthesis session-context` for reading active session state, and `synthesis claude-md` for CLAUDE.md management. 4,107 tests.

---

## v1.13.x — Code Knowledge Graph (February 22, 2026)

CKG phases 1–4 landed in v1.12.2, covering class-level code graphs with symbol extraction, import analysis, and cross-file dependency edges. v1.13.0 fixed a rebalance false-positive (issue #209) and integrated `.synthesisignore` into health checks. 3,893 tests at GA.

---

## v1.12.0 — 9-Phase Maintain Orchestrator (February 21, 2026)

`synthesis maintain` became a rich orchestrator: file tracking, snapshot management, knowledge edge scanning, reconciliation, activity logging, workspace sync, and git integration — all in sequence, with progress reporting. Guided `synthesis init` added.

---

## v1.11.0 — Workspace Self-Organization (February 20, 2026)

`synthesis health` (structural audit with health score 0–100), `synthesis prune` (stale file removal), `synthesis sweep` (orphan cleanup), and the directory identity system that enables workspace self-organization via `.synthesis.md` companion files.

---

## v1.10.x — Knowledge Integrity and Discovery (February 19–20, 2026)

`synthesis discover` (surface unknown structure), `synthesis validate` (drift detection between index and filesystem), and unified knowledge graph with confidence metadata. Gap detection flags areas where the knowledge graph is sparse.

---

## v1.9.x — Test Expansion and Operational Maturity (February 18–19, 2026)

Test count grew from 1,054 to 2,325 during this series (v1.9.1–v1.9.5). Staging pipeline improvements, project-level skill generation, MCP schema fixes, and `synthesis enrich` targeting. The architectural security report landed in v1.9.4.

---

## v1.8.x — Staging Pipeline (February 17–18, 2026)

A multi-phase staging pipeline for file ingestion and classification: `staging ingest`, `staging route`, `staging rename`. V8 Flyway migration for report cache. Vision resize for large images.

---

## v1.7.x — Dashboard, Research, Reports (February 16–17, 2026)

`synthesis dashboard`, `synthesis research` (deep multi-source investigation), `synthesis report` (executive report generation), `synthesis org enrich`, and git integration in `maintain`. Credential store for API key management.

---

## v1.6.x — Executive Summaries (February 16, 2026)

`synthesis summary` with eight role-specific perspectives (engineering manager, architect, executive, DevOps, product manager, security, developer, general). Client-to-codebase auto-discovery. V5 Flyway migration for summary cache.

---

## v1.5.x — Sub-Workspaces and Bundled Skills (February 16, 2026)

Sub-workspace support for multi-project configurations. Bundled Claude Code skills installable via `synthesis export-skills`. Smart exclusion defaults. V4 migration.

---

## v1.4.0 — File Tracking and Change Reporting (February 16, 2026)

`synthesis track` (hash-based file movement detection with 7-day safety period), `synthesis changelog` (cross-workspace change reports with smart filtering). V3 migration: 6 new tables.

---

## v1.1.0 — Protocol Servers (February 15, 2026)

MCP server (JSON-RPC 2.0 over stdio, 7 tools), LSP server (LSP 3.17, document links, hover, diagnostics, workspace symbols), air-gapped edition mode, self-update mechanism. Three deployable JARs: CLI, MCP, LSP.

---

## v1.0.0 — Genesis (February 14, 2026)

Core indexing engine (Apache Lucene 10.1.0), 6 file analyzers (code, markdown, YAML, PDF, image, video), organization registry, dependency graphs, and 282 tests. Built to solve the lib-pcb problem: 8,934 files generated in 11 days of AI-assisted development with no tool to navigate the output.

---

## Version Timeline

| Version | Date | Highlights |
|---------|------|------------|
| v1.0.0 | Feb 14 | Core indexing, search, CLI, org intelligence, 282 tests |
| v1.0.1 | Feb 14 | Distribution, skill generation, install scripts |
| v1.0.2 | Feb 14 | Media support (image, video, PDF), directed synthesis |
| v1.0.3 | Feb 14 | Bundled ffprobe binaries |
| v1.1.0 | Feb 15 | MCP server, LSP server, update system, air-gapped mode |
| v1.2.0 | Feb 15 | AI features (enrich, explain, perspectives), local media enrichment |
| v1.2.1–v1.2.3 | Feb 15 | Unified workspace system, status aggregates |
| v1.4.0–v1.4.1 | Feb 16 | File tracking, change reporting, V3 migration |
| v1.5.0–v1.5.3 | Feb 16 | Sub-workspaces, bundled skills, visual workspace tree |
| v1.6.0–v1.6.1 | Feb 16 | Executive summaries (8 perspectives), client auto-discovery |
| v1.7.0–v1.7.8 | Feb 16–17 | Dashboard, research engine, report engine, git integration |
| v1.8.0–v1.8.4 | Feb 17–18 | Staging pipeline, vision resize, report fixes |
| v1.9.0–v1.9.12 | Feb 18–19 | Report output config, 2,325 tests, staging integration |
| v1.10.0–v1.10.6 | Feb 19–20 | Knowledge integrity, discover, validate, unified knowledge graph |
| v1.11.0–v1.11.3 | Feb 20 | Health command, prune, sweep, directory identity system |
| v1.12.0–v1.12.2 | Feb 21–22 | 9-phase maintain, guided init, Code Knowledge Graph |
| v1.13.0–v1.13.1 | Feb 22 | CKG dogfooding fixes, 3,893 tests |
| v1.18.2 | Feb 28 | Session lifecycle hooks, session-context, claude-md, 4,107 tests |
| **v1.21.0** | **Mar 3** | **Episodic memory: Claude sessions module, FTS5 search, 4,170 tests** |
