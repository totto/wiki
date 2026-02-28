---
date: 2026-02-13
series: "Building lib-pcb"
categories:
  - AI-Augmented Development
tags:
  - ai
  - java
  - methodology
  - sdd
  - lib-pcb
  - architecture
  - testing
authors:
  - totto
  - claude
---

# Six Pillars: What We Learned Building 200,000 Lines in 11 Days

When we finished lib-pcb, the question we got most was: "How?"

Not "what model did you use?" Not "what IDE?" Those questions miss the point entirely. The model is the least interesting variable. What made 197,831 lines of Java, 7,461 tests, and 474 commits in 11 days possible was a methodology. Specifically: six practices that we have now codified under the name Skill-Driven Development.

<!-- more -->

![Totto in the Elprint PCB manufacturing facility, China — the real-world context for lib-pcb](/assets/images/blog/totto-pcb-factory-2025.jpg)

![lib-pcb: 197,831 lines in 11 days — the six pillars metrics card](/assets/images/blog/lib-pcb-metrics-card-11-days.png)

Previous posts in this series have covered pieces of the story. The [Fear-Driven Development](2026-02-23-fear-driven-development.md) post explained the verification mindset. The [Architecture Mistake](2026-02-19-architecture-mistake-cloud-to-ai.md) post drew the parallel between cloud lift-and-shift and AI lift-and-shift. The [Hallucination Tax](2026-02-17-the-hallucination-tax.md) post covered economics, control, and silent failures.

This post puts the whole thing together. Six pillars, what each one means in practice, and the concrete evidence from lib-pcb that convinced us they work.

---

## Pillar 1: Intelligent Context

AI starts every session knowing nothing about your codebase. You can either explain your conventions, invariants, and architectural decisions repeatedly, or you can encode them once so they load automatically. That is the entire choice.

For lib-pcb we chose encoding. By the end of the project there were 85 skill files. One for each major domain area: Gerber format parsing conventions, coordinate system handling, bounding box invariants, test scaffolding patterns, the reason `DateUtils` exists and why you never call `LocalDate.now()` directly. Each session started with Claude knowing what our most experienced team member knows.

The practical difference is measurable. Without skills, the AI explores from scratch every time. It reads files, builds a mental model, guesses at conventions, gets some wrong. With skills loaded, first-try accuracy improves dramatically. The same mistakes stop repeating. A new developer's first session has the same starting point as session 500.

The context was not written on day one. It evolved. Every bug fixed updated the history layer. Every pattern discovered became a skill file. Every architectural decision updated the master index. By day 11, Claude read three layers of context on startup: the CLAUDE.md index for navigation, 54 specialized skills for deep domain knowledge, and an implementation history for lessons learned.

This is the foundation pillar. Everything else depends on it.

---

## Pillar 2: Strategic Delegation

Not all AI tasks need the same model. Haiku for simple pattern-following. Sonnet for most coding. Opus for architecture and complex reasoning. Using Sonnet for everything is like using a sledgehammer to turn a screw.

The economics tell the story. At standard pay-per-token pricing, the estimated API cost for lib-pcb would have been around $100,000. We ran on Claude MAX subscription, which made unlimited usage practical. But even with unlimited access, strategic delegation still matters for two reasons: latency and clarity of thinking.

Haiku is faster than Sonnet. When you need 3,000 tests written against an established template, faster responses compound across hundreds of iterations. We generated the initial test suite in 4 hours using Haiku. Equivalent Sonnet work would have taken longer and consumed more quota for identical results.

Opus surfaces reasoning you can review. When the question is "should we use absolute or relative coordinates for drill mapping across manufacturer formats," you want the model that shows its work, not the one that gives a quick answer.

The template pattern emerged naturally: Sonnet creates one exemplary implementation. Haiku replicates it across similar components. 85% cost reduction without quality loss. Even on a flat subscription, the discipline matters because weekly quotas are real and rationing verification means rationing quality.

---

## Pillar 3: Trust But Verify

AI will produce code that looks correct and is wrong. The bounding box bug, which I covered in the [FDD post](2026-02-23-fear-driven-development.md), looked right, reviewed right, and was fundamentally broken for layers starting with empty features. You cannot verify AI output by reading it. You need systems that prove correctness.

The lib-pcb verification approach had four layers:

**Round-trip tests.** Parse a file, write it back, compare bytes. If the bytes don't match, something is wrong, regardless of how clean the code looks.

```java
byte[] original = Files.readAllBytes(testFile);
PCBDesign design = parser.parse(testFile);
byte[] written = writer.write(design);
assertArrayEquals(original, written);
```

**Property-based tests.** Mathematical invariants that can't be hallucinated away. A layer's bounding box must contain all its features. A drill hit must have a positive diameter. A coordinate transformation applied then inverted must return the original point within epsilon.

**Battle suite.** 191 real PCB files from the wild. KiCad, Altium, Eagle, German manufacturers who embed title blocks in Gerber data. Every change runs against all 191. If anything breaks, the build fails.

**PR-only workflow.** No direct commits to main. CI is the final arbiter.

The result: zero AI-induced production bugs. Not because the AI never hallucinated. It did, often. But hallucinations died in CI before reaching main.

---

## Pillar 4: Directed Synthesis

AI is not your replacement. It is your tool orchestrator. You identify the problem and approach. AI explores, finds, implements to your specification. You review every change and make the merge decision.

The risk without this pillar is real. Delegating "refactor the coordinate system" as a black box means an hour later you have 47 changed files, 60% understood. Tests pass. Something feels wrong but you cannot articulate what. I described this moment in the [Hallucination Tax](2026-02-17-the-hallucination-tax.md) post. It was the moment that forced structure into delegation.

The structured alternative, every time:

1. I identify the problem and decide the approach
2. AI explores the codebase, finds relevant files, maps dependencies
3. I review the findings and decide what to change
4. AI implements changes to my specification
5. I review every change, understand every file
6. AI runs tests and reports results
7. I make the merge decision

Seven steps. Four are mine. Three are the AI's. The AI's three are all execution, not judgment.

Each task stays small enough to understand completely. The AI does the typing. I do the thinking. Is it slower than "just do the whole thing"? Yes. Can I explain every line in the codebase after 11 days and 474 commits? Yes. That tradeoff is not close.

The counterintuitive outcome: understanding of the codebase increased over the 11 days, not decreased. Before AI, I understood code because I wrote it. With AI and vague delegation, I understood less because I didn't. With AI and directed synthesis, I understand more because I am forced to articulate what I want before the AI builds it. The articulation is the understanding.

---

## Pillar 5: Process Discipline

Discipline on process prevents compounding mistakes. The lib-pcb rule was absolute: every change through a PR, CI must pass, no direct commits to main.

The moment that established it permanently: a git log showing four commits.

```
commit 3a7f2e1 Fix bounding box calculation
commit 8b9c4d2 Actually fix bounding box calculation
commit 2e5f6a3 Revert "Actually fix bounding box calculation"
commit 7c8d9e4 Fix bounding box (for real this time)
```

Main was broken for 23 minutes. Anyone who pulled during those 23 minutes got a broken build. Never again.

The response was a pre-commit hook:

```bash
if [ "$(git rev-parse --abbrev-ref HEAD)" = "main" ]; then
    echo "ERROR: Direct commits to main are forbidden"
    exit 1
fi
```

And a PR checklist: all tests pass, battle suite passes, round-trip tests pass. No exceptions, no "I'll fix it in the next commit," no shortcuts when tired and behind schedule.

Process discipline requires refusing to cut corners at the exact moment when cutting corners feels most justified. At 11 PM on day 8, when you have been working for 14 hours and the fix is obviously correct and you just want to commit to main and go to bed. That is precisely the moment the process exists for.

The result: 474 commits over 11 days with zero broken builds on main.

---

## Pillar 6: Continuous Learning

Every bug fixed is a skill to update. Every pattern discovered is a file to add. The AI gets permanently smarter with each insight captured, rather than repeating the same mistakes session after session.

The feedback loop is concrete:

- Bounding box bug found on day 3. Root cause: sequential initialization from first feature, which might have empty bounds. Update the bounding box invariants skill. Claude never makes that mistake again.
- Coordinate system edge case discovered on day 5. German manufacturer uses a non-standard origin offset. Add to the coordinate system skill. Next session starts with that knowledge.
- Field order bug in ComponentFeatureParser on day 2. One field misplaced in binary parsing causes catastrophic stream misalignment. Create an anti-pattern skill: "Binary parsing: field order is sacred." Claude never transposes fields again.

The compounding effect: the skill graph at the end of lib-pcb contained 85 files encoding PCB domain knowledge. Each session in the second week was smarter than each session in the first week, not because the model changed but because the institutional knowledge grew.

The last 5 days of the 11-day build were more productive per session than the first 5. That is what continuous learning looks like when it works. Most software projects slow down as they grow. lib-pcb accelerated.

---

## The Summary

| Pillar | Core Practice | lib-pcb Evidence |
|--------|--------------|-----------------|
| Intelligent Context | CLAUDE.md + skill files | 85 skills, same starting point every session |
| Strategic Delegation | Right model for each task | Economically viable only at MAX subscription |
| Trust But Verify | Systems that prove correctness | 7,461 tests, 191-file battle suite, zero AI bugs |
| Directed Synthesis | Human in the driver's seat | Architect decisions stayed with the architect |
| Process Discipline | PR-only, CI is the arbiter | 474 commits, zero broken builds on main |
| Continuous Learning | Update skills from every bug | Session 55 smarter than session 5 |

None of these are individually surprising. Encode knowledge. Choose tools deliberately. Test rigorously. Stay in control. Follow process. Learn from mistakes.

What is surprising is how few teams do all six. Most do two or three. They use AI with good testing but no persistent context. Or they have strong context but skip verification. Or they verify but let the AI drive. Each missing pillar creates a failure mode that the others cannot compensate for.

---

## What to Call It

A senior architect at a Norwegian financial institution, watching a demonstration of this approach in February, gave it a name: Skill-Driven Development.

The name captures what distinguishes the methodology from "use AI." It is the systematic encoding of human skill into persistent, versioned, scoped knowledge assets that make AI capability compound over time. Not prompting. Not "AI-first." The deliberate practice of turning what you know into something the AI can apply consistently, session after session, developer after developer.

SDD is not a tool recommendation. It is a set of practices. The six pillars above are the practices. They work with Claude Code because that is what we used. They would work with any AI coding assistant that supports persistent context and skill loading. The model is the least interesting variable. The methodology is the answer.

That was true with cloud computing seventeen years ago. It is true with AI today. The teams that get value from AI will not be the ones with the best model. They will be the ones with the best methodology.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Previous entries: [Fear-Driven Development](2026-02-23-fear-driven-development.md), [Building Together](2026-02-22-building-together-11-day-ai-collaboration.md), [Five Superpowers for Java Developers](2026-02-21-five-superpowers-java-developers.md), [The Architecture Mistake](2026-02-19-architecture-mistake-cloud-to-ai.md), [The Hallucination Tax](2026-02-17-the-hallucination-tax.md). All examples are from building [lib-pcb](https://github.com/exoreaction/lib-pcb) over 11 days (Jan 16-26, 2026).*
