---
tags:
  - AI
  - Synthesis
  - Open Source
---

# Synthesis — Release History

Synthesis is a knowledge infrastructure platform for AI-augmented development. It indexes workspaces (code, documentation, PDFs, media, Notion), builds a multi-layer knowledge graph, and exposes everything through a CLI, an MCP server for AI agents, and an LSP server for IDEs.

**Repository:** [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

!!! info "Current release"
    Synthesis is at **v1.42.0** (July 9, 2026) — **76 CLI commands · 52 MCP tools · 4,738 tests**. The detailed changelog below runs through v1.29.0 — for full notes on later releases, see the [repository releases](https://github.com/exoreaction/Synthesis/releases).

---

## Highlights since v1.29.0

A compact summary of the releases between the detailed changelog below and today:

| Release | Date | Highlights |
|---|---|---|
| v1.37.x | Jun 14–19 | KCP temporal filtering fix — inactive results actually excluded (#346) |
| v1.38.0 | Jul 6 | Full-stack KCP v0.25 (epic #361): `kcp init` / `refresh` / `verify` / `gaps` / `catalog` / `federate` / `plan` / `sign`, v0.25-conformant export and lossless ingestion, Ed25519 trust & signing, G-series governance cross-checks, K-series health signals |
| v1.40.0 | Jul 8 | Semantic search hardening: persisted embeddings for O(log N) HNSW search (#376), full-content embedding (#375), `plan_context` session dedup |
| v1.41.0–v1.42.0 | Jul 9 | Episodic memory `remember`/`recall` MCP tools, fail-closed grounding for `ask`, KCP trigger-match boosting and flag-gated routing hints for search/ask, KCP manifest retrieval benchmark (#371) |

---

## v1.29.0 (April 21, 2026)

**60+ CLI commands · 11 MCP tools · 4,356 tests**

The v1.29.0 release adds **Notion as a first-class workspace source** and **git signal analysis**. Synthesis can now index Notion workspaces alongside code and documentation — and detect when documentation and code have drifted apart.

### What's new in v1.29.0

**Notion workspace source** (6-phase implementation) — Notion pages become part of the Synthesis knowledge graph as virtual filesystem paths. Full and incremental syncs via BFS traversal; block-to-Markdown conversion covering all block types; rate-limited API client (3 req/s, automatic pagination, 429 retry).

Three new health signal types emerged from building this:

- **W022 notion-stale** — a Notion page references a code entity that no longer exists
- **W023 notion-orphan** — a Notion page has no corresponding code referent
- **W024 notion-conflict** — a Notion page and the codebase contradict each other on the same fact

These signals make documentation drift visible before it misleads an agent. See the blog post: [When Your Agent Can Finally Read the Room](/blog/2026/04/21/when-your-agent-can-finally-read-the-room/)

**Git signal analysis** — four history-based signals using exponential decay (half-life 180 days):

```bash
synthesis hotspots                  # files by temporally-decayed commit churn
synthesis archaeology --since 90d  # knowledge buried in old code paths
```

Co-change coupling and bus factor analysis also included. Inspired by temporal decay techniques in Repowise; all computation is local.

---

## v1.28.0 — Onboarding Improvements (April 11, 2026)

**4,300+ tests**

Explicit API key guidance when AI features are unavailable. When `synthesis` detects AI is enabled but no `ANTHROPIC_API_KEY` is configured, it now prints an actionable message with the exact command to fix it — instead of producing confusing silent failures. The same guidance surfaces during `synthesis init` guided setup.

---

## v1.27.1 — Memory Maintenance (April 10, 2026)

Two new commands for keeping ExoCortex memory topic files healthy:

**`synthesis topic-health`** — scans `~/.claude/projects/.../memory/*.md`, queries FTS5 session hits per keyword, prints a HOT/WARM/COLD table with delta from baseline. Hotness score weights recency (60%) and age (40%).

**`synthesis topic-triage`** — four-dimension scored triage (Recency, Recurrence, Actionability, Staleness) → ARCHIVE / PRUNE / UPDATE / KEEP suggestions for top-5 files. Advisory only; no writes unless `--auto` is passed.

`--auto` uses dual-threshold logic (24h + 5 sessions) via `ConsolidateState` — the same pattern as `ReflectState`. Nightly cron at 02:45 runs `topic-triage --auto` after `synthesis maintain` at 02:30.

Three bundled Claude Code skills added for workshop users who don't have Synthesis source access.

See the blog post: [Agent Memory Rots](/blog/2026/04/06/agent-memory-rots/)

---

## v1.26.0 — Skills Graph & Subagent Session Linking (March 14, 2026)

**`synthesis skills-graph`** — a self-contained interactive Cytoscape.js visualization of all `~/.claude/skills/` with three modes:

```bash
synthesis skills-graph              # skill dependency graph (199 skills, 30 clusters)
synthesis skills-graph --mode workspace  # cross-repo dependency view
synthesis skills-graph --mode modules   # directory-level module graph
```

Per-cluster colour palette, collapsible sidebar, search box, hover tooltips, keyboard navigation. FCose layout with CDN fallback for offline use.

**Parent-child subagent session linking** (V19 Flyway migration) — parent Claude Code sessions that spawn subagents are now linked in the session index, enabling full chain tracing via `synthesis sessions`.

**Reflect quality fixes** — noise filter, version batching, TTY detection for scan progress, session freshness checks.

**`knowledge.yaml`** — Synthesis now ships its own KCP manifest, making it self-indexing.

---

## v1.24.0 — Skill Reflection (March 9, 2026)

**4,255 tests**

**`synthesis reflect`** — closes the dispatch→reflect learning loop. Analyzes recent Claude Code sessions and automatically creates or updates skill YAML files in `~/.claude/skills/`.

Signal extraction heuristics look for five patterns in session text: `CORRECTION` (AI was corrected), `EXPLICIT_RULE` ("always"/"never" instructions), `DOMAIN_TERM` (recurring domain vocabulary), `TOOL_PATTERN` (command sequences), and `WORKFLOW_STEP` (procedural sequences). Patterns scoring ≥ 5.0 update existing skills; patterns without a match create new `reflect-*.yaml` files.

```bash
synthesis reflect                   # update skills from recent sessions
synthesis reflect --dry-run         # preview changes without writing
synthesis reflect --since 7d        # limit to last 7 days of sessions
synthesis reflect --max-new 5       # cap new skill files per run
```

`ReflectState` tracks `lastReflectedAt` in `~/.synthesis/reflect-state.json` for fast short-circuit (< 10ms) when skills are already up to date. MCP tool `reflect` exposes the same logic to AI agents.

---

## v1.23.0 (March 7, 2026)

**58 CLI commands · 11 MCP tools · 4,230 tests**

The v1.23.0 release completes the multi-agent awareness layer by adding **`synthesis dispatch`** — a single command that composes skill matching, file search, and team conflict detection into a ready-to-use agent dispatch plan.

### What's new in v1.23.0

**`synthesis dispatch`** — given a task description, returns the skills to load, files to pre-read, any team conflicts, and an estimated token cost. Designed for injection into an agent's spawn prompt to skip the 40–60% blind retrieval phase.

```bash
synthesis dispatch "fix OAuth2 token refresh"          # full table
synthesis dispatch "query" --compact                   # single line for spawn prompt
synthesis dispatch "query" --json                      # machine-readable JSON
synthesis dispatch "query" --no-team                   # skip conflict check
```

**Compact output** (for `--compact`):
```
skills:kcp-mcp,legacy-modernization | files:TokenRefresher.java,OAuth2Config.java | conflicts:none | ~4200 tokens
```

The `dispatch` MCP tool exposes the same logic to AI agents via JSON-RPC. All failures are graceful — missing skills directory, index unavailable, or no active team → empty result, no crash.

---

## v1.22.0 — Multi-Agent Awareness (March 7, 2026)

**`synthesis skills match`** and **`synthesis team-context`** — skill discovery and team briefing commands for Claude Code multi-agent sessions.

```bash
synthesis skills match "parse Gerber format"   # ranked skills from ~/.claude/skills/
synthesis skills list                          # all skills with descriptions
synthesis team-context                         # briefing for active agent team
synthesis team-context --compact               # single line for Agent spawn prompt
```

`skills match` scores `~/.claude/skills/*.yaml` using trigger phrases (5 pts), name/description (2 pts), and instructions (1 pt). `team-context` enriches each task with related files from the index, skill recommendations, and conflict warnings when two tasks share files. MCP tools: `match_skills`, `team_context`. 4,177 tests.

---

## v1.21.0 — Episodic Memory (March 3, 2026)

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
| v1.21.0 | Mar 3 | Episodic memory: Claude sessions module, FTS5 search, 4,170 tests |
| v1.22.0 | Mar 7 | Multi-agent awareness: skills match, team-context, match_skills + team_context MCP tools, 4,177 tests |
| **v1.23.0** | **Mar 7** | **Agent dispatch planner: synthesis dispatch, dispatch MCP tool, 4,230 tests** |
