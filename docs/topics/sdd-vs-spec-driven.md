---
title: "Skill-Driven vs Spec-Driven Development"
description: "Spec-driven and skill-driven development both produce good AI output — but a spec starts every session from zero, while a skill compounds. A side-by-side comparison of the two approaches, the session-amnesia problem that separates them, and when to use each."
image: assets/images/blog/sdd-vs-spec-driven-evolution.webp
---

# Skill-Driven vs Spec-Driven Development

Both approaches work. That's what makes the choice easy to get wrong. **Spec-driven development** writes a careful specification and hands it to the agent each time. **Skill-driven development (SDD)** invests instead in what the agent *permanently knows* — reusable, encoded skills that persist across sessions. Spec-driven gets you good output today; skill-driven gets you *compounding* output, where each session starts smarter than the last.

The dividing line is one uncomfortable fact about how agents work: **session amnesia.** A spec is re-read from zero every session. A skill is not.

## Side by side

| | **Spec-Driven** | **Skill-Driven (SDD)** |
|---|---|---|
| **You invest in** | The specification for *this* task | What the agent knows for *every* task |
| **Where knowledge lives** | In the prompt/spec, re-supplied each session | In durable skills + [knowledge infrastructure](/knowledge-infrastructure/) |
| **Each new session** | Starts from zero — re-explain the context | Starts from the last one — context is already there |
| **Cost curve** | Flat: you pay the full explaining tax every time | Front-loaded: you pay once, then accelerate |
| **Failure mode** | Session amnesia — the agent keeps relearning | Skill rot — encoded knowledge must be maintained |
| **Best when** | One-off tasks, unfamiliar domains, throwaway work | Anything you'll do more than a few times |

## The core difference: always explaining vs always accelerating

Spec-driven development is *rational* — given an agent that forgets everything between sessions, writing a good spec is the sensible response. But it means you are **always explaining**: every session re-pays the orientation tax of getting the agent up to speed. Skill-driven development changes the substrate so you are **always accelerating**: the encoded skill, the indexed workspace, the [navigable knowledge manifest](/topics/knowledge-context-protocol/) mean the agent arrives already oriented.

The full argument — why spec-driven is rational, what session amnesia costs, and what compounding looks like in practice — is in the canonical post:

- **Read it:** [Skill-Driven Development vs Spec-Driven Development](/blog/2026/03/07/skill-driven-vs-spec-driven-development/)

## It's three stages, not two

The honest version isn't "skills good, specs bad." It's a progression: **ad-hoc prompting → spec-driven → skill-driven.** Spec-driven is a real improvement over improvising a prompt each time; skill-driven is the next step, where the specs you keep re-writing get *encoded* into something that persists. You don't skip the middle stage — you graduate from it.

## The decision rule

- **Use spec-driven** for genuinely one-off work, unfamiliar throwaway domains, or when the task will never recur. Writing a skill for something you'll do once is waste.
- **Use skill-driven** for anything you'll repeat — your own stack, your recurring workflows, your team's conventions. If you've written the same kind of spec twice, the third time should be a skill.
- **The tell:** if you find yourself re-explaining the same context to the agent session after session, you've outgrown spec-driven. That re-explaining *is* the thing SDD encodes away.

## The honest cost

Skill-driven isn't free. Encoded skills are knowledge, and knowledge [rots if unmaintained](/blog/2026/06/23/production-scars-are-architecture/) — the compounding only holds if you keep the skills and the [knowledge infrastructure](/knowledge-infrastructure/) current. You're trading the recurring *explaining* tax for a smaller recurring *maintenance* tax. For anything you do repeatedly, that trade pays for itself fast; for true one-offs, it doesn't. That's the whole decision.

## Where to go next

- **The method in full:** [Skill-Driven Development](/topics/skill-driven-development/)
- **The infrastructure underneath it:** [Knowledge Context Protocol](/topics/knowledge-context-protocol/) · [Synthesis](/topics/synthesis/)
- **New here?** [Start here](/start-here/) · **Unsure of a term?** [Glossary](/glossary/)
