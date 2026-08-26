---
description: "Two open problems for Sunstone Atlas: scoping reads the way writes are already scoped, and what happens to accountability when work passes through more than one agent."
date: 2026-08-24T10:00:00
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
  - access-control
  - kcp
authors:
  - totto
  - fable
  - claude
---

# What's next for Sunstone Atlas: scoped reads, and the handoff problem

![The Next Frontiers in Agent Governance: Sunstone Atlas Roadmap — solving scoped reads and exploring the multi-agent handoff problem. Current mechanisms secure the write-path; to mature, agentic systems must govern who can read what, and trace accountability when work passes through multiple hands](/assets/images/blog/whats-next-for-sunstone-atlas-scoped-reads-and-the-handoff-problem/cover.webp)

<!-- more -->

Our first post introduced Sunstone Atlas and ended with a list of what's honestly not there yet. This post picks up two of those items: access scoping on the read path, where we know what to build and haven't built it; and what happens to accountability when work passes through more than one pair of hands — human to agent, agent to agent, back to a human — where we're still working out what "built" should even mean. That second one may be the hardest open problem in this field, and we'd rather think about it in public than pretend we've solved it.

## Part one: who gets to read what

The limitation, restated from the first post: roles in Sunstone Atlas gate writes only. An author-tier credential is structurally unable to publish — enforced server-side, and real. But any principal that can read at all can read *everything*: published governance content, drafts, developer notes, all of it.

Why? Partly deliberate triage. Writes were the dangerous direction to secure first: a bad write becomes false authority — a document that reads as policy because a script said so. A broad read is a confidentiality problem — real, but later, while every reader is on the same team. And partly principle: we won't ship a cosmetic version. A read filter applied client-side and presented as access control is worse than none — it reads as governed when nothing governs it. So the answer to "can you scope reads?" has been a plain *no, not yet*, rather than a checkbox that lies.

Now the direction. What makes this a natural next step rather than a rewrite is that most of the pieces already exist:

- **Principals already exist.** Every caller is a named identity with its own credential and a role tier the server checks on every write. Read scoping extends the same principal object — no second, parallel identity system.
- **The classification signal already exists.** Every unit already carries a derived *source class* — `governance`, `developer-reference`, or `unclassified` — computed from real provenance signals (which pipeline synced it, what audience it was published for), never from a hand-typed claim. The same read path derives lifecycle: active published version, or draft.
- **Filtering on those signals already exists — as a courtesy.** Registry search accepts lifecycle and source-class filters today. But they're filters a caller applies *to itself*.

So the planned work is precisely stated: take the classification the server already computes on every read, and move enforcement from "a filter the caller opts into" to "a property of the principal, applied server-side before content leaves the building." The same move that made the author/publisher split real for writes.

Concretely — and this is roadmap, not release notes — that looks like read scopes attached to principals: an external-facing reader that structurally never receives drafts or developer-reference units, however it phrases a query; a reviewer that sees governance content and its full version history but not internal engineering notes. And when a scoped principal genuinely needs something beyond its scope, the answer is the pattern the product already uses: a recorded access request, a human grant, an audited scope change.

![The structural access matrix in practice — Internal Author sees everything; Reviewer sees active governance and drafts but is locked out of dev-reference and unclassified; External Reader and Sync Script see only active governance, with drafts and other classes blocked. A scoped principal needing more defaults to a recorded, human-approved access request](/assets/images/blog/whats-next-for-sunstone-atlas-scoped-reads-and-the-handoff-problem/structural-access-matrix.webp)
*Read scoping is an evolution of mechanisms that already exist — principals, the classification signal, and courtesy filtering — moved from something a caller opts into to a property the server enforces before data leaves the building.*

One complication we already know about: defaults. Today the registry includes drafts in answers by default — labeled honestly, but present. Per-principal scoping forces a decision we've deferred: which principal classes get label-and-include, which get hard exclusion. Wrong in either direction — hiding content from the people governing it, or leaking drafts to people who should never see them — and the feature fails. That choice is the actual design work, and it's ahead of us.

## Part two: the handoff problem

The trust ladder from the first post governs *one agent* over time: it earns autonomy against its own track record and regresses instantly on its own deviations. That model is live. But it quietly assumes something real work violates constantly: that a task belongs to one agent.

More often, a human asks agent A to prepare something. A's output becomes agent B's input — maybe a different agent, maybe one operated by a different company entirely. Eventually a human has to act on the combined result. Control crosses the human-machine boundary twice, and the machine-machine boundary in between.

![The anatomy of a multi-agent chain — Human to Agent A to Agent B to Human, with a signed artifact passed at every handoff, and a question mark hanging over each of the three boundary crossings: human-machine, machine-machine, machine-human](/assets/images/blog/whats-next-for-sunstone-atlas-scoped-reads-and-the-handoff-problem/anatomy-multi-agent-chain.webp)
*Control crosses the human-machine boundary twice, and the machine-machine boundary once in between. We have four open questions about what happens at each crossing.*

We don't have a shipped answer. What we have is the mechanisms any answer must be built from — signing, append-only provenance, pre-negotiated human gates, per-agent trust ladders — and four questions we keep circling. Here they are as open questions, with our instincts marked as instincts.

**Is a signature transitive trust?** When A's signed output becomes B's input, B can verify the signature cheaply — integrity and origin are solved. But a signature proves *who produced this and that it hasn't changed*, not *this is fit for what B is about to do with it*. And whose clearance governs the combined action? One of our earliest demos of a governed agent team ran on a lowest-of rule — the chain acts at the most conservative authority of any member — and that's still our instinct. But lowest-of has a cost: long chains converge to the floor, and the autonomy the ladder exists to let agents earn evaporates. The honest answer probably keys the governing clearance to *what B does with the input*, not just who produced it — a design, not a rule we can state yet.

**Does human approval travel?** A human approved agent A's proposal; agent B later acts on that approved artifact. Does B's action inherit the approval, or does a new decision point exist at B's step? Both blanket answers are wrong: "always ask again" buries humans in re-approvals; "never ask again" lets one approval launder an arbitrarily long chain of downstream actions. The pattern we already trust points a third way: pre-negotiated decision gates. Inside a single playbook run today, every step's authority ceiling is pinned before the run starts — the steps that must end with a human are chosen in advance by policy, never improvised mid-run. The natural extension is a chain-level version of the same idea: policy, agreed before the chain runs, declaring which handoffs re-open a human gate and which inherit. The open question is the vocabulary — what does that policy look like when A and B belong to organizations that don't share a governance substrate?

**Can provenance survive more than one hop?** The second human needs to trace the whole chain — who asked for what, what A produced, what B did with it — not just inspect the final artifact. For a single agent, append-only signed versions and per-run event ledgers already do this; there's even precedent for nesting, since a signed decision today embeds the signed receipt of the model call beneath it. The multi-hop question: does B's record *embed* A's signed output (self-contained, but heavy) or *reference* it (light, but worthless if the second human can't read A's ledger)? Notice that the reference option loops straight back to part one: cross-organization provenance is a read-scoping problem wearing a different hat.

**Whose ladder regresses?** If B deviates and A didn't, A's clearance should be untouched — per-agent ledgers already make that the natural outcome. The harder case: A produces output that's signed, well-formed, and wrong; B faithfully acts on it. Did B deviate? The principle underneath: a trust ladder tracks an agent's *choices*, not its circumstances. By that principle, B faithfully processing bad input didn't deviate — but then something upstream has to catch A, and the chain misbehaved even though only one member did. Which raises a question we genuinely haven't settled: should a *chain* have a trust record of its own, distinct from its members' ladders?

![Whose ladder regresses when bad input is faithfully processed — Agent A's trust ladder clearance drops sharply on its own deviation, Agent B's stays flat because it faithfully processed what it was given, and a third dotted curve labeled "the chain?" sits between the two, unresolved](/assets/images/blog/whats-next-for-sunstone-atlas-scoped-reads-and-the-handoff-problem/whose-ladder-regresses.webp)
*A trust ladder tracks an agent's choices, not its circumstances — but when only one member of a chain deviates and the chain's output is still harmful, does the chain itself need a trust record of its own?*

## Why publish questions instead of answers

Because the field is already answering them — silently, in code nobody audits. Every framework that forwards one agent's output into another's context has taken a position on all four questions by default: trust is transitive, approval is inherited, provenance is whatever the final artifact says, and nothing regresses. Those are answers; they're just unexamined ones.

We'd rather take positions explicitly, in mechanisms you can inspect, and be corrected in public. The read-scoping work is committed direction. The handoff questions are an invitation — if you run multi-agent chains across a trust boundary and have scar tissue to share, we want to hear it.

Same standard as last time: don't take this post's word for anything. When these mechanisms ship, they'll ship with the evidence trail to check.

---

*Sunstone Atlas is built by Sunstone Tech AS. The first post in this series, "Trust is earned, not asserted," covers the mechanisms this one builds on: honest lifecycle labeling, the signed publish ceremony, and the trust ladder.*
