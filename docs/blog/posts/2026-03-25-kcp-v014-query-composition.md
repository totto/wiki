---
date: 2026-03-25
categories:
  - Knowledge Infrastructure
  - AI-Augmented Development
tags:
  - kcp
  - knowledge-context-protocol
  - ai-agents
  - open-source
  - agentic-systems
  - manifest-composition
  - query-vocabulary
authors:
  - totto
---

# Every Agent That Queries a Knowledge Manifest Reinvents Filtering

If you build AI agents that consume structured knowledge — from internal docs, compliance libraries, API references — you have written this code before. Your agent has a task and a token budget. It loads a manifest. Then it implements its own logic to figure out which units to actually read: filtering by audience, checking if content is stale, skipping units that need capabilities the agent does not have. Every team writes this differently. None of it interoperates.

Knowledge Context Protocol v0.14 standardises this. And separately, RFC-0014 proposes a composition model for manifests that lets you stop forking them.

<!-- more -->

Both are format-level. No servers to deploy, no SDKs to upgrade. If you have a `knowledge.yaml`, you can use the query vocabulary today. Composition is an open RFC — we want your input before it ships.

![KCP v0.14 infographic](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-infographic.png)

**Repo:** [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)

---

## The query problem, concretely

An agent gets a task: "summarise our GDPR obligations." The manifest has 200 units. The agent's context window has room for maybe 8,000 tokens of loaded content. Which units should it read?

Until v0.14, every tool that consumed KCP manifests answered this question with custom code. One tool filters on `audience`. Another checks `hints.token_estimate` against a budget. A third ignores stale content. None of them agree on the query format, so you cannot swap one for another without rewriting the glue.

v0.14 promotes RFC-0007 and RFC-0008 into a normative query vocabulary (SPEC.md §15). All fields are optional. An empty query matches everything:

```yaml
terms: ["authentication", "oauth2"]
audience: agent
max_token_budget: 8000
has_capabilities: [tool:kubectl, permission:deploy-prod]
exclude_stale: true
federation_scope: declared
```

The response is scored and budget-aware:

```yaml
results:
  - unit_id: auth-guide
    score: 13
    path: docs/api/authentication.md
    token_estimate: 4200
    match_reason: [trigger, intent]
    source_manifest: null

  - unit_id: sso-integration-guide
    score: 8
    path: docs/sso.md
    token_estimate: 3100
    match_reason: [intent]
    source_manifest: identity-service
```

Three filters are new in v0.14:

**`has_capabilities`** — The agent declares what it can do. Units that require capabilities the agent lacks are excluded. An agent without `kubectl` never sees the deployment runbook. This saves tokens and prevents the agent from generating instructions it cannot execute.

**`exclude_stale`** — Units past their `freshness_policy.max_age_days` are dropped. In regulated domains, you do not want an agent silently basing its answers on a compliance policy that expired six months ago.

**`federation_scope: declared`** — The query expands to all manifests in the `manifests[]` block (one hop). Results carry a `source_manifest` field so the agent knows where each unit lives. Query across a federated knowledge graph without custom traversal logic.

All of this is advisory. Metadata guides, it does not gatekeep.

---

## The composition problem (RFC-0014 — open for discussion)

![Manifest Forking & Drift](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-fork-drift.png)

A platform team maintains a manifest with 200 units. The EU compliance team needs those 200 units, but with tighter freshness policies on some, three US-only units suppressed, and GDPR-specific triggers added to others. A separate APAC team needs the same base with different localised content.

Today, both teams fork. The platform team ships unit #201. Neither fork gets it. Within a month, three manifests are drifting apart and nobody is confident any of them is current.

RFC-0014 proposes three composition primitives: `includes`, `overrides`, `excludes`:

```yaml
# eu-compliance/knowledge.yaml
composition:
  includes:
    - source: https://platform.acme.internal/knowledge.yaml

  overrides:
    - id: data-retention-policy
      triggers: ["GDPR", "data retention", "right to erasure"]
      sensitivity: confidential

  excludes:
    - id: us-state-tax-calculation
    - id: us-hipaa-audit-log

units:
  - id: gdpr-data-map
    path: compliance/gdpr-data-map.md
    intent: "What personal data does the platform process and under what GDPR legal basis?"
    triggers: [GDPR, data map, legal basis, Article 6]
```

When the platform team adds unit #201, all regional overlays inherit it. No fork. No drift.

This is an RFC, not shipping code. The open questions — schema merging semantics, version pinning in includes, conflict reporting — are exactly what needs input from people who manage knowledge at this scale.

---

## Try it

1. Read the [query vocabulary spec (§15)](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md).
2. Read [RFC-0014](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0014-Manifest-Composition.md) and tell us what is wrong with it.
3. Join the conversation in [GitHub Discussions](https://github.com/Cantara/knowledge-context-protocol/discussions).
