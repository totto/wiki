---
title: "The KCP Manifest"
description: "The knowledge.yaml manifest that makes a decision system navigable and governable — kind, metadata, a temporal window, and explicitly declared governed units instead of a flat pile of files."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# The KCP Manifest

A defendable agent needs to know exactly which knowledge it is allowed to load, which version of it, and when that knowledge was last true. A directory of files cannot answer any of those questions. A manifest can. The Knowledge Context Protocol manifest — `knowledge.yaml` — is the small declarative file that turns a heap of prompts, scoring models and reference data into a set of named, versioned, temporally-bounded units the harness can reason about.

I treat the manifest as the contract between the deterministic parts of the system and the model at the edge. Everything the agent may consult is declared here, or it does not exist as far as the [governance harness](/topics/defendable-agents/architecture/governance-harness/) is concerned. That is the whole point of [fail-closed](/topics/defendable-agents/primitives/fail-closed-policy/) design: undeclared knowledge is unreachable knowledge.

## Structure: kind, metadata, temporal, units

Every manifest has four parts, and each earns its place.

- **`kind`** — always `manifest`. It tells the loader what schema to validate against. `kcp-agent` exposes `kcp_validate` precisely so this is checked before anything runs.
- **`metadata`** — identity and provenance: `name`, `version`, `domain`, `description`. The `version` is not decoration; it is what drift detection compares against. When a scoring model changes, the manifest version changes, and every temporal pin taken under the old version is now visibly stale.
- **`temporal`** — a `valid_from` date and a `refresh_interval`. This is the manifest declaring, out loud, how fresh its own knowledge is expected to be. It is the anchor that [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) hangs off.
- **`units`** — the list of governed knowledge units. Each has an `id`, a `path`, `tags`, a `description`, and an optional `depends_on`. These are the only things `kcp_load` will load.

## A minimal example

Here is a trimmed manifest for the Lodestar example — a decision system that scores buyers in a regulated professional-services market. It declares the scoring models as governed units so they are selected deterministically and never silently swapped underneath a running session.

```yaml
kind: manifest
metadata:
  name: lodestar-decision-knowledge
  version: 4.2.0
  domain: regulated-professional-services
  description: >
    Governed knowledge units for buyer scoring, match scoring
    and account tiering in a regulated professional-services market.

temporal:
  valid_from: 2026-05-01
  refresh_interval: P30D

units:
  - id: buyer-scoring-model
    path: models/buyer-scoring.yaml
    tags: [scoring, buyer, deterministic]
    description: >
      3-layer weighted composite (Need 0.40, Attractiveness 0.25,
      Winnability 0.35) over 18 variables, scored 1-5.
  - id: match-scoring-model
    path: models/match-scoring.yaml
    tags: [scoring, match, deterministic]
    depends_on: [buyer-scoring-model]
    description: >
      4-layer weighted composite (Need-match 0.25, Market-match 0.20,
      Commercial-match 0.25, Winnability-priority 0.30), 21 variables.
  - id: account-tiering-rules
    path: models/account-tiering.yaml
    tags: [tiering, deterministic]
    description: Maps composite scores to tier_1..tier_3 / out_of_scope.
  - id: priority-bands
    path: reference/priority-bands.yaml
    tags: [reference, banding]
    description: >
      Band thresholds — Very high >=85, High >=70,
      Interesting-but-with-gaps >=55, Lower-priority >=40.
```

The harness then references this manifest in `harness.yaml`:

```yaml
governance:
  domains:
    - manifest: knowledge.yaml
      paths: [models/, reference/]
      tools: [kcp_plan, kcp_load]
policy:
  fail_closed: true
  audit_all: true
```

`kcp_plan` resolves which units are needed for a task and in what order (respecting `depends_on`); `kcp_load` loads exactly those and nothing else. Both are ordinary MCP tools, which is how the [KCP-to-agent wiring](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/) stays clean.

## Why this beats a flat file list

A flat directory is an implicit, undeclared, unversioned dependency graph. You can `cat` any file, load two incompatible model versions at once, and never notice that `buyer-scoring.yaml` was edited an hour ago. Nothing records what was consulted. The manifest closes each of those gaps.

| Concern | Flat file list | KCP manifest |
| --- | --- | --- |
| What may be loaded? | Anything on disk | Only declared `units` |
| Which version? | Whatever is on disk now | Pinned by `metadata.version` |
| How fresh? | Unknown | `temporal.valid_from` + `refresh_interval` |
| Dependencies | Implicit, in someone's head | Explicit `depends_on` |
| Loaded-what record | None | Auditable `kcp_load` calls |
| Silent swaps | Easy and invisible | Version change is visible drift |

The manifest is also what makes reproducibility mean something. A [decision trace](/topics/defendable-agents/primitives/decision-traces/) records the model and variables used; the manifest is what guarantees the loader would select that same model version again given the same inputs. Declaring the models as governed units — rather than importing them as code — is covered in more depth under [declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/). For the wider design philosophy, the [Knowledge Context Protocol](/topics/knowledge-context-protocol/) pillar is the place to start.

## Honest limits

The manifest declares intent; it does not enforce truth. A `valid_from` date is a claim about freshness, not a measurement — [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) can detect that a pin has aged past `refresh_interval`, but neither the manifest nor the pin will fetch newer data for you. Someone still has to refresh it. Likewise, a `depends_on` edge is only correct if a human wrote it correctly; the loader trusts your graph. And a governed unit can hold a wrong model as easily as a right one — the manifest ensures the *same* model is applied reproducibly and visibly, which is how you eventually catch the error, not that the model is correct on day one. That is the recurring bargain of [defendable design](/topics/defendable-agents/argument/what-defendable-means/): the manifest buys you navigability and governability, not omniscience, and it is maintained knowledge, not a one-time setup.
