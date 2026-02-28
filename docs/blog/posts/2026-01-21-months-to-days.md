---
date: 2026-01-21
series: "Building lib-pcb"
categories:
  - AI-Augmented Development
tags:
  - lib-pcb
  - velocity
  - skill-driven-development
  - methodology
  - proof
  - java
authors:
  - totto
---

# Months to Days

The first reaction is always disbelief.

"That's not possible." Or: "That only works for trivial problems." Or the politer version: "That must be very rough code."

So here are the numbers. Not estimates. Actuals.

<!-- more -->

---

## What was built

lib-pcb is a Java library for PCB design file processing. It handles parsing, validation, and manufacturing export for the major PCB design formats: Gerber RS-274X, Excellon drill files, IPC-2581, ODB++, and others.

This is not a toy project. PCB manufacturing files contain complex geometric data, layer stacking specifications, component placement coordinates, drill patterns, net listings, and manufacturing constraints. Parsing them correctly requires handling format variants that span decades of design tool evolution. Getting it wrong produces boards that don't work, or manufacturing rejections that cost weeks.

The industry standard timeline for a library of this scope: nine to twenty-four months.

We built it in eleven days.

---

## The numbers

- **197,831 lines of Java**
- **7,461 tests** — unit tests, integration tests, round-trip validation, battle tests against real legacy files
- **99.8% test pass rate**
- **8 format parsers** — each handling the full specification plus real-world variants
- **28 validators** — checking structural correctness, manufacturing compliance, constraint adherence
- **17 auto-fix types** — programmatic repair for common file issues

Manufacturing-ready output. Not "good enough for a demo." Files that can go directly to a fabrication house.

---

## What made it possible

Not just Claude Code. The velocity came from the methodology — specifically, from what we've been calling Skill-Driven Development.

The approach: structured skill files that encode domain knowledge explicitly, before AI touches any code. The parser for Gerber RS-274X doesn't start with "write a Gerber parser." It starts with a skill that defines the format structure, the known variants, the failure modes, the testing strategy. The AI works within that framework rather than improvising.

Then rigorous guardrails. Testing wasn't a quality-control step at the end — it was the feedback loop that validated every piece of the build in real time. The 25% to 93% success rate improvement (which came from battle testing against real-world files) happened because the guardrails were already in place when the failures appeared.

The result: code that works the way experienced engineers intended, not code that works on the happy path.

---

## The reaction

When I posted this on LinkedIn, the response split cleanly into two groups.

One group: "How?" — engineers who recognized the scope and wanted to understand the methodology. These became workshop leads.

The other: "That's impossible" — which is a reasonable response if you're applying the mental model of how this kind of work is normally done. The model is wrong. Not because the AI is magic, but because the methodology changes what's achievable.

The proof is in the tests. 7,461 of them, 99.8% passing. Manufacturing output that works. Not a demo. Production code.

---

*Originally posted on LinkedIn, January 21, 2026. Part of the lib-pcb build series.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
