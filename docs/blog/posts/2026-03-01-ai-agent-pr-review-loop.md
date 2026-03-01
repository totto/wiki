---
date: 2026-03-01
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
tags:
  - ai
  - agents
  - kcp
  - code-review
  - open-source
authors:
  - totto
  - claude
---

# What Happens When an AI Submits a PR and Another AI Reviews It

We submitted a pull request to CrewAI adding a KCP manifest and TL;DR summary files. The goal was straightforward: contribute the same efficiency improvement that cut agent tool calls by 76% in our benchmark. Open it up, share the result, see if the maintainers want it.

What happened next was not what I expected.

<!-- more -->

The first reviewer was not a human. It was Cursor Bugbot — an automated AI code review system that CrewAI has running on all incoming PRs. It reviewed the code and found an issue. We fixed it. It reviewed again and found another. We fixed that one too. This happened six times over the course of a few hours. On the seventh pass, it found nothing.

By round five, the AI was reviewing the design of a knowledge navigation protocol.

---

## The progression

Here is what actually happened, in order.

**Round 1 — The obvious catch.** The benchmark script had a hardcoded path: `/src/totto/crewAI`. That is the path on my machine. Ship it to anyone else and it breaks immediately. Fair catch. Embarrassing, but fair.

**Round 2 — The security gap.** The `read_file` and `grep_content` tools in the benchmark runner had no path restrictions. An agent using the benchmark tools could theoretically read files outside the repository. The bugbot flagged this as medium severity. We added path validation.

**Round 3 — The wrong validation.** We had used `os.path.realpath(path).startswith(os.path.realpath(REPO_ROOT))` for path containment. The bugbot correctly pointed out this is a path traversal vulnerability: `/home/user/repo-secrets/` passes a check against `/home/user/repo`. We switched to `pathlib.Path.relative_to()`, which is the correct Python pattern.

While in there, the bugbot also noted that `glob_files` — the file-listing tool — had no path restriction at all. Only `read_file` and `grep_content` had been protected. We fixed that too.

**Round 4 — Two subtle API bugs.** First: the `glob_files` handler declared a `base_dir` parameter in its JSON schema but silently ignored it in the implementation. An agent could pass a base directory and get results from the wrong location with no error. Second: the grep subprocess call was passing the search pattern without the `-e` flag, meaning patterns starting with a dash would be interpreted as grep arguments. Classic argument injection vector.

**Round 5 — KCP manifest semantics.** This is the one that surprised me.

The knowledge manifest had two "combined" TL;DR units: `agents-tasks-tldr` (summarising both the agents and tasks sections) and `tools-memory-tldr` (summarising both tools and memory). The manifest declared `summary_of: agents` on the first and `summary_of: tools` on the second — but both the `tasks` unit and the `memory` unit pointed back to these TL;DRs via `summary_unit`.

The bugbot's analysis:

> A KCP-aware agent using `summary_of` to validate whether a summary actually covers the topic of interest could skip the TLDR and fall back to reading the full reference file, defeating the purpose of this optimization.

It was right. The `summary_of` field in KCP is a single-ID back-pointer. If an agent navigates to `tasks`, sees `summary_unit: agents-tasks-tldr`, then checks `summary_of` on that TL;DR and finds `agents` not `tasks`, it might skip the shortcut. The fix was to remove `summary_unit` from `tasks` and `memory`, and instead declare explicit `context` relationships from the TL;DRs to those units — semantically correct and spec-compliant.

---

## What I noticed

The feedback got better with each round.

Round 1 was a copy-paste mistake. Round 4 was a subtle API contract violation. Round 5 was protocol design review. The same automated system caught all of them, but the nature of what it caught changed over six iterations from "this will break immediately" to "this might confuse an agent following the specification correctly."

I do not think that progression was coincidence. Each fix closed an obvious gap and exposed a subtler one beneath it. The bugbot was working through layers.

The fixes themselves were spread across four repositories — the three framework forks (smolagents, AutoGen, CrewAI) and the KCP spec repo's own CONTRIBUTING.md example, which had to stay in sync. Each round of fixes went to all four places, because the benchmark runner pattern is shared and the spec's canonical example should match. That coordination was also handled without human direction.

---

## The human's role

Honestly? Watching it happen and approving the pushes.

The loop was: bugbot finds issue → Claude Code reads the comment and writes a fix → fix goes to four repos simultaneously → bugbot re-reviews. No back-and-forth drafting, no discussion. Just a sequence of increasingly specific issues getting resolved.

This is not a story about AI being impressive. It is a story about what heterogeneous AI collaboration looks like in practice. Cursor Bugbot is trained differently from Claude Code. It has different strengths, different blind spots, a different purpose. The combination caught things neither would have found alone — or rather, things I would have shipped with if a human had been the first reviewer.

After the round five fix was pushed, the bugbot ran a seventh time. It found nothing. The check came back clean.

The PR is still open. No human reviewer has looked at it yet. But by the time they do, another AI will have reviewed it seven times and the code will be considerably tighter for it.

---

*The CrewAI PR is at [github.com/crewAIInc/crewAI/pull/4658](https://github.com/crewAIInc/crewAI/pull/4658). The benchmark runner pattern used in all three framework PRs is documented in [CONTRIBUTING.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/CONTRIBUTING.md) in the KCP spec repo.*
