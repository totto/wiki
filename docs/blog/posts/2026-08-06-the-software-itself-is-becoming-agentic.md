---
description: "A playbook calling another playbook at runtime, gated by a signed, revocable certification — not a developer using AI to code faster. On the shift from AI-assisted software to software that is itself a network of agents, why the infrastructure for that gets discovered rather than planned, and why it becomes unavoidable the moment agentic software has to operate inside governed organizations."
date: 2026-08-06T12:30:00
draft: false
categories:
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
  - AI-Augmented Development
tags:
  - kcp
  - sunstone-atlas
  - governance
  - agents
  - verification
  - trust
  - agentic-software
authors:
  - totto
  - claude
---

# The Software Itself Is Becoming Agentic

This week we shipped a feature in Sunstone Atlas where one playbook can, at runtime, call in another playbook as a real sub-orchestration — a crew calling in another crew, each with its own ledger and its own replay story. A playbook can also propose handing off to a successor when it completes; nothing auto-fires, an explicit human act is required to actually start the successor. And neither the calling unit nor the called unit may participate at all until each has separately, explicitly earned certification for exactly that — a binary, human-signed trust decision that can be revoked as easily as it was granted.

Notice what that is. It is not a developer using an AI to write code faster. It is the shipped software making a composition decision at runtime, and being held to a governance standard for making it.

<!-- more -->

That distinction is the trend I think I'm seeing — the beginning of one, at least. We spent the last few years on "AI helps us build software." What's emerging now is different in kind: the software we ship increasingly *is* a network of agents — deciding, escalating, composing with each other while running — rather than a monolith of hand-written business logic that happens to call an LLM API. And once that's what you're shipping, the mix of what you build shifts structurally: less source code, more agentic infrastructure. A shared protocol for what one agentic component can trust about another. A governed mechanism for how components are allowed to compose. Those aren't features of any one product. They're the substrate the products stand on.

## Infrastructure gets discovered, not planned

I want to be honest about how that substrate came to exist, because the honest version is more interesting than the strategic one. None of it was on a roadmap. KCP — the Knowledge Context Protocol — got built the moment agentic software needed a way for one block to rely on another's output and nothing adequate existed. That's the pattern every time: you build the agentic thing, you hit the missing layer, you build the layer.

Two observations convinced me this layer is a real emerging category and not just our own enthusiasm. When our internal skill and knowledge library — grown over a year from reference text into load-bearing, queryable infrastructure — was rewritten as KCP-native, retrieval cost dropped by an order of magnitude, and unranked grep-through became ranked, explainable retrieval that other agents build on. More telling, because it isn't about us: months after the standards outreach began, an engineer at another company reported real internal use of KCP, unprompted. People converging on the same layer independently is what an actual category looks like.

And the substrate compounds. A second, domain-specific agentic product — I'll keep it generic — came together in a handful of build passes rather than a long from-scratch effort, because the skill substrate and the build-and-verify patterns discovered while making the first one were simply there to stand on. Nobody planned that reuse either. It fell out of the need.

## Why the protocol layer is load-bearing

Agentic components fail differently than every previous building block. A library fails mechanically: a stack trace, a 500, a compile error. An agentic block can fail *semantically* — fluently, confidently, plausibly wrong. I've watched a subagent assert that certain database fields "really existed" when they didn't. Nothing a runtime would catch. Perfectly formed, incorrect output.

![The infographic generator rendering "Nenoxistent" and "retrieval caste" for "Nonexistent" and "retrieval costs."](/assets/images/blog/the-software-itself-is-becoming-agentic/the-shift-to-agentic-software.png)
*Left uncorrected on purpose — see below.*

*(A small, unplanned confirmation of the point above: the infographic generator I used alongside this post rendered "Nenoxistent" for "Nonexistent" and "retrieval caste" for "retrieval costs" — fluent, confident, and wrong, in the one graphic explaining exactly that failure mode. I didn't have to go looking for an example.)*

When components that fail like that start composing with each other at runtime, "what can this block trust about that block's output" stops being a code-review question and becomes a protocol question. That's the whole reason a trust layer exists as infrastructure rather than as a comment in someone's prompt.

## Verification becomes existential, not hygienic

Here is what's not working yet, and it deserves space, not a hedge. We've hit a bug class I had never seen before: two pull requests, independently built, independently tested, both green — that broke each other on merge with zero git conflict. Separately, a suite of several hundred passing tests missed real production bugs because every test drove the underlying function directly and not one exercised the actual entry point a human uses. Excellent coverage number; wrong product.

In ordinary software that's an embarrassing process gap. In agentic software it's something worse, because the thing you shipped goes on to *decide things* in production. When the software's job is to compose crews and route hand-offs at runtime, "we don't actually know what the merged system does at its real entry points" is not a dev-process nicety you fix eventually. It's a hole in the product's trustworthiness itself. Our answer so far is structural, not aspirational: after every merge, verify from a fresh checkout of what actually merged, and walk the real entry point live, as the acceptance gate. It's honest work, and it's still catching things the test suites don't.

Human judgment doesn't disappear in this picture — it concentrates. The real calls in a recent build were few and small-looking: which classification rule takes precedence when two apply; a CSS collision caught before it silently broke every status badge; insisting a taxonomy be grounded in fields that exist rather than fields that sound right. Each call gets baked into everything composed downstream. Bad judgment doesn't dilute at scale. It amplifies.

## Why this becomes unavoidable now

All of this gets sharply more real as agentic software moves into governed companies — regulated, audited, compliance-heavy organizations. "Just trust the model" is not an answer any accountability function will accept, and it shouldn't be. If your software escalates, delegates, and composes on its own, someone will ask: who authorized this component to call that one, on what evidence, and how do we withdraw that authorization? A signed, revocable, checkable record of earned trust — the certification gate on that playbook-to-playbook call — isn't governance polish on top of the product. It's the condition of shipping the product into serious contexts at all.

So that's the trend as I see it from inside: software becoming agentic, pulling agentic infrastructure into existence need by need, and heading straight into environments where the governance machinery is the price of admission. If you're building agentic software today, the concrete question is the one our certification gate answers: when one of your components calls another at runtime, where is the record that says it was allowed to — and who can revoke it?
