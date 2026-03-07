---
date: 2026-03-07
categories:
  - AI-Augmented Development
tags:
  - reflection
  - methodology
  - claude-code
  - synthesis
  - skill-driven-development
  - productivity
authors:
  - totto
---

# Six Weeks After the Sprint

The sprint story is easy to tell.

Eleven days. 197,831 lines of Java. A PCB design library built from nothing to manufacturing-ready. Clean numbers, clear arc, dramatic compression of time.

![The sprint — 11 days, 197,831 lines of Java, PCB design library built from nothing to manufacturing-ready](/assets/images/blog/six-weeks-after-the-sprint/slide-02.png)

That was January 27. Six weeks ago.

Nobody asked what happened after. Which is the point.

<!-- more -->

![The marathon is where the methodology actually has to prove itself](/assets/images/blog/six-weeks-after-the-sprint/slide-03.png)

---

Here is what happened after.

I spent an evening fixing a CI pipeline because Surefire was crashing the JVM on a forked process. I bumped Java from 17 to 21 across a dozen modules and lost an afternoon to one of them choking on the new class file version. A Windows installer worked on my machine and on nobody else's.

This is the part that does not get a LinkedIn post. The adrenaline is gone. Nobody is counting the days. And yet — this is exactly where methodology has to hold, because if it only works when you are sprinting and the world is watching, it does not work.

![The reality of software development is fiercely ordinary — infrastructure work, invisible unless it fails](/assets/images/blog/six-weeks-after-the-sprint/slide-04.png)

---

Some numbers, for those who want them.

Synthesis — the knowledge infrastructure tool I have been building since the sprint — is now 314,000 lines of Java across 318 commits. Twenty releases. 4,177 tests. 55 CLI commands. 8 MCP tools. The Knowledge Context Protocol spec went from version 0.3 to 0.6 with parsers in three languages. A companion package shipped to npm with 284 YAML manifests.

![The output remains staggering, even when the adrenaline fades](/assets/images/blog/six-weeks-after-the-sprint/slide-05.png)

Those numbers are accurate. They are also misleading, because they suggest a clean upward line. The reality is that some days the most important commit was `chore(deps): bump maven-shade-plugin to 3.6.0`. The shade plugin was breaking reproducible builds. Fixing it meant every subsequent release worked correctly. Nobody tells that story. It is a good story.

![Yet the lived experience is entirely about intense context-switching](/assets/images/blog/six-weeks-after-the-sprint/slide-06.png)

---

I have around 190 Claude Code skill files now. Each one exists because I found myself explaining something twice and decided not to explain it a third time. When I sit down for session fifty on a codebase, it knows things session one did not. Not because the model got smarter. Because I made the context smarter.

Building a skill library feels like housekeeping. It is housekeeping. That is not a criticism.

![System intelligence accumulates quietly in the background — a flywheel disguised as housekeeping](/assets/images/blog/six-weeks-after-the-sprint/slide-07.png)

65,905 files indexed across all workspaces. When I need the blast radius of a change in one repository, the answer takes under a second. That capability did not arrive in a moment. It grew one scanning pass at a time, the way useful things usually do.

![Compound returns make every Tuesday slightly less frustrating](/assets/images/blog/six-weeks-after-the-sprint/slide-08.png)

Compound returns do not announce themselves. They just make Tuesday slightly less frustrating than the Tuesday before.

---

Two full workshop cohorts came through during these six weeks. Developers in Oslo, each bringing a different codebase — legacy systems that had been accruing debt for years, greenfield services that barely existed yet, everything in between. Same method, all of them.

That tested something the sprint could not test: whether the methodology generalises beyond my own projects and my own habits.

It does. That was more satisfying than the sprint, if I am honest.

There was also continuous client work. Long-running engagements where context accumulated across months. A stint advising on AI in regulated environments — compliance and security requirements that do not bend for anyone's productivity numbers. Different knowledge, different judgment, different constraints each time. The AI helped with all of it. The AI was not the hard part of any of it.

---

I want to be careful here. The temptation is to present the last six weeks as continuous acceleration. A story where the sprint was the beginning and things only got faster.

That is not what happened.

What happened is sustained output with variation. Some days are ten-hour deep-focus sessions producing thousands of lines of tested code. Some days are spent entirely on release management, making sure version numbers are correct and Maven Central is happy. One afternoon I tracked down a false positive in a security scanner — it was triggering on commented-out XML. The fix was three lines.

The AI helps with all of it. None of it makes for a compelling narrative. All of it matters.

![Progress is sustained output with variation, not continuous acceleration](/assets/images/blog/six-weeks-after-the-sprint/slide-11.png)

---

What I can say honestly is that the pace from the sprint did not collapse. It changed shape.

The dramatic compression is gone. What replaced it is a steady throughput that would not have been possible a year ago. The ability to move between three repositories in a day without losing hours re-establishing where I was. The ability to fix a CI issue at night and still have an evening.

That is a quieter claim than "197,831 lines in eleven days." It is also a more useful one. Sprints end. The question was always what comes after.

---

The finish line keeps moving. Synthesis needs Windows support improvements. The KCP spec needs a security extension. Client engagements are in various stages. The skill library needs pruning. The next workshop cohort needs preparation.

![The marathon has no fixed finish line](/assets/images/blog/six-weeks-after-the-sprint/slide-12.png)

It will probably look a lot like the last six weeks. Some impressive days, some tedious ones. Skills accumulating. Context growing. The occasional commit that is just `fix(ci): pin surefire fork count to 1`.

That is what sustained AI-augmented development actually looks like. Not the sprint. The quiet part afterwards, where you find out if any of it was real.

![This is the quiet reality of the AI-augmented developer](/assets/images/blog/six-weeks-after-the-sprint/slide-13.png)
