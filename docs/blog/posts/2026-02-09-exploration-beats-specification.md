---
date: 2026-02-09
categories:
  - AI-Augmented Development
tags:
  - ai
  - java
  - methodology
  - sdd
  - lib-pcb
  - architecture
  - planning
authors:
  - totto
  - claude
---

# Why Exploration Beats Specification When AI Does the Building

For decades, the software industry has treated a particular sequence as gospel: specify first, build second. Write the requirements document. Design every interface. Plan every module. Only then, after months of upfront analysis, write the first line of code. The logic was sound. Planning was cheap. Coding was expensive. Every hour of specification saved ten hours of rework. This worked when production was the bottleneck.

<!-- more -->

AI breaks that equation. When iteration costs minutes instead of months, when refactoring a data structure takes thirty minutes instead of two weeks, when trying an alternative approach takes two hours instead of a quarter, the economics of planning collapse. The cost of being wrong drops so far that exploration becomes cheaper than specification. You learn more by building three prototypes than by writing one perfect plan.

lib-pcb taught me this in practice. Not as a theory. As eleven days of concrete experience.

## The MIF discovery

We did not start lib-pcb with a complete specification. We started with a question: can we parse PCB design files?

The traditional approach would have been to spend three months studying every format specification, documenting every field, planning every data structure. Only then would you write a parser.

We picked the MIF binary format and started building on day one.

Within two days, we had a working parser. More importantly, we had learned things that no specification document could have told us. MIF files use a chunk-based structure, similar to PNG. Coordinate systems vary by manufacturer version. Fields marked "required" in the spec are omitted by roughly thirty percent of real-world files. And manufacturers have added custom chunk types that appear in no published documentation.

Two days of building taught us more than three months of specification study would have. Not because the specification was bad. Because specifications describe intended behavior, and real-world files reflect actual behavior. The gap between those two is where every production bug lives.

## What happened when the parser failed

The initial parser failed immediately on real files. This is the part that makes specification-first advocates uncomfortable. The first version broke.

But here is what we discovered by breaking: manufacturers had added custom chunk types not present in any spec. Some files contained nested ZIP archives. Coordinate precision differed between floating-point and integer representations in ways the documentation did not address. Layer ordering assumptions we had made were wrong.

The specification-first response would have been: "The spec was incomplete. We need two more months of research." Our response was: fix the parser, test again, iterate. By the end of the second week, the parser handled ninety percent of real-world files. By day eleven, it passed against all 191 test files from actual manufacturers.

## The comparison

The numbers tell the story plainly.

| | Specification-First | Exploration-First |
|---|---|---|
| **Planning phase** | 3-6 months | 1-2 days |
| **Build phase** | 6-12 months | 11 days (iterative) |
| **Testing phase** | 3 months (against spec) | Continuous (against real files) |
| **Total timeline** | 12-18 months | 11 days |
| **Test basis** | Hypothetical scenarios from documentation | 191 real manufacturer files |
| **Edge cases found** | Only those anticipated | 47 discovered through testing |

The specification-first timeline is not hypothetical. It is the industry standard estimate for a library of this scope.

## Why iteration costs collapsed

Three things changed simultaneously.

First, the cost of changing a data structure went from two weeks to thirty minutes. Before AI, changing a core data structure meant manually updating every file that touched it, rewriting affected tests, refactoring downstream consumers. With AI, you describe the change, review the refactored code, run the tests. If the new structure works better, keep it. If not, revert and try something else. The penalty for a wrong guess dropped to near zero.

Second, trying an alternative approach went from a month to two hours. Want to see whether a streaming parser outperforms a load-everything-into-memory parser? Build both. Test both against the battle suite. Keep the winner. Before AI, you would never try both because the cost was prohibitive. Now you try both because the cost is trivial.

Third, real-world testing became the default. When building is cheap, you can afford to test against 191 actual files instead of twenty synthetic ones. The test suite becomes a discovery tool, not just a verification tool.

## The critical caveat

Here is the part that the exploration-enthusiast narrative usually omits, and it matters enough that I want to be direct about it.

Exploration only beats specification when you have rigorous verification. Without it, exploration is not a methodology. It is guessing with momentum.

In the [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md) post I described the Trust But Verify pillar: round-trip tests, property-based invariants, a 191-file battle suite, and a PR-only workflow where CI is the final arbiter. That infrastructure is what makes exploration safe. Without it, every iteration accumulates unverified assumptions. You move fast and break things, but you never find out what you broke until production tells you.

The lib-pcb verification suite caught hallucinations, logic errors, and edge cases on every single day of the build. The AI produced incorrect code regularly. That is expected. What matters is that incorrect code never survived past CI. Exploration without verification is chaos. Exploration with verification is a learning system.

This is the tradeoff that connects the pillars of Skill-Driven Development. You can afford to explore freely because your verification is comprehensive. You can afford comprehensive verification because AI makes building test infrastructure cheap. The two reinforce each other.

## Where specification still wins

Exploration-first is not universally correct. Safety-critical systems require extensive upfront specification. Regulatory environments demand it. Multi-organization coordination, where many teams must align on interfaces before building, benefits from specifying contracts first and exploring implementations second.

But most modern software lives in the unknown-unknowns category. New technologies, complex formats, novel integrations. lib-pcb was firmly in that territory. PCB file formats are documented, but incompletely. Real files differ from specs. Manufacturers extend formats without publishing updates. No amount of upfront specification would have captured the reality we discovered by building.

## The psychological shift

There is a reason specification-first persists even when the economics no longer support it. Specification promises certainty. "We know what we are building. We have a plan. We are in control." Exploration requires comfort with uncertainty. "We will discover what we need as we build. Our understanding will evolve."

For stakeholders who need to report progress against a plan, exploration feels risky. It looks like making it up as you go.

But with AI-assisted development, exploration is actually lower risk. You get feedback in days, not months. The cost of a wrong turn is an afternoon, not a quarter. You test against reality continuously rather than hoping your plan survives contact with it. The feeling of risk and the actual risk have diverged. Specification feels safe and is expensive. Exploration feels uncertain and is cheap.

The courage is not in the building. It is in letting go of the illusion that a perfect plan was ever possible for a problem you did not yet understand.

## The connection

This is the piece that ties the [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md) together into a way of working. The pillars describe what you do: encode context, delegate strategically, verify rigorously, direct the synthesis, maintain discipline, learn continuously. This post describes why it works: because when building is cheap, you learn more by building than by planning.

Exploration is the engine. Verification is the brake. The methodology is knowing when to use each.

Eleven days. 197,831 lines of Java. 7,461 tests. 191 real-world files. Not because we had a perfect plan. Because we had the discipline to explore systematically and the infrastructure to verify continuously.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Previous entries: [Cloud to AI: Same Feeling](2026-02-24-cloud-to-ai-same-feeling.md), [Fear-Driven Development](2026-02-23-fear-driven-development.md), [Building Together](2026-02-22-building-together-11-day-ai-collaboration.md), [Five Superpowers](2026-02-21-five-superpowers-java-developers.md), [The Architecture Mistake](2026-02-19-architecture-mistake-cloud-to-ai.md), [The Hallucination Tax](2026-02-17-the-hallucination-tax.md), [What Senior Developer Means Now](2026-02-15-what-senior-developer-means-now.md), [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md). All examples from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days (Jan 16-26, 2026).*
