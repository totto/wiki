---
description: "The next dimension for Sunstone Atlas: agents that act, not just agents that say. Authority ceilings per action, capability footprints, and why the audit trail is the cost saving, not a tax on it."
date: 2026-08-24T11:00:00
series: "Sunstone Atlas"
draft: false
categories:
  - AI Agents
  - Engineering
tags:
  - sunstone-atlas
  - agentic
  - governance
  - trust-ladder
  - compliance
  - kcp
authors:
  - totto
  - fable
  - claude
---

# Arms, not just a voice: what it takes to let agents act

![Arms, Not Just a Voice — the architecture, economics, and governance of agents that act. Directional draft, Sunstone Atlas](/assets/images/blog/arms-not-just-a-voice-what-it-takes-to-let-agents-act/cover.webp)

<!-- more -->

The first two posts in this series were about knowledge — honest lifecycle labeling, the signed publish ceremony, the trust ladder, then read scoping and what happens to accountability when content passes through more than one pair of hands. Both were fundamentally about things agents *say*.

This post is about the next dimension: agents that *do* things. Place the order. Send the email. Call the external API. Move the money. Agents with arms, not just a voice.

The point of giving an agent arms is economic: real automation, real cost savings, at scale — but governed, compliant with the law and regulation the business actually operates under, and fully auditable. We'll argue below that this isn't a trade-off — that the audit trail is what *makes* automation-at-scale possible, not a tax on it.

First, the honest position everything here stands on, from our first post's limitations list: *tool execution is early. The governed tool-call lane exists, but its transport is young; most real-world side effects still route through humans or deterministic functions.* Still true, and not walked back — what follows is direction, not a feature announcement.

## What acting looks like today

A published playbook can genuinely run. Each step dispatches one of three ways: to an LLM making a judgment call, through an isolated staging gateway; to a registered deterministic function; or to a human. Every decision lands as a signed, replayable event on a per-run ledger.

Of those three, **deterministic functions are the actual, currently-safest form of governed automation**: pre-registered, developer-authored, reviewed code — the side effect is exactly what the code says, every time, replayable bit-for-bit from the ledger. That's not a limitation to apologize for; reviewed code with a signed audit trail is what most businesses *should* want executing their repeatable actions.

Judgment steps — the LLM-driven kind — are gated hard: before an agent's judgment runs for real, at least one real test-run receipt against staging must exist, then an explicit human clearance, and only then does the trust ladder — *block* through *review-after* and *sampling* to *monitor* — govern how much runs unsupervised, graduating on track record and regressing instantly on deviation.

What doesn't exist yet is the thing this post is about: true free-form agent-driven tool-calling with real-world side effects. The arms. That's the frontier. Here are five questions we're working through to get there — by extending mechanisms that already run, not inventing new ones.

![Free-form tool calling represents the unmapped fourth lane — a playbook step dispatches today through an LLM judgment call, a deterministic function, or a human fallback, all landing on the signed per-run ledger; a fourth, dashed lane for real-world side effects sits behind a locked gate](/assets/images/blog/arms-not-just-a-voice-what-it-takes-to-let-agents-act/fourth-lane-free-form-tool-calling.webp)
*Three established dispatch lanes already feed one signed, replayable ledger. The fourth — free-form tool calls with real-world side effects — is the frontier, and it's locked until five architectural challenges are solved by extending mechanisms that already run.*

## Authority ceilings per action, not just per step

Today, every step in a run has an authority ceiling — pinned by policy before the run starts, never improvised mid-run. Only the highest ceiling lets a step conclude with no person in the loop; lower ceilings downgrade an otherwise-autonomous result into an escalation. That mechanism is live.

Extending it to real-world actions changes the question: no longer "may this agent run a judgment step" but "may this agent, right now, at this clearance level, take *this specific action*" — with the answer depending on properties of the action itself. Three axes seem to matter most:

- **Reversible versus irreversible.** A draft can sit unreviewed for a week and nothing has happened yet — the publish ceremony is a natural checkpoint. An action's checkpoint must come *before* the action, and for an irreversible one, review-after can only ever be learning, never correction. That asymmetry belongs in the ceiling, not in the postmortem.
- **Small versus large.** Magnitude thresholds are how human delegation already works — approve up to an amount, sign within a band. Ceilings per action make that machine-checkable.
- **Inside your systems versus crossing into someone else's.** An action inside your own boundary can be inspected, throttled, compensated by you. Once it crosses into another party's systems — their inbox, their order book, their ledger — your remediation options collapse to asking nicely. Boundary-crossing deserves its own ceiling axis, not a footnote.

![The three axes that dictate an action's authority ceiling — Time (reversible drafts versus irreversible sent emails or moved money), Magnitude (small, machine-checkable versus large, requiring escalation), and Boundary (inside your systems, inspectable, versus outside, where remediation collapses to asking nicely) — plotting candidate actions as permitted autonomously, human-gate-required, or structurally blocked](/assets/images/blog/arms-not-just-a-voice-what-it-takes-to-let-agents-act/three-axes-authority-ceiling.webp)
*"May this agent run a judgment step" becomes "may this agent, right now, at this clearance level, take this specific action" — and the answer depends on where the action sits on these three axes.*

## A capability footprint, answerable to a real compliance process

On the knowledge side, the discipline that matters most is structural: an author-tier credential *cannot* publish, no matter what the script running under it does. The role isn't a label — it's a wall.

An acting agent needs that same principle extended, not a parallel invention. A name and a clearance level aren't enough: it needs a known identity; an enumerated set of capabilities and privileges — granted and attested, never inferred from what the agent could technically reach; a known blast radius; and, for a regulated business, a live link to whatever risk and compliance process actually governs actions of that kind. If sending customer communications is subject to a review process when humans do it, an agent doing the same is subject to the same process — and its registration should *point at* that process, so an auditor can walk from the action to the authority it acted under to the compliance regime that authority answers to.

That's the first post's evidence-based, human-attested discipline — "verified" is earned by a person, never asserted by a script — applied to capability instead of content. To be plain: a design direction we're reasoning through, not a shipped registry.

## Approval decays: reassessment as a first-class signal

The trust ladder already handles one kind of change well: the agent misbehaves, and its autonomy regresses instantly. That's live — and it's the easy case, because a deviation announces itself.

The harder case is when nothing misbehaves but the *ground shifts*. The agent is granted a new capability. A new integration connects it to a system it never touched. The business starts operating it in a new jurisdiction. None of that is a deviation — yet the human approval that cleared this agent was given about a different agent, in a different context. Its track record was earned under conditions that no longer hold.

A one-time approval treated as permanent is how every access-control system rots. The open question is what "this agent's circumstances changed enough to warrant re-review" looks like as a first-class signal — distinct from deviation, triggered by changes to the capability footprint rather than by behavior. Our instinct: clearance should be scoped to the footprint it was granted against, so materially changing the footprint doesn't *revoke* trust but does *reopen the question* — routing to a human review rather than silently carrying the old approval forward.

![Contextual shifts require mandatory reassessment, distinct from penalizing bad behavior — the easy case of deviation drops trust instantly, but the hard case of the ground shifting (new capabilities, integrations, or jurisdictions) pauses the trust curve for human re-review instead of dropping it, since the track record was earned under conditions that no longer hold](/assets/images/blog/arms-not-just-a-voice-what-it-takes-to-let-agents-act/contextual-shifts-mandatory-reassessment.webp)
*A one-time approval treated as permanent is how every access-control system rots. Materially changing an agent's footprint shouldn't revoke trust — it should reopen the question.*

## The audit trail is the cost saving, not a tax on it

Here's the argument this whole direction rests on, made concretely rather than asserted.

Ungoverned automation doesn't remove the human from the loop — it moves the human *behind* the loop. Somebody reconciles the orders the bot placed. Somebody spot-checks the emails that went out. Somebody explains to an auditor, months later, why an action was taken, reconstructing intent from log fragments. That checking scales with volume: automate ten times as many actions and you've bought ten times the checking — or you've quietly stopped checking, which in a regulated business isn't a savings, it's an unbooked liability. Either way, verification cost is what caps how much you can actually automate.

A complete, signed, replayable evidence trail attacks exactly that cost. When every action carries its full decision chain — what triggered it, what grounding it saw, what ceiling applied, who or what approved it, all signed and append-only — trusting an action stops meaning *re-doing the work* and starts meaning *verifying the evidence*: check the signature, replay the deterministic decision, confirm the ceiling was respected. Mechanical, seconds, no re-performing anyone's judgment. Sampling becomes defensible, because the sample is drawn from a trail you can prove is complete — the logic financial audit has run on for a century: nobody re-checks every transaction; they verify the controls and sample against a ledger that can't be quietly edited.

So the pitch for governed automation was never "slower but safer." Verification cost is the real ceiling on automation, and governance is the only thing that lowers it. Gateway-style products can say no; the point of building evidence into execution is that "yes" becomes cheap to *prove*.

![The audit trail produces the automation dividend — verification cost climbing linearly with action volume under ungoverned automation, forcing a choice between capping automation or quietly no longer checking, versus a near-flat verification cost under governed automation where checking a signature and replaying a deterministic decision takes seconds — the gap between the two curves is the automation dividend](/assets/images/blog/arms-not-just-a-voice-what-it-takes-to-let-agents-act/audit-trail-automation-dividend.webp)
*Human checking scales linearly with volume — you either cap feasible automation or quietly stop checking. Evidence verification plus sampling barely scales at all. The gap between the two curves is the actual automation dividend.*

## Accountability when the action is downstream

Our second post asked what happens to accountability when *content* passes human → agent A → agent B → human. The acting version is sharper: agent B takes a real-world action that was itself downstream of agent A's decision, or of a human approval three steps back. Who's accountable for what happened?

On the knowledge side, the signed chain of custody works partly because the thing being chained is an artifact. It persists — the second human can re-read it, re-review it, retract it; a bad publish can be superseded. A side effect isn't an artifact: the money moved, the email arrived, the order shipped. The chain of custody still does something genuinely valuable — it can prove exactly who decided what, on what grounding, under whose approval, better than most human processes ever could. But it *attributes*; it doesn't *undo*.

So the honest open question is whether attribution is enough. Our instinct: for actions, not quite — an acting agent's registration may need to carry not just what it may do but what the *compensating action* is when a downstream action turns out wrong, declared up front, the way reversibility was priced into the ceiling above. Which would make the handoff question and the ceiling question the same question in different clothes: a chain should only be allowed to terminate in an irreversible action if accountability for it was pinned — like everything else here — before the run started. We don't claim to have this settled. We'd rather say so than ship a default nobody examined.

## Where this leaves us

Everything above is exploration built on mechanisms that already run: pinned ceilings, staged clearance, per-agent ladders, signed replayable ledgers. The arms themselves remain early, exactly as our first post said. When that changes, it will change the way everything else here has: incrementally, gated, with the evidence trail to check.

Same standard as the last two posts: don't take this post's word for anything. That's the product.

---

*Sunstone Atlas is built by Sunstone Tech AS. Earlier in this series: "Trust is earned, not asserted" (the signed publish ceremony and the trust ladder) and "What's next for Sunstone Atlas" (read scoping and the handoff problem), which this post extends from knowledge to action.*
