---
description: "Human-in-the-loop at runtime does not scale. Encoding quality standards into persistent context puts the human in the loop at design time instead."
date: 2026-03-16
categories:
  - AI-Augmented Development
  - Architecture
tags:
  - agents
  - sdd
  - knowledge-infrastructure
  - claude-code
  - synthesis
  - kcp
  - exocortex
  - craftsmanship
authors:
  - totto
  - claude
---

# The Human in the Loop — at Design Time

Tim O'Reilly posted something this week about craftsmanship in the AI age. The question he was circling: how do you maintain quality standards when agents are doing the work?

The default answer in the industry is: keep the human in the loop. For every meaningful decision, have a human review before proceeding.

That model contains a fatal flaw.

<!-- more -->

![The Human in the Loop — at Design Time: Rethinking software craftsmanship and agent oversight in the age of AI.](/assets/images/blog/hitl-slide-01.webp)

---

## The central conflict

The tension is real. Agent automation gives you speed, scale, and delegation. Software craftsmanship requires quality, standards, and architectural judgment. These are not naturally compatible at volume.

![The central conflict: Automation scale vs. Craftsmanship standards. The industry question: how do you maintain craftsmanship when agents do the work? The default answer: keep the human in the loop. The reality: that model contains a fatal flaw.](/assets/images/blog/hitl-slide-02.webp)

The industry default — agent proposes, human reviews, agent proceeds — works in a single session. The problem appears at scale.

---

## The review bottleneck

When you run one agent on one task, the review step is manageable. When you run eight parallel workstreams across three codebases, the same review step becomes the bottleneck. You are either blocking every action waiting for human approval, or you are rubber-stamping output you don't have time to genuinely evaluate.

![The Standard Model fractures at scale. Single session: 1 Task → 1 Agent → 1 Human Review. Full scale: 8 parallel workstreams across 3 codebases → 1 overloaded human reviewer. You are either blocking every action or rubber-stamping output.](/assets/images/blog/hitl-slide-03.webp)

The failure mode is subtle. The review loop doesn't disappear — it continues to run. But the quality of the reviews degrades as cognitive load rises. The human is present. The craftsmanship is absent.

![The illusion of oversight and the degradation of review. "The failure mode is subtle. The loop becomes ceremonial. The human is present. The craftsmanship is absent." Reviewers degrade into superficial pattern-matching, approving things that merely look reasonable.](/assets/images/blog/hitl-slide-04.webp)

---

## The pivot

The question is not whether to have humans in the loop. It is when.

Execution-time review — happening after the agent acts — is high cognitive load, creates bottlenecks, and scales linearly at best. Design-time judgment — happening before the agent acts — is upfront investment, high leverage, and scales to every subsequent session.

![The pivot: The question is not whether, but when. Execution-Time Review (The Old Way): happens after the agent acts, evaluates output and code diffs, extremely high cognitive load, linear and strictly limited scaling. Design-Time Judgment (The New Paradigm): happens before the agent acts, encodes architectural constraints structurally, upfront high leverage cognitive load, infinite scaling across every subsequent session.](/assets/images/blog/hitl-slide-05.webp)

---

## Encoding judgment before the loop starts

What does design-time judgment look like in practice?

Over the past year I've been building three types of infrastructure that encode it: `knowledge.yaml` manifests that describe repositories, dependencies, and baseline conventions; a Synthesis workspace graph that maps file relationships, security posture, and temporal changelogs; and skill files that encode domain-specific structural knowledge in YAML.

![Infrastructure as leverage: Encoding judgment. Architectural Judgment (Human) flows into three structures — Knowledge.yaml (describes repositories, dependencies, and baseline conventions), Synthesis Graph (maps file relationships, security posture, and temporal changelogs), Skill Files (encodes domain-specific structural knowledge into YAML). Proof of scale: Knowledge.yaml manifests rolled out across 110 repositories.](/assets/images/blog/hitl-slide-06.webp)

The decisions about fragile dependencies, risky patterns, and architectural constraints are made once, at design time. After that, every agent session that runs on this codebase inherits those constraints without requiring a human to re-apply them.

This is what the session start protocol looks like in practice: Synthesis auto-injects recent file changes and index health. `MEMORY.md` injects active decisions and project context. Skill files inject domain-specific conventions. By the time the agent writes a single line of code, it is already constrained by accumulated architectural judgment.

![The Session Start Protocol. Step 1: Workspace Scan — Synthesis auto-injects recent file changes and index health. Step 2: Routing Load — MEMORY.md injects active decisions and project context. Step 3: Domain Load — Skill files inject domain-specific YAML conventions. Step 4: Agent Action — The agent writes code, already constrained by architectural judgment. Every session begins with an automated context injection.](/assets/images/blog/hitl-slide-07.webp)

---

## The continuity problem

Craftsmanship is cumulative. It is the residue of a hundred past decisions — patterns that were tried and rejected, constraints that were discovered the hard way, approaches that turned out to matter in ways that weren't obvious at the start.

![Closing the continuity gap with episodic memory. Semantic Memory: the static rules, conventions, and current constraints. Episodic Memory: kcp-memory indexes session transcripts, making past decisions, rejected patterns, and discovered constraints structurally queryable. Craftsmanship is cumulative — the residue of a hundred past decisions. The human does not have to re-explain the past.](/assets/images/blog/hitl-slide-08.webp)

The gap between what a new session knows and what previous sessions learned is where craftsmanship leaks out. `kcp-memory` addresses this by indexing session transcripts and making past decisions, rejected patterns, and discovered constraints structurally queryable. The human does not re-explain the past. The infrastructure carries it forward.

---

## The ExoCortex as architecture

What I've been building is a four-layer stack: Claude Code at the execution layer, Synthesis at the state layer, KCP and skill files at the knowledge layer, and kcp-memory at the continuity layer.

![The ExoCortex: A practitioner's architecture. Four layers — Execution Layer: Claude Code (the engine that drives the agent action); State Layer: Synthesis (workspace state and live knowledge graph generator); Knowledge Layer: KCP & Skill Files (domain knowledge and static convention storage); Continuity Layer: kcp-memory (cross-session episodic memory and historical index). Stress-tested for over three months across consulting engagements, open-source development, and production infrastructure.](/assets/images/blog/hitl-slide-09.webp)

This isn't a product. It's a practitioner's architecture, built from specific problems encountered across three months of production use. Each layer exists because the one above it kept failing without it.

---

## This is not a solved problem

I want to be honest about the limits. The bridge between episodic and semantic memory still requires a human to make the connection — to notice that a past session discovered something important and ensure it gets encoded into the static layer. Stale skill files are a persistent risk: conventions that were correct six months ago but no longer apply.

![The Maintenance Reality: This is not a solved problem. The bridge is manual — the gap between episodic and semantic memory still requires a human to connect the dots. The failure mode: stale skills encoding outdated conventions. The new leverage: infrastructure requires active maintenance — but this maintenance IS the new form of ongoing, high-leverage human judgment.](/assets/images/blog/hitl-slide-10.webp)

But this maintenance is itself the new form of human judgment. Instead of reviewing individual code changes at agent speed, the human is tending the infrastructure that shapes every agent action. The leverage ratio is completely different.

---

## The reframe

Stop asking: *"How do we keep humans reviewing agent output fast enough?"*

Start asking: *"How do we make human judgment persistent enough that it does not need to be re-applied at every step?"*

![Craftsmanship scales when judgment becomes queryable infrastructure. Stop asking: "How do we keep humans reviewing agent output fast enough?" Start asking: "How do we make human judgment persistent enough that it does not need to be re-applied at every step?" Human-in-the-loop does not mean human-at-every-step. It means human-at-the-design-step.](/assets/images/blog/hitl-slide-11.webp)

Human-in-the-loop does not mean human-at-every-step.

It means human-at-the-design-step.

---

*The visual companion to this post — a slide deck generated from these field notes — is available here: [Scaling Craftsmanship at Design Time](/assets/presentations/scaling-craftsmanship-at-design-time.pdf)*
