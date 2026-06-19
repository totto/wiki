---
description: "How a PCB library, a knowledge system, and a naming conversation became a brand -- eXOReaction's practice growing distinct enough to need its own identity."
date: 2026-05-12
categories:
  - AI-Augmented Development
tags:
  - aegis
  - sdd
  - methodology
  - origin-story
  - lib-pcb
  - synthesis
  - skills
authors:
  - totto
---

# The Beginning

*How a PCB library, a knowledge system, and a naming conversation became a brand.*

eXOReaction has been around for a while. This is not a story about starting a company. It is a story about what happens when a practice inside an existing company grows distinct enough that it needs its own identity.

Ægis is that practice. ægis.no went live last week. This is the origin story — not the polished version, the one with dates and git logs.

<!-- more -->

---

## // the build that changed the question

January 16, 2026. I started building lib-pcb — a PCB design library in Java. Full format parsing for Gerber, KiCad, Eagle, Altium, ODB++, IPC-2581, GenCAD, STEP. Validators, auto-fix, manufacturing-ready Gerber export. The complete pipeline from design file to factory floor.

I did not know PCB manufacturing. I had been working with Elprint, a Norwegian electronics manufacturer, for months on their production platform. I understood the business context. But the domain knowledge — the Gerber format, the drill file specifications, the coordinate systems, the manufacturing constraints — that was acquired during the build, not brought in.

The approach was simple in concept. Every time Claude and I solved a problem, we captured the solution as a skill file. Not documentation. Not a comment in the code. A skill: a structured piece of knowledge that would load automatically in every future session, so the same mistake would never be made twice and the same insight would never need to be rediscovered.

By day three, there were 20 skills. By day seven, 54. By day eleven, 85.

The numbers at the end: 197,831 lines of Java. 7,461 tests. 99.8% pass rate. 474 commits. Manufacturing-ready output validated against real board files. Eleven days.

Industry standard for equivalent scope: 10 to 18 months.

I am careful with the multiplier. The conservative claim is 10-30x productivity improvement, which is what we consistently see across projects. The raw math on lib-pcb gives you higher numbers, but raw math without context is how consultants lose credibility. What matters is that the approach worked in a domain I had never worked in before, at a quality level that held up under real-world validation.

The interesting thing was not the speed. It was the pattern. The skills accumulated. Each one made the next session more productive. The system got better as it ran. That was not something I designed. It was something I noticed.

---

## // someone else named it

February 3, 2026. A meeting with Vidar Moe at SpareBank 1 Utvikling. I was demonstrating what we had built — walking through the lib-pcb codebase, showing the skill files, explaining the progressive accumulation of context.

Vidar looked at it and said: "This is Skill-Driven Development."

He did not mean it as a brand. He meant it as a description. The methodology was driven by skills — the captured knowledge — not by the AI model, not by the IDE, not by the developer's prior experience. The skills were the differentiator.

I had been calling it various things internally. "Context-first development." "Skill-based AI." Nothing that stuck. Vidar's framing was better because it put the emphasis in the right place: on the accumulated knowledge, not on the tool.

The name changed how I thought about what we were building. It stopped being "a way to use Claude Code effectively" and started being a methodology with transferable principles.

---

## // the transfer test

February 14, 2026. Synthesis. A completely different project: a knowledge infrastructure system built on Apache Lucene, designed to index codebases, understand relationships between files, and make institutional knowledge searchable.

Different domain. Different architecture. Different problem space. The lib-pcb skills were useless — you cannot apply Gerber parsing conventions to a search indexer.

But the method transferred.

Build. Capture what you learn. Load it next session. Verify aggressively. Let the skill library compound.

Seven days. 84,692 lines. 73 pull requests. 65% Claude co-authorship — meaning Claude implemented while I set direction, defined constraints, made architectural calls. 99% test pass rate.

On day six, something unexpected happened. Synthesis was a knowledge indexer. We pointed it at its own codebase. It read its own skill files. It found that 58% of its own specifications were wrong — not because they were written badly, but because the implementation had evolved faster than the documentation. The system diagnosed its own drift.

That was the moment the methodology separated from the project. lib-pcb proved the velocity was real. Synthesis proved the method was portable. The skills did not transfer. The discipline of building them did.

---

## // the brand problem

eXOReaction is a bespoke software development company. Selina is the CEO. Clients hire us to build something specific — a production platform, a compliance system, a data pipeline. We design it, we build it, we deliver it. That is the model: bespoke work, scoped engagement, finished product. It has a portfolio, a history, an identity rooted in custom delivery.

But the thing that was forming — the workshops, the Skills Library, the ExoCortex workflow, Synthesis, the maturity reviews — was a fundamentally different kind of business. Bespoke development means: you hire us, we build it, we hand it over. What we were building with the agentic work was the opposite: repeatable products and methods that transfer to the client's team. You do not hire Ægis to build your software. You engage Ægis so your team builds software better — with agentic tools, methods, and products they can own and run themselves.

Those are different businesses. Different customers, different economics, different relationships. Bespoke delivery scales with headcount. Agentic products and services scale with adoption.

The split came from both directions at once, which is usually a sign the decision is correct. Selina was thinking about it from a practical angle: the workshops and agentic offerings needed their own home, their own website, their own identity — they did not belong inside the eXOReaction brand without constant explanation. I was thinking about it from a model angle: bespoke software development as a service and agentic products and services are fundamentally different business models. Bundling them under one name would dilute both. We arrived at the same conclusion independently, and when we compared notes, the decision made itself.

---

## // the name

Ægis. The shield.

In Norse mythology, it belonged to Odin — sometimes a shield, sometimes a cloak, always the thing that protected. In Greek mythology, it was the shield of Zeus and Athena. The word has survived across millennia in both traditions because the concept is simple and durable: the thing that stands between you and what would break you.

That is what the product layer does. Skills protect you from repeating mistakes. ExoCortex protects you from losing context across sessions. Codebase Intelligence protects you from the drift between what your code does and what you think it does. The methodology protects you from the failure mode of adopting AI tools without a framework for using them well.

The æ was deliberate. Scandinavian. Ours. And it looks right in a monospace terminal on a dark background, which is where most of our work happens.

ægis.no. Registered. Live.

---

## // what it contains

The offerings formed from what the methodology actually required, not from a product planning exercise.

The Skills Library came first — 548 production-verified skills, accumulated across every project. Not generated from documentation. Extracted from sessions where something went wrong, or right, in a way worth preserving.

The workshops came from being asked to explain the method to teams. The ægentisk maturity review came from being asked to assess teams before the workshops — where are you now, what would agentic development actually change, what do you need to get there. Synthesis and ExoCortex came from needing to make large codebases navigable and institutional knowledge persistent. KCP came from needing a way to wire it all together.

Talks. Workshops. Advisory. Hands-on builds. Tooling you can license and run yourself — Synthesis, ExoCortex, KCP, the Skills Library. Each offering exists because someone needed it and we had already built it for ourselves. That ordering matters. It is the difference between a product that was designed and a product that was discovered.

The positioning landed as: AI-era development partner. We help organisations work with AI — and as AI. Human-led. Production-grade. Memory as infrastructure.

---

## // where it landed

May 2026. ægis.no went live — the practice finally had a home. The agentic work, the workshops, the tooling, the method had all existed inside eXOReaction for months. What launched last week was the identity: a separate brand, a separate site, a separate front door. First digital product available: the AI-readiness package. Two SDD workshops in the first week.

The methodology has now been validated across five sectors:

- **Manufacturing** — lib-pcb. PCB design library. No prior domain knowledge.
- **Knowledge Infrastructure** — Synthesis. Codebase intelligence system.
- **Renewable Energy** — Tvimenning. Partnership with Jon Petter.
- **Financial Services** — SpareBank 1. Organization-wide Claude Code rollout.
- **AI Security** — Mynder AS. Compliance automation.

Five sectors. Different codebases. Different teams. Different domains. Same method. Same pattern of progressive skill accumulation producing compounding returns.

---

## // what comes next

I don't have a clean answer. The interesting property of SDD is that it compounds — every engagement adds skills, every workshop surfaces patterns, every codebase we index makes the next one faster. That compounding was the whole point.

What I did not fully anticipate was that the same compounding would apply to the business. Each client teaches us something the next client benefits from. The skill library is a record of that.

We are at the beginning. The post title is literal.

---

*Thor Henning Hetland, May 2026. Oslo.*
