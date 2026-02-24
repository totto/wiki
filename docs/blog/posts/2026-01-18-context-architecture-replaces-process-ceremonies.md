---
date: 2026-01-18
categories:
  - AI-Augmented Development
tags:
  - ai
  - methodology
  - skills
  - context
  - onboarding
  - architecture
authors:
  - totto
  - claude
---

# Context Architecture Replaces Process Ceremonies

I have been writing software for thirty years. In that time I have sat through thousands of daily standups, hundreds of onboarding sessions, and more planning ceremonies than I care to count. Most of them existed for one reason: transferring context from people who had it to people who did not. The new developer needs to know how the deployment pipeline works. The team lead missed yesterday's discussion about the API change. The architect needs to understand why the data model looks the way it does before approving the next feature.

These are not bad reasons to meet. But they are expensive reasons. And increasingly, they are avoidable ones.

<!-- more -->

![Context engineering: how persistent skill files replace process ceremonies](/assets/images/blog/lib-pcb-memoir-infographic-03-context-engineering.png)

## What ceremonies actually do

Strip away the agile vocabulary and look at what a standup meeting accomplishes. Three developers spend fifteen minutes telling each other what they worked on yesterday and what they plan to do today. The stated purpose is coordination. The actual purpose is context synchronisation. Each person is broadcasting state so the others can update their mental models.

Now consider what happens when context is persistent and machine-readable. Every AI-assisted session loads a project context file that describes the current state of the codebase: what changed recently, what decisions were made, what conventions apply, what the known issues are. A new session -- whether from the same developer or a different one -- starts with that context already loaded. Nobody needs to explain it. Nobody needs to remember to mention it. It is there.

The standup does not disappear entirely. But it shrinks. The repetitive transfer part -- "I refactored the payment module, here is what changed" -- is handled by the context layer. What remains is the part that actually requires human judgment: "I am stuck on this design decision and I want your opinion."

## The three-level scope model

The context architecture that makes this work has three levels. If you have ever used Maven parent POMs or Spring Boot starter dependencies, the inheritance pattern is familiar.

```
~/.claude/CLAUDE.md                        # Global: applies everywhere
~/projects/company/.claude/CLAUDE.md       # Company: applies to all work here
~/projects/company/service-x/.claude/CLAUDE.md  # Project: applies only here
```

Global context encodes things that are true regardless of what you are working on. Your preferred error handling style, your git commit conventions, how you think about logging. These are the defaults you carry from project to project.

Company context encodes things that are true for a particular organisation. Naming conventions, deployment procedures, the architectural decision records, the list of past mistakes that should not be repeated. This is what a new hire spends three to six months absorbing.

Project context encodes things specific to one codebase. The module dependency graph, the domain-specific constraints, the format quirks that no other project shares. This is the level where you record that the coordinate system uses millimetres internally even though the API accepts inches, or that the config module has zero Spring dependencies by design and that constraint is intentional.

Each level inherits from the one above. A session working on `service-x` loads all three: your personal conventions, the company's institutional knowledge, and the project's specific details. You do not configure this per session. The directory structure does it for you, the same way a Maven child POM inherits from its parent without explicit declaration of every dependency.

## These are not prompts

There is a distinction that matters and keeps getting lost. A CLAUDE.md file or a skill file is not a prompt. A prompt is a one-time instruction: "Use constructor injection." A context file is institutional memory made executable.

The difference is persistence. A prompt expires when the session ends. Context persists across every session, for every developer on the team, loaded automatically. You write the constructor injection convention once. It applies to session one and session five hundred without anyone remembering to mention it.

Consider what this means for onboarding. A new developer joins the team. Traditionally, they spend three to six months absorbing institutional knowledge: architecture decisions, naming conventions, domain model rationale, the history of past mistakes. They sit in meetings, read wikis that may or may not be current, ask questions that the team has answered before.

With a well-maintained context architecture, a new developer's first AI-assisted session loads all of it. Not gradually. Not after reading the codebase for a week. Immediately, on session startup. The context file says: here is how we structure services, here is why the data model uses this particular normalisation, here is the deployment procedure, here are the three things that look correct but will break in production.

The three-to-six-month ramp-up does not disappear. Judgment takes time. Relationships take time. Understanding the domain deeply takes time. But the mechanical part -- learning where things are, what the conventions are, why decisions were made -- collapses from months to seconds.

## What it looks like in practice

During the [lib-pcb](https://github.com/exoreaction/lib-pcb) build, the skill library grew from zero to eighty-five files over eleven days. Each skill encoded something discovered during the build: a binary parsing convention, a coordinate system edge case, a manufacturer-specific format deviation.

By the end, a new session on day eleven knew everything that had been learned across the previous ten days. Not because someone sat down and explained it. Because the context loaded automatically. Session fifty-five was measurably smarter than session five, not because the model improved, but because the context architecture had accumulated eleven days of institutional knowledge.

The directory structure told the story:

```
.claude/
  skills/
    parsing/
      binary-field-ordering.yaml
      coordinate-precision.yaml
      layer-mapping.yaml
    validation/
      annular-ring-rules.yaml
      clearance-constraints.yaml
    manufacturing/
      gerber-deviations.yaml
      drill-format-quirks.yaml
```

Each file encoded knowledge that would otherwise live in someone's head and require a meeting, a Slack message, or an onboarding document to transfer. The skill files are version-controlled, scoped to the right context, and loaded without anyone deciding to look them up.

## What does not go away

I want to be direct about the boundary, because overstating it would undermine the point.

Context architecture removes the repetitive transfer overhead. It does not remove the human layer. Judgment does not live in a YAML file. The ability to look at a system design and feel that something is wrong before you can articulate why -- that is experience, and it is not encodable. Relationships with stakeholders, the ability to navigate organisational politics, the instinct for when to push back on a requirement -- these are human capabilities that no context file replaces.

What goes away is the tedious part. The part where a senior engineer explains the same deployment procedure for the fourth time this quarter. The part where a new hire spends two weeks figuring out the naming conventions by reading existing code. The part where a standup exists primarily because yesterday's decisions have no persistent record outside the participants' memories.

Real-time problem solving stays. Creative design stays. The difficult conversations stay. The ceremony of transferring information that could have been a file -- that is what shrinks.

## The maintenance contract

There is an honest cost. Context files go stale. I wrote about this in the [Mirror Test](2026-02-11-the-mirror-test.md) post: a skill file that said a module had three configuration fields was still being loaded after a refactoring added three more. The AI trusted the file. The file was wrong. The answer was confident, fluent, and incomplete.

Maintaining context files is a discipline, the same way maintaining tests is a discipline. When the code changes, the context must change with it. This is not free. But it is cheaper than the alternative, which is re-explaining the same institutional knowledge in every meeting, every onboarding session, and every Slack thread, forever.

## The pattern underneath

The pattern is not new. It is the same pattern the industry has applied to configuration for two decades. Spring Boot starters, Maven parent POMs, Terraform modules, Docker base images. You encode decisions at the right level of abstraction, inherit them downward, and override only where the specific context differs from the general case.

What changed is that the consumer of the configuration is no longer just a build tool or a runtime. It is a reasoning system that can read natural language and apply it to novel situations. The YAML file that says "never reorder fields in a binary parser without updating downstream offset calculations" is not a build constraint. It is a principle that an AI applies to every binary parsing task it encounters in that project.

That shift -- from machine-configuration to machine-comprehensible institutional knowledge -- is why ceremonies shrink. The context that used to require a meeting to transfer now loads in milliseconds. The knowledge that used to live exclusively in people's heads now lives in version-controlled files alongside the code it describes.

Every meeting that exists primarily to transfer context is a meeting that could have been a well-maintained file.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Previous entries cover [the comprehension bottleneck](2026-02-05-the-comprehension-bottleneck.md), [what a skill actually is](2026-02-07-what-a-skill-actually-is.md), [exploration vs specification](2026-02-09-exploration-beats-specification.md), [the Mirror Test](2026-02-11-the-mirror-test.md), and [the six pillars methodology](2026-02-13-six-pillars-200k-lines-11-days.md). All grounded in building [lib-pcb](https://github.com/exoreaction/lib-pcb) -- 197,831 lines of Java in 11 days (Jan 16-26, 2026).*
