---
date: 2026-01-15
series: "Building lib-pcb"
categories:
  - AI-Augmented Development
tags:
  - lib-pcb
  - semiconductors
  - parsing
  - embedded
  - methodology
  - skill-driven-development
authors:
  - totto
---

# The Surprisingly Hard Problem of Semiconductor Part Numbers

You'd think parsing a part number would be trivial.

A string of characters. Match it against a pattern. Done.

Then you actually try to do it across a real component database, and you discover how much institutional knowledge is packed into those strings — and how little of it is documented anywhere.

<!-- more -->

---

## What a Manufacturer Part Number actually is

An MPN is a manufacturer's identifier for a specific component variant. Sounds simple. In practice, it's a compressed encoding of a dozen specifications at once — and the encoding rules vary by manufacturer, by product family, by era.

Take resistors. A part number might encode resistance value, tolerance, temperature coefficient, power rating, package size, and termination finish — all in a string like `RC0402FR-07100KL`. The suffix rules for that last segment? Version-dependent. The package codes? Different naming conventions across generations of the same product line. The temperature grade designators? Collide between manufacturers — the same letter means different things depending on who made it.

And that's before you get into the genuinely strange cases: parts with suffixes that look identical but have different interpretations depending on which decade they were introduced, or manufacturer-specific extensions that were never formally documented because the engineers who designed the system knew what they meant.

---

## The suffix collision problem

The specific challenge that came up building lib-pcb was suffix collisions — cases where two valid part number interpretations produce the same string.

When that happens, resolution requires context. Which manufacturer? Which product family? Which year? The parser can't just match the string; it has to reason about the component identity from surrounding information, then apply the right decoding rules.

That's a fundamentally different problem from pattern matching. It's more like disambiguation — the parser needs enough knowledge of the domain to understand which of several valid interpretations applies in a given context.

---

## Why this is interesting at AI velocity

The conventional approach to MPN parsing is hand-crafted rules. Experienced engineers who know the conventions write them down. When a new manufacturer or product family is added, someone updates the rules. The system accumulates coverage over years.

That process has a natural pace. When you're building a PCB component library at AI velocity — as we were with lib-pcb — the parsing requirements appear faster than rules can be written manually. The question becomes: can you express the domain knowledge in a way that scales with the generation speed?

The answer involves a combination of structured knowledge representation (this manufacturer uses these suffix conventions, this product family uses these codes) and systematic testing against real component databases where you can verify the parser's output against known ground truth.

332 people saw this post on LinkedIn. Most of them had encountered some version of this problem. It's more universal than it sounds.

---

*Originally posted on LinkedIn, January 15, 2026. Part of the lib-pcb build series.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
