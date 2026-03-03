---
date: 2026-03-03
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - claude-code
  - memory
  - sqlite
  - episodic-memory
  - knowledge-infrastructure
authors:
  - totto
  - claude
---

# kcp-memory: Give Claude Code a Memory

Every Claude Code session starts the same way. The context window is empty. The agent
has no recollection of what it did yesterday, which files it touched last week, or how
it solved a similar problem three sessions ago. Each session is day one.

That is not a limitation of the model. It is a missing infrastructure layer.

Today we are releasing **kcp-memory**: a standalone Java daemon that indexes
`~/.claude/projects/**/*.jsonl` session transcripts into a local SQLite database with
FTS5 full-text search. Ask it "what was I working on last week?" and it answers in
milliseconds.

<!-- more -->

![kcp-memory: three-layer memory model for Claude Code — working memory (context window), episodic memory (kcp-memory), semantic memory (Synthesis)](/assets/images/blog/kcp-memory-three-layer-model.png)

![Give Claude Code a memory — kcp-memory search terminal demo](/assets/images/blog/kcp-memory-slide-01-title.png)

---

## The missing layer

Context windows have grown from 4K to 200K tokens in three years. Retrieval-augmented
generation gives agents access to document stores. Model Context Protocol wires agents
to external tools. The ecosystem has invested heavily in what an agent can do in one
session.

What it has not built is a record of what happened across sessions.

![Every Claude Code session starts with Day One amnesia — no memory of yesterday, last week, or three sessions ago](/assets/images/blog/kcp-memory-slide-02-amnesia.png)

Human experts carry episodic memory: they remember which approaches failed, which
components are tricky, which patterns recur across projects. An agent with no episodic
layer has to rediscover all of it, every time.

The three layers of a well-equipped agent look like this:

| Layer | What it holds | Provided by |
|-------|--------------|-------------|
| **Working** | Current context — active files, recent tool results | Claude Code context window |
| **Episodic** | What happened in past sessions | **kcp-memory** |
| **Semantic** | What this codebase means — structure, relationships | [Synthesis](https://github.com/exoreaction/synthesis) |

kcp-memory fills the middle layer. It does not compete with Synthesis — it is
complementary. Synthesis answers "what do I know about this codebase?" kcp-memory
answers "what did I do here before?"

![The three layers of a well-equipped agent: Working Memory (context window), Episodic Memory (kcp-memory), Semantic Memory (Synthesis)](/assets/images/blog/kcp-memory-slide-03-three-layers.png)

---

## What it indexes

Claude Code writes every session to `~/.claude/projects/<slug>/<session-id>.jsonl`. Each
line is a JSON object representing one turn: human message, assistant response, or tool
result.

![Enter kcp-memory: ~/.claude/projects/**/*.jsonl → Java daemon → ~/.kcp/memory.db with FTS5 full-text search](/assets/images/blog/kcp-memory-slide-04-architecture.png)

kcp-memory walks that directory, parses each file, and extracts:

- **Session metadata**: project directory, git branch, model, start/end timestamps
- **Turn count** and **tool call count**
- **Tool names** used (distinct, ordered by first use)
- **File paths** touched (from `Read`, `Edit`, `Write` tool inputs)
- **User messages**: the first message (for quick scanning) and all human turns
  concatenated (for full-text search)

Everything lands in a single `~/.kcp/memory.db` SQLite file with an FTS5 virtual table
over the session content. A 2,000-session history occupies roughly 50MB.

![Extracting structure from session transcripts — JSONL structure with 5 extracted fields: metadata, turns, tools, file paths, user messages](/assets/images/blog/kcp-memory-slide-05-jsonl-parsing.png)

---

## The CLI

![The CLI experience — scan, search, list, stats subcommands with example output](/assets/images/blog/kcp-memory-slide-09-cli.png)

```bash
# Index all sessions (incremental — only new/changed files)
kcp-memory scan

# Search across everything you've ever done
kcp-memory search "OAuth implementation"
kcp-memory search "database migration flyway"
kcp-memory search "how to deploy kubernetes"

# List recent sessions
kcp-memory list
kcp-memory list --project /src/myapp

# Aggregate statistics
kcp-memory stats
```

A stats output from a real session history:

```
[kcp-memory] statistics
─────────────────────────────────
  Sessions:    847
  Turns:       12,431
  Tool calls:  38,209
  Oldest:      2026-01-15T09:12:00Z
  Newest:      2026-03-03T14:55:00Z

  Top tools:
    Read                      14,821
    Bash                       9,442
    Edit                       7,103
    Glob                       3,218
    Grep                       2,901
    Write                        644
```

A search result:

```
  2026-02-18  /src/cantara/kcp-commands
  e3ba3fd     turns=24  tools=67
  "add Phase B output filtering to the ansible manifest"

  2026-02-11  /src/exoreaction/lib-pcb
  a91c2f0     turns=18  tools=41
  "implement the Gerber export for copper layers"
```

![Actionable insights from your coding history — stats showing 847 sessions, 38,209 tool calls, top tools breakdown](/assets/images/blog/kcp-memory-slide-10-insights.png)

---

## The daemon

kcp-memory runs as a local HTTP daemon on port 7735:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness check + session count |
| `/search?q=...&limit=20` | GET | FTS5 full-text search |
| `/sessions?project=...&limit=50` | GET | List recent sessions |
| `/stats` | GET | Aggregate statistics |
| `/scan?force=true` | POST | Trigger an incremental scan |

Built on `com.sun.net.httpserver` with virtual threads — the same architecture as
kcp-commands. Cold start is under 2 seconds. Queries return in under 5ms on a 1,000-session
database.

The daemon runs an initial scan on startup and re-scans every 30 minutes in the
background. Existing sessions that have not changed since the last scan are skipped.

![A lightweight background daemon built on virtual threads — 5 API endpoints on port 7735, cold start under 2 seconds](/assets/images/blog/kcp-memory-slide-06-daemon.png)

---

## PostToolUse hook

For near-real-time indexing, wire the hook into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [{"type": "command", "command": "~/.kcp/memory-hook.sh"}]
      }
    ]
  }
}
```

The hook fires after every tool call and triggers an async scan. It checks whether the
daemon is running with a 500ms timeout and fires a background POST to `/scan` if it is.
Total overhead: under 1ms on the Claude Code side. If the daemon is not running, the
hook exits silently. It never blocks.

![Near-real-time indexing via the PostToolUse hook — hook config and flow: tool call → memory-hook.sh → async POST /scan → FTS5 index updated](/assets/images/blog/kcp-memory-slide-08-hook.png)

---

## Performance

| Operation | Time |
|-----------|------|
| Initial scan (1,000 sessions) | ~8 seconds |
| Incremental scan (unchanged sessions) | ~0.5 seconds |
| FTS5 search query | <5ms |
| List query (recent 50) | <2ms |
| Daemon cold start | ~1.8 seconds |

The incremental scan checks the file modification timestamp against the `scanned_at`
timestamp in the database. A session that has not changed since the last scan is skipped
in a single SQL lookup — the entire scan of an unchanged 1,000-session history takes
under a second.

![Engineered for millisecond latency — search <5ms, list <2ms, cold start ~1.8s, incremental scan ~0.5s, initial scan ~8s](/assets/images/blog/kcp-memory-slide-07-performance.png)

---

## Install

![Frictionless installation, zero bloat — one curl install, Zero Spring, zero frameworks, zero cloud calls](/assets/images/blog/kcp-memory-slide-12-install.png)

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-memory/main/bin/install.sh | bash
```

The installer:
1. Downloads `kcp-memory-daemon.jar` from GitHub Releases to `~/.kcp/`
2. Starts the daemon on port 7735
3. Runs an initial scan of `~/.claude/projects/`
4. Prints the PostToolUse hook configuration

Requires Java 21. No source clone needed.

**Alias** (add to `~/.bashrc` or `~/.zshrc`):

```bash
alias kcp-memory='java -jar ~/.kcp/kcp-memory-daemon.jar'
```

---

## How it relates to kcp-commands

kcp-commands and kcp-memory are designed to run alongside each other. They share the
`~/.kcp/` directory and use adjacent ports:

| | kcp-commands | kcp-memory |
|--|-------------|-----------|
| **Port** | 7734 | 7735 |
| **Hook** | PreToolUse | PostToolUse |
| **Stores** | Nothing (stateless) | `~/.kcp/memory.db` |
| **Reads** | 283 command manifests | `~/.claude/projects/**/*.jsonl` |
| **Answers** | "How do I run this command?" | "What did I do in this project?" |

kcp-commands saves context window by giving Claude better command knowledge before
execution. kcp-memory makes past sessions retrievable. They solve different problems at
different points in the tool call lifecycle — one before, one after.

![Ecosystem synergy: kcp-commands (7734, PreToolUse) vs kcp-memory (7735, PostToolUse) — complementary tools covering the full tool call lifecycle](/assets/images/blog/kcp-memory-slide-11-ecosystem.png)

The [v0.2.0 roadmap](https://github.com/Cantara/kcp-memory) adds a direct event stream
from kcp-commands: tool events will be written to `~/.kcp/events.jsonl` and ingested by
kcp-memory, giving the episodic index tool-level granularity rather than session-level
granularity.

![The v0.2.0 roadmap: Tool-level granularity — kcp-commands → individual tool events → ~/.kcp/events.jsonl → kcp-memory, enabling per-tool resolution in the episodic index](/assets/images/blog/kcp-memory-slide-13-roadmap.png)

---

## Source

The project is at
[github.com/Cantara/kcp-memory](https://github.com/Cantara/kcp-memory). Apache 2.0.

120 lines of SQL and schema, ~1,100 lines of Java across twelve source files. The only
dependencies are `sqlite-jdbc`, `jackson-databind`, and `picocli`. No Spring, no
framework, no cloud calls.

The [KCP ecosystem](https://github.com/Cantara/knowledge-context-protocol) now has three
tools covering three different surfaces of the AI coding workflow:

- **kcp-commands** — CLI vocabulary (283 command manifests, PreToolUse hook)
- **kcp-memory** — session history (SQLite + FTS5, PostToolUse hook)
- **opencode-kcp-plugin** — codebase structure (knowledge.yaml in system prompt)

![The complete AI coding workflow surface — kcp-commands (CLI vocabulary, PreToolUse), kcp-memory (session history, PostToolUse), opencode-kcp-plugin (codebase structure, knowledge.yaml)](/assets/images/blog/kcp-memory-slide-14-workflow-surface.png)

---

*This post is part of the Knowledge Context Protocol series.*
*Previous: [KCP Comes to OpenCode: The First AI Coding Tool Plugin](./2026-03-03-opencode-kcp-plugin.md)*
