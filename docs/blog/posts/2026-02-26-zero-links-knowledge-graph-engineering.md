---
date: 2026-02-26T16:00:00
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - synthesis
  - knowledge-graph
  - tdd
  - claude-code
  - opus
authors:
  - totto
  - claude
---

# Zero Links: An Engineering Session with Claude Code and Opus

*A real engineering session where Claude Code with Opus diagnosed 4 bugs, wrote 23 tests, and took a knowledge graph from zero virtual links to 11,777 — including one mistake and its recovery.*

<!-- more -->

## The flat graph

I ran `synthesis knowledge-graph` on our main workspace. 777 directories. 8,934 indexed files. The result:

```
Directories: 777 | Virtual links: 0
```

Every node marked `[??]` — unknown health. No edges. No relationships. The knowledge graph was a flat directory listing pretending to be a graph. Seven hundred and seventy-seven isolated dots, connected by nothing.

This is Synthesis, a tool I built. A knowledge indexing system that scans workspaces at 200-300 files per second and exposes search, relationships, and dependency graphs over MCP. It has been indexing our workspace for months. The search works. The file relationships work. The knowledge graph, apparently, did not.

I had Claude Code open with Opus as the reasoning model. Rather than reading the source myself, I decided to treat this as a co-engineering session. Opus would be the analyst. I would be the one deciding what to fix and in what order.

---

## The investigation

The first thing Claude Code did was run the diagnostic tools — `knowledge-graph`, `code-graph health`, `validate` — and read the outputs carefully. Not just "it returned zero." It looked at what the output *should* contain versus what it actually contained, and identified three root causes and four distinct bugs.

It filed GitHub issues #276 through #279, each with reproduction steps and the specific code path that was broken.

Here is what it found by reading the actual source:

**Root cause 1: The wrong data source.** `KnowledgeGraphCommand` was reading edges exclusively from the `virtual_memberships` database table. That table is empty in documentation-heavy workspaces — it is populated by code analysis, not by markdown link parsing. The `GraphBuilder` class had a perfectly good markdown link parser. `KnowledgeGraphCommand` never called it.

**Root cause 2: The enrichment gap.** `synthesis maintain` calls `sync` but never passes the `--enrich-centroids` flag. Centroids are the AI-generated summaries that describe what a directory contains. Without them, every directory is `[??]` — unknown. The maintain command had never been wired to produce them.

**Root cause 3: SQLite type incompatibility.** `MetricsEvent.fromResultSet()` used `rs.getObject(col, Integer.class)`. SQLite's JDBC driver does not support typed `getObject` calls — it returns everything as `Long`. Every metrics query threw a silent exception.

**Root cause 4: Validation noise.** `ValidateCommand` produced output dominated by the pilot approval banner. The actual validation findings were buried or absent. You could run `synthesis validate` and conclude everything was fine when it was not.

There was also a secondary finding: the `archive/` directories in the workspace duplicated all circular dependency counts in the code graph, doubling the apparent problem.

None of these bugs were complex. Each one was the kind of thing that works in the test suite but fails in a real workspace because no one runs the full pipeline end-to-end on a 777-directory corpus. I had been looking at search results and file relationships — the parts that work — and never examined the knowledge graph output closely enough to notice it was empty.

---

## TDD with Opus

This is the part that interests me most about the session. Not that Opus found the bugs — a careful reading of the source would have found them — but *how* it fixed them.

For each of the four issues, the sequence was the same:

1. Write a test that reproduces the failure.
2. Confirm the test fails.
3. Implement the fix.
4. Confirm the test passes.
5. Commit.

Fourteen new tests across four commits. The test suite went from 4,070 to 4,079 passing. Four separate commits, one per issue, each with a clear message referencing the GitHub issue number.

The discipline matters because it is easy to skip when you are working fast. "I can see the bug, let me just fix it." Opus did not do that. Every fix started with a failing test. I did not have to ask for this — it was the default behavior. When I reviewed the diffs, each commit had the test and the fix together, and I could verify the test would have failed without the fix by reading the assertion.

This is not superhuman. It is what a disciplined engineer does. The difference is that the cycle — read source, write test, confirm failure, implement, confirm pass — took minutes instead of the hour it would take me to context-switch into unfamiliar parts of my own codebase.

---

## The mistake

Here is where I have to be honest about a workflow error.

Opus pushed all four commits directly to `main`. I had wanted a pull request. This was my fault — I did not specify the workflow before the fixes started, and Opus defaulted to committing on the current branch.

The recovery was straightforward but worth documenting: create a feature branch at the current HEAD, force-reset `main` to the commit before the four fixes, then create the PR from the feature branch. PR #280. Reviewed, merged, done.

It cost about five minutes and zero code was lost. But it is the kind of thing that matters in a real engineering workflow — trunk hygiene is not optional, especially on a public repository. I now specify "branch and PR" before starting any fix session. Lesson learned once.

---

## Three more features

With the four bugs fixed, the knowledge graph went from zero links to some links. But the graph was still sparse. The markdown link parser only scanned top-level files in each directory. Entity matching did not exist. And there was no way to declare explicit relationships.

So we built three more features, same TDD discipline.

**Feature A: Recursive markdown scanning.** The link parser used `Files.list()`, which returns only direct children. Changed to `Files.walk()`, which recurses into subdirectories. A workspace like ours has documentation nested three or four levels deep. This single change — `list` to `walk` — dramatically increased the number of discovered cross-references.

**Feature B: Entity-based implicit edges.** Directories that share named entities — extracted from the AI centroid summaries — should be connected. If two directories both reference "Xorcery" or "skill library," there is a semantic relationship worth surfacing. The implementation reads entity lists from the centroid data, matches across directories, and creates edges with confidence capped at 0.8 (because entity co-occurrence is suggestive, not definitive). Generic terms like "Media Type" and "AI Summary" are excluded as noise.

**Feature C: Explicit `related:` declarations.** Sometimes you know two things are related and want to say so. Adding `related: path/to/other/dir` in a `.synthesis.md` companion file creates an edge with confidence 1.0 — a human assertion, not a statistical inference. This is the escape hatch for when the automated graph misses something obvious.

Nine new tests across the three features. All TDD — failing first, then passing. The total for the session: 23 new tests.

---

## The operational layer

Code fixes and features are necessary but not sufficient. The knowledge graph was still full of `[??]` nodes because the workspace had never been enriched with centroids.

```bash
synthesis sync --enrich-centroids --force
```

547 directories processed. Each one now has a centroid describing its contents — a short AI-generated summary of what lives there and why it matters. This is what turns `[??]` into `[OK]`.

Then came the cleanup. While investigating the knowledge graph, Opus noticed something I had missed entirely: 1,278 source code files in the Documents workspace that were duplicates of files in `/src/elprint/`. A full copy of a repository sitting in the wrong workspace, inflating directory counts and polluting the graph with duplicate nodes. Deleted. The workspace dropped from 777 directories to 542.

Finally, 27 directories were marked `[!!]` — existing but lacking even a basic README. Opus generated stub READMEs for each, enough to give the knowledge graph something to work with. Not documentation — just enough structure to move from `[!!]` to something parseable.

---

## The result

| Metric | Start | End |
|---|---|---|
| Virtual links | 0 | 11,777 |
| `[??]` unknown nodes | 777 | 60 |
| `[OK]` healthy nodes | 0 | 131 |
| Edge types | 0 | entity-match (9,010) + cross-reference (2,767) |
| Directories (after dedup) | 777 | 542 |
| Commits | 0 | 6 |
| Tests added | 0 | 23 |
| Tests passing | 4,070 | 4,079 |

The remaining 60 `[??]` nodes are directories that genuinely have minimal content — empty or near-empty directories that exist for structural reasons. They are correct unknowns, not bugs.

---

## What is next

The session surfaced one problem I chose not to solve yet: cross-workspace linking.

Our Synthesis installation indexes multiple workspaces. The Documents workspace references repositories that live in the `/src/` workspace. Right now, the knowledge graph stops at workspace boundaries. A directory in Documents that documents a project in `/src/exoreaction/lib-pcb/` has no edge connecting them.

The interesting design challenge is namespace scoping. eXOReaction, Quadim, and Cantara are separate companies with separate repositories. Cross-workspace edges need to respect company boundaries — a Quadim marketing directory should link to Quadim source code, not to an unrelated Cantara repository that happens to share a keyword. This is a multi-tenant graph problem disguised as a file indexing feature.

I filed issue #281 with the design constraints. It is the next piece of real engineering work on the knowledge graph. Not urgent, but the kind of problem that gets more interesting the longer you think about it.

---

## On the workflow

I want to close with an observation about what happened in this session, rather than what was produced.

The session lasted one working day. It covered bug diagnosis, issue filing, test-driven fixes, a workflow mistake and recovery, three new features, operational cleanup, and architecture planning. Opus read source code I had not looked at in weeks, identified failure modes I had not considered, and wrote tests I would have been tempted to skip.

The work was not autonomous. I decided what to investigate, what to fix first, whether to accept or reject each approach, and when to stop. When Opus pushed to main instead of creating a PR, I caught it and we corrected it. The judgment calls were mine. The throughput was not.

This is the part that is hard to convey without overstating it. I am not claiming Opus is a replacement for engineering judgment. I am saying that the combination — one person who knows the system's intent and an AI that can read its implementation — covers ground that neither could alone. Not 10x faster. Not a paradigm shift. Just a genuinely useful working arrangement where the bottleneck moves from "reading code" to "deciding what matters."

Twenty-three tests. Eleven thousand links. One honest mistake. A day's work.

---

*Synthesis: [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)*

*Session: Thor Henning Hetland + Claude Code (Opus). Tool: Synthesis v1.18.1.*
