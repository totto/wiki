---
title: "The Scoring-Model Manifest"
description: "How to design a deterministic scoring model as a governed YAML manifest — layers, weights, variables, 1-5 scales, scoring guides, and decay — versioned as a KCP unit."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# The Scoring-Model Manifest

A scoring model is the most dangerous kind of business logic you can put near a language model: it looks like judgement, it produces a number people act on, and if it lives in a prompt it changes every time the wind does. In Lodestar — the example system I use throughout this guide, an agent that ranks buyers in a regulated professional-services market — the model does not live in a prompt. It lives in a manifest: a flat, reviewable YAML document that a pure function reads and a human can diff.

This page shows what that manifest looks like, why it is declared as a governed [KCP](/topics/knowledge-context-protocol/) unit rather than a config file the code happens to load, and how you hang a version on it so a score can never be silently produced by a model nobody signed off on.

## What the manifest declares

The [deterministic engine](/topics/defendable-agents/architecture/deterministic-planner/) needs only four things to turn evidence into a number: which **layers** exist, what each layer **weighs**, which **variables** feed each layer, and how a human is meant to pick a 1-5 score for each variable. The manifest is exactly those four things and nothing else — no I/O, no model calls, no branching on the current date.

Here is an anonymized cut of the buyer model. It is deliberately boring, and that is the point.

```yaml
model: buyer-score
version: 3.2.0
scale:
  min: 1
  max: 5
  step: 0.5
  projection: linear      # layer = mean(variables) * 20 -> 0..100
bands:
  - { min: 85, label: "Very high" }
  - { min: 70, label: "High" }
  - { min: 55, label: "Interesting but with gaps" }
  - { min: 40, label: "Lower priority" }
  - { min: 0,  label: "Not prioritized now" }
layers:
  - id: need
    weight: 0.40
    variables:
      - id: signal-strength
        scoring_guide:
          1: "No observable buying signal"
          3: "Indirect or second-hand signal"
          5: "Named, dated, first-party trigger event"
      - id: signal-freshness
        decay:
          kind: half_life
          half_life_days: 30
          table: { "3": 5, "7": 4.5, "14": 4, "30": 3, "60": 2, "90": 1.5 }
          floor: 1
      - id: signal-relevance
      - id: signal-velocity
      - id: buying-journey-stage
      - id: internal-mobilization
  - id: attractiveness
    weight: 0.25
    variables:
      - { id: mandate-value }
      - { id: strategic-value }
      - { id: growth-potential }
      - { id: sector-fit }
      - { id: reference-value }
      - { id: cross-sell-potential }
  - id: winnability
    weight: 0.35
    variables:
      - { id: competitive-position }
      - { id: relationship-proximity }
      - { id: known-criteria }
      - { id: decision-access }
      - { id: internal-capacity }
      - { id: relevant-experience }
```

Three layers, weights that sum to 1.0, eighteen variables, one explicit decay rule, five bands. A layer score is the mean of its variable scores times twenty, giving 0-100; the buyer total is the weighted composite `0.40*need + 0.25*attractiveness + 0.35*winnability`. The sibling MATCH model has the same shape with four layers and twenty-one variables. I unpack the arithmetic in [Anatomy of a Score](/topics/defendable-agents/decisions/anatomy-of-a-score/) and the layer/weight/band design in [Layers, Weights, Bands](/topics/defendable-agents/decisions/layers-weights-bands/).

## The scoring guide is the model

Weights get the attention; the `scoring_guide` is where the defendability actually lives. A weight of 0.40 means nothing if two analysts disagree about whether a signal is a 2 or a 4. The guide pins the 1-5 scale to observable facts, so the model is auditable at the variable level and not just the total. When a buyer is scored, the full variable trace — every id, its score, and the guide it was read against — lands in the [audit log](/topics/defendable-agents/primitives/audit-trail/) and the [decision trace](/topics/defendable-agents/primitives/decision-traces/). That is what lets someone six months later ask "why a 4 here" and get an answer instead of a shrug. Writing good, discriminating guides is its own discipline, covered in [Variable Design](/topics/defendable-agents/decisions/variable-design/).

The `decay` block on `signal-freshness` deserves a note. It is the one place the model is a function of time, and it is declared, not computed in code: a 30-day half-life where a signal three days old scores 5 and one over ninety days scores 1. Keeping decay in the manifest means the [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) records exactly which decay curve produced a stale score, so drift detection can tell "the data moved" from "the curve changed".

## Why it is a governed KCP unit

A YAML file the code reads with `open()` is a config file. A YAML file declared in a [KCP manifest](/topics/defendable-agents/kcp/manifest-basics/) is a *governed unit*: `kcp-agent` selects it deterministically through `kcp_plan` and `kcp_load`, records which unit answered, and refuses to run if the requested model is absent. There is no code path where the engine quietly falls back to a different model because a file moved.

```yaml
kind: manifest
metadata:
  name: lodestar-scoring
  version: 1.4.0
  domain: buyer-intelligence
units:
  - id: model.buyer-score
    path: models/buyer-score.yaml
    tags: [scoring, buyer, governed]
    description: "Buyer priority model, 3 layers / 18 variables"
  - id: model.match-score
    path: models/match-score.yaml
    tags: [scoring, match, governed]
    depends_on: [model.buyer-score]
```

Declaring the models this way is how the [governance harness](/topics/defendable-agents/architecture/governance-harness/) grants the scoring domain access to exactly these two units and nothing else. The wiring between harness, `kcp-agent`, and the MCP tool surface is walked through in [Wiring KCP, agent, MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/).

## The versioning hook

Every score a governed session emits carries a `modelVersion` and a `modelHash` in its temporal pin. `modelVersion` is the `version:` field in the model file (`3.2.0` above); `modelHash` is a content hash of the manifest as loaded. Bump a weight, edit a scoring guide, retune the decay table — the hash changes, and any pin taken under the old hash now reports **model drift** on its next check. Model drift alone is enough to recommend reanalysis, which is deliberate: a re-weighted model is a new model, and old numbers should not be trusted as comparable. The full policy lives in [Versioning Models](/topics/defendable-agents/decisions/versioning-models/), and the guarantee that the same manifest plus the same inputs always yields the same total is [Reproducibility](/topics/defendable-agents/decisions/reproducibility/).

## Honest limits

The manifest makes the model *inspectable and reproducible*; it does not make it *correct*. If `signal-relevance` is weighted too hard, or a scoring guide rewards the wrong evidence, the engine will apply that mistake to every buyer, forever, identically. That is a feature of the defence, not a defect: a consistent, visible, versioned error is one you can find in a review and fix with a version bump — unlike a prompt that is wrong differently on every run. The manifest guarantees the process. Getting the model right is still your job, and it is never finished.
