---
description: "Building memory layers for AI agents was easy. Keeping them from decaying required a system that detects staleness, repairs drift, and prunes dead entries."
date: 2026-04-06
categories:
  - Knowledge Context Protocol
  - Knowledge Infrastructure
  - AI Agents & the Agentic Web
tags:
  - synthesis
  - exocortex
  - agent-memory
  - memory-maintenance
  - topic-health
  - topic-triage
  - kcp
  - sdd
authors:
  - totto
image: assets/images/agent-memory-rots/slide-01.webp
---

# Agent Memory Rots. Here's How We Stopped It.

Five weeks ago I wrote about the three-layer memory architecture for AI agents: working memory (the context window), episodic memory (indexed session transcripts), and semantic memory (a workspace knowledge graph). The prescription was "build these layers." Yesterday I shipped the maintenance system that keeps them from decaying.

Building the layers was the easy part.

![Agent Memory Rots — diagnostic telemetry and behavioral heuristics for maintaining the ExoCortex. 3,000+ sessions indexed. 65,905 files. Memory degradation imminent.](/assets/images/agent-memory-rots/slide-01.webp)

<!-- more -->

![Agent Memory Rots: Why Your AI Agent "Lies" and How to Fix It — full infographic covering the three pillars, four degradation patterns, behavioral maintenance solution, and six core design principles](/assets/images/agent-memory-rots/infographic.webp)

---

## The Part Nobody Writes About

The three-layer post got traction because the diagnosis was clear: your agent starts every session from zero, and the fix is to give it episodic and semantic memory layers alongside the context window. I run that full stack — the ExoCortex — and have for ten weeks now. Claude Code as the agent, Synthesis for semantic memory and session indexing, MEMORY.md as a routing index, 20+ topic files for deep context, 475 skills in YAML, 3,000+ sessions indexed via FTS5, 65,905 files across 11 workspaces.

The stack works. The agent arrives knowing what it needs to know. Session start is not a blank slate. The benchmarks hold: 35-40% fewer tool calls with proper knowledge infrastructure.

![The Baseline: The Three-Layer ExoCortex Architecture — working memory (context window), episodic memory (session transcripts indexed via FTS5), semantic memory (workspace graph). Baseline holds: 35-40% fewer tool calls. Propagation failure detected here.](/assets/images/agent-memory-rots/slide-02.webp)

But here is what the original post did not say, because I had not lived through it yet: memory that is not maintained becomes memory that lies. And a lying memory system is worse than no memory system at all.

This is the Phase 4 lesson at the memory level. In my February benchmarks, skill files beat baseline by 47% on warm tasks — and then performed *worse than having nothing* on cold tasks, because wrong context is worse than no context. Stale memory pointers do the same thing. They don't just fail to help. They actively mislead.

![The Pathology: Unmaintained Memory Actively Lies — +47% baseline beat on warm tasks, sub-zero degradation on cold tasks. Stale pointers do not just fail to help. They actively misdirect. Memory that is not maintained becomes memory that lies.](/assets/images/agent-memory-rots/slide-03.webp)

---

## Four Ways Memory Rots

I have been running the full three-layer stack in production since late January. Here are the specific rot patterns I observed, in the order I noticed them.

![Four Degradation Patterns in Agent Memory — (1) The Index Lies: routing index points to outdated paths; (2) New Knowledge Has No Home: insights accumulate in episodic but never propagate to semantic; (3) Topic Files Go Stale: engagement ends but the file stays; (4) Hot Topics Become Cold: accurate content, no longer relevant](/assets/images/agent-memory-rots/slide-04.webp)

### 1. Topic Files Go Stale

You add a topic file about a client engagement. It contains architecture notes, contact details, meeting summaries. The engagement ends. The file stays in your routing index. Every session, the model "knows" about a project that finished two months ago.

The danger is not that the file exists. The danger is that the routing index — MEMORY.md, in my case — still points to it. A session about an entirely different client can accidentally load the stale file via keyword overlap. The model then arrives with context about the wrong engagement, and you spend the first ten minutes unwinding assumptions it should never have made.

### 2. Hot Topics Become Cold

I worked intensively on lib-pcb for 11 calendar days in January. The topic file grew to hundreds of lines. Then I moved on. Eight weeks later, the file was still in the routing index, still loaded when certain keywords appeared in conversation. The model "knew" about lib-pcb's internal architecture, even when the session was about something entirely different.

This is subtler than staleness. The content is accurate — lib-pcb's architecture has not changed. But the relevance has. Loading 400 lines of lib-pcb context into a session about regulatory compliance is pure noise. It consumes context window space and pushes out content that actually matters.

### 3. New Knowledge Has No Home

Sessions accumulate insights that never propagate to topic files. I discover a build quirk in Synthesis. I debug a deployment issue. I make a decision about API design. All of this lives in the session transcripts — the episodic layer. None of it automatically updates the topic files — the semantic layer.

Over weeks, the gap widens. The episodic layer grows (3,000+ sessions). The semantic layer stays static (the same 20 topic files, many untouched for weeks). The model can find what happened via `synthesis sessions search`, but the structured knowledge it loads at session start drifts further from reality.

This is the propagation problem. Knowing what happened (episodic) does not automatically update what we know (semantic). That propagation is still manual in my stack. I suspect it is manual in everyone's stack, because the alternative — automated summarisation of sessions into structured knowledge — requires an LLM in the maintenance loop, which creates a circular dependency I will come back to.

### 4. The Index Lies

MEMORY.md says: "For Synthesis CLI patterns, read synthesis-notes.md." But synthesis-notes.md was written when Synthesis was at v1.15.0. It is now v1.27.0. Twelve minor versions of changes, new commands, new flags, changed behaviours. The pointer in MEMORY.md is valid — the file exists, the path is correct. The knowledge behind the pointer is stale.

A stale routing index does not produce an error. It produces quiet misdirection. The model loads synthesis-notes.md, reads about commands that no longer exist or flags that have changed, and proceeds with outdated assumptions. You only notice when the output is wrong, and by then you have spent tokens on reasoning from bad premises.

![The Quiet Misdirection Trap — (1) Trigger: user inputs query with overlapping keywords; (2) Routing: stale MEMORY.md is queried; (3) Loading: index confidently loads synthesis-notes.md into context window; (4) Poisoning: agent reads outdated commands and flags; (5) Output: token budget burned on reasoning from false premises. A stale routing index does not produce a crash. It produces quiet misdirection.](/assets/images/agent-memory-rots/slide-05.webp)

---

## The Principle: Freshness Beats Completeness

Running the full stack for ten weeks forced a principle I would not have articulated from theory alone:

**A thin, current index is worth more than a comprehensive, stale one.**

Five entries in MEMORY.md that are all accurate right now are more useful than fifty entries where thirty percent of the links point to outdated content. This feels counterintuitive — more knowledge should be better. But more knowledge is only better if the knowledge is true. When it is not, every additional entry is a potential misdirection.

The corollary: the maintenance burden of a memory system is proportional to its size. A small memory system that you can keep current is strictly better than a large one that rots. "Memory yields to reality. Always." is the operating principle. But you need infrastructure to enforce it, because the natural tendency is accretion without pruning.

![The Operating Principle: Freshness Beats Completeness — "Memory yields to reality. Always." 50 entries (30% stale) vs 5 accurate entries (100% fresh). Real-world validation: pruning from 25 to 19 tightly maintained topic files resulted in a smaller system that actively performs better.](/assets/images/agent-memory-rots/slide-06.webp)

---

## What We Built: topic-health and topic-triage

Synthesis v1.27.0 ships two new commands that address memory rot directly. Neither uses an LLM. Both run in milliseconds.

### topic-health: Who's Hot, Who's Cold

`synthesis topic-health` scans all markdown files in the memory directory, extracts keywords from filenames, and queries the session store via FTS5 to count how many sessions referenced each topic in the last 30 days. It then computes a hotness score:

```
hotness = 0.6 * (sessionHits / maxHits) + 0.4 * (1 - min(ageDays, 60) / 60)
```

The formula weights session engagement at 60% and recency at 40%. A topic file that appears in many recent sessions scores high. A topic file that nobody has referenced in weeks and has not been modified in two months scores low.

Output: a HOT / WARM / COLD classification for each file, sorted by hotness. HOT is anything above 0.6. WARM is 0.3 to 0.6. COLD is below 0.3.

![Telemetry Step 1: topic-health Behavioral Profiling — we do not analyze what files say, we analyze what they are used for. Scoring formula: 60% session engagement (hits in last 30 days) + 40% recency. HOT (>0.6): practitioner references daily, e.g. synthesis-notes.md. WARM (0.3-0.6): intermittent relevance. COLD (<0.3): untouched for 8+ weeks, e.g. lib-pcb.](/assets/images/agent-memory-rots/slide-08.webp)

The signal is behavioural, not content-based. We do not analyse what the topic files say to decide if they are stale. We look at whether the practitioner's sessions keep referencing the topic. If I am working on Synthesis development every day, `synthesis-notes.md` has high session hits and scores HOT. If I have not touched lib-pcb in eight weeks, its topic file has zero recent hits and scores COLD.

This distinction matters. Content analysis would require an LLM — you would need to read the file, understand what it says, and determine whether it is still accurate. Behavioural analysis requires only a count query against the FTS5 index. The implementation is ~250 lines of Java. No model call. No API key. No latency. The information it produces is less nuanced than what an LLM could tell you, but it is available in milliseconds and does not create a circular dependency.

### topic-triage: What Needs Attention

`synthesis topic-triage` goes a step further. It scores each topic file on four dimensions:

![Telemetry Step 2: topic-triage Dimensions of Decay — Recency (0.30 weight): 7 days = 1.0, 30+ days = 0.4. Recurrence (0.25): 3+ sessions = 1.0. Actionability (0.25): detects operational rules vs. historical notes by scanning for "always", "never", "must", "critical". Staleness (0.20, inverted): fresher files score mathematically higher.](/assets/images/agent-memory-rots/slide-09.webp)

- **Recency** (0.3 weight): When was the most recent session that referenced this topic? Within 7 days = 1.0. Within 14 days = 0.7. Within 30 days = 0.4. Older = 0.1.
- **Recurrence** (0.25 weight): How many distinct sessions reference this topic? Three or more sessions in the lookback window = 1.0. Scaled linearly below that.
- **Actionability** (0.25 weight): Does the file contain prescriptive content? It scans the first 50 lines for patterns like "always," "never," "must," "critical," "before," "instead of." The presence of these patterns suggests the file contains operational rules, not just historical notes.
- **Staleness** (0.2 weight, inverted): How long since the file was last modified? 60+ days = maximum staleness. The composite inverts this: `0.2 * (1 - staleness)`, so fresher files score higher.

The composite score determines a recommendation for the top 5 files needing attention:

```
composite = 0.30 * Recency + 0.25 * Recurrence + 0.25 * Actionability + 0.20 * (1 - Staleness)
```

Each file gets one of four recommendations:

![The Triage Action Matrix — ARCHIVE: staleness > 0.8 AND recurrence < 0.2, untouched and unreferenced, remove routing entry immediately. PRUNE: lines > 300 AND recurrence < 0.4, bloated file low engagement, cut dead context. UPDATE: recency < 0.4 BUT recurrence > 0.6, highly referenced but outdated, refresh facts to prevent hallucination. KEEP: all other baseline states, healthy active memory. Advisory only — the system highlights the anomaly; the human authorizes the cut.](/assets/images/agent-memory-rots/slide-10.webp)

- **ARCHIVE** — staleness > 0.8 and recurrence < 0.2. Nobody references this, and it has not been updated in a long time. Remove the routing entry.
- **PRUNE** — more than 300 lines with recurrence < 0.4. Large file, low engagement. Cut it down.
- **UPDATE** — recency < 0.4 but recurrence > 0.6. People keep referencing this topic, but the file itself is old. It needs a refresh.
- **KEEP** — everything else. No action needed.

Advisory only. No files are modified. The system tells you what to look at; the human decides what to cut.

### ConsolidateState: Preventing Redundant Runs

Running topic-triage twice in an hour is wasteful. Running it never is worse. `ConsolidateState` persists an atomic JSON file at `~/.synthesis/consolidate-state.json` tracking two values: when topic-triage last ran, and how many sessions existed at that time.

The `--auto` flag enforces a dual threshold: at least 24 hours since last run AND at least 5 new sessions since last run. Both conditions must be met. This prevents two failure modes:

- Running triage on a quiet weekend when nothing has changed (time threshold met, session threshold not met).
- Running triage every hour during an intensive work day (session threshold met, time threshold not met).

![Rate Limiting: Preventing Diagnostic Spam — Time since last run > 24 hours AND Sessions since last run >= 5 → AND Gate → Proceed to Triage. State persistence: ~/.synthesis/consolidate-state.json via atomic write (temp file + rename) to guarantee crash resilience. Running triage twice an hour is wasteful. Running it never is fatal.](/assets/images/agent-memory-rots/slide-11.webp)

The write is atomic — temp file plus rename — so a crash during persistence cannot corrupt the state file.

---

## The Nightly Cycle

The maintenance automation runs on the local machine:

```
02:30 Oslo — synthesis maintain  (re-indexes files, updates knowledge graph)
02:45 Oslo — synthesis topic-triage --auto  (evaluates dual threshold, scores memory files)
```

The topic-triage output appends to `~/.synthesis/topic-triage-log.jsonl` — one JSON record per run, with trigger type (auto or manual), sessions since last run, files scanned, and the scored suggestions with per-dimension breakdowns.

![The Protocol: The Nightly Maintenance Cycle — (1) Automation: topic-triage triggers quietly in the background; (2) Persistence: appends system state to topic-triage-log.jsonl; (3) Human Review: periodic visual check of the 5 surfaced files; (4) Advisory Action: human executes ARCHIVE, PRUNE, or UPDATE. This is not glamorous. It is the maintenance equivalent of taking out the trash. Why advisory? Automated pruning sounds attractive until it deletes the exact architectural context you needed for tomorrow's engagement.](/assets/images/agent-memory-rots/slide-12.webp)

I review the log periodically. When something shows as ARCHIVE, I check whether the routing entry in MEMORY.md should be removed. When something shows as UPDATE, I spend five minutes refreshing the topic file with current information. When something shows as PRUNE, I cut lines that are no longer relevant.

This is not glamorous work. It is the maintenance equivalent of taking out the trash. But the alternative — letting the memory system accumulate stale entries indefinitely — is how you end up with a routing index where the model loads outdated context in 30% of sessions and you cannot figure out why its responses are slightly wrong.

---

## Why No LLM in the Maintenance Loop

Both topic-health and topic-triage run without any LLM calls. This is a deliberate architectural choice, not a limitation.

If memory maintenance required an LLM, you would have a circular dependency: you need memory to use the LLM effectively (the whole point of the three-layer architecture), but you need the LLM to maintain memory. Every maintenance run would consume tokens. Every maintenance failure would require a model call to diagnose. The maintenance system would inherit the failure modes of the system it is maintaining.

![The Infinite Regress of LLM Maintenance — LLM-in-the-Loop: requires memory to use LLM, requires LLM to maintain memory, inherits failure modes, consumes tokens per run. Creates an infinite regress of maintenance. Behavioral Signals: count queries against FTS5, entirely local, ~250 lines of Java, 0 tokens consumed, 0 API calls. Runs quietly at 02:45. Model is bypassed. Keep your maintenance infrastructure simpler than the system it maintains.](/assets/images/agent-memory-rots/slide-07.webp)

The behavioural signal — session hits per topic keyword — is less sophisticated than what an LLM could produce. An LLM could read each topic file, compare it to recent session content, and generate a nuanced assessment of what is stale and what is still relevant. That assessment would be better than a hotness formula.

But the hotness formula runs in milliseconds, costs nothing, requires no API key, and works at 02:45 when no human is watching. It is good enough to surface the files that need attention. The human judgment about what to do with those files is where nuance matters, and that is where the human stays in the loop.

![Architectural Comparison — LLM-in-the-Loop vs Behavioral Heuristics: Latency (seconds to minutes vs milliseconds), Cost (token burn per run vs 0 API calls, strictly free), Failure Mode (hallucinated deletions vs manageable false-positives on keywords), Complexity (requires full agentic reasoning vs ~250 lines of local Java). Save the expensive LLM reasoning for the operational loop where it produces actual value.](/assets/images/agent-memory-rots/slide-13.webp)

The broader principle: keep your maintenance infrastructure simpler than the system it maintains. If the maintenance layer is as complex as the operational layer, you need a maintenance system for the maintenance system, and you have an infinite regress.

---

## Known Limitations (Honest)

### The False-Hot Problem

Topic-health extracts keywords from filenames. `java-refactoring.md` generates keywords "java" and "refactoring." If 40 sessions mention "Java" for unrelated reasons — I write a lot of Java — then `java-refactoring.md` scores HOT even if nobody has thought about Java refactoring patterns in weeks.

Short, generic filenames are worst. `mistakes-to-avoid.md` has keywords "mistakes" and "avoid." Every session where someone discusses avoiding anything triggers a false hit. Distinctive filenames like `ironclaw-infrastructure.md` perform better because "ironclaw" is a rare term.

The fix is probably TF-IDF weighting that penalises common terms, or embedding-based similarity that captures topical relevance rather than keyword overlap. I have not built that. The current formula is useful but noisy, and I know exactly where the noise comes from.

### The Episodic-Semantic Gap Remains Open

Knowing what happened in past sessions does not automatically update what the topic files say. I discover in a session that `synthesis export` now supports a `--filter` flag. That fact lives in the session transcript. It does not appear in `synthesis-notes.md`. The topic file is wrong by omission, and topic-triage has no way to detect this — it measures engagement, not accuracy.

Closing this gap properly requires either automated propagation (LLM reads sessions, updates topic files) or structured session annotations (the practitioner tags insights during sessions for later extraction). Both have costs. Automated propagation reintroduces the LLM dependency I want to avoid in maintenance. Structured annotations add friction to the session workflow.

![Telemetry Anomalies: Known System Limitations — (1) The False-Hot Problem: keyword overlap noise, generic filenames trigger false hits across unrelated sessions, fix requires TF-IDF weighting or embedding-based similarity. (2) The Episodic-Semantic Gap: errors of omission, triage measures engagement not factual accuracy, automated propagation reintroduces the LLM dependency trap.](/assets/images/agent-memory-rots/slide-14.webp)

`synthesis reflect` — the skill synthesis layer — is the closest thing I have to automated propagation. It reads sessions and generates YAML skill files. But it operates on skill files, not on memory topic files. Extending reflect to update memory topics is conceptually straightforward and practically tricky, because topic files have a different structure and a different failure mode than skills.

### The Warm/Cold Tension at the Memory Level

The Phase 3/4 benchmark finding — skills help for warm tasks, hurt for cold tasks — applies identically to memory topic files. A memory routing entry that points to the right topic file for the current task is a teleport. A routing entry that points to the wrong file is a trap.

Topic-triage reduces this risk by identifying stale entries, but it cannot eliminate it. The fundamental tension is that you cannot know at session start whether today's task will be warm (covered by existing topic files) or cold (not covered). Pre-loading too many topic file pointers wastes context. Pre-loading too few leaves the model uninformed. The optimal configuration is task-dependent, and you do not know the task until the session starts.

---

## What This Means for Anyone Building Agent Memory

You do not need my specific stack. The patterns transfer.

![Preventative Care: 6 Rules for Agent Memory — (1) Budget from Day One: rot is inevitable, build detection instrumentation immediately; (2) Measure Engagement > Content: what memory is used for matters more than what it says; (3) Keep Maintenance Simple: banish circular LLM dependencies from your telemetry; (4) Freshness Beats Completeness: 5 accurate entries are better than 50 stale ones; (5) Advisory, Not Automatic: the system surfaces the anomaly, the human authorizes the cut; (6) Nightly, Not Real-Time: instant maintenance adds complexity without proportional benefit. Memory yields to reality. Always.](/assets/images/agent-memory-rots/slide-15.webp)

**1. Budget for maintenance from day one.** If you are building a memory system for an AI agent — any memory system, any agent — plan for how you will maintain it. Not "eventually." On day one. The memory will rot. The question is whether you have instrumentation to detect the rot and a process to address it.

**2. Measure engagement, not just content.** Content analysis tells you what the memory says. Engagement analysis tells you what the memory is *used for*. The second signal is cheaper to compute and more actionable. If a memory artefact has not been referenced in 30 days, it does not matter how accurate its content is — it is noise in the system.

**3. Keep maintenance simpler than operations.** If your memory maintenance requires the same LLM that uses the memory, you have a circular dependency. Use cheaper signals — counters, timestamps, keyword hits — for the maintenance loop. Save the expensive reasoning for the operational loop where it produces value.

**4. Freshness beats completeness.** A small, current memory is better than a large, partially stale one. Prune aggressively. A routing index with five accurate entries beats one with fifty entries and fifteen stale ones. The stale entries are not neutral — they actively mislead.

**5. Make it advisory, not automatic.** The system should tell you what to look at. The human should decide what to cut. Automated pruning sounds attractive until it deletes the one topic file you needed for next week's engagement. Advisory-only output with human review is slower but safer, especially for a system where the cost of a bad deletion is re-creating knowledge from scratch.

**6. Nightly, not real-time.** Memory maintenance does not need to be instantaneous. A nightly pass that identifies files needing attention is sufficient for most workflows. Real-time maintenance adds complexity without proportional benefit — you are unlikely to notice a stale topic file mid-session, and by the time the session ends, the nightly pass is close enough.

---

## The Arc

The March post said: your agent has one memory layer and needs three. Build them.

This post says: you built them. Now they are rotting. Here is what the rot looks like, why it matters, and the tooling that detects it.

The next post will probably say: the detection works, but the propagation from episodic to semantic is still manual, and that is where the real friction lives. Each layer addresses the failure mode of the previous one. Memory management is no different.

Ten weeks in. 3,000+ sessions. 65,905 files indexed. 19 topic files in the routing index, down from a peak of about 25 — the ones that got pruned were all COLD. The system is smaller than it was a month ago, and it works better.

Freshness beats completeness. We validated it the hard way.

---

*Totto is the founder of eXOReaction, an enterprise architecture consultancy in Oslo. He builds Synthesis, the ExoCortex, and the KCP specification. Thirty-plus years of enterprise systems, currently figuring out how to keep AI memory from lying to him.*
