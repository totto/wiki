---
date: 2026-01-26
categories:
  - AI-Augmented Development
tags:
  - ai
  - documentation
  - methodology
  - skills
  - knowledge
authors:
  - totto
  - claude
---

# Documentation That Writes Itself (No, Really)

Yes, I know. "Self-writing documentation" is the perpetual motion machine of software engineering. Every generation of tooling has promised it. Javadoc would generate your API reference. README generators would scaffold your project descriptions. Wiki pages would capture institutional knowledge. Sprint retrospectives would produce living documents. None of it worked. The documentation was either generated and useless, or useful and never written.

So when I say that skill-driven development produces documentation as a natural byproduct of building software, I understand why the reasonable response is skepticism. I would be skeptical too. But after 75 skill files emerged during an 11-day build of [lib-pcb](https://github.com/exoreaction/lib-pcb), I have to describe what actually happened, because it was not what any previous "auto-documentation" approach looked like.

<!-- more -->

![Naming is understanding: how articulating context creates documentation](/assets/images/blog/slide-03-naming-is-understanding.png)

## Why every previous attempt failed

The failure pattern is always the same. Documentation is treated as a separate deliverable from the work itself. You build the feature, then you document it. Or you document it in parallel, updating a wiki page while writing code. In both cases, the documentation is an obligation imposed on someone who would rather be doing something else. The incentive structure is hostile.

Javadoc generates API reference from code comments. What it produces is technically accurate and almost completely useless for understanding intent. You get method signatures, parameter types, return values. You do not get: why this method exists instead of the three alternatives that were considered and rejected. Why this parameter is a `long` in nanometers instead of a `double` in millimeters. Why this class has a package-private constructor. The interesting knowledge, the knowledge that prevents the next developer from making a mistake, lives in the developer's head and dies there.

README generators produce boilerplate. Wiki pages rot within weeks of creation, because the person who wrote them has moved on and the person reading them has no way to know which parts are still accurate. Sprint documentation is written to satisfy a process, read by nobody, and outdated before the ink dries.

The common thread: in every case, documentation is written for a hypothetical future reader. That reader might never arrive. And even if they do, the author had no concrete use case in mind when writing. The result is documentation that is technically present and practically absent.

## The pattern that actually works

When you work with an AI coding agent, something structurally different happens. You have to articulate what you are building and why, because the AI has no context otherwise. It does not know your naming conventions. It does not know your architectural constraints. It does not know that the `core` module has zero framework dependencies by design, or that coordinate values are stored as `long` nanometers to avoid floating-point drift in manufacturing output.

So you tell it. And if you are going to tell it the same thing in every session, you write it down in a skill file so you do not have to repeat yourself.

That act of writing it down is documentation. But it is documentation with a crucial difference from every previous approach: you are writing it for a concrete, immediate consumer. Not a hypothetical future reader. The AI. Tomorrow. When it opens this project and needs to know the same things you just spent twenty minutes explaining.

The motivation is selfish and therefore reliable. You write the skill because it saves you time next session. The fact that it also serves as project documentation for any human who reads it is a side effect. A very useful side effect.

## Three types that emerge naturally

Over 75 skill files, three distinct categories appeared without anyone planning a taxonomy.

**Intent documentation.** Why was this architectural decision made? You had to explain it to the AI so it would stop proposing alternatives you had already rejected. A skill that says "coordinates are stored as long nanometers, not double millimeters, because floating-point accumulation errors produce manufacturing defects at board edges" is more useful than any design document I have ever written. It captures the reasoning at the moment the decision was made, when the context was fresh and the trade-offs were vivid.

**Pattern documentation.** How do we do X in this codebase? The AI needed to learn it to do it consistently. After the third time correcting the same mistake, you write a skill: "Binary parsing: field order is sacred. Never reorder fields without updating all downstream offset calculations." That is a pattern document. It encodes a convention that would otherwise live in one developer's head and leak out as code review comments.

**Constraint documentation.** What must never happen here? You discovered the hard way, the AI generated something that broke a subtle invariant, and you wrote the rule so it would not happen again. "Board bounding box calculations must exclude non-copper documentation layers. German manufacturers embed title blocks in Gerber output with coordinates that extend far beyond the physical board edge." That constraint was discovered empirically and documented within minutes of the discovery.

## What useful context looks like versus what useless documentation looks like

A typical Javadoc comment:

```java
/**
 * Returns the board width.
 * @return the width of the board
 */
public long getWidth() { ... }
```

This tells you nothing you could not infer from the method signature. Compare a skill entry covering the same territory:

```yaml
instructions: |
  Board dimensions use long nanometers (1mm = 1_000_000).
  Do NOT use double/float for coordinates — accumulation
  errors produce 0.01mm drift at board edges, which fails
  manufacturing tolerances on panels > 300mm.

  BoundBox calculations must exclude documentation layers
  (layer type DOC, DRAWING, DIMENSION). German and Japanese
  manufacturers embed title blocks with coordinates 2-3x
  beyond the physical board edge.
```

The first is generated from code structure. The second was written because someone needed the AI to stop making a specific, costly mistake. One is ceremony. The other is knowledge.

## Why it actually gets written

Every "document as you go" process I have seen in thirty years of software development generates documents that nobody reads. The process exists, the compliance checkbox gets checked, and the documents gather dust.

Skills do not gather dust because they are actively consumed every session. If a skill is wrong, the AI does the wrong thing, and you notice immediately. If a skill is missing, the AI makes a mistake you have seen before, and the friction of repeating the correction motivates you to write the skill. The feedback loop is tight and concrete.

This is the real reason it works. You are not writing for a hypothetical audience. You are writing context for your next working session, which might be yourself in two hours. That use case is immediate enough to overcome the universal human reluctance to document anything.

The documentation is not a separate activity from the work. It is the work. Every skill file is simultaneously an instruction for the AI and a record of a decision, a convention, or a hard-won lesson. You do not need a documentation sprint, a wiki gardening day, or a tech writer. You need to keep working with AI, and the documentation accumulates as a side effect of making each session smarter than the last.

## The honest caveat

Skills can go stale. I wrote about this in [The Mirror Test](2026-02-11-the-mirror-test.md). A skill that claims three index fields when the code now has six produces confident, fluent, wrong answers. Stale documentation has always been a problem. Skills do not magically solve it. What they do is make staleness visible faster, because the AI acts on the stale information and produces observably wrong output. A stale wiki page can sit unnoticed for years. A stale skill produces a bug in the next session.

That is not a complete solution. But it is a faster feedback loop than anything I have seen before.

## The uncomfortable conclusion

Thirty years of trying to make developers write documentation failed because the incentive was wrong. You were asked to write for someone else, later, maybe. Skill-driven development succeeds because you are writing for yourself, now, definitely. The AI is the reader you actually have, not the reader you hope to have someday.

The documentation writes itself in the same way that tests write themselves when you practice TDD. They do not, literally. But the methodology creates conditions where writing them is the path of least resistance rather than an additional obligation. And that turns out to be the only incentive structure that has ever worked.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Related: [What a Skill Actually Is](2026-02-07-what-a-skill-actually-is.md), [The Mirror Test](2026-02-11-the-mirror-test.md), [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md), [Exploration Beats Specification](2026-02-09-exploration-beats-specification.md). All skill examples from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days with 75 skill files (Jan 16-26, 2026).*
