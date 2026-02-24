---
date: 2026-02-07
categories:
  - AI-Augmented Development
tags:
  - ai
  - sdd
  - skills
  - methodology
  - java
  - claude-code
authors:
  - totto
---

# What a "Skill" Actually Is (And Why It's Not a Prompt)

The term "skill" keeps appearing in discussions about AI-assisted development, and most explanations reduce it to "a file that Claude Code reads." That description is technically accurate and completely inadequate. It is like saying a class is "a file the JVM loads." True, unhelpful, and it obscures the thing that makes the concept powerful.

<!-- more -->

In the [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md) post, I described Intelligent Context as the foundation pillar of Skill-Driven Development. This post goes deeper into the mechanism. What a skill actually is, what it is not, why the distinction matters, and how 85 of them changed the trajectory of an 11-day build.

## The problem skills solve

Every Claude Code session starts from zero. The AI knows nothing about your codebase. Not your naming conventions, not your architectural decisions, not why `DateUtils.java` exists and why you never call `LocalDate.now()` directly. It does not know which modules are allowed to depend on which. It does not know that the `core` module has zero Spring dependencies by design, or why that constraint exists.

A new developer takes three to six months to absorb this kind of institutional knowledge. Claude Code without skills takes even longer in aggregate, because it never fully absorbs anything. It rediscovers conventions by reading code, often getting them wrong. It proposes `@Autowired` on fields when your team uses constructor injection exclusively. It puts `@Transactional` on repository methods when your convention puts it on service methods. It creates an H2-based integration test when your team uses TestContainers.

Each of these is a small mistake. Each one requires correction. Across hundreds of sessions, the corrections compound into a significant tax on development speed.

Skills front-load the knowledge so every session starts with what your most experienced team member knows. Not gradually, not after reading the codebase for twenty minutes, but immediately on session startup.

## The anatomy of a skill

A skill is a YAML or Markdown file that lives in `.claude/skills/`. It has a name, a description, trigger context, and instructions. The instructions contain the encoded knowledge: conventions, patterns, anti-patterns, gotchas.

A concrete example from a Spring-based payment service:

```yaml
name: spring-wiring-conventions
version: 1.0.0
description: Spring wiring conventions for the payment-service module.

trigger_phrases:
  - "add a new service"
  - "wire a bean"
  - "dependency injection"

instructions: |
  # Spring Conventions (payment-service)
  
  - @Transactional goes on service methods, never repositories
  - Constructor injection only (no @Autowired on fields)
  - All REST controllers return ProblemDetail for 4xx/5xx
  - The core module has zero Spring dependencies by design
  - Integration tests use @SpringBootTest with TestContainers, never H2
```

That is not clever prompting. It is the knowledge your senior engineer carries in their head, written down in a form Claude can load every session. The difference is persistence. A prompt is a one-time instruction that expires when the session ends. A skill is version-controlled, scoped to the right context, and loaded automatically every time the AI works on that project.

## What a skill is not

Three things that look similar but are structurally different.

**A skill is not a prompt.** A prompt is ephemeral. You type "write a Spring service that uses constructor injection" and the AI follows the instruction for that response. Next session, it has forgotten. A skill persists across every session. You write the constructor injection convention once. It applies forever, to every developer on the team, without anyone remembering to mention it.

**A skill is not a template.** Templates produce documents. A Cookiecutter template generates a project skeleton. A skill does not generate anything by itself. It encodes the knowledge that makes generation correct. The template says "here is the structure." The skill says "here is why the structure looks this way, and here are the constraints that must hold."

**A skill is not documentation.** Documentation is written for humans to read. READMEs, Confluence pages, design documents. AI can read documentation, but it does not know when to. A developer reads the deployment guide when they need to deploy. The AI reads whatever is in its context window. A skill is loaded automatically based on what the AI is doing. It is documentation that activates at the right moment without anyone deciding to look it up.

The distinction matters because documentation scales to humans, one reader at a time, when they choose to read it. Skills scale to AI: every session, for every developer on the team, automatically.

## Scoping: the three tiers

Skills have a scoping model that prevents cross-contamination:

| Scope | Location | Loads when |
|-------|----------|------------|
| Global | `~/.claude/skills/common/` | Every session, every project |
| User | `~/.claude/skills/` | Every session for that user |
| Project | `.claude/skills/` | That project only |

You do not want PCB rendering conventions loading when you are writing a REST API. You do not want your personal coding preferences overriding a team's project conventions. The scoping prevents this the same way Maven module boundaries prevent unwanted transitive dependencies. Each layer adds context without interfering with the others.

Global skills encode things that apply everywhere: your preferred error handling style, your git commit conventions, your approach to logging. Project skills encode things specific to that codebase: the module dependency graph, the naming patterns, the domain-specific constraints that no other project shares.

## The compounding effect

lib-pcb ended with 85 skill files. Not because anyone planned 85 skills on day one. Because each time a convention was discovered or a mistake was made, a skill was created or updated.

Day 2: Claude transposes two fields in a binary parser. Stream misalignment cascades through the entire file. A skill is created: "Binary parsing: field order is sacred. Never reorder fields without updating all downstream offset calculations." Claude never makes that mistake again.

Day 3: The bounding box calculation includes a documentation layer with inflated coordinates. A German manufacturer had embedded title blocks in Gerber output. The bounding box skill is updated with the layer filtering rule. Every subsequent session knows to exclude non-copper layers from board dimension calculations.

Day 5: A coordinate system edge case surfaces. A manufacturer uses a non-standard origin offset not documented in the format specification. The coordinate system skill grows by three lines. Next session starts with that knowledge.

By the end of the build, session 55 was measurably smarter than session 5. Not because the model improved. Because the skill library had grown. The last five days of the eleven-day build were more productive per session than the first five. That is what compounding institutional knowledge looks like when the mechanism is explicit and version-controlled.

Most software projects slow down as complexity grows. The skill library inverted that trajectory.

## Any workflow can become a skill

The pattern extends beyond domain knowledge. If your team uses an internal deployment tool:

```yaml
name: deploy-service
trigger_phrases:
  - "deploy to staging"
  - "release to production"
instructions: |
  Use platform-cli deploy. Never kubectl apply directly.
  Staging:    platform-cli deploy --env staging --service <name>
  Production: platform-cli deploy --env prod --service <name> --approval-ticket <JIRA>
  
  Production deployments require a JIRA approval ticket.
  Deployments without --approval-ticket will succeed on staging
  and fail silently on production. This is the most common
  deployment mistake in this organization.
```

Thirty seconds to write. Every developer on the team now has deployment expertise encoded in their Claude Code sessions. The person who wrote the skill does not need to be in the room when someone deploys at midnight.

This is the mechanism by which institutional knowledge survives team changes, late nights, and the steady erosion of tribal knowledge that every organization experiences. Not because someone remembered to mention it. Because it loads automatically.

## The integrity problem

There is a failure mode I need to be honest about, because I discovered it empirically.

Skills can go stale. The [Mirror Test](2026-02-11-the-mirror-test.md) benchmarks found that a skill claiming three Lucene boost fields was loaded by agents who then confidently reported three fields. The source code had six. The skill had not been updated after a refactoring. The agents with no skills at all read the source directly and got the right answer.

Stale skills produce confident, fluent, wrong answers. That is worse than no skills at all, because no skills at least generate hedging and verification behavior. A skill that says "trust me" gets trusted.

This is a solvable problem. You update skills when the code changes, the same way you update tests. The Synthesis project now tracks file changes against skill references, flagging when a skill's claims may be outdated. But the failure mode is real, and anyone adopting skills should know it exists. A skill is a claim about the codebase. Claims require maintenance.

## The real distinction

The question I get most often about Skill-Driven Development is some variation of "so it's better prompting?" No. It is not prompting at all.

Prompting is talking to the AI. Skills are teaching the AI before the conversation starts. The difference is the same as the difference between telling a new hire what to do on every task versus onboarding them so they already know. One scales to one conversation. The other scales to every conversation, for every team member, permanently.

Eighty-five skills, accumulated over eleven days, encoding the domain knowledge of PCB manufacturing, Java conventions, coordinate geometry, format parsing, and the specific ways manufacturers deviate from their own specifications. That is not a prompt library. It is institutional memory in machine-readable form.

The model is the least interesting variable. The methodology is the answer. And the skill file is the unit of methodology that makes everything else work.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Previous entries: [Cloud to AI: Same Feeling](2026-02-24-cloud-to-ai-same-feeling.md), [Fear-Driven Development](2026-02-23-fear-driven-development.md), [Building Together](2026-02-22-building-together-11-day-ai-collaboration.md), [Five Superpowers](2026-02-21-five-superpowers-java-developers.md), [The Architecture Mistake](2026-02-19-architecture-mistake-cloud-to-ai.md), [The Hallucination Tax](2026-02-17-the-hallucination-tax.md), [What Senior Developer Means Now](2026-02-15-what-senior-developer-means-now.md), [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md), [The Mirror Test](2026-02-11-the-mirror-test.md), [Exploration Beats Specification](2026-02-09-exploration-beats-specification.md). All examples from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days (Jan 16-26, 2026).*
