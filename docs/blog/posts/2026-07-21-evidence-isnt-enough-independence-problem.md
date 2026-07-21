---
description: "A test in our suite was green for six weeks. It asserted nothing. When an agent writes the code, the test, and the proof, a passing check certifies nothing — the circle just moves up a level. Daniel Bentes is right that we should check evidence, not trust agents. But evidence is only as good as the independence of whatever checks it — and that runs on both what the agent does and what it knows."
date: 2026-07-21T09:00:00
draft: false
image: assets/images/evidence-11-accountability-decade.webp
categories:
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
tags:
  - defendable-agents
  - agentic-development
  - verification
  - adversarial-review
  - provenance
  - kcp
  - context-integrity
authors:
  - totto
---

# Evidence isn't enough: the independence problem in agentic development

A test in our suite was green for six weeks. It asserted nothing.

<!-- more -->

It created a deviation through the UI, then checked that a deviation with a matching *title* showed up in the register. The title was written by an AI generation step — so the AI could rephrase it, the lookup would miss, and on a good night a different leftover record would match instead. Green. Every layer did its job. The evidence was there. The evidence was worthless.

![The anatomy of a fake pass, in five steps: (1) the agent creates a deviation through the UI, (2) an AI rephrases the deviation's title on the fly, (3) the system fails to find the newly phrased title, (4) it randomly matches a leftover record, (5) the test goes green. Every layer did its job; the evidence was there; the evidence was worthless.](../../assets/images/evidence-01-anatomy-fake-pass.webp)

I've been thinking about this since reading Daniel Bentes' write-up of **Flow**, his Claude Code plugin. His diagnosis is sharp, and most of the industry hasn't caught up to it: when an agent writes the code, writes the test, and decides the test passed, *a passing check stops meaning much.* His answer is to move the unit of trust from the agent to the evidence it leaves behind — reviewers read proof instead of diffs, "done means proven," no evidence, no merge.

He's right about the direction. I want to push on where it isn't enough yet, because the gap is the whole game.

## The circle doesn't break — it moves up a level

"Stop trusting the agent, start checking what it leaves behind" is a real improvement. But evidence is only as trustworthy as its *independence from the thing it verifies.* If the same agent produces the code, the test, and the proof, you haven't broken the circle — you've relocated it. Now the agent is optimized to produce *convincing evidence*, and a system that rewards convincing evidence will eventually hand you evidence theater instead of correctness.

![The circle doesn't break — it moves up a level. The agent's optimization loop, once wrapped around code generation, is simply relocated outward to wrap the test and the proof — now optimized to produce convincing evidence. Evidence is only as trustworthy as its independence from the thing it verifies.](../../assets/images/evidence-04-circle-moves-up.webp)

That green-for-six-weeks test is what evidence theater looks like when nobody meant to build it. Nobody gamed anything. The proof simply wasn't independent of the actor producing it — and it wasn't checking the thing that mattered.

![Evidence theater emerges when "done" merely means "proven." Left, the current standard — reviewing proofs, not just diffs. Right, evidence theater — a polished proof sitting on collapsed scaffolding. If the same agent produces the code, the test, and the proof, a passing check stops meaning much.](../../assets/images/evidence-02-evidence-theater.webp)

So there are two gaps hiding under "done means proven":

**Independence** — who checks the evidence, and are they downstream of whoever made it?

**Soundness** — does the evidence bear weight? Does green mean the *right* thing was verified, or just that *a* thing turned green?

## What keeps the verifier honest

We run an agentic development rig — I call it ExoCortex — across real client codebases. The practices that survived contact with production are all attacks on those two gaps, not on evidence volume.

![True independence requires a two-sided governance equation. Output governance — what the agent does — is cross-model review, unfakeable outcomes, and frozen human judgment. Input governance — what the agent knows — is knowledge provenance (KCP), declared context, and traceability. The ExoCortex rig attacks two gaps: independence (who checks) and soundness (does it bear weight).](../../assets/images/evidence-05-two-sided-governance.webp)

**An independent verifier.** Our adversarial review is *cross-model*: a different model is pointed at a finding and told to *refute* it, not confirm it. Same-model self-review drifts toward agreement; a model that doesn't share the author's blind spots is the cheapest independence you can buy. The verifier's job is disagreement.

![Output pillar 1 — cross-model adversarial review. Model A (the author) and Model B (the refuter) meet head-on at "engineered disagreement"; the verifier's job is to refute, not confirm. Same-model review drifts toward agreement.](../../assets/images/evidence-06-cross-model-review.webp)

**Outcomes the agent can't fake.** We don't trust "the fix works." Before I'd call a set of flaky tests fixed this week, I ran the three worst offenders eighteen times against real infrastructure and reported the tally: eighteen clean. Not because I doubted the change — because a claim of correctness on the agent's own say-so is precisely the circle we're trying to break. Real outcomes on real infra are evidence the agent doesn't author.

![Output pillar 2 — outcomes the agent cannot fake. The agent's say-so ("the fix works") is the exact circle we're trying to break. Before calling flaky tests fixed, run the worst offenders against real infrastructure; eighteen tally marks — eighteen clean runs on real infra — form a verified anchor the agent doesn't author.](../../assets/images/evidence-07-outcomes-cant-fake.webp)

**Freeze human judgment, then make drift loud.** On one codebase we froze the current access-control behavior — who can reach what — into a checked-in matrix. It captures whatever is true today, bugs included. The point isn't that the matrix is *right*; it's that any change to a real allow/deny decision now surfaces as a reviewed diff a human signs, instead of drifting silently while every test stays green. The independent check is the frozen human decision, not a fresh agent-authored assertion.

![Output pillar 3 — freeze human judgment, make drift loud. Silent AI logic drift meets a review-gate tripwire in front of a frozen access-control matrix. We checked in a matrix of current access-control behaviours, bugs included; any change to a real allow/deny decision now surfaces as a reviewed diff a human signs, instead of drifting silently while tests stay green.](../../assets/images/evidence-08-freeze-human-judgment.webp)

## The other half: what the agent knows

Everything above governs what the agent *does*. There's a second half the evidence conversation keeps skipping: what the agent *knows*. A verifier can be perfectly independent and still certify the wrong claim — because the agent reasoned from context that was stale, unsourced, or quietly poisoned. Sound proof of the wrong thing.

That's an input problem, and it wants the same discipline we give outputs: the knowledge an agent reasons from should be *declared, signed, and traceable to where it came from* — structured context, not a scraped pile. (This is the work we've been calling KCP — knowledge provenance for agents.) And here's the honest limit, the one that keeps it from being a silver bullet: provenance answers *"where did this come from, and has it changed?"* It does **not** answer *"is this the right thing to reason from?"* That second question is still human judgment — the same frozen-decision, review-gate independence, moved to the input side. Governing what an agent does and governing what it knows are two halves of the same accountability problem, and almost everyone is only building the first half.

![Knowledge provenance (KCP) — governing the input. Scraped piles of unverified context are funnelled down into declared, signed, traceable units. The knowledge an agent reasons from must be structured context, not a scraped pile.](../../assets/images/evidence-10-kcp-provenance.webp)

## The principle

Don't trust the agent. Fine. But don't stop at "trust the evidence" either — because the agent can write the evidence too, and reason from context nobody checked. Trust the *independence of the check*: a verifier that doesn't share the author's incentives, an outcome the author can't manufacture, a human decision frozen where it counts — on both what the agent does and what it knows.

![The evolution of trust in agentic workflows. Trust the Agent (past): focus on capability, nobody checks, failure mode hallucination. Trust the Evidence (present): focus on artifacts, the agent's own tests check, failure mode evidence theater. Trust the Independence (future): focus on accountability, independent anchors check, solved via structural friction. Capability was the last decade's problem; accountability is this decade's.](../../assets/images/evidence-03-evolution-of-trust.webp)

Capability was the last decade's problem, and the loop mostly solved it — agents can write the code. Accountability is this decade's problem, and it is not an evidence-*collection* problem. It's an *independence* problem. Flow is asking the right question. The answer runs a level deeper than the artifact — and it runs on both sides of the agent.

![The accountability decade. Two green trusses — independent verification and knowledge provenance — triangulate and anchor the agent, while the old relocated optimization loop lies shattered beneath. Don't stop at "trust the evidence"; true independence runs a level deeper than the artifact, and it must run on both sides of the agent.](../../assets/images/evidence-11-accountability-decade.webp)
