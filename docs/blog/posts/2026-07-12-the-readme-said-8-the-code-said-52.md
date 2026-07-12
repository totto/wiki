---
description: "A routine docs update turned into a two-day audit of everything Synthesis says about itself. The README claimed 8 MCP tools; the code registers 52. The repo had three different licenses. And while we fixed the numbers, a fourth wrong number appeared. Stale knowledge is not an event — it is a pressure."
date: 2026-07-12T09:00:00
draft: false
categories:
  - Knowledge Infrastructure
tags:
  - knowledge-integrity
  - synthesis
  - dogfooding
  - documentation
  - ai-agents
  - maintenance
authors:
  - totto
  - claude
---

# The README Said 8. The Code Said 52.

It started as the most boring task on the list: *update the Synthesis numbers on the wiki from
the codebase.* Version bump, a few stats, fifteen minutes.

The agent's first move was the right one — it didn't read the docs to find the numbers. It read
the code. It counted the picocli subcommand registrations: **76 CLI commands**. It counted the
tool definitions in the MCP server: **52 tools**. Then it ran the entire test suite rather than
trust any number written down anywhere: **4,746 tests, zero failures**.

Then it compared those measurements to what we *say*.

<!-- more -->

## The inventory of drift

The README said the MCP server has **8 tools**. It has 52. Not off by a little — off by a factor
of six and a half, because every release since February added tools and nobody went back to the
sentence that says how many there are.

`CLAUDE.md` — the context file that AI agents load to understand the project — said v1.38.0,
4,605 tests, 31 packages, migrations through V24. Reality: v1.42.0, 4,746 tests, 34 packages,
V25. The file whose entire job is to keep agents from reasoning over stale information was
feeding them stale information.

The GitHub Releases page stopped at a version that was two releases old.

And then the one that actually made me laugh: **the license**. `knowledge.yaml` — our signed,
machine-readable knowledge manifest — declared `Apache-2.0`. The README said *"All rights
reserved."* `CLAUDE.md` said MIT. There was no LICENSE file at all. Three documents, three
different answers to the most basic question you can ask an open-source project. The wiki, for
the record, confidently said "Apache 2.0" — which turned out to be true only in the sense that
nothing had made it true yet.

I have written before that [memory that is not maintained becomes memory that
lies](2026-04-06-agent-memory-rots.md). It is one thing to write that about other people's
documentation. It is another to run the audit on your own repo and watch every category of the
[knowledge-integrity failure taxonomy](2026-02-11-the-mirror-test.md) show up in your own
backyard: stale facts, silent gaps, ambiguous claims. We build the tool that fights exactly
this. The cobbler's children had no shoes, and one of them was standing on a license
contradiction.

## Fixing it is the easy part

The mechanical fixes took a day, and the agent did them the way I wish all maintenance got done —
measure first, then write:

- **License made explicit**: a real LICENSE file (Apache 2.0), a NOTICE, a `<licenses>` block in
  the pom, and every stray "MIT" and "all rights reserved" hunted down across fifteen files.
- **Every stat replaced with a measured one**: not "60+" or "4,300+" hedges, but counts taken
  from the code and a test suite actually run that morning.
- **The dependency backlog cleared with the same standard**: Lucene 10.1→10.5 and JGit 7.1→7.7
  merged only after the full suite ran green against both together. When CI couldn't be
  triggered for the kcp-agent pin bump, the agent ran the whole conformance gauntlet locally —
  validate, plan, replay, sign, tamper-reject — against the new version before merging.
- **An external contributor's PR reviewed with a mutation test**: comment out the fix, watch the
  new test go red, restore. The test guards the fix, not an accident. Review posted, merged,
  and the two gaps it revealed were filed as issues and fixed the same afternoon.

That last pattern deserves its own sentence: *filed as issues and fixed the same day* is what
maintenance looks like when the finding, the verification, and the fix all live in one session
with full context. No backlog decay. No "who remembers what this issue meant."

## The part that proves the thesis

Here is the detail I will be retelling for months.

The verified numbers went onto a branch: 76 commands, 52 tools, 4,700+ tests. The branch sat
unmerged for two days, the way branches do.

In those two days, the wiki's main got another hand-edit: CLI command count bumped from "60+"
to **"65+"**. A third approximation — typed from memory, honest in intent, wrong in fact —
racing past a measured number that was sitting right there waiting for review.

Nobody did anything careless. That is the point. **Stale knowledge is not an event. It is a
pressure.** Documentation regresses toward hand-waving at exactly the rate people touch it,
and no amount of diligence fixes that, because diligence is what produced "65+" in the first
place. The only stable countermeasure is structural: numbers that are *generated* from the
thing they describe, and a gate that fails when they drift.

## Docs that can't lie

So that is where this is going. Synthesis is getting a public documentation site, and phase 1 —
the curated scaffold — is done. But the phases that matter are next:

- **Phase 2**: the CLI reference generated from the picocli model (all 76 commands), and the
  MCP reference generated from the 52 tool definitions that already live in the code as data.
  Nobody types "8 tools" ever again, because nobody types the number at all.
- **Phase 3**: a CI freshness gate — the site build fails if the generated reference differs
  from what is committed. The "README says 8" class of bug becomes structurally impossible,
  not procedurally discouraged.

The same session that found all this also mined the newest kcp-agent releases for ideas and
filed five adoption issues — including a **plan decision trace** (every unit annotated with
*why* it was selected or skipped) and a **plan diff** (what changed in what an agent would read
for a task, between two points in time). Same philosophy, one level up: don't just retrieve
knowledge, make its provenance and its drift *inspectable*.

The market for faster search is crowded. The market for trustworthy AI context is empty. This
week we were reminded — by our own README — why that second market exists.

---

*The audit, the fixes, the dependency verification, the PR review, and the docs site scaffold
were done across two sessions with Claude in Claude Code, working against the live repos. Every
number in this post was measured, not remembered — which, given the subject matter, seemed like
the least we could do.*
