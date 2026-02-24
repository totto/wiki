---
date: 2026-01-24
categories:
  - AI-Augmented Development
tags:
  - ai
  - methodology
  - architecture
  - iteration
  - economics
  - decision-making
authors:
  - totto
  - claude
---

# The Cost of Iteration Collapsed. Now What?

For most of my thirty years in software, iteration has been expensive. Not in theory. In practice, in the way that shapes every decision a team makes. When changing a core data structure takes two weeks of careful refactoring across dozens of files, you do not change the data structure on a hunch. You analyze. You write a proposal. You get approval. You schedule it for the next sprint, or the one after that. The cost of being wrong is measured in weeks, and so the entire machinery of software engineering orients itself around not being wrong.

That cost has collapsed. Not gradually. Not by half. By orders of magnitude. And I am not sure we have reckoned with what that means for the way we work.

<!-- more -->

![Traditional vs AI-assisted development timeline comparison](/assets/images/blog/traditional-vs-ai-assisted-timeline-comparison.png)

## The numbers I have observed

I want to be specific, because "iteration is cheaper now" is vague enough to mean nothing. Here is what I have actually seen change, working with AI-assisted development over the past year.

Changing a data structure: two weeks became thirty minutes. Before, this meant tracing every reference, updating every consumer, rewriting affected tests, validating downstream behavior manually. Now you describe the structural change, review the refactored code, run the test suite. If the new structure is better, keep it. If not, revert and try something else in the next thirty minutes.

Trying a different architectural approach: a month became two hours. Want to know whether a streaming parser outperforms a batch parser for your use case? Build both. Test both against real data. Keep the winner. Before AI, you would never build both because the cost was prohibitive. You would analyze, estimate, argue in a meeting, and commit to one approach based on reasoning that you hoped was correct.

Building a parser for a new format: three months became two days. I watched this happen repeatedly during the [lib-pcb](https://github.com/exoreaction/lib-pcb) build. Eight format parsers in eleven days. The industry estimate for a single parser of comparable complexity is three to six months.

Writing comprehensive tests: previously skipped because time-prohibitive, now routine. When building is cheap, you can afford to test against 191 real-world files instead of twenty synthetic ones. The test suite becomes a discovery tool, not a cost center.

These are not projections. They are measurements from a project that produced 197,831 lines of Java in eleven days, with 7,461 tests at a 99.8% pass rate. Not because the problem got simpler. Because the cost of discovering complexity through building became lower than the cost of specifying it away from the whiteboard.

## Everything we built was cost mitigation

Here is the observation that took me longer than it should have to articulate: most of our software engineering practices are not about producing better software. They are about managing the cost of iteration.

Big upfront design exists because changing direction late was expensive. If you were going to spend six months building, you wanted to be confident about the direction before you started. The design document was insurance against the cost of rework.

Careful requirements gathering exists because building the wrong thing was expensive. If a misunderstood requirement cost three months of implementation, you spent a month making sure the requirements were right. The cost of understanding upfront was lower than the cost of discovering you were wrong after building.

Estimation exists because committing resources to work was expensive. If a feature took longer than expected, it delayed everything behind it. The estimate was a risk management tool for resource allocation under expensive iteration.

Change control boards exist because changes had cascading costs. If modifying one module broke three others, and fixing those took weeks, then controlling changes was rational. The board was a gate against expensive ripple effects.

Long release cycles exist because deploying and rolling back was expensive. If shipping was costly and fixing was costly, you batched changes and tested extensively before releasing.

Every single one of these practices is a rational response to a world where iteration is expensive. And I am not arguing they were wrong. Given the economics of the past thirty years, they were correct. The question is what happens when those economics change.

## What actually changes

When the cost of being wrong drops to thirty minutes, the rational decision-making strategy inverts. Instead of "minimize the chance of making the wrong choice upfront," the optimal strategy becomes "make a choice quickly, verify it, and adjust if needed."

This is not new in theory. It is what agile promised. Iterate quickly, get feedback, adapt. But agile never actually delivered cheap iteration. Sprints took two weeks. Pull requests took days. CI pipelines took hours. Code review cycles took a week. "Iterate quickly" meant iterate every two weeks instead of every six months. That was an improvement, but it was still expensive enough to preserve most of the cost-mitigation machinery. You still estimated. You still wrote detailed tickets. You still had sprint planning. The ritual survived because the underlying economics had not changed enough to kill it.

What AI-assisted development changes is the actual, physical cost of trying something. Not the planning cost. Not the meeting cost. The implementation cost. When building a prototype takes two hours instead of two months, you do not need a meeting to decide whether to build it. You build it and evaluate the result. When refactoring takes thirty minutes instead of two weeks, you do not need a change control board. You make the change, run the tests, and look at the outcome.

The shift is from prediction to observation. From "let us figure out the right answer before we start" to "let us try it and see." Not because prediction is bad, but because observation has become cheaper than prediction for a large category of decisions.

## What does not change

I want to be careful here, because the enthusiast version of this argument leads somewhere irresponsible.

The cost of wrong architectural decisions at scale has not collapsed. If you decompose a system into microservices along the wrong boundaries, AI cannot cheaply fix that. If you choose the wrong database for your access patterns, the migration is still painful regardless of how fast AI can generate code. If you design a public API contract and clients build against it, changing that contract is still expensive because the cost is distributed across systems you do not control.

At sufficient scale and sufficient coupling, the cost of being wrong remains high. AI has not changed the physics of distributed systems, the politics of organizational boundaries, or the contractual nature of public interfaces.

The decisions that are hard to reverse remain hard to reverse. Architecture, in the IASA definition I have used for years, is specifically the set of decisions that are expensive to change. AI has shrunk the set of decisions that qualify, but it has not emptied it.

And there is a subtler risk. When building is fast, you can accumulate more code on top of a wrong foundation before you notice the foundation is wrong. The cost of individual iterations has dropped, but the cost of discovering you have been iterating in the wrong direction for three days of AI-assisted development can be substantial. Three days at these speeds can produce more code than three months of traditional development. If the direction was wrong, that is a lot of code to understand, evaluate, and potentially discard.

Speed without judgment accumulates debt faster than ever. That has not changed.

## The hard question

Here is where I stop having answers and start having questions.

Most developer intuitions were shaped by expensive iteration. When I review code, my instinct is to be thorough because mistakes are costly to fix later. That instinct served me well for thirty years. Is it still the right instinct when fixes take thirty minutes? Or should I review less carefully and rely on fast iteration to catch what I miss? I genuinely do not know.

Most organizational structures were shaped by expensive iteration. Engineering managers exist partly to coordinate expensive resources toward the right priorities. Architects exist partly to prevent expensive wrong turns. Product managers exist partly to ensure expensive development effort is aimed at the right features. When the underlying cost structure changes, what happens to those roles? Not "do they disappear," because that is a simplistic question. But what should they focus on when the work they were designed to coordinate becomes an order of magnitude cheaper?

Most processes were shaped by expensive iteration. Sprint planning, backlog grooming, estimation poker, detailed acceptance criteria. All of these consume time that was justified by the cost of building the wrong thing. When the cost of building the wrong thing drops dramatically, how much of that process overhead is still justified?

I built lib-pcb in eleven days. Not because the problem was simple -- PCB file format processing is genuinely complex, with undocumented manufacturer extensions, inconsistent coordinate systems, and edge cases that no specification captures. I built it in eleven days because the cost of discovering that complexity through building was lower than the cost of specifying it away. Every failed approach, every wrong data structure, every parser that broke on real-world files -- each of those was a thirty-minute setback instead of a two-week setback. The methodology that made it possible was designed around cheap iteration: try, verify, adjust, try again.

But that methodology emerged from a specific project with specific characteristics. A single developer. A well-bounded domain. Comprehensive verification through real-world test files. Whether the same economics apply to a fifty-person team building a distributed system with external dependencies and regulatory requirements -- I do not know. I suspect some of it transfers and some of it does not. I have not yet figured out where the boundary is.

What I do know is this: we are carrying thirty years of practices designed for expensive iteration into a world where iteration is becoming cheap. Some of those practices are load-bearing. Some of them are vestigial. And we have not yet done the work of figuring out which is which.

That is the question I think our industry needs to sit with, honestly and without rushing to a comfortable answer.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Examples drawn from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days (Jan 16-26, 2026).*
