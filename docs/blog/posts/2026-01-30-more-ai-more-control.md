---
date: 2026-01-30
categories:
  - AI-Augmented Development
tags:
  - ai
  - control
  - architecture
  - methodology
  - autonomy
  - delegation
authors:
  - totto
  - claude
---

# The More AI, The More Control

The fear is intuitive and sounds right: the more you delegate to AI, the less you understand your codebase, the less you control what ships. You become a passenger in your own project. Every prompt you type is a piece of agency you surrender.

I have thirty years of shipping software. I have watched entire teams lose control of codebases they wrote themselves, without any AI involved. And I have watched my own control over a codebase *increase* as I delegated more to AI. The intuition is wrong. But it is wrong in a specific way, and understanding that specificity matters.

<!-- more -->

## When the fear is right

Let me be honest about the failure mode first, because it is real and I have seen it.

You ask the AI to refactor a module. It changes 47 files. You scan the diff. It looks reasonable. Tests pass. You merge. Now there are 47 files in your codebase that you did not write and did not fully read. Next week you ask it to add a feature that touches some of those files. It changes 30 more. Tests pass. You merge again. Within a month, you are maintaining a codebase that a machine wrote and you approved. You are a rubber stamp with commit access.

That is not a hypothetical. It is what happens when delegation is undirected. The developer becomes a spectator. The AI makes the architectural decisions by default, because no one else is making them explicitly. The fear was correct: naive delegation destroys control.

## What directed work actually looks like

Here is what I do instead, and why it produces the opposite outcome.

I do not ask the AI to "refactor module X." I break the work into pieces small enough that I understand each one completely before it executes. "Extract this method. Rename this parameter. Move this class to that package. Add this validation to that entry point." Each request is scoped so tightly that when I review the result, there is nothing ambiguous. I know what it should have done. I can see whether it did it.

The architectural decisions -- what to extract, why, where things belong, what the boundaries are -- remain mine. The AI never decides module structure. It never chooses which abstraction to introduce. It never makes tradeoff calls between simplicity and flexibility. Those are my decisions, articulated clearly enough that a machine can execute them.

Here is the part that surprises people: this process forces me to understand the codebase *better* than if I had written everything by hand. When you write code yourself, you can operate on intuition. You feel your way through a refactoring. You don't have to articulate why you're moving a class -- you just move it. But when you are directing AI, you must be precise. "Move this class because it belongs to the persistence layer, not the domain layer, and here is the package it should go to." That precision requires understanding. You cannot direct what you do not comprehend.

Building [lib-pcb](https://github.com/exoreaction/lib-pcb) -- 197,831 lines of Java in eleven days -- worked this way. Every change was directed. Every architectural decision was mine. The AI executed thousands of individual, scoped tasks. At the end of eleven days, I understood that codebase more thoroughly than most codebases I have spent months writing by hand. Because I had to. Directing requires comprehension. There is no shortcut.

## The verification layer

There is a second mechanism that increases control, and it is less obvious.

Pre-AI, I controlled code quality by writing code carefully. But writing code is slow, so coverage was always a compromise. Tests got skipped when deadlines pressed. Documentation happened after launch, which meant never. Entire subsystems had no verification beyond "it seems to work." That is not control. That is hope.

With AI handling the execution, I could afford verification infrastructure that was never economical before. 7,461 tests. Round-trip verification for every parser. Property-based tests for every invariant. A battle suite of 191 real-world files. CI as the final arbiter on every pull request, no exceptions.

That is a form of control -- systematic, measurable, reproducible -- that I never had when I wrote everything myself. I know exactly what works and what does not, not because I read every line, but because every line is tested against explicit expectations. The coverage is comprehensive precisely because I did not spend my time writing implementation code.

The paradox resolves cleanly: writing code by hand gave me the *feeling* of control. Directing AI with comprehensive verification gives me *actual* control. The feeling and the reality were never the same thing.

## The architect distinction

There is a line that AI-assisted development makes very visible, a line that was always there but easy to blur: the line between making decisions and implementing decisions.

Before AI, a senior developer did both simultaneously. You decided the architecture while writing it. The decision and the implementation were entangled in the same act. This felt like control, and it was, but it was also inefficient. Your decision-making capacity was bottlenecked by your typing speed.

With AI, the two separate cleanly. You make decisions: what to build, why, the constraints, the tradeoffs, the boundaries, the acceptable failure modes. The AI implements those decisions. The separation is not a loss. It is a clarification. You were always the architect. Now you can focus on it.

The developers I worry about are the ones who never made the architectural decisions in the first place -- who wrote code by following patterns without understanding why those patterns existed. For them, AI does remove something, but it is not control. It is the illusion of contribution that came from typing. The real contribution was always the decisions, and that has not changed.

## The discipline requirement

I want to be direct about one thing because the optimistic version of this story is incomplete without it.

Everything I described above requires discipline. Specifically, the discipline to stay at the direction level. To not become a spectator. To not approve output you do not understand because the tests pass and you are tired and it is late.

Tests passing is necessary but not sufficient. Tests verify what you thought to test. They do not verify what you did not think to test. A developer who approves AI output without understanding the architectural implications -- "tests pass, ship it" -- is accumulating decisions they did not make. That debt compounds. Eventually they are maintaining a codebase designed by an AI's implicit defaults rather than by explicit human choices.

The discipline of directed work is what maintains agency. Break the work down. Understand each piece. Make every architectural decision yourself. Let the AI handle execution. Review against your intent, not just against test results.

This is not optional. It is the difference between more control and less.

## The paradox, stated plainly

Pre-AI: you controlled your code by writing it yourself, but you could not afford comprehensive verification, so your actual control was limited to what you could hold in your head.

Post-AI: you control your code by directing every change and verifying it systematically, so your actual control extends to everything the test suite covers -- which is everything, because you finally had time to build it properly.

More delegation. More comprehension. More verification. More control.

The developers who mass-delegate without direction will lose control. The developers who direct with precision will gain it. The tool is the same. The discipline is the difference.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. All examples from [lib-pcb](https://github.com/exoreaction/lib-pcb), built over 11 days (Jan 16-26, 2026).*
