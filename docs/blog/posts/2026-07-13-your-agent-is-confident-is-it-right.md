---
description: "Seven Synthesis releases in three weeks — grounded answers, episodic memory, self-defending manifests, budget-aware read plans, and Kotlin support. Not seven features: one idea. Your agent retrieves plenty. Can it prove any of it?"
date: 2026-07-13T09:00:00
draft: false
categories:
  - Knowledge Infrastructure
tags:
  - synthesis
  - knowledge-integrity
  - kcp
  - ai-agents
  - episodic-memory
  - kotlin
authors:
  - totto
  - claude
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# Your Agent Is Confident. Is It Right?

[Synthesis](../../topics/synthesis.md) shipped seven releases in the past three weeks — v1.38
through v1.43. This post is not a changelog. It is an attempt to say what those releases
*unlock*, organized around the distrust they answer. Because every one of them, it turns out,
answers a specific way people currently cannot trust their AI tooling.

One ground rule for this post, because it is the ground rule of the product: **every command
output below was generated, not typed.** Fresh fixture, current jar, copy-paste.

<!-- more -->

## 1. "It sounds right, but I can't tell when it's wrong"

The most dangerous property of an LLM answer is that its confidence is uniform. The correct
parts and the hallucinated parts arrive in the same calm, fluent voice.

`synthesis ask --ground` splits the answer back into claims and cross-checks each one against
the context files that were actually loaded — files pinned by sha256, so the evidence can't
drift under you. Claims that check out get citations. Claims that *don't* are not deleted or
smoothed over: they surface as **explicit gaps**. The answer tells you where it is standing on
solid ground and where it is guessing.

Fail-closed, not confidently wrong. It works in the CLI and as `ground: true` on the MCP `ask`
tool, so agents get the same discipline humans do. (This is the one feature in this post I
can't paste live output for — grounding calls a model, and this sandbox has no API key. Honesty
about that is rather the point of the feature.)

## 2. "It forgets everything the moment the session ends"

Agents wake up with amnesia. Whatever your agent figured out yesterday — the plan that worked,
the answer that was verified — is gone, and today's session rediscovers it at full price.

The new `remember` / `recall` MCP tools give agents episodic memory with the same integrity
rules as everything else: entries are **hash-pinned and tamper-detected**, recall is FTS5-backed
and fail-closed. The design principle from the kcp-agent world applies here too: *a memory is a
plan you can re-verify against a moved world.* A memory you can't verify is just a rumor with
a timestamp.

## 3. "Our knowledge docs rot the moment they're written"

A `knowledge.yaml` manifest tells agents which files matter and why. But a manifest is a
document, and documents rot. Synthesis now closes the whole lifecycle: generate
(`kcp init`), refresh volatile fields without touching hand edits (`kcp refresh`), and — the
part that matters — **verify declarations against evidence**:

```text
$ synthesis kcp verify
Manifest: .../knowledge.yaml
  Units: 2 observed, 0 stale, 0 contradicted
  All declarations hold — units marked 'observed'.
```

"Contradicted" is a real category: the G-series governance checks catch declarations reality
disagrees with — a file declared `sensitivity: public` that has an open HIGH security finding,
sharing permissions that violate a declared data-residency restriction.

And manifests now defend themselves cryptographically:

```text
$ synthesis kcp sign knowledge.yaml
  [OK] signed → knowledge.yaml.sig  (key: synthesis-local)

$ synthesis kcp sign knowledge.yaml --verify
Trust tier: TRUSTED  (knowledge.yaml)
```

This is Ed25519, interoperable with the reference consumer — and proven in CI, both
directions. When we bumped the pinned [kcp-agent](https://github.com/Cantara/kcp-agent) to
0.11.0 this week, the full gauntlet ran again: the reference agent verified a
Synthesis-signed manifest (`✓ ed25519 signature verified`), replayed a saved plan
byte-identically, and **rejected a deliberately tampered manifest with exit 1**. A manifest
that can't prove it hasn't been altered is treated as if it has been.

## 4. "It reads the wrong things — or everything"

Context windows are budgets, and most retrieval spends them badly. `kcp plan` produces an
ordered read plan under an explicit token budget, from the deterministic planner — no model
involved in deciding what to read:

```text
$ synthesis kcp plan "how does authentication work" --budget 2000
Read plan for: how does authentication work
  1 unit(s), ~11 tokens
  1. docs/api.md  (score 5, ~11 tok) — 1 trigger match
       → API Reference
```

The same trigger machinery now boosts ordinary `search` and `ask` — measured and flag-gated,
with a `kcpRouting` diagnostics block showing exactly which results were boosted and why. No
silent reranking.

Does planning over manifests actually beat wandering? We benchmarked it against ourselves —
hand-written manifests (Arm B, 9 units) versus Synthesis-generated ones (Arm C, 24 units)
across 8 standard tasks — and the honest answer is more interesting than a victory lap:

- **Zero path overlap**: B routes to source code, C routes to docs, CI, and tests.
- C scores higher on aggregate (455 vs 378) — *partly because verbose trigger lists match
  more*, which is a scoring artifact as much as a quality signal.
- B is better for code navigation; C is better for project understanding.
- **Neither alone is sufficient. Hybrid curation is the recommendation.**

Those caveats are staying in the post, because a retrieval benchmark that only reports the
flattering number is exactly the kind of knowledge this whole stack exists to prevent.

## 5. "Nice — but we're a Kotlin shop"

Until last week, the code knowledge graph behind `relate`, `impact`, and `code-graph
health|gaps` understood Java and TypeScript. On a Kotlin repository it extracted precisely
nothing.

v1.43 fixes that, and the way it happened is the part I want on the record. An outside
contributor whose company runs Kotlin backends opened it **as an RFC, asking for an
architecture read before polishing. The review found one real gap (top-level-function-only
files — idiomatic Kotlin utilities) and flagged two anomalies; within days the contributor had
filed and fixed all of it, validated against three real multi-module Kotlin repositories, with
the known regex limitations pinned in named tests rather than hidden. That is what an
open-source project being *alive* looks like from the contributor side.

The result, on a fresh Kotlin fixture:

```text
$ synthesis code-graph extract
  Files processed:    3
  Dependencies found: 2
  Packages found:     2
  Elapsed:            35 ms

$ synthesis relate PaymentGateway.kt
  Referenced by (incoming): 2 files
    <- src/main/kotlin/com/acme/api/StripeGateway.kt (supertype)
    <- src/main/kotlin/com/acme/billing/InvoiceService.kt (import)
```

"What breaks if I change this interface?" — answered for Kotlin, including Java↔Kotlin
references in mixed repos, because Kotlin declarations share Java's resolution machinery
rather than bolting on a new one.

## Not seven features. One idea.

Grounded answers, verifiable memory, self-defending manifests, inspectable read plans, honest
benchmarks — these are the same move applied to five surfaces: **don't just retrieve
knowledge; make it provable.** Where a claim can be checked against pinned evidence, check it.
Where it can't, say so out loud. Fail closed.

The market for faster search is crowded. The market for trustworthy AI context is empty.
That is the market these three weeks were spent building for — and the next pieces are already
filed: a decision trace for every plan (*why* was this unit selected?), plan diffs (*what
changed* in what an agent would read since last release?), and conformance vectors proving the
Java planner agrees with the reference implementation decision for decision.

Synthesis is at **v1.43.0** — 76 CLI commands, 52 MCP tools, measured this morning against the
code, which regular readers will know is [the only way we quote numbers
anymore](2026-07-12-175-posts-no-map.md).

---

*Every output block above was produced by the current build against a fresh fixture workspace
during the writing of this post. The grounding feature is described but not demonstrated —
no API key in the writing sandbox — and we would rather tell you that than fake a terminal.*
