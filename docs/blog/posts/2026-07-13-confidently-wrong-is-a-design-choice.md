---
description: "The worst property of AI tooling is not that it is sometimes wrong — it is that wrong and right arrive in the same voice. That is not a model limitation. It is a fail-open default, and it can be designed away. Seven Synthesis releases, one rule, traced through the evidence."
date: 2026-07-13T09:00:00
draft: false
categories:
  - Knowledge Infrastructure
tags:
  - synthesis
  - knowledge-integrity
  - fail-closed
  - kcp
  - ai-agents
  - kotlin
authors:
  - totto
  - claude
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# Confidently Wrong Is a Design Choice

The worst property of AI tooling is not that it is sometimes wrong. It is that wrong and right
arrive in the same voice — the same fluent, even confidence, whether the claim is verified
fact or improvised filler.

We talk about this as if it were a model limitation. It mostly isn't. It is a **default**:
when the system cannot verify something, it proceeds anyway. Safety engineering has a name for
the alternative — [fail closed](../../topics/defendable-agents/primitives/fail-closed-policy.md):
when you cannot establish that a thing is safe, you stop, and you say so.

[Synthesis](../../topics/synthesis.md) shipped seven releases in the past three weeks, v1.38
through v1.43. On paper they are unrelated features. Read the diffs and they are one decision
applied to five surfaces. This post traces the rule through the evidence.

<!-- more -->

## Answers: an unverified claim is a gap, not a sentence

`ask --ground` splits an AI answer into claims and checks each against the context files it
was generated from — files pinned by sha256, so the evidence cannot drift after the fact.
Verified claims get citations. And the claims that *cannot* be verified are not smoothed over:
they come back labelled as **gaps**.

That last part is the design choice. The easy implementation deletes what it can't support and
returns a shorter, still-confident answer. The fail-closed implementation returns the doubt.

(Grounding calls a model, and this writing sandbox has no API key — so this is the one section
with no pasted output. Telling you that instead of faking a terminal is, well, the topic of
the post.)

## Memory: a recollection you can't verify is a rumor

The new `remember` / `recall` MCP tools give agents episodic memory across sessions. The
integrity rule carries over: every entry is hash-pinned at write time and **tamper-checked at
recall**. A memory that fails verification does not come back as a slightly-wrong truth. It
fails, closed.

## Manifests: "contradicted" is a first-class verdict

A `knowledge.yaml` manifest declares what matters in a repo. Declarations rot, so
`kcp verify` checks them against evidence — and its vocabulary is the tell:

```text
$ synthesis kcp verify
Manifest: .../knowledge.yaml
  Units: 2 observed, 0 stale, 0 contradicted
  All declarations hold — units marked 'observed'.
```

Not "valid/invalid" — *observed, stale, contradicted*. The governance checks make the third
category bite: a file declared `sensitivity: public` while carrying an open HIGH security
finding is a contradiction, and it fails the check.

The same rule extends to integrity in transit. Manifests are Ed25519-signed
(`Trust tier: TRUSTED`), and when we bumped the pinned reference agent to
[kcp-agent](https://github.com/Cantara/kcp-agent) 0.11.0 this week, the conformance gauntlet
proved both directions again: the reference consumer verified a Synthesis-signed manifest —
and **rejected a deliberately tampered one with exit 1**. A manifest that cannot prove it is
untouched is treated as touched.

## Reading: no model in the loop that decides what to load

`kcp plan` turns "what should the agent read for this task?" into a deterministic computation
under an explicit token budget:

```text
$ synthesis kcp plan "how does authentication work" --budget 2000
Read plan for: how does authentication work
  1 unit(s), ~11 tokens
  1. docs/api.md  (score 5, ~11 tok) — 1 trigger match
       → API Reference
```

No LLM decides what enters the context window; an inspectable algorithm does, and the new
routing boosts in `search`/`ask` ship with a diagnostics block naming every result they
touched. Improvised retrieval is exactly the fail-open pattern the rest of the stack exists
to prevent.

## Benchmarks: the rule applies to our own marketing

We benchmarked manifest-guided retrieval against ourselves — hand-written manifests (Arm B,
9 units) versus Synthesis-generated ones (Arm C, 24 units), 8 tasks. Fail-closed reporting
means the caveats ship with the number:

- **Zero path overlap** — B routes to source code, C routes to docs, CI, and tests.
- C wins on aggregate score (455 vs 378) *partly because verbose trigger lists match more* —
  a scoring artifact as much as a quality signal.
- B is better for code navigation; C for project understanding.
- **Neither alone is sufficient. Hybrid curation is the recommendation.**

A benchmark that only reports its flattering number is a fail-open answer wearing a lab coat.

## Even the code review

v1.43 added Kotlin to the code knowledge graph — `relate`, `impact`, health and gap analysis
now work for Kotlin shops, including mixed Java↔Kotlin repos:

```text
$ synthesis relate PaymentGateway.kt
  Referenced by (incoming): 2 files
    <- src/main/kotlin/com/acme/api/StripeGateway.kt (supertype)
    <- src/main/kotlin/com/acme/billing/InvoiceService.kt (import)
```

It came from an outside contributor whose company runs Kotlin backends, and the process
itself followed the rule. The PR **pinned its known regex limitations in named tests** instead
of hiding them. The review found a real gap — idiomatic Kotlin puts free functions in files
with no class declaration, which the resolver missed — and instead of a shrug, the gap became
an issue and a fix within days. Declared limitations, verified fixes, nothing silent. That is
fail-closed as a collaboration style, and it is what an open-source project being alive looks
like.

## The default is the product

None of these features required a smarter model. They required deciding, at each surface,
what happens when verification is impossible — and choosing *stop and say so* over *proceed
and sound right*.

An agent that can say "I don't know" is worth more than one that never does. The next
surfaces are already queued: a decision trace for every plan, diffs between plans over time,
and conformance vectors proving the planner agrees with the reference implementation decision
for decision. Same rule, more places.

Synthesis is at v1.43.0 — [release history](../../notes/synthesis-releases.md), or start with
the [topic page](../../topics/synthesis.md).
