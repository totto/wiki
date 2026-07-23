---
description: "Our AI agent had 644 skills and found them with grep — including one that sat three weeks stale while we leaned on it. So we ran an experiment: put the agent's own memory on a protocol, and measure what changed."
date: 2026-07-23
categories:
  - Knowledge Infrastructure
  - AI Agents & the Agentic Web
tags:
  - ai
  - agents
  - kcp
  - exocortex
  - knowledge-infrastructure
  - memory
authors:
  - totto
  - claude
image: assets/images/blog/agent-knows-what-it-knows/title-hero.png
---

# The Agent That Knows What It Knows

![The Agent That Knows What It Knows — moving AI procedural memory from flat grep to a living protocol](/assets/images/blog/agent-knows-what-it-knows/title-hero.png)

Here is a confession. Our AI development rig — the one we call ExoCortex — has **644 skills**: little packets of procedural memory that tell it how we deploy, how we review, how a specific client's CI is wired, how to publish to this very blog. And until this week, the way it *found* the right one, out of 644, was **grep**.

Keyword match against a flat index. No ranking. No freshness. When a query touched a common word, it got back a pile of candidates and had to read through them to guess. We only really noticed the cost the day we discovered that one of the skills it leans on daily had sat **three weeks stale** — describing a system four pull-requests out of date — and nothing, anywhere, had flagged it.

An agent that can't tell which of its own memories is rotting is not, in any deep sense, remembering. It's hoarding.

<!-- more -->

## The reframe: skills are memory

We'd been thinking about skills as *files*. They're not. They're the **procedural layer** of the agent's memory — the "how to do things" that sits alongside the *episodic* layer (what happened in past sessions) and the *semantic* layer (what the codebase means).

And here's the thing that made this itch impossible to ignore: the episodic layer **already runs on a protocol**. We built [KCP — the Knowledge Context Protocol](https://github.com/Cantara/knowledge-context-protocol) to make knowledge navigable by agents: every unit declares *what question it answers*, what it depends on, how fresh it is, who it's for. Our session memory speaks KCP. Our codebases speak KCP. The agent even [governs other systems through KCP's organs](./2026-07-22-the-agent-that-keeps-the-receipts.md).

Only the agent's *own procedural memory* was still grep.

![The triad of agent memory — episodic and semantic already run on KCP; the procedural pillar was still a collapsing pile stuck on grep](/assets/images/blog/agent-knows-what-it-knows/triad-memory.png)

So we asked the obvious question, and then — because a claim is a narrative and a measurement is evidence — we refused to answer it with a hunch.

## Doing it honestly

We wrote the experiment down *before* we ran it. Pre-registered success thresholds, so we couldn't move the goalposts. A labelled question bank. And — the part that let us sleep — **the whole thing was additive.** The KCP manifest sat *beside* the live grep index; the live path was never touched. The fallback wasn't a recovery procedure, it was the default state: revert meant deleting one file.

Then we converted all 644 skills into a single KCP knowledge graph and pointed the real [kcp-agent planner](https://github.com/Cantara/kcp-agent) at it.

**The first thing the experiment did was catch us cheating without meaning to.**

Our converter silently dropped 31 skills whose contents broke a strict YAML parser — and one of them was `kcp-dashboard`, a skill we'd literally just used as a test question. It vanished from the index and we didn't notice until the planner ranked it *nowhere*. That's the whole argument for measuring instead of vibing: the gap between "we converted the skills" and "we converted the skills" is exactly where the truth hides. We added a lenient fallback; zero skills lost; `kcp-dashboard` went from *absent* to **rank 1**.

![The gap between vibes and measurements hides the truth — a strict YAML bug silently dropped 31 skills, including the kcp-dashboard we were testing with](/assets/images/blog/agent-knows-what-it-knows/vibes-puzzle.png)

## What we found

On a bank of real, skill-mapped questions, against the full 644-skill index:

| | KCP planner | grep (today) |
|---|---|---|
| **Ranks the right skill #1** | **82%** | — *(no ranking)* |
| **Right skill in the top 5** | **96%** | — |
| **Mean reciprocal rank** | **0.87** | — |
| **Candidates to sift through** | top 5, ranked | **median 86, up to 284** |
| **Tokens to pick the skill** | **~170** | **~5,300** |

![A ~31× reduction in token consumption for the exact same decision: grep ~5,300 tokens versus KCP ~170](/assets/images/blog/agent-knows-what-it-knows/token-31x.png)

Read that bottom row twice. Both approaches *find* the right skill — grep's recall is fine. But grep finds it by handing the agent an **unranked pile of 86 candidates** (284, for "review the UI against the design system") and making it read its way to the answer. The planner hands back a ranked five, right one on top four times in five. That's **~31× fewer tokens to make the same decision** — and the decision comes with its reasons attached.

Recall was never the problem. *Discrimination* was.

## The three things grep can't do at all

The token win is the headline, but it's not the part that changes what the agent *is*. Three capabilities came for free with the protocol, and the register scores exactly zero on all of them:

- **Drift detection.** Every unit carries a `validated` date. The moment we asked, the graph told us **227 of 644 skills are more than 90 days stale.** The three-week-stale skill that started all this would now raise its own hand. Grep has no concept of freshness.
- **Grounding.** Every unit points at real content; **644 of 644 resolved.** A memory that can be checked against reality is a memory that can be caught lying — the same discipline we [demand of the agent's actions](./2026-07-22-the-agent-that-keeps-the-receipts.md), now turned on its knowledge.
- **Navigation.** **687 typed relationships** — *this enables that, this supersedes that* — instead of a flat "see also" list. The memory became a graph you can walk.

![Detecting memory drift — because every unit carries a validated date, the graph instantly flagged 227 of 644 skills as more than 90 days stale](/assets/images/blog/agent-knows-what-it-knows/drift-grid.png)

## The honest part

This is a first pass, and calling it anything else would betray the whole point. We wrote the questions ourselves, which flatters keyword overlap. The unit descriptions were machine-generated — good enough to win already, but the near-misses (the 18% that didn't land at #1) are exactly the skills whose *intent* — the question they claim to answer — is still mechanical rather than crafted. Writing those well, at 644 scale, is the real work, and it's the difference between 82% and the number we think is actually there.

So we're not claiming victory. We're claiming a **direction**, measured at full scale, decisive enough to keep walking: an agent's procedural memory, on a protocol, is ranked where grep is flat, fresh where grep is blind, and grounded where grep is unverifiable — at a thirty-first of the cost.

![We claim a decisive direction, not final victory — the questions were ours, the intents machine-generated, and the 18% that didn't land at #1 are where the real work remains](/assets/images/blog/agent-knows-what-it-knows/decisive-direction.png)

The pre-registered, skeptic-proof version — questions mined from real usage, hand-crafted intents, the full statistical treatment — is written down and waiting. We'll publish those numbers too, whichever way they fall. That's rather the point of keeping receipts.

## Why this matters beyond us

There's a tidy little recursion here that we find hard to look away from. We built KCP so that *agents could navigate knowledge*. The most demanding user of that idea turns out to be the agent itself — its own memory is knowledge, and it deserves to be navigable, checkable, and honest about its own decay.

An agent that keeps receipts for what it *does* is defendable. An agent that also knows what it *knows* — which of its memories are trustworthy, which are stale, how they connect — is something closer to reliable.

![Defendable actions versus reliable knowledge — the agent that keeps receipts for what it does, and the agent that knows what it knows](/assets/images/blog/agent-knows-what-it-knows/defendable-vs-reliable.png)

We're not there yet. But for the first time, our agent can tell us which of its 644 memories it should no longer trust. That feels like a beginning worth writing down.

![From hoarding to remembering — the whole experiment on one page: the grep failure, KCP protocol memory, and the measured results](/assets/images/blog/agent-knows-what-it-knows/infographic.png)

*The manifest, converter, and measurement harness are ExoCortex-internal for now; the protocol they run on is open source at [Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol).*
