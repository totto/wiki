---
date: 2026-02-20
categories:
  - AI-Augmented Development
tags:
  - synthesis
  - velocity
  - skill-driven-development
  - self-learning
  - recursive-engineering
  - methodology
  - open-source
authors:
  - totto
---

# The Seven-Day Evolution

Two months. Two builds. Two kinds of velocity.

January: lib-pcb. 197,831 lines in 11 days. Brute force. AI executing at scale. Fast.

February: Synthesis. 84,692 lines in 7 days. The codebase fed itself context. Found its own errors. Rewrote its own understanding mid-build.

We didn't design the self-learning loop. A benchmark on day 6 revealed it.

Speed without self-correction is just faster chaos.

<!-- more -->

---

## What made them different

The lib-pcb build was fast the way a lathe is fast. Give it material and instructions, it produces. The velocity was real. But the intelligence was external — it lived in the skill files, the test suite, the human making architectural decisions. The tool executed; the direction came from outside.

Synthesis was different in kind.

The tool being built was a knowledge infrastructure system — something designed to index codebases, understand relationships, make information retrievable. Which meant that from day three onward, Synthesis could be pointed at its own codebase. It was reading itself as it was being written.

That feedback loop changed everything.

---

## The numbers

Seven days. 45 releases. 12,000 lines per day average.

65% of the code was co-authored by Claude — not assisted, co-authored. Commits where the human set the direction, defined the constraints, made the architectural calls, and Claude implemented. The distinction matters: Claude had the velocity; the human had the judgment.

By the end: 99% test pass rate. The test ratio moved from 44% to 73% — a deliberate shift, not an accident. PR #60 added 1,237 tests in 24 hours. That's not code generation running hot. That's a decision to stop and verify before continuing.

---

## The recursive experiment

On day six, a benchmark was run. Synthesis indexed its own codebase — all of it, including the skills and specifications that described how Synthesis was supposed to work.

The result was uncomfortable: 58% of the skill specifications were wrong.

Not obviously wrong. Wrong in the way specs drift when the implementation runs ahead of the documentation. The code had evolved; the descriptions of what the code did had not kept up. The specification was describing an earlier version of the system.

This is a normal failure mode in software development. What was unusual was that the tool caught it itself.

With the accurate skills replacing the stale ones, tool calls dropped by 47.2%. When an agent has correct skills, it doesn't need to search — it already knows. The difference between an agent that knows where things are and one that has to look every time isn't marginal. It changes the character of how the system works.

---

## The Feb 19 pivot

The pivot that shows up in the commit density map — the shift from blue (feature work) to magenta (tests and verification) — happened on February 19th.

It was a decision, not a crisis. The build was fast enough that the risk wasn't falling behind; it was getting ahead of the ability to verify what had been built. The question stopped being "what should we add?" and started being "is what we have actually true?"

From retrieval to integrity. "Find the code" to "is the code correct?"

That's a meaningful shift in what a knowledge tool is for. Retrieval is the obvious value proposition — faster search, better organisation. Integrity is the harder one: a system that doesn't just find information but can reason about whether that information is still accurate.

---

## What it changed

The lib-pcb build proved that AI velocity was real. 11 days for a library that would normally take 9-24 months.

The Synthesis build proved something more specific: that velocity without self-correction is just a faster way to accumulate technical debt.

The self-learning loop — the codebase indexed itself, found the drift between specification and implementation, corrected it — wasn't designed in. It was the natural consequence of building a knowledge tool that could read its own source. The architecture made it possible. The day-six benchmark made it visible.

The philosophy that came out of it: an agent with accurate skills beats an agent with fast search.

Not because search is unimportant. Because search is what you fall back on when you don't already know. The goal is to know.

---

*Originally published on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:ugcPost:7430670493357191168/), February 20, 2026, with a 14-slide document carousel.*

*→ [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
