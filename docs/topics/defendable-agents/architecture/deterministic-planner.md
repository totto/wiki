---
title: "The Deterministic Planner"
description: "Anatomy of the deterministic planner: a pure function over declared metadata that produces an inspectable, reproducible plan before any content loads or any model runs."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# The Deterministic Planner

Most agent frameworks decide what to read by reading. They stuff a pile of documents into context, let the model skim, and hope the relevant passage survives the noise. That approach has two defects I refuse to ship: it costs tokens to make a decision you have not justified yet, and the decision leaves no record you can inspect afterwards. The deterministic planner exists to fix both.

The planner is a **pure function over declared metadata**. It reads a manifest — not the content the manifest describes — and emits a plan: an ordered list of units to load, each with a machine-readable reason, and an explicit list of units it chose to skip, each with a skip-reason. Same manifest plus same query in, byte-identical plan out. No model call happens inside it. In the Lodestar reference system this planner is `kcp-agent`, exposed over MCP as the tools `kcp_plan`, `kcp_load`, and `kcp_validate`.

## Plan before load

The sequence matters, so I will be pedantic about it. The planner runs `kcp_plan` first. Only after a plan exists — and, in a governed session, only after the [governance harness](/topics/defendable-agents/architecture/governance-harness/) has admitted it against the fail-closed policy and the budget ceiling — does anything call `kcp_load` to pull the actual bytes into context. Planning is a metadata operation. Loading is a content operation. Keeping them separate is what makes the agent [defendable](/topics/defendable-agents/argument/what-defendable-means/) rather than merely clever.

This is the practical payoff of the [plan-before-load discipline](/topics/defendable-agents/architecture/overview/): the expensive, irreversible act (spending context on content, then calling the model at the edge) is gated behind a cheap, inspectable act (producing a plan). You get to read the plan, diff it against last week's, and reject it — all before a single token of source material is loaded.

## Zero-token navigation

Because the planner reads metadata rather than content, navigation costs zero model tokens. A manifest describing forty knowledge units might be a few kilobytes of declared `id`, `path`, `tags`, and `description` fields. The planner selects across all forty deterministically; only the handful that survive selection are ever loaded. In a governed session with a `context_budget` of 200000 tokens, that difference is the difference between fitting the work and blowing the ceiling.

Here is the manifest the planner reads. This is [KCP](/topics/knowledge-context-protocol/) — the same `knowledge.yaml` shape covered in [manifest basics](/topics/defendable-agents/kcp/manifest-basics/):

```yaml
kind: manifest
metadata:
  name: lodestar-scoring
  version: 3.2.0
  domain: professional-services-market
  description: Deterministic scoring models for buyers and firms
  temporal:
    valid_from: 2026-05-01
    refresh_interval: 30d
units:
  - id: buyer-scoring-model
    path: models/buyer-scoring.yaml
    tags: [scoring, buyer, need, attractiveness, winnability]
    description: 3-layer weighted composite; 18 variables
  - id: match-scoring-model
    path: models/match-scoring.yaml
    tags: [scoring, match, commercial]
    description: 4-layer weighted composite; 21 variables
    depends_on: [buyer-scoring-model]
  - id: signal-freshness
    path: models/signal-freshness.yaml
    tags: [temporal, decay]
    description: 30-day half-life freshness decay, 1-5
```

## Scored reasons and skip-reasons

A plan is not just a list of paths. Every entry carries why it is there, and the skip list carries why the rest are not. For a query about scoring a buyer, the planner emits something like:

```json
{
  "query": "score buyer signal for account tiering",
  "selected": [
    { "id": "buyer-scoring-model", "reason": "tag:scoring+tag:buyer matched query terms", "score": 0.91 },
    { "id": "signal-freshness", "reason": "tag:temporal required by buyer Need layer", "score": 0.64 }
  ],
  "skipped": [
    { "id": "match-scoring-model", "skip_reason": "tag:match absent from query; depends_on chain not triggered" }
  ],
  "modelVersion": "3.2.0",
  "modelHash": "sha256:9f3c…"
}
```

The `skipped` array is the part people underrate. A defendable agent has to answer "why did you *not* consult that document?" as readily as "why did you consult this one." A silent omission is indistinguishable from a bug. An explicit skip-reason turns the omission into a claim you can audit, and if it is wrong, it is wrong *visibly* — which is the only kind of wrong you can fix.

## Reproducibility for free

Because the planner is pure, reproducibility is not a feature you build — it falls out of the design. The plan records `modelVersion` and `modelHash`, so the exact scoring model the plan selected is pinned. Re-run the same query against the same manifest version and you get the same plan, the same units, the same hash. That is the foundation the [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) and the [reproducibility guarantee](/topics/defendable-agents/decisions/reproducibility/) stand on: a decision you cannot reproduce is a decision you cannot defend, and everything downstream inherits determinism from the planner upward.

Declaring the scoring models as governed KCP units is what makes this hold. The models are not hard-coded constants buried in application logic — they are units the planner selects by `id`, so a model can never be silently swapped without the version and hash changing in the plan. See [declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/) for how that wiring works.

## Honest limits

Two things the planner does not give you, so nobody mistakes the boundary.

First, determinism guarantees **process, not correctness**. If a `description` or a tag on a unit is misleading, the planner will select — or skip — that unit the same wrong way every single time. The value is not that it is right; the value is that it is *consistently and inspectably* wrong, which is precisely how you catch it in a plan diff before it reaches production. Contrast that with a model skimming content, where the same mistake is a different mistake every run.

Second, the planner navigates; it does not comprehend. It matches declared metadata to a query with a scoring function. The comprehension still happens later, when the loaded content reaches the [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) — and that is still a model, with all a model's fallibility. The planner's job is narrower and, deliberately, dumber: make the navigation decision cheap, explicit, and reproducible, so the expensive probabilistic step operates on a defensible, minimal, audited slice of context.

For the full runtime picture — how a plan becomes an audited operation with a budget entry and a pin — continue to the [governed session](/topics/defendable-agents/architecture/overview/) and the [case study](/topics/defendable-agents/reference/case-study-lodestar/).
