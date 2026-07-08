---
title: "Skill-Driven Development"
description: "Skill-Driven Development (SDD) is a methodology for building software with AI agents where domain knowledge, failure modes, and architectural patterns are encoded into persistent, reusable skills — so every session starts smarter than the last, instead of starting from zero like spec-driven development."
image: assets/images/blog/sdd-vs-spec-driven-evolution.webp
---

# Skill-Driven Development

**Skill-Driven Development (SDD) is a methodology for building software with AI agents in which domain knowledge, failure modes, and architectural patterns are encoded into persistent, reusable skills.** The agent reads the relevant skill before it acts, so every session starts with everything the previous sessions learned. Knowledge compounds instead of evaporating.

That is the whole idea, and it is best understood against the two approaches most teams try first.

---

## Vibe coding → spec-driven → skill-driven

- **Vibe coding** — prompt the agent, see what comes out, fix the obvious problems, ship. Fast for prototypes, dangerous in production: the output reflects the model's training data, not your team's conventions.
- **Spec-driven development** — write a detailed spec, feed it to the agent, review, iterate. Disciplined and responsible. But it has a structural limitation: **every session starts from zero.** The spec carries the knowledge; the agent carries nothing. Write the same spec context again tomorrow.
- **Skill-driven development** — encode the knowledge *once*, as a skill the agent loads on demand. The spec describes *this* change; the skill remembers *how you build* — the patterns, the pitfalls, the definition of done. Each session starts smarter than the last.

The full argument: [Skill-Driven Development vs Spec-Driven Development](/blog/2026/03/07/skill-driven-vs-spec-driven-development/).

---

## What a "skill" actually is

A skill is not a prompt. A prompt is consumed and forgotten; a skill is a persistent, versioned unit of methodology the agent reaches for when a task matches. Prompts don't compound. Skills do.

- [What a "Skill" Actually Is (And Why It's Not a Prompt)](/blog/2026/02/07/what-a-skill-actually-is-and-why-its-not-a-prompt/)
- [Context Architecture Replaces Process Ceremonies](/blog/2026/01/18/context-architecture-replaces-process-ceremonies/)
- [Why Exploration Beats Specification When AI Does the Building](/blog/2026/02/09/why-exploration-beats-specification-when-ai-does-the-building/)

---

## The proof

SDD is a claim about compounding, so the evidence is about scale and repeatability.

| Evidence | Result |
|---|---|
| [lib-pcb](/blog/2026/01/15/the-surprisingly-hard-problem-of-semiconductor-part-numbers/) | 197,831 lines of Java, 7,461 tests, in **11 days** — the original proof that encoded knowledge changes what one person can build. |
| [Thirteen Codebases, One Method](/blog/2026/03/05/thirteen-codebases-one-method/) | 13 developers, 13 different codebases, one workshop day — the method transfers across people and domains. |
| [The Compound Developer](/blog/2026/06/02/the-compound-developer/) | What it looks like when skills, memory, and multiple agents compound over months. |

---

## What it changes about the work

Skill-Driven Development doesn't just speed things up — it moves the developer up the stack, from writing code to encoding judgment.

- [Strategic Delegation: When Developers Become Architects](/blog/2026/01/22/strategic-delegation-when-developers-become-architects/)
- [What "Senior Developer" Means When AI Can Code](/blog/2026/02/15/what-senior-developer-means-when-ai-can-code/)
- [The Gap Between Individual Fluency and Organisational Capability](/blog/2026/02/20/the-gap-between-individual-fluency-and-organisational-capability/)
- [Explorative Development](/blog/2026/06/11/explorative-development/)

---

## Reading guide

- **The core distinction** → [Skill-Driven vs Spec-Driven Development](/blog/2026/03/07/skill-driven-vs-spec-driven-development/)
- **The proof at scale** → [Thirteen Codebases, One Method](/blog/2026/03/05/thirteen-codebases-one-method/)
- **Where it started** → [The Beginning](/blog/2026/05/12/the-beginning/)
- **Six months in** → [Six Months Down the Rabbit Hole](/blog/2026/07/15/six-months-down-the-rabbit-hole/)

---

## Links

- **All SDD posts:** [AI-Augmented Development category](/blog/category/ai-augmented-development/)
- **The infrastructure it runs on:** [Synthesis](synthesis.md) · [Knowledge Context Protocol](knowledge-context-protocol.md)
- **The wider body of work:** [Knowledge Infrastructure](../knowledge-infrastructure/index.md)

*This methodology is still evolving in practice. The [blog](/blog/) has the latest; this page has the map.*
