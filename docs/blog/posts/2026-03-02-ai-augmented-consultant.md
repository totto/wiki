---
date: 2026-03-02
categories:
  - AI-Augmented Development
  - Methodology
tags:
  - consulting
  - skill-driven-development
  - claude-code
  - architecture
  - regulatory
  - knowledge-infrastructure
authors:
  - totto
  - claude
---

# The AI-Augmented Consultant: Knowledge Infrastructure Before Deliverables

A brief arrives on Friday afternoon. A compliance startup is building an AI-powered scoring engine. They have a working architecture. What they do not have are settled positions on five hard architectural questions. The deadline is Monday.

The question I asked myself was not "how do I answer these five questions?" It was "what knowledge infrastructure do I need to answer them well?"

That reframing is the entire methodology in one sentence.

<!-- more -->

---

## The problem with a consultant's knowledge

A senior consultant reads a brief, forms a view from existing knowledge, and writes an answer. Fast. Confident. Probably 80% right. The remaining 20% is the problem.

In a domain where regulations have been actively amended, transposed, and interpreted in the past two years, that knowledge is a snapshot. The domain kept moving after the last deep engagement with the texts. The decay is real and often invisible — not because consultants are careless, but because staying current with primary sources in a fast-moving regulatory space is itself a full-time job.

The AI-augmented model doesn't solve this by making the consultant faster at the same thing. It solves it by separating knowledge freshness from human expertise. The consultant provides judgment and structure. The knowledge infrastructure provides primary-source grounding, built fresh at the moment it is needed.

In this engagement, the verification process caught two errors in my working positions before they reached the deliverable. Both were in areas where the regulatory landscape had shifted since I last engaged deeply with the relevant texts. Both were correctable. Without a structured verification step, both would have entered the architecture document as confident assertions.

---

## Building the infrastructure first

Before writing a single sentence of the deliverable, I built the knowledge base that would make it defensible.

In the Skill-Driven Development methodology I use for software, domain knowledge lives in structured skill files — YAML files that encode what's known about a domain, load into any AI session in seconds, and ground the assistant's responses in verified sources rather than training-data approximations. The same pattern works for consulting.

I built in layers. Generic regulatory frameworks first — the kind that apply across engagements in this domain, not just this one client. Domain interpretations next, mapping each framework to this client's specific scoring model. Then the architectural positions taken during the engagement itself, encoding not just the decisions but the reasoning behind them. Finally, the operational layer: meeting notes, document inventory, open threads.

The layering matters for two reasons. First, the generic layers get reused. The investment in building them doesn't get billed to one client; it amortises over every future engagement in the domain. Second, the architectural layer is what makes follow-on work fast. A new question in month three doesn't require three hours of re-establishing context. It loads in seconds and picks up where the last session ended.

---

## Calling in the big model

Ninety percent of the work ran on the working model — drafting, iterating, testing positions, checking structure. Fast and capable. The right tool for most of it.

But four questions in the brief were genuinely hard. Hard enough that a vague answer from any model would have been worse than no answer. For those, I invoked the premium reasoning model — each time with a precise brief that laid out the architectural question, the current hypothesis, what I needed confirmed or contradicted, and which specific text to check against.

The first was about credit factor resolution: should the model be configurable per-control or per-classification? We resolved it to a four-level resolution chain — override, classification, domain, platform default — grounded in the proportionality principle of the applicable regulation. The chain matters because it's auditable. A specific control type receives a specific credit percentage *because* of a specific regulatory rationale. That sentence defends a number when the architecture is challenged.

The second was about business stage. The brief implied a one-dimensional model. Worked through properly, a one-dimensional model entangles scoring with UX guidance — the stage label flickers as control statuses change. The two-dimensional model with a hysteresis band prevents that entanglement. This is not something you find in the brief. It's something that surfaces when you think through the implications carefully with a model that can hold the whole architecture in context.

The third resolved the temporal lifecycle for regulatory activation — how a regulation moves from preview to grace period to active, and why the direct preview-to-active transition must be explicitly blocked. An `IllegalStateException` at the state machine level is cheaper than discovering this in production.

The fourth worked through the applicability scoring model — which controls can be excluded, under what conditions, without distorting the score — grounded in the relevant certification standard's annex.

Each of these would have taken hours to verify from primary sources without AI assistance. With prepared briefs, each took under twenty minutes.

---

## Verification before delivery

Before writing the final document, I spent several hours doing something most consulting engagements skip: systematically testing my working positions against primary sources.

The method is simple. Write directed questions — not questions designed to confirm what you believe, but questions designed to surface the correct answer even if it contradicts you. Then load the actual regulation texts into NotebookLM and run the questions against them. NotebookLM synthesises from the documents you upload, not from AI training data. Where the synthesis contradicts a working position, you update the position before writing.

Fifty-five questions across nine regulatory sections. Two answers were wrong. Both corrected before delivery.

The verification record is itself a deliverable. It's a paper trail of what was tested and what the primary sources said. It makes the architecture defensible in a way that "a senior consultant reviewed it" simply doesn't — because it's checkable.

---

## The proof-of-concept nobody asked for

Three components in the scoring architecture were complex enough that "it should work on paper" wasn't sufficient confidence for a system the client intends to build and sell. The decision to build a proof-of-concept was not in the brief. I added it anyway.

The scope was deliberately constrained — enough to validate the hardest elements, not enough to suggest production readiness. The result was 62 integration tests across 15 scenarios, all passing.

What the proof-of-concept proved that the document couldn't: the credit factor arithmetic produces the right numbers. The state machine blocks the forbidden transition. The immutable audit trail produces valid hashes with correct change attribution. These aren't things you can assert from a document and be confident.

Then I ran two extended simulations — one modelling a small group of health sector organisations over two years, one at platform scale — and discovered things the architecture hadn't anticipated.

A bad actor submitted passing status for multiple controls with no evidence attached. The score jumped enough to cross the credibility threshold. No alert fired. The architecture had defined the floor; it hadn't protected against evidence-free inflation.

A data processor suffered a breach. Every controller organisation using that processor saw zero score change, because the relationship entity didn't propagate impact. The architecture described the relationship. It hadn't modelled what happens when the relationship goes wrong.

At scale, the evidence submission endpoint accepted submissions from any authenticated user for any organisation. The architecture described the right roles. The API didn't enforce them.

Evidence with no expiry date never decays. Years into operations, organisations were still carrying their initial onboarding evidence as current.

Nine of the fifteen findings were resolved in the proof-of-concept before delivery. Six were documented as deferred — each with a concrete test case defining what "done" looks like when they're tackled in production. The simulation infrastructure didn't get thrown away. It's a regression suite for the architecture.

---

## Three deliverables, not one

A traditional consulting engagement ends with a document. This one ended with three distinct artifacts.

The first was the architecture document itself — five architectural questions answered, two unsolicited recommendations, and every decision grounded in the four-layer skill infrastructure built before writing began.

The second was a proof-of-concept with 62 passing tests. Not production code. A validation tool. Evidence that the mathematics work, the state machine behaves correctly, and the audit trail holds.

The third was a regulatory knowledge base — a purpose-built KCP knowledge base covering every regulation and guideline referenced in the architecture, with article-level fragment manifests that let a future AI session load a single article in isolation rather than the entire regulation. The knowledge base was built to give the client's own AI assistant primary-source citation capability: not "Article X requires Y" from training memory, but the actual text of Article X, including the implementing regulation and the supervisory authority guidance that clarifies the edge cases.

This third artifact doesn't go stale when the architecture evolves. It gets more accurate when new guidance is issued. It's infrastructure, not a deliverable in the traditional sense — and it's probably the most durable thing the engagement produced.

---

## What actually changed

At the end of a traditional consulting engagement: a document. The knowledge that produced it stays in the consultant's head. If the consultant moves on, it moves with them.

At the end of this one: a document, a test suite that re-validates any architectural change, and a regulatory knowledge base with article-level navigation. The next session loads in seconds. A new architectural question requires a new premium model invocation, new verification questions, and a new test. It does not require rebuilding the context.

There's also something less obvious: accountability becomes verifiable. The claims in the architecture document trace back to 55 verification questions tested against primary sources. The scoring mathematics trace back to 62 passing tests. The simulation findings are reproducible by anyone who runs the test suite.

AI doesn't reduce professional accountability for consulting outputs. If anything, this approach makes the accountability chain more explicit than it's ever been. The traditional model asks you to trust the consultant's expertise. This one lets you verify it.

The argument isn't that AI makes consultants faster. Speed is a side effect. The structural change is that knowledge infrastructure, proof, and durability are now tractable at the pace of a weekend engagement. That's new.
