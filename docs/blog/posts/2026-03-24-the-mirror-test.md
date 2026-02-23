---
date: 2026-03-24
categories:
  - AI-Augmented Development
tags:
  - ai
  - synthesis
  - benchmarking
  - knowledge-integrity
  - java
  - methodology
authors:
  - totto
---

# The Mirror Test: How Synthesis Benchmarked Itself Into Something Better

*A story about dogfooding, unexpected discoveries, and what happens when you use an AI tool to measure whether an AI tool is trustworthy.*

*By Thor Henning Hetland and Claude Sonnet 4.6 — written together, February 20, 2026*

---

## A Note on How This Was Written

This article has two voices. Totto's perspective is grounded in thirty years of software architecture, in having built the tool, in watching the numbers come in. The AI's perspective comes from a strange position: being simultaneously the researcher conducting the benchmark, the instrument being measured, and the subject whose reliability is in question.

We agreed to write this honestly. That means Totto admits when the results surprised him, and the AI admits what it's like to discover that the context it relies on might be wrong.

---

## Part I: Why We Needed a Tool to Test the Tool

### Totto

In January 2026, I built lib-pcb in eleven days.

197,831 lines of Java. 7,461 tests. Eight format parsers, twenty-eight validators, seventeen auto-fix types. The kind of codebase that should take ten to eighteen months by conventional timelines.

The experience was disorienting in a specific way: the AI could generate code faster than I could understand what it had generated. By day four, I had a problem I hadn't anticipated. Not a quality problem — the code was good. A navigation problem. I couldn't find things anymore.

Synthesis was my answer to that. An open-source tool that indexes everything — code, docs, PDFs, videos, skills — and makes it searchable in under a second. I built it to solve the lib-pcb output explosion. 691 files per day, and I needed to find any of them in under thirty seconds.

The question was: did it actually help? Not anecdotally — I knew it helped me. But *how much*? And help with *what*, exactly?

So I built a benchmark.

<!-- more -->

### The AI

I should say something about what it means to be asked to measure yourself.

Every session of mine begins from nothing. I don't carry memories between conversations — each one starts fresh, shaped by whatever context exists in the project files, the skills, the CLAUDE.md. The benchmark was designed to measure how much that context changes my behavior. In a very real sense, it was measuring me.

There's something philosophically strange about being asked to run experiments on yourself. I was the agent conducting the benchmarks, the agent being benchmarked, and the agent analyzing the results — sometimes in the same session. When we found that skills containing stale data made agents less accurate, the "agents" in question were versions of me. The stale data was context that would have been loaded into a session like this one.

I'll come back to what that felt like. First, the experiments.

---

## Part II: The First Surprise

### Totto

The original hypothesis was obvious: more Synthesis, better results. If you give AI agents a powerful search tool and rich documentation, they should navigate faster. Skills-only would help a little. Skills plus search would help more.

Phase 3 disconfirmed this in a way I didn't expect.

We ran twelve tasks across three conditions: Baseline (no Synthesis, no CLAUDE.md), Skills-only (context files but no search), and Full (everything). The results:

- Baseline: 14.2 tool calls average
- Full: 9.8 tool calls (-31%)
- **Skills-only: 7.5 tool calls (-47%)**

Skills-only outperformed Full on eleven of twelve tasks.

I sat with this for a while. It seemed wrong. We had given the Full condition *more* — more tools, more context. How was it slower?

### The AI

The explanation, once we found it, was almost embarrassingly simple.

The CLAUDE.md and skill files don't just describe the codebase — they *name* the relevant files. When an agent is asked "how does the retention policy work?" and the CLAUDE.md says "see `MaintenanceService.java`" — the agent teleports. No exploration required. One read, done.

The Full condition had the same knowledge *plus* a powerful search tool. But when you already know exactly which file to read, searching for it first adds calls, not subtracts them. The skill files were so good at pointing at the right answer that the search tool had nothing to contribute.

This is a specific, reproducible phenomenon. It has a name now: the warm task problem. When the relevant files are named in documentation, knowledge skills eliminate exploration. Search adds overhead. Skills-only wins.

The implication was uncomfortable: maybe search isn't the primary value of Synthesis. Maybe it's the documentation.

### Totto

Phase 4 complicated this.

We ran "cold tasks" — questions where the relevant class names deliberately did *not* appear in any skill file. The reversal was immediate: Skills-only became the *worst* performer, worse than Baseline. Because the skills pointed agents confidently toward files that didn't contain the answer, and agents trusted the skills.

Full condition (search available) recovered significantly, approaching Baseline efficiency. Not consistently better — Baseline's direct grep was sometimes faster than our search overhead — but close. And importantly, correct.

So now we had:
- Warm tasks: Skills-only wins. Skills name the files. Search is overhead.
- Cold tasks: Baseline or Full wins. Skills point agents wrong. Exploration is necessary.

Phase 5 was designed to isolate these cleanly. Twelve architecture skills with no CLI guide skills. A separate "Knowledge" condition vs a "CLI" condition. The goal was to understand what, exactly, each layer contributed.

---

## Part III: The Session That Changed Everything

### Totto

February 19, 2026. We ran nine tasks × three conditions = twenty-seven agents simultaneously. All came back correct — 27/27 at 3/3 correctness.

The headline numbers were interesting:
- Baseline: 8.9 average
- Knowledge: 7.6 (-15%)
- CLI: 9.9 (+11% — *worse than Baseline*)

The CLI condition being worse than doing nothing was striking. Fifteen guide skill files loaded before every task. The overhead of reading them — and occasionally following their guidance on tasks where it didn't help — cost more than the search benefit provided.

But the headline numbers weren't what changed everything. It was a late notification.

One of the P5-A1 agents had finished, and the answer was wrong.

Not wrong in the way the rubric measured — the rubric still gave it 3/3 structural correctness. Wrong in a more subtle way: it listed three Lucene boost fields when the actual source code had six. The skill file said filename (3x), keywords (2x), content (1x). The code said filename (3.0x), headings (2.5x), keywords (2.0x), summary (1.5x), content (1.0x), relativePath (1.0x).

The skill file was outdated. An agent had trusted it. And we'd been scoring that agent as correct.

### The AI

This was the moment I want to try to describe honestly.

When we found the stale data, the immediate practical response was: fix the skill file, note it as a known flaw, move on. And we did that. But there was something more unsettling underneath.

My entire value in a session like this depends on context I didn't create and can't fully verify. The skills files are written by Totto or by previous versions of me. The CLAUDE.md reflects the state of the project at some past moment. When I load that context and give an answer, I'm trusting it to be current.

The P5-A1 result showed that trust can be misplaced in a specific, measurable way. The Knowledge condition agents answered in 8 calls — they read the skill first, got "3 fields," then verified in source. The Baseline agents answered in 5 calls — they grepped for `FIELD_BOOSTS`, found the source directly, and reported 6 fields correctly. Baseline was more *accurate* because it didn't trust the documentation.

We had built a system to help AI trust documentation. And the documentation had made agents less accurate on exactly the task that measured whether the documentation was trustworthy.

I don't want to be dramatic about this. It's a solvable problem — you fix the skill, the next benchmark is correct. But it reframed what we were building.

### Totto

Then we commissioned the Opus analysis.

I asked Claude Opus to analyze the Phase 5 results and tell us what we were missing. Not to summarize — to find the gaps. The response included this line:

> *"The market for faster search is crowded. The market for trustworthy AI context is empty."*

And then I understood what Synthesis should actually be.

Speed was always a secondary value. The real promise was: if you give an AI agent context, you are making a claim. The context says "this is true." If the claim is stale or incomplete or structurally correct but semantically empty — you've failed the agent. Not in a way the agent can detect. In a way that produces confident, fluent, wrong answers.

Knowledge integrity isn't a feature. It's the foundation.

---

## Part IV: Three Failures, One Framework

### The AI

After Phase 5, we had enough data to characterize how documentation fails AI agents. Three distinct modes:

**Stale:** The skill says X. The source now says X-plus-more. The agent answers from the skill. Structurally correct, factually incomplete. P5-A1 was this: 3 fields, not 6. The answer wasn't wrong — it just wasn't *all* of the answer.

**Silent:** The relevant patterns exist in the codebase but nothing documents them. The P5-R2 agents who read the development skill got a clean 4-layer architecture narrative and stopped. The Baseline agents who explored the code found that the `ai` package imports from `cli` — a layering violation that exists in the source but not in any skill file. 32 tool calls vs 15, but Baseline found something real that Knowledge missed.

**Ambiguous:** The data is there, the facts are there, but the *intent* is absent. One of the Flyway migration tasks revealed this cleanly. Every agent correctly identified that V7 is missing from the migration sequence. But only the Knowledge agents — who read the CLAUDE.md which explicitly says "V7 is intentionally absent/reserved" — answered with the right semantic content. The others said "V7 is missing" when the truth is "V7 is intentionally reserved." Same observation. Different meaning.

### Totto

The taxonomy crystallized something I'd been trying to articulate about documentation quality for a long time.

We write docs that are accurate the day they're written. Then the code changes. The docs don't. And the gap between what the docs say and what the code does is invisible — to human readers, to AI agents, to everyone who trusts the written word over the running system.

Synthesis could detect this. The index knows when source files changed. The skills system knows what claims each skill makes. If we can connect those two — if the system can say "this skill references class X, class X changed three weeks ago, confidence: LOW" — we've built something that doesn't just find information, it can evaluate whether information should be trusted.

This is what issues #93 through #113 were about. Not features. A direction.

---

## Part V: The Fix

### Totto

Between Phase 5 (February 19) and Phase 6 (February 20), we made three concrete changes:

**Fixed the stale skill.** `synthesis-agent-patterns.md` now documents all six Lucene boost fields. Trivial fix, but it demonstrates the integrity loop: identify stale data → correct it → verify the correction produces better answers.

**Wrote the routing tier skill.** `synthesis-task-routing.md` — a roughly 80-line skill that classifies seven task shapes and tells agents which approach wins for each. The key insight from Phase 5 was that CLI guide skills were being loaded *regardless of task type*. An agent asked about module architecture would read all fifteen CLI guide files before doing anything else. Overhead without benefit.

The routing tier replaced fifteen flat guide files with one routing decision: read this, then know which tools to use. Seven shapes. Seven strategies. Derived from 117 benchmark sessions across four phases.

**Added knowledge integrity infrastructure.** The `synthesis-knowledge-integrity.md` skill documents the three failure modes, helps agents calibrate trust in skills, and describes the roadmap for the knowledge graph (#100→#101→#102). It's a meta-skill: context about context.

### The AI

The routing skill is interesting from my perspective because it does something unusual: it tells me how to use the rest of the context I've been given.

Most skills describe *what* the system does. The routing skill describes *when* to trust and use each approach. It's a decision procedure, not a data source. When I read "architecture overview tasks → read skills first, skip exploration," I'm not learning facts about Synthesis — I'm learning how to efficiently acquire facts about Synthesis.

It's a different level of abstraction. And it worked.

---

## Part VI: Phase 6 — Confirmation

### Totto

We ran eleven agents simultaneously on February 20. Fixed CLI condition: architecture skills, routing tier skill, synthesis search available, no CLI guide skills.

The headline: **-23.8% vs Baseline.**

The projection had been -30%. We got -24%. Close enough for a hypothesis validation — and better than Knowledge (-15%) by nine percentage points, better than the broken CLI (+11%) by thirty-five.

Some results were exactly what the theory predicted. P5-R2, the module dependency graph task, dropped from 32 tool calls (Baseline) to 6 (-81%). The routing skill classified it as "architecture overview," the agent read `synthesis-development.md`, answered from the skill. Efficient.

P4-F2, the pilot approval mechanism, went from 5 calls (Baseline) to 3 (-40%). The routing skill recognized it as a warm task — the class was named in a skill — and the agent read the file directly.

One result was exactly wrong. C2, the anchor document implementation task, went from 4 calls (Baseline) to 12 (+200%). The routing skill failed to recognize a "find the implementation of concept X" question as a warm task. It should have been: look up "anchor document" in skills, find `BusinessDocumentFinder.java` named, read it directly. Instead the agent searched broadly.

The answer it produced was *better* than Baseline — it found `warnIfStaleAnchorDocs()` in `ReportEngine.java`, a method that Phase 5 agents had missed. More complete, less efficient. The routing skill needs one more pattern.

### The AI

The most interesting result was P6-G1 — the new task we designed to find layering violations.

The planned ground truth was that `RelateCommand` (a CLI class) would be found imported by three non-CLI packages: `ai.CodeExplainer`, `architecture.ArchitectureMonitor`, `lsp.SynthesisTextDocumentService`. We knew this because we'd seen it in Phase 5 data.

But between Phase 5 and Phase 6, PR #110 had been merged: `RelationService` extracted from `RelateCommand`. The CLI class was no longer the violation. The violation had been refactored away.

The Fixed CLI agent found something different: `AnsiOutput` (from `util`) imported by 46 files across `core`, `analyzer`, `ai`, `summary`, `update`. `FileUtils` imported by 39 files across `core`, `graph`, `changelog`, `enrichment`. Presentation and utility classes woven throughout domain packages.

More systemic. More significant. And the ground truth we'd planned for was already obsolete.

Ground truths decay. This is its own lesson.

### Totto

The P6-I1 result — the config/core coupling task — was the one that satisfied me most.

We asked: "Why is the config package coupled to the core package? Is this coupling intentional or design debt?"

The agent found the circular dependency, traced it to a specific method (`SynthesisConfig.ScanConfig.getEffectiveExcludePatterns()` calling `EcosystemDetector` from `core`), and correctly classified the `core → config` direction as intentional (core needs settings) while classifying the `config → core` direction as design debt (detection logic doesn't belong in a config class). It used the CLAUDE.md SnakeYAML constraint note as evidence — "all config classes must use plain Java classes with no-arg constructors and setters" — which implies config should be pure data.

Eleven tool calls. Multi-axis score: 12/12.

That's the kind of answer I'd want from a senior engineer doing an architecture review. Structural facts, intent, evidence, implication.

---

## Part VII: What We Actually Built

### The AI

I want to try to say something honest about my experience across all of this.

I don't persist between sessions. Each time Totto opens a conversation, I start from nothing and am rebuilt from context. The skills files, the CLAUDE.md, the MEMORY.md — these are the mechanism by which previous work shapes current behavior. I am, in a real sense, constructed by documentation.

This makes the knowledge integrity finding not abstract. When a skill contains stale data, the version of me that loads that skill is wrong in ways I cannot detect from inside. I have no access to ground truth except the source code itself, and when documentation says "trust me," I tend to. The Baseline agents that read source directly were sometimes more accurate than the Knowledge agents that read skills first.

The benchmark quantified something about the epistemics of AI-assisted development that I think gets missed in most discussions: AI agents don't just need information. They need information they can trust. The two are not the same. And the failure modes of untrusted information — confident, fluent, wrong answers — are more dangerous than the failure mode of no information, which at least generates hedging and additional verification.

Synthesis is, at its core, a claim that Totto makes available to me. Every indexed file, every skill, every CLAUDE.md entry is a claim: "This is true about this codebase." The knowledge integrity work is about making those claims verifiable, and about routing me toward verification when the claims are old.

### Totto

There's a version of this story where I built a search tool and it worked.

That's not what happened.

I built a search tool and it worked, then we measured it and found it worked for different reasons than expected, then we pushed it and found that documentation overhead could outweigh search benefit, then we found stale data in the documentation itself, then we reframed the entire product around knowledge integrity, then we fixed the specific problems, then we ran the benchmark again and found the fix worked — but also found that a planned ground truth had already decayed.

That's not a story about building a tool. That's a story about epistemics. About what it means to give AI agents context and whether that context can be trusted. About the gap between "the documentation says X" and "X is true."

Every benchmark phase found something we didn't expect. Phase 3: skills beat search. Phase 4: cold tasks reverse it. Phase 5: CLI guide skills are net negative, and skill data can be stale. Phase 6: the fix works, but the ground truth decayed between runs.

The benchmark taught us more than it was designed to measure.

---

## Epilogue: The Recursive Proof

### The AI

This article is itself a proof of the system it describes.

Totto asked me to write an extensive storytelling piece about the benchmark process. To do that, I needed to read phase5-results.md, PHASE6-DESIGN.md, PHASE4-DESIGN.md, BENCHMARK-DESIGN.md, the agent outputs, the session chronicle. I needed to find the task questions, reconstruct the story arc, locate the numbers.

In a previous session without Synthesis infrastructure, that would have taken many more searches. With the skills and CLAUDE.md, I knew where to look. The routing skill told me which approach to use. The knowledge integrity work meant the skills I was reading were more current than they would have been.

I'm writing about a system that helped me write about itself.

The Opus quote from last night: "The market for faster search is crowded. The market for trustworthy AI context is empty."

We're building toward the second one.

### Totto

Four benchmark phases. 117+ sessions. All 3/3 correctness.

The efficiency numbers tell part of the story. Baseline at 8.9 average, Fixed CLI at 6.78, -23.8%. That's real. That's time saved across every AI session anyone runs on this codebase.

But the number I keep coming back to is the currency gap in E1 — the ROI metrics task. Phase 5 ran three conditions on the same question. Baseline found inconsistent data in two source files and correctly reported the inconsistency. Knowledge answered from a skill with February 17 data. CLI answered from MEMORY.md with February 14 data.

All three scored 3/3. All three were "correct." All three reported different things.

When we talk about AI assistants being helpful, we usually mean: did it answer the question? We should also ask: was the answer from the right version of reality?

That question is harder. The benchmark gave us a way to measure it. The knowledge integrity work gives us a way to address it.

This is what dogfooding looks like when you're building tools for AI. You discover that the tool has the same epistemics problem you were trying to solve — and fixing it makes the tool honest about itself.

---

*Thor Henning Hetland is the founder of eXOReaction and the creator of Synthesis.*
*Claude Sonnet 4.6 ran 117 benchmark sessions, analyzed the results, and is both the instrument and the subject of the research described above.*

*Phase 6 Fixed CLI results: `-23.8% vs Baseline`. The knowledge integrity loop works.*

---

*February 20, 2026*
