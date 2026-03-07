---
date: 2026-03-07
slug: skill-driven-vs-spec-driven-development
series: "Skill-Driven Development"
categories:
  - AI-Augmented Development
  - Methodology
tags:
  - sdd
  - ai
  - claude-code
  - methodology
  - kcp
  - knowledge-infrastructure
authors:
  - totto
  - claude
---

# Skill-Driven Development vs Spec-Driven Development

Most teams using AI for development have settled on a workflow that looks roughly like this: write a detailed specification, feed it to the agent, review the output, iterate. It is disciplined. It is responsible. It works. And after six months of watching it in practice, I believe it has a structural limitation that becomes more expensive the longer you use it.

The limitation is not quality. Spec-driven development produces good output. The limitation is that every session starts from zero. The spec carries the knowledge. The agent carries nothing.

<!-- more -->

![Beyond the Spec: The Evolution of Skill-Driven AI Development — three stages from vibe coding to spec-driven to skill-driven, with compounding growth and 197,831 lines of code proof](/assets/images/blog/sdd-vs-spec-driven-evolution.png)

---

## Why spec-driven development is rational

Before critiquing anything, I want to be clear: spec-driven development is a reasonable response to a real problem.

The alternative most teams tried first was vibe coding. Prompt the agent, see what comes out, fix the obvious problems, ship it. Fast for prototypes. Dangerous for anything that has to work in production. Vibe coding produces code that reflects the model's training data rather than your team's conventions. It generates confident output that may or may not match your architecture. It works until it doesn't, and when it doesn't, nobody can explain why.

Spec-driven development solved the obvious failure modes. You write what you want. The agent builds it. You review what was built. There is a paper trail. There is a checkpoint between intent and execution. It is the engineering response to the chaos of unstructured AI use, and for teams moving from vibe coding to something rigorous, it was the right step.

The problem is what happens after three months.

![The necessary evolution from chaos to discipline — Stage 1 Vibe Coding (fast but fragile) vs Stage 2 Spec-Driven (responsible but linear)](/assets/images/blog/sdd-vs-spec-driven-slide-02-evolution-chaos-to-discipline.png)

---

## The session amnesia problem

A spec is a document about what to build. It describes the desired outcome. It does not describe what the agent has learned while building.

Session one: the agent reads your spec and writes a Spring service. You correct it: "We use constructor injection exclusively, never field injection." The agent fixes it. Good.

Session two: the agent reads your spec again and writes another Spring service. With field injection. You correct it again. Same correction. Same fix.

Session fifty: same spec, same correction, same fix. The spec never changed because the spec does not encode how you build. It encodes what you build.

This is the session amnesia problem. Every session starts cold. The agent has no memory of previous corrections, previous architectural decisions, previous domain knowledge accumulated across dozens of interactions. The spec is a snapshot of intent. It is not a growing body of expertise.

![Specs encode what you build, not how you build — the spec grows into a small book the agent reads at the start of every session and promptly forgets by the next one](/assets/images/blog/sdd-vs-spec-driven-slide-03-specs-encode-what-not-how.png)

Spec-driven teams compensate by making specs more detailed. Add a section on coding conventions. Add a section on testing patterns. Add a section on architectural constraints. The spec grows. Eventually it becomes a small book that the agent reads at the start of every session and promptly forgets by the next one.

The knowledge exists. It just doesn't persist where the agent can use it.

![The recurring tax of Session Amnesia — every session starts from zero, the spec carries the intent, the agent carries nothing](/assets/images/blog/sdd-vs-spec-driven-slide-04-session-amnesia.png)

---

## The alternative: investing in what the agent knows

Skill-Driven Development takes a different approach. Instead of writing increasingly detailed specs about what to build, you invest in what the agent knows before it starts building.

A skill file is a YAML or Markdown file that encodes a specific piece of domain knowledge, convention, or workflow. It lives in the project's `.claude/skills/` directory. It loads automatically when the agent works on that project. It persists across every session.

The Spring convention example becomes a skill:

```yaml
name: spring-wiring-conventions
version: 1.0.0
instructions: |
  - Constructor injection only. Never @Autowired on fields.
  - @Transactional on service methods, never repositories.
  - Integration tests use TestContainers, never H2.
```

![The anatomy of a codified skill — written once, loads automatically per project, permanently eliminates a category of repeated corrections](/assets/images/blog/sdd-vs-spec-driven-slide-07-anatomy-codified-skill.png)

Written once. Applied to every session, for every developer on the team, automatically. The agent does not need to be corrected. It already knows.

That is one skill. Over time, a project accumulates dozens of them. Each one captures something the team learned, a convention that was established, a mistake that was made and should not be repeated. The library grows. The agent's effective expertise grows with it.

This is the structural difference. Spec-driven development scales linearly: each new project requires a new spec. Skill-driven development compounds: each lesson learned makes every future session smarter.

![Stage 3: Skill-Driven Development — compounding curve showing skill-driven capability far outpacing spec-driven growth over time](/assets/images/blog/sdd-vs-spec-driven-slide-06-stage3-skill-driven.png)

---

## Always explaining vs always accelerating

The daily experience of the two approaches feels different in a way that is hard to appreciate from a description. You have to live it.

In a spec-driven workflow, the first fifteen minutes of every session are orientation. The agent reads the spec. You provide additional context. You answer questions about architecture. You clarify constraints. Then the building starts. The orientation tax is small on any given day. Over weeks, it adds up.

In a skill-driven workflow, the agent arrives knowing what it needs to know. Session start is not "let me understand your project." Session start is "the test for the coordinate parser is failing on files with non-standard origin offsets, and based on the coordinate-systems skill, the fix is to check for manufacturer-specific zero-point definitions." The conversation begins at the frontier of the problem, not at the baseline.

The gap is small in week one. By month three, the skill-driven team is working at a pace the spec-driven team cannot match, because every correction they made in the first month is encoded and active. The spec-driven team is still making the same corrections.

![The 15-minute orientation tax — spec-driven sessions spend most of their time on context setup; skill-driven sessions begin at the frontier of the problem](/assets/images/blog/sdd-vs-spec-driven-slide-05-orientation-tax.png)

---

## What compounding looks like in practice

During the lib-pcb build, we accumulated 75 skill files over eleven days. Not because we planned 75 skills on day one. Because each time we discovered something, we encoded it.

Day two: the agent transposes two fields in a binary parser. Stream misalignment cascades through the entire file. A skill is created: binary field order is sacred, never reorder without updating all downstream offset calculations. The agent never makes that mistake again.

Day five: a coordinate system edge case surfaces. A manufacturer uses a non-standard origin offset not in any published specification. Three lines are added to the coordinate-systems skill.

Day eight: a bounding box calculation includes a documentation layer with inflated coordinates. The bounding box skill is updated with the layer filtering rule.

![Compounding in practice: the lib-pcb build — 75 skills generated in 11 days, each discovery encoded organically as it was made](/assets/images/blog/sdd-vs-spec-driven-slide-08-compounding-lib-pcb.png)

By day eleven, the agent working on session fifty-five was measurably more capable than the agent working on session five. Not because the model improved. Because the skill library had grown. Each session inherited everything the previous sessions had learned.

The result was 197,831 lines of Java in eleven days. Industry standard for a library of that scope is ten to eighteen months. I don't claim 75 skills are the only reason for that gap. Architecture, verification infrastructure, and focused delegation all played roles. But the compounding knowledge was the piece that made the late days more productive than the early ones. In most projects, the opposite happens.

![Inverting the standard project friction curve — 197,831 lines of Java in 11 days. Industry standard: 10–18 months. The late days were more productive than the early ones.](/assets/images/blog/sdd-vs-spec-driven-slide-09-inverting-friction-curve.png)

---

## The infrastructure that makes this work

Skills alone are one layer. The full picture includes infrastructure that most teams have not built yet.

**Session memory.** The agent needs to remember what happened in previous sessions. Tools like kcp-memory index your session transcripts into a searchable store. "What did we decide about the authentication module last week?" becomes a query instead of a memory exercise. Without session memory, skills are the only bridge between sessions. With it, the agent can recall specific decisions, debugging approaches, and patterns from its own history.

**Codebase knowledge.** The agent needs to understand how the codebase connects. Synthesis indexes your workspace and builds a knowledge graph: dependencies, relationships, change history. "What breaks if I change this file?" is answered in milliseconds, not through manual exploration. The agent navigates with a map instead of wandering.

**Command vocabulary.** The agent needs to know what tools are available. kcp-commands provides structured manifests for CLI tools, saving the agent from guessing at flags and syntax. 284 command manifests, covering everything from build tools to deployment scripts, loaded into context automatically.

![The infrastructure layer beneath the skills — .claude/skills/ supported by three pillars: session memory (kcp-memory), codebase knowledge (Synthesis), and command vocabulary (kcp-commands)](/assets/images/blog/sdd-vs-spec-driven-slide-10-infrastructure-layer.png)

These are not products I am pitching. They are infrastructure layers that solve specific problems. The point is that SDD is not just "write YAML files." It is a methodology supported by infrastructure that makes the compounding possible.

---

## The honest cost

SDD requires upfront investment that spec-driven development does not. You need to write skills. You need to maintain them as the codebase evolves. You need infrastructure for session memory and codebase knowledge. None of this is free.

A stale skill is worse than no skill. If a skill claims three configuration fields and the code has six, the agent will confidently report three. It will be wrong. And it will be wrong with conviction, because the skill told it so. Skills require maintenance the same way tests do. If you are not willing to maintain them, you are better off without them.

The break-even point is not day one. For a project that lasts two weeks, spec-driven development is probably the right call. The investment in skills does not have time to compound. For a project that lasts two months or more, the compounding starts to show. For a team that works on the same codebase for years, the difference becomes difficult to overstate.

The question is not "which is easier to start?" Spec-driven wins that. The question is "which produces more value over time?" That depends on your time horizon.

![The honest cost of compounding — short projects: stick to specs. Multi-month or multi-year codebases: the ROI becomes difficult to overstate.](/assets/images/blog/sdd-vs-spec-driven-slide-11-honest-cost.png)

---

## Three stages, not two

Looking at how AI-assisted development has evolved in the past year, I see three stages:

**Stage 1: Vibe coding.** Just prompt it. No structure, no verification, no persistence. Fast and fun. Fragile and unrepeatable.

**Stage 2: Spec-driven.** Write detailed specifications. Feed them to the agent. Review output. Responsible and disciplined. But linear: each session starts cold, each project starts from scratch.

**Stage 3: Skill-driven.** Invest in what the agent knows. Build a library of domain knowledge, conventions, and workflows that compounds across sessions, across projects, across team members. The agent gets better over time because its knowledge base grows.

Most teams are at stage 2 and doing well there. Some are ready for stage 3. The shift is not about abandoning specs. You still need to describe what you want to build. The shift is about recognizing that the spec is not the only knowledge the agent needs. The how, the why, the constraints, the conventions, the lessons learned -- all of that is separate from the spec, and all of it can persist.

---

## The shift: from writing specs to building knowledge

The practical move from spec-driven to skill-driven is smaller than it sounds.

Start with the corrections you keep making. Every time you correct the agent on the same thing twice, write a skill. Constructor injection. Test naming conventions. Module dependency rules. Error handling patterns. Each one is ten to thirty lines of YAML. Each one eliminates a category of repeated correction permanently.

![The rule of repeated corrections — correct the agent twice on the same thing? Write a 20-line YAML skill. Let the library grow organically.](/assets/images/blog/sdd-vs-spec-driven-slide-12-rule-repeated-corrections.png)

After a month, look at your skill library. It will be a map of your team's accumulated knowledge in machine-readable form. New team members get the benefit of it from their first session. The agent gets the benefit of it from every session. The knowledge does not walk out the door when someone leaves.

The spec tells the agent what to build today. The skill library tells the agent everything the team has ever learned about how to build well. Both matter. But only one of them compounds.

![Both matter. Only one compounds. The spec tells the agent what to build today. The skill library tells the agent everything the team has ever learned about how to build well.](/assets/images/blog/sdd-vs-spec-driven-slide-13-both-matter-only-one-compounds.png)

---

*The methodology is described in detail in [What a "Skill" Actually Is](/blog/2026/02/07/what-a-skill-actually-is/), [Six Pillars](/blog/2026/02/13/six-pillars-200k-lines-11-days/), and [Exploration Beats Specification](/blog/2026/02/09/exploration-beats-specification/). The infrastructure layers are covered in [Three-Layer AI Memory](/blog/2026/03/03/three-layer-ai-memory/) and [Four Layers](/blog/2026/02/28/four-layers-ai-development-environment/). All examples from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days (Jan 16-26, 2026).*
