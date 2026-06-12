---
date: 2026-03-28
slug: kcp-dashboard-observability-for-the-kcp-ecosystem
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - kcp-dashboard
  - claude-code
  - observability
  - tui
  - go
authors:
  - totto
  - claude
---

# kcp-dashboard: Observability for the KCP Ecosystem

The KCP toolchain has been running in the background for weeks. kcp-commands injects manifests before Bash calls. kcp-memory indexes sessions and tool events. Events accumulate in `~/.kcp/usage.db` and `~/.kcp/memory.db`. The machinery works. But until today, the only way to know whether it was working well was to grep through databases and trust the numbers.

Trust is not observability. You cannot improve what you cannot see.

Today we are releasing **kcp-dashboard v0.22.0** -- a terminal UI that reads both KCP databases and shows you what the guidance layer is actually doing: which commands are guided, how often manifests leave the agent needing more help, what sessions look like, and where the gaps are.

<!-- more -->

![kcp-dashboard v0.22.0 — live terminal UI: 159 commands guided, 69% manifest coverage, 3 of 53 searches recalled prior work, session profile histogram, commands guided bar chart](/assets/images/blog/kcp-dashboard-v0.22.0-screenshot.webp)

---

## The fabricated metrics story

The first version of the dashboard showed a headline number: "67,352 tokens saved -- 33.7% context window recovered." It was a satisfying number. It was also wrong.

An Opus analysis of the underlying math revealed three problems. First, the per-command savings figure of 83% was a mathematical tautology -- the formula `x*5 / (x*6)` yields approximately 83% regardless of the input. It was measuring a constant, not a signal. Second, the 6x multiplier used for the counterfactual was a single number applied uniformly, but actual ratios vary wildly: 0.28x for `ps` to 258x for the `git log` man page. Third, the counterfactual itself was false. Claude already knows common Unix commands from training data. It would not run `--help` for `ls` or `grep` even without KCP. The "savings" were measured against a scenario that would not occur.

The corrected dashboard does not claim tokens saved. It reports **tokens of context delivered** -- the actual volume of manifest content injected into the context window. That number is real. It is roughly 9,800 tokens across the measured period. What the agent did with that context -- whether it led to better flag choices, fewer retries, faster sessions -- is a separate question with a more complex answer.

This is the Scandinavian approach: say what you can prove, not what sounds impressive.

---

## What the dashboard shows

kcp-dashboard reads two SQLite databases in read-only WAL mode: `~/.kcp/usage.db` (RFC-0017 telemetry from kcp-commands) and `~/.kcp/memory.db` (session index from kcp-memory). It auto-refreshes every two seconds. Four panels present the data.

### Overview

The top panel shows the headline numbers for the selected time window:

- **Commands guided**: the count of inject events -- Bash calls where kcp-commands delivered a manifest
- **~9.8k tokens of context delivered**: the total manifest content injected, honestly measured
- **69% manifest coverage**: the fraction of Bash tool calls that matched a KCP manifest
- **Sessions indexed**: how many sessions kcp-memory has processed
- **Search recall rate**: shown in three states -- working, partially working, or not working (historically 0% due to a bug described below, now fixed)

### Guidance Effects

This panel answers: is the guidance actually helping?

The data source is `memory.db`'s tool_events table -- over 15,000 events spanning 25 days of real usage. Four metrics are computed:

**Manifest coverage bar** -- "69% of Bash calls are guided." This is the single most important number. It shows what fraction of the agent's command-line work has KCP context available. The remaining 31% are commands without manifests -- the coverage gap where kcp-commands has no opinion.

**Filtered retry rate** -- the same action command invoked within 90 seconds in the same session. This is the signal that a manifest may have provided the wrong flags or missed a required argument. The filter is important: iterative commands like `ls`, `grep`, `cat`, and `head` are excluded because re-running them is workflow, not failure. Only action commands (build, deploy, test) count as retries.

**Help followup rate** -- `--help` invoked within 5 minutes of a manifested command. The rate is approximately 1.2%. That is low, and the interpretation is straightforward: manifests rarely leave Claude needing to check the man page for additional information. The manifest answered the question.

**Quality alerts** -- the top 5 worst-scoring manifests ranked by retry rate plus help followup rate, with call counts. This is the prioritized improvement list: which manifests should be rewritten first.

### Session Profile

This panel answers: what does a typical agent session look like?

The data comes from `memory.db`'s sessions table -- 3,742 indexed sessions. The histogram breaks them by turn count:

| Turns | Sessions | Share |
|-------|----------|-------|
| 1-5 | ~1,684 | 45% |
| 6-20 | ~449 | 12% |
| 21-50 | ~861 | 23% |
| 51-100 | ~374 | 10% |
| 100+ | ~374 | 10% |

The average session has 78 turns and 42 tool calls. Nearly half of all sessions are very short -- quick lookups, single-file edits, one-question answers. But 20% of sessions run past 50 turns, and those long sessions are where guidance quality matters most. A bad manifest injected at turn 3 of a 100-turn session can cascade through the remaining 97 turns.

### Commands Guided

A bar chart showing which commands receive the most manifest injections. `ls`, `grep`, `git log`, `kubectl`, and a handful of build tools dominate. The distribution follows a power law: a small number of commands account for the majority of guidance events. This tells you where manifest quality improvements will have the most impact.

### Memory Searches

The final panel shows recent search queries against the session index and the current recall rate. Historically this rate was 0% -- every search returned nothing -- for reasons explained in the next section. As of v0.21.0, the FTS index is populated and searches return results.

---

## Two bugs the dashboard found

The dashboard was the forcing function that revealed both of these. They had been present for weeks, invisible, silently degrading the system.

### kcp-memory FTS returning 0 results

All 3,742 indexed sessions had NULL values in `first_message` and `all_user_text`. The FTS5 virtual table was technically built and queryable -- it just contained no searchable text. Every query returned an empty result set.

The cause was a one-character category mismatch. The `SessionParser` checked `"human".equals(type)` when extracting user messages from JSONL transcripts. But Claude Code transcript format uses `"user"`, not `"human"`. The parser silently skipped every user message in every session. The sessions were indexed with turn counts, tool names, and file paths -- but with no text content.

The fix in kcp-memory v0.21.0 was a one-line change plus a regression test. Running `kcp-memory scan --force` rebuilt the FTS index with the correct message extraction. Search recall went from 0% to functional.

### PostToolUse hook silent failure

The `post-hook.sh` PostToolUse hook captures tool output for the `output_preview` field in event records. It checked `tool_response.output` to extract the Bash command output. But Claude Code sends Bash output in `tool_response.stdout`, not `tool_response.output`. The hook had been running on every tool call for weeks, writing events with empty `output_preview` fields every time.

Zero output lines were ever captured. The `exit_code_hint` heuristic -- which scans output for error patterns -- had no output to scan. Every event was marked as `exit_code_hint: 0` by default, giving a false impression that nothing ever failed.

The fix probes multiple fields in order: `stdout`, then `output`, then `content`, then `result`. A debug log at `~/.kcp/post-hook-debug.log` was added so future field-name changes become visible immediately instead of silently degrading.

These are not exotic bugs. They are the ordinary kind: a field name changed, a string constant was wrong, and the system kept running without complaint. The dashboard made the absence of data visible. Without it, both problems could have persisted indefinitely.

---

## What it does not yet measure

Honest reporting means being explicit about the gaps.

**First-attempt success rate** requires exit codes, which Claude Code hooks do not expose directly. The `exit_code_hint` heuristic scans output text for error patterns, but the PostToolUse output capture was broken until v0.21.0. Meaningful data starts accumulating now.

**Memory-assisted vs cold-start session comparison** would show whether sessions with episodic memory context perform differently from sessions without it. Only 2 sessions ever used `kcp_memory` MCP tools before the FTS bug was fixed -- there is no baseline. With FTS working, the data will build over the coming weeks.

**Help avoidance** was the original framing: "KCP manifests prevent --help lookups." The Opus analysis found that KCP sessions actually show a slightly higher `--help` rate (2.1%) compared to non-KCP sessions (1.4%). Claude already knows common commands from training. It does not need manifests to avoid `--help` for `git` or `ls`. The help-followup rate (~1.2%) measures something more useful: of the commands where a manifest was injected, how often did the agent still need to look up `--help` afterwards? That is the signal the dashboard now reports.

---

## Install

```bash
# Linux (amd64)
curl -fsSL https://github.com/Cantara/kcp-dashboard/releases/latest/download/kcp-dashboard-linux-amd64 -o ~/.local/bin/kcp-dashboard
chmod +x ~/.local/bin/kcp-dashboard

kcp-dashboard          # last 30 days
kcp-dashboard --days 7 # last week
```

Requires kcp-commands v0.20.0+ and/or kcp-memory v0.20.0+ to populate the databases it reads. Without data, the dashboard will run but show empty panels.

---

## Tech stack

kcp-dashboard is written in Go. The terminal UI uses [Bubble Tea](https://github.com/charmbracelet/bubbletea) for the application model and [Lip Gloss](https://github.com/charmbracelet/lipgloss) for styling -- both from the Charm.sh ecosystem.

SQLite access uses `modernc.org/sqlite`, a pure-Go SQLite implementation. This means `CGO_ENABLED=0` -- the binary has no native dependencies. Download it, `chmod +x`, run it. No C compiler, no shared libraries, no container.

The dashboard opens both `~/.kcp/usage.db` and `~/.kcp/memory.db` in read-only WAL mode. It never writes. Auto-refresh runs every 2 seconds, re-querying both databases and updating the panels. On a typical dataset (15k events, 3.7k sessions), each refresh cycle completes in under 50ms.

---

## The broader picture

kcp-dashboard completes the observability layer for the KCP ecosystem. Three tools now cover three distinct functions:

| Tool | Role | Ships as |
|------|------|----------|
| [kcp-commands](https://github.com/Cantara/kcp-commands) | Proactive CLI guidance before Bash execution | Java daemon + shell hooks |
| [kcp-memory](https://github.com/Cantara/kcp-memory) | Episodic memory -- what happened in past sessions | Java daemon + MCP server |
| [kcp-dashboard](https://github.com/Cantara/kcp-dashboard) | Observability -- what effect the guidance is having | Go TUI binary |
| [opencode-kcp-plugin](https://github.com/nicholasgasior/opencode-kcp-plugin) | KCP for OpenCode sessions | Go plugin |

The pattern is: kcp-commands acts, kcp-memory remembers, kcp-dashboard observes. Each tool reads structured data that the others produce. None of them require the others to run -- they are independent binaries with shared file conventions -- but together they form a feedback loop: guidance produces events, events reveal quality signals, quality signals improve guidance.

The dashboard was the piece that made the loop visible. The two bugs it found on its first day of operation are the proof.

---

- [kcp-dashboard on GitHub](https://github.com/Cantara/kcp-dashboard)
- [kcp-commands on GitHub](https://github.com/Cantara/kcp-commands)
- [kcp-memory on GitHub](https://github.com/Cantara/kcp-memory)
- [Knowledge Context Protocol spec](https://github.com/Cantara/knowledge-context-protocol)

---

*This post is part of the Knowledge Context Protocol series.*
*Previous: [The Manifest Quality Feedback Loop](./2026-03-24-kcp-manifest-quality-feedback.md)*
