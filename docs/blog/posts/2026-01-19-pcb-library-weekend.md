---
date: 2026-01-19
series: "Building lib-pcb"
categories:
  - AI-Augmented Development
tags:
  - lib-pcb
  - gerber
  - pcb-design
  - testing
  - round-trip-validation
  - weekend-project
  - skill-driven-development
authors:
  - totto
---

# Building a PCB Library: A Weekend Experiment

The plan was to spend a weekend validating whether a complete PCB design library was actually buildable at AI velocity.

Not a prototype. Not a demo with curated inputs. Something that could consume real Gerber RS-274X files — the manufacturing format that PCB designers actually export from KiCad, Altium, Eagle — parse them completely, and produce manufacturing-ready outputs.

<!-- more -->

---

## What the formats actually look like

Gerber RS-274X is the primary format for PCB manufacturing. It describes copper layers, drill files, silkscreen, solder mask — everything a fabrication house needs to produce a board. The format has been around since the 1980s. It's been extended repeatedly, in ways that aren't always backward-compatible. Real files from real design tools contain implementation quirks specific to the tool that generated them.

MIF (Manufacturing Information Format) is a companion format for some workflows, encoding additional metadata about the manufacturing intent.

Both formats had to be parsed correctly — not just the well-formed examples from documentation, but files that had accumulated the idiosyncrasies of twenty years of design tool evolution.

---

## The guardrail: round-trip validation

The core testing methodology was round-trip validation: parse a Gerber file, reconstruct it from the parsed representation, compare the output against the original.

This is more demanding than it sounds. It's not just checking that parsing doesn't crash — it's checking that the semantic content is preserved completely. If the round-trip output differs from the input, something was lost or misinterpreted in parsing.

Round-trip validation exposes a class of bugs that unit tests against synthetic inputs miss entirely: cases where the parser can handle the documented format but silently drops information that appears in real files. Those silent failures are the dangerous ones — the parse succeeds, the code runs, but the manufacturing output is subtly wrong.

---

## Visualization as verification

The second verification layer was visualization: rendering parsed Gerber files as SVG or PNG and comparing them visually against what the original design should look like.

This catches geometric errors that round-trip validation misses — cases where the data is technically preserved but interpreted incorrectly, producing traces in the wrong positions or pads with wrong dimensions.

A human glancing at the rendered output can immediately see if something is wrong. That visual check is fast to do and catches a different class of error than the numerical comparison.

---

## What the weekend produced

By the end of the weekend: a parser that handled the full RS-274X specification, round-trip validation working, visualization producing correct output for a test set of real board files.

Not finished — the scope of lib-pcb was much larger than a single weekend. But the critical question was answered: yes, the approach was sound. The methodology worked. The guardrails held.

What would have taken months of careful hand-coding was proving to be buildable in days.

---

*Originally posted on LinkedIn, January 19, 2026. Part of the lib-pcb build series.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
