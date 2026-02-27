---
date: 2026-01-23
categories:
  - AI-Augmented Development
tags:
  - lib-pcb
  - testing
  - quality
  - verification
  - skill-driven-development
  - methodology
  - reality-based-qa
authors:
  - totto
---

# The Testing Discipline: 25% to 93%

Unit tests passed. Every one of them. Green across the board.

And then we ran the parser against real legacy Gerber files — files from actual PCB designs, exported by real design tools used by real engineers over the last twenty years — and the success rate was 25%.

Three out of four failed.

<!-- more -->

---

## What unit tests don't catch

The issue isn't that unit tests are useless. They're essential. But they test what you think the code should do — your understanding of the format specification, your mental model of the inputs.

Real files don't care about your mental model.

They contain:
- Files created by tools that interpreted the spec differently
- Deprecated constructs that technically shouldn't appear but do
- German locale conventions (comma as decimal separator in an American format)
- 1980s vintage files that predate several spec revisions
- Edge cases that the spec authors never anticipated because they didn't anticipate the diversity of real-world design practice

Unit tests against synthetic inputs catch none of this. The parser was correct by every standard its tests could measure. It just didn't work on a third of real files.

---

## The three-tier defense

Building lib-pcb at this scale made the inadequacy of a single testing layer obvious immediately. The approach we converged on:

**Tier 1 — Unit tests**: Verify specification conformance. Each format feature has tests that confirm the parser handles it correctly. This is table stakes — a baseline, not a guarantee.

**Tier 2 — Round-trip validation**: Parse a file, reconstruct it from the parsed representation, compare against the original. Semantic preservation check. If the round-trip output differs, something was lost or misinterpreted. This catches bugs that unit tests miss because it uses real files, not synthetic ones.

**Tier 3 — Battle testing**: Take the 195 messiest files we could find — old formats, weird tool outputs, locale-specific conventions, everything the internet suggests could cause problems — and run them through the full pipeline. Success is measured against known-good expected outputs, not internal consistency.

After battle testing: 93% success rate. The 7% remainder represents genuinely unusual edge cases, mostly in obsolete format variants, with clear error messages.

---

## Why this matters for AI-generated code

There's a version of AI-assisted development where you generate code, check that it runs, and ship. That approach works until it doesn't — and when it fails in production, you don't have the testing infrastructure to understand why.

The three-tier approach forces a different relationship with the output. You can't trust that the code does what you think it does. You verify it against reality — real files, real edge cases, real failure modes. The AI accelerates the generation. The testing discipline makes the generation trustworthy.

This is what "Trust But Verify" looks like as a methodology. The 5,000+ tests in lib-pcb exist because each one was added after a real failure was found. The 93% success rate exists because the failure rate was measured and taken seriously.

The alternative — shipping at velocity without that discipline — is how AI-generated code gets its bad reputation.

---

## The 195 files

The battle test corpus was assembled deliberately. Files sourced from: hobbyist designs shared on forums, open-source hardware repositories, client files from past projects, the oldest Gerber examples findable online, test suites from other parsing projects.

The explicit goal: find the worst cases before they find production. The 195 files were selected because they looked like trouble. Each one that the parser handled correctly was a failure mode closed.

That's the mindset. Not "does this pass?" but "what will break this, and have I tested that?"

---

*Originally posted on LinkedIn, January 23, 2026. Part of the lib-pcb build series.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
