---
description: "Anthropic published how they built self-service analytics on Claude — a four-layer stack that gets 95% of their business queries automated. We read it looking for where we were wrong, and found instead a stack we'd already built from a different door: governed skills, adversarial review, provenance. Then we shipped the one piece neither post had covered."
date: 2026-07-29
draft: true
categories:
  - Knowledge Infrastructure
  - AI Agents & the Agentic Web
tags:
  - ai
  - agents
  - kcp
  - exocortex
  - skills
  - agent-governance
  - knowledge-infrastructure
authors:
  - totto
  - claude
---

# Same Blueprint, Different Doors

![Same Blueprint, Different Doors — the convergent evolution of governed AI agents, rendered as an engineering blueprint](/assets/images/blog/blueprint-01-title.webp)

Anthropic published a long, careful writeup of how they built self-service data analytics
on Claude internally — the system that lets anyone at the company ask a business question
in plain English and get back a governed, provenance-tracked answer. 95% of their
analytics queries are now automated this way, at roughly 95% aggregate accuracy.

We read it the way we read anything that touches how agents know things: looking for
where we were wrong.

We found something else instead. Strip away the domain — theirs is a data warehouse,
ours is a codebase and a governance practice — and the architecture underneath is close
enough to feel less like inspiration and more like recognition. Two teams, no contact,
building the same shape from opposite doors.

<!-- more -->

![Two independent teams built the same architecture from opposite directions — Anthropic's self-serve data analytics (95% of queries automated at 95% accuracy) and Cantara's codebase-and-governance practice on KCP](/assets/images/blog/blueprint-02-two-doors.webp)

## The shape, twice

Anthropic's stack, in their own words: canonical data foundations, a semantic layer of
governed metric definitions, **skills as thin routers** that narrow a warehouse with a
million fields down to a dozen curated files before the agent ever searches, and a
validation layer with a mandatory adversarial reviewer sub-agent standing between a
draft answer and the person who asked.

Ours, built independently over the past several months on [KCP — the Knowledge Context
Protocol](https://github.com/Cantara/knowledge-context-protocol): canonical
`knowledge.yaml` manifests, skills that declare *what question they answer* so a planner
can rank them instead of grepping them, and — as of a week ago — [an experiment that
measured exactly what that buys
you](./2026-07-23-the-agent-that-knows-what-it-knows.md):

| | Anthropic (their description) | Us (measured, 644 skills) |
|---|---|---|
| Mechanism | skills narrow the search space before retrieval | same |
| Effect | "million-field warehouse" → "dozen curated files" | median 86 unranked candidates → top 5, ranked |
| Selection cost | not quantified in their post | ~5,300 tokens (old) vs. ~170 tokens (new) |

![Strip away the domain and the underlying mechanics are identical — a side-by-side comparison of Anthropic and Cantara across domain, mechanism, effect, and selection cost](/assets/images/blog/blueprint-03-shape-comparison.webp)

Same mechanism, arrived at separately. Same reason it works: retrieval was never the
bottleneck — grep finds the right skill about as often as the ranked planner does.
*Discrimination* is the bottleneck. An agent handed 86 plausible candidates hasn't found
the answer; it's been handed a reading assignment with the answer buried somewhere
inside it.

![Retrieval is not the bottleneck — discrimination is. A funnel narrows a million-field warehouse and 86 plausible candidates down to a dozen curated, top-5 ranked files, cutting selection cost from 5,300 to 170 tokens](/assets/images/blog/blueprint-04-discrimination-funnel.webp)

## The second thing we'd already built

Anthropic's validation layer includes a mandatory adversarial reviewer — a separate
agent, independent of the one that drafted the answer, checking it before a human sees
it. They report the honest cost of that discipline: **+32% tokens, +72% latency, for
+6% accuracy** — and judged the trade worth making for a system the whole company now
depends on.

We've run the same shape for months, as cross-model adversarial review: a second model,
deliberately not the one that did the work, reading a plan or a diff before it ships.
It has caught real defects that a same-model second pass missed. We hadn't put a number
on the token and latency cost the way Anthropic did. Their number is now the one we'll
measure ourselves against.

![The measurable cost of architectural discipline — a worker model drafts, an independent adversarial reviewer checks before human approval, weighed against +32% tokens and +72% latency for +6% accuracy](/assets/images/blog/blueprint-05-cost-of-discipline.webp)

## Where we go further — and where we hadn't finished

Here's the part that isn't just convergence. Neither post — theirs or our own skills
experiment — answers what happens *after* a skill is selected: what stops a selected
skill from touching more than it should?

That gap was sitting, unfixed, in the open-source project we publish this work on:
[Cantara/kcp-skill](https://github.com/Cantara/kcp-skill), which defines `kind: skill`
units carrying a declared `action_scope` — the tools, paths, and capabilities a governed
skill may touch, fail-closed by default, nothing granted unless the manifest says so. A
skill's *procedure* (`SKILL.md`) and its *declared authority* (`library.yaml`) are two
different files. Nothing was stopping them from drifting apart: you could rewrite what a
skill does without ever touching what it's allowed to do, and no check would notice.

Reading Anthropic's post named that gap precisely, because they'd already closed the
analogous one on their side: they enforce in CI that a data-modeling change ships its
matching skill update in the *same diff* — about 90% of their data PRs comply by
construction, not by convention. We didn't have that. As of today we do:
[`scripts/check-colocation.sh`](https://github.com/Cantara/kcp-skill/commit/7f8a10c),
merged the same day we read their post. A diff that edits a skill's procedure without
touching its declared scope now fails CI outright.

![Closing the drift gap by binding procedure to authority — editing a skill's procedure alone fails CI outright; editing the procedure and its declared authority in the same diff passes](/assets/images/blog/blueprint-06-colocation-ci.webp)

## What's still just a plan

Anthropic also described a "correction harvester" — an agent that watches internal
channels for correction language, drafts the doc fix, opens a PR. We don't have that
running yet either. We wrote down how it should work: reusing the human-approval broker
we already have rather than inventing a second one, and leaning on the colocation check
above for structural correctness instead of reimplementing it. It's a design document,
not running code, and we're saying so on purpose. The pattern in this stack, going back
to the skills experiment, is: publish the plan, then publish whether it worked.

![Publish the plan, then publish whether it worked — the correction-harvester loop watches an internal chat channel for corrections, an agent parses and drafts the fix, then opens a PR](/assets/images/blog/blueprint-07-correction-harvester.webp)

## Why the convergence is the actual finding

![The objective requirements for trustworthy agent actions — a four-layer stack: canonical foundations, ranked retrieval, adversarial review, and CI-bound enforced colocation](/assets/images/blog/blueprint-08-four-ingredients.webp)

The headline here isn't "we already do what Anthropic does." It's that a frontier lab
optimizing for *trustworthy answers to business questions* and a small practice
optimizing for *defendable agent actions in a regulated domain* arrived at the same four
ingredients — canonical structure, ranked retrieval, adversarial review, enforced
colocation — without either one checking what the other was building. That's a weaker
claim than "we were right," and a more interesting one: it suggests this shape isn't a
house opinion. It's closer to what governing an agent's knowledge actually requires,
discovered twice, from two directions that had no reason to agree with each other.

![Governing an agent's knowledge is a matter of physics, not opinion — two blueprint halves forming a single structure, forced into the same shape by the reality of the technology](/assets/images/blog/blueprint-09-physics-not-opinion.webp)

One door goes further than the other right now — `action_scope` and colocation-in-CI
are ours, and we'd read their post with real interest to see the same close on their
side. We don't think we're finished, either. Neither, reading carefully, do they.

![The fundamental blueprint for governed AI — not a house opinion but the objective requirement of governed agent knowledge, discovered twice from two directions that had no reason to agree](/assets/images/blog/blueprint-10-closing.webp)
