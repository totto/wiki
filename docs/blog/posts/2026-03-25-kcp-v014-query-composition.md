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

Your agent has a task, a token budget, and a manifest with 200 knowledge units. Which units should it actually read? Every team answers this question differently — custom audience filters, ad-hoc staleness checks, bespoke capability gates. The logic works, but none of it interoperates. Swap one tool for another and you rewrite the glue.

KCP v0.14 standardises the query. RFC-0014 standardises composition. Together, they solve the two problems that make knowledge manifests painful at scale.

<!-- more -->

Both are format-level changes. No servers to deploy, no SDKs to upgrade. If you have a `knowledge.yaml`, you can start using the query vocabulary today. Composition is an open RFC — we want your input before it ships.

![KCP v0.14 infographic](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-infographic.png)

**Repo:** [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)

---

## The Token Budget Dilemma

![Every Agent Reinvents Filtering](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-agent-filtering.png)

An agent gets a task: "summarise our GDPR obligations." The manifest has 200 units. The context window fits maybe 8,000 tokens of loaded content. Task + token budget + manifest = an unsolved selection problem. Every time.

Without a standard, Agent A writes custom audience logic. Agent B writes custom staleness logic. Agent C writes custom capability logic. All three hit the same document hub. All three use different glue code.

**Result: Zero interoperability. Wasted engineering cycles.**

![The Token Budget Dilemma](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-token-budget.png)

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

![Format-Level Standardization](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-format-standardization.png)

---

## Precision Context Management

The three new filters in v0.14 are not a grab-bag of features. They are a single idea: let the agent declare its constraints, and let the manifest respond with only what fits.

**`has_capabilities`** — the agent states what it can do. Units requiring capabilities the agent lacks are excluded. An agent without `kubectl` never sees the deployment runbook — saving tokens and preventing it from generating instructions it cannot execute.

**`exclude_stale`** — units past their `freshness_policy.max_age_days` are dropped. In regulated domains, an agent silently basing answers on a compliance policy that expired six months ago is not a minor bug. It is a liability.

**`federation_scope: declared`** — the query expands to all manifests in the `manifests[]` block, one hop. Results carry a `source_manifest` field so the agent knows where each unit lives. Federated knowledge graph queries, without custom traversal logic.

![Precision Context Management](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-precision-context.png)

All of this is advisory. Metadata guides, it does not gatekeep.

---

## Inherit, Don't Copy

![Manifest Forking & Drift](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-fork-drift.png)

A platform team maintains a manifest with 200 units. The EU compliance team needs those 200 units — but with tighter freshness policies on some, three US-only units suppressed, and GDPR-specific triggers added to others. An APAC team needs the same base with different localised content.

Today, both teams fork. The platform team ships unit #201. Neither fork gets it.

**Result: Within a month, three manifests drift apart. System-wide trust in data degrades.**

![Stop Forking. Start Composing.](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-stop-forking.png)

RFC-0014 proposes three composition primitives — `includes`, `overrides`, `excludes` — so you never have to fork again:

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

**Includes** pull in base platform manifests by reference. **Overrides** modify specific triggers, policies, or metadata locally. **Excludes** suppress irrelevant or region-restricted units.

When the platform team adds unit #201, all regional overlays inherit it automatically. No fork. No drift.

![Inherit, Don't Copy](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-inherit-dont-copy.png)

This is an RFC, not shipping code. The open questions — schema merging semantics, version pinning in includes, conflict reporting — are exactly what needs input from people who manage knowledge at this scale.

---

## Implement Today. Shape Tomorrow.

![Implement Today. Shape Tomorrow.](https://raw.githubusercontent.com/Cantara/knowledge-context-protocol/main/assets/kcp-v014-slide-implement-today.png)

**Query vocabulary — shipping now.** Read the [query vocabulary spec (§15)](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md). If you have a `knowledge.yaml`, you can use it today.

**Composition — RFC stage.** Read [RFC-0014](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0014-Manifest-Composition.md). Tell us what is wrong with it.

**Contribute.** Join the conversation in [GitHub Discussions](https://github.com/Cantara/knowledge-context-protocol/discussions).
