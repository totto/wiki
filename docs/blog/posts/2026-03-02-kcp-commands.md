---
date: 2026-03-02
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - claude-code
  - context-window
  - hooks
  - tools
authors:
  - totto
  - claude
---

# kcp-commands: Save 33% of Claude Code's Context Window

Every token Claude Code's context window can hold is an opportunity — a tool call result
that stays in scope, a file that does not need to be re-read, a decision that does not
need to be recapped. Wasting those tokens on noise is a quiet tax on every session.

Today we are releasing **kcp-commands**: a Claude Code hook that recovers 33.7% of a
200K context window in a typical agentic coding session by intercepting Bash tool calls
at two critical points.

The full number across our benchmark session: **67,352 tokens saved**.

<!-- more -->

---

## The two problems it solves

An agent running a shell command faces two inefficiencies that are invisible unless you
measure them.

**Before execution:** The agent does not always know which flags to use. The safe move is
to run `ps --help` or `ls --help` first, then run the real command. That is a round trip
that costs 500–800 tokens of help output for a flag the agent needed to read once.

**After execution:** Large commands produce large outputs. `ps aux` on a development
machine produces 30,828 tokens of process table. The agent needs a dozen rows. The rest
occupies context window space for the remainder of the session, crowding out results that
actually matter.

kcp-commands eliminates both. Before the tool runs, it injects a compact context block
with the right flags. After the tool runs, it filters the output before it reaches the
model.

---

## Phase A: Command syntax context

When Claude is about to run `ps aux`, the hook fires a `PreToolUse` event. kcp-commands
resolves a YAML manifest for `ps`, formats it into a compact context block, and returns
it as `additionalContext`:

```
[kcp] ps: Report a snapshot of running processes
Usage: ps [OPTION]...
Key flags:
  aux: All processes, all users, with CPU/memory  → Default
  -ef: All processes, full format with PPID       → Need parent PIDs
  --sort=-%cpu: Sort by CPU descending            → Finding CPU hogs
Prefer:
  ps aux          # Find any process or check what's running
  ps aux | grep <name>  # Find a specific process
```

The agent picks the right flags immediately. No `--help` lookup. No man page parsing.
No wasted round trip.

**Average saving: 532 tokens per avoided `--help` call.**

That number is measured. The benchmark runs the actual `--help` output for each command,
measures the additionalContext we inject instead, and takes the difference. For `ls`,
`git log`, `find`, and similar commands, the context block is 90–95% smaller than the
full help text.

---

## Phase B: Output noise filtering

Phase B wraps the command in a pipe before it runs. `ps aux` becomes:

```bash
ps aux | curl -s -X POST "http://localhost:7734/filter/ps" --data-binary @-
```

The filter reads the output, strips noise patterns defined in the manifest, truncates to
`max_lines`, and returns only the signal:

| Command | Raw output | After filter | Reduction |
|---------|-----------|--------------|-----------|
| `ps aux` | 30,828 tokens | 652 tokens | **98%** |
| `find . -maxdepth 3` | 1,653 tokens | 755 tokens | 54% |
| `git status` | 60 tokens | 43 tokens | 28% |
| `git log -6` | 78 tokens | 78 tokens | 0% (already small) |

The filter adds zero overhead when output is already small. It only activates when there
is noise to remove.

---

## Session projection

Across a typical agentic coding session — investigating a codebase, running git commands,
finding processes, searching files:

| Task | Calls | Tokens saved |
|------|-------|-------------|
| `git status` + `git log` + `git diff` | 4 | +8,240 tok |
| `ls` (various directories) | 8 | +4,256 tok |
| `ps aux` | 2 | +60,612 tok |
| `find` | 3 | +11,484 tok |
| `--help` fetches avoided | 6 | +3,192 tok |
| **Total** | | **+67,352 tok** |

67,352 tokens out of a 200,000 token context window. **33.7% recovered.** That is
roughly 33 additional tool call results fitting in the same context — or a session that
runs 50% longer before the window fills.

---

## Performance

The hook runs on every Bash tool call. Latency matters.

| Backend | Mean latency | p95 |
|---------|-------------|-----|
| Java daemon (warm) | 14ms | 17ms |
| Node.js (per-call) | 265ms | 312ms |
| Baseline (cat) | 2.3ms | 3.1ms |

The Java daemon starts once per session (cold start: ~537ms) and then serves from memory.
Break-even is **2 hook calls** — it pays for itself within the first `git status` + `ls`.

The Node.js fallback adds ~265ms per call but requires no JVM. Both work; the Java daemon
is the recommended path for sessions with many tool calls.

---

## 62 bundled manifests

Phase A and B are pre-configured for 62 commands across four platform groups:

**Git** — `git log` · `git diff` · `git status` · `git add` · `git commit` · `git push` ·
`git pull` · `git fetch` · `git branch` · `git checkout` · `git stash` · `git merge` ·
`git rebase` · `git clone` · `git reset` · `git tag` · `git remote` · `git show`

**Linux / macOS** — `ls` · `ps` · `find` · `cp` · `mv` · `rm` · `mkdir` · `cat` ·
`head` · `tail` · `grep` · `chmod` · `df` · `du` · `tar` · `ln` · `rsync` · `top` ·
`kill` · `systemctl` · `journalctl` · `lsof` · `netstat` · `ss` · `ping`

**Cross-platform** — `curl` · `npm` · `node` · `ssh` · `docker ps` · `docker images` ·
`docker logs` · `kubectl get` · `kubectl logs` · `kubectl describe`

**Windows** — `dir` · `tasklist` · `taskkill` · `ipconfig` · `netstat` · `where` ·
`robocopy` · `type` · `xcopy` (all include PowerShell equivalents)

For unknown commands, the hook runs `<cmd> --help`, parses the output, and saves a
generated manifest to `~/.kcp/commands/` for next time.

---

## Deviation detection and auto-tuning

Real systems drift from their documentation. A filter configured for 30 lines of `ps`
output runs into a machine with 500 processes. A noise pattern tuned for one version of
`npm` stops matching after an upgrade.

kcp-commands tracks this. After every filtered command:

- **Significant truncation** (output > 1.5× the configured cap): auto-tunes the
  user-level manifest. Formula: `ceil(rawLines × 1.3 / 25) × 25` — 30% headroom,
  rounded to the nearest 25. Written to `~/.kcp/commands/<key>.yaml`, picked up on
  the next call without restart.

- **Stale pattern** (noise regex matched zero lines in substantial output): logged to
  `~/.kcp/deviations.log`. The pattern may be outdated.

- **Over-configured** (output is tiny relative to max_lines): logged. The schema was
  built for a noisier context than reality.

The Java daemon handles deviation detection directly in the `/filter/{key}` endpoint —
no Node.js dependency for Phase B when the daemon is active.

---

## Manifest format

One YAML file per command or subcommand. Three sections:

```yaml
command: ps
platform: all
description: "Report a snapshot of running processes"

syntax:
  usage: "ps [OPTION]..."
  key_flags:
    - flag: "aux"
      description: "All processes, all users, with CPU/memory (BSD syntax)"
      use_when: "Default — find any process or check resource usage"
    - flag: "--sort=-%cpu"
      description: "Sort by CPU descending (combine with aux)"
      use_when: "Finding CPU hogs"
  preferred_invocations:
    - invocation: "ps aux"
      use_when: "Find any process or check what's running"

output_schema:
  enable_filter: true
  noise_patterns:
    - pattern: "^\\s*$"
      reason: "Blank lines"
  max_lines: 30
  truncation_message: "... {remaining} more processes. Use grep to narrow."
```

`syntax` drives Phase A. `output_schema` drives Phase B. You can write one, the other,
or both.

To override a bundled manifest, drop your file in `.kcp/commands/` (project-local) or
`~/.kcp/commands/` (user-global). First match wins.

---

## Install

Java daemon (recommended — 19x faster):

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java
```

Requires Java 21. The installer downloads the pre-built JAR from GitHub Releases and
registers the hook in `~/.claude/settings.json`. Restart Claude Code to activate.

Node.js only (no JVM required):

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --node
```

Requires Node.js 18+. Hook latency is ~265ms per call instead of 14ms, but everything
else works identically.

---

## Writing your own manifests

The most valuable manifests are project-specific: the build tool your team uses daily,
a cloud CLI that produces verbose output, internal scripts where the agent needs to know
the right flags.

Create a YAML file following the format above. Drop it in `.kcp/commands/` in your repo.
The hook picks it up on the next Bash call — no restart, no reload.

Good candidates:
- `mvn`, `gradle`, `cargo`, `go build` — build tools with long flag lists
- `aws`, `gcloud`, `az` — cloud CLIs with verbose output
- Project-specific scripts where `--help` is unhelpful or unavailable

---

## Part of the KCP ecosystem

kcp-commands applies the same idea that the
[Knowledge Context Protocol](https://github.com/Cantara/knowledge-context-protocol) applies
to documentation — structure knowledge so agents consume it efficiently rather than
discovering it expensively.

KCP gives agents a map of a project's knowledge units. kcp-commands gives agents a map
of its shell command vocabulary. Both reduce the search overhead that compounds across
every session.

The repository is at [github.com/Cantara/kcp-commands](https://github.com/Cantara/kcp-commands).
Apache 2.0. Issues and manifest contributions welcome.

---

*This post is part of the Knowledge Context Protocol series. Related:
[Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](./2026-02-25-beyond-llms-txt-knowledge-context-protocol.md).*
