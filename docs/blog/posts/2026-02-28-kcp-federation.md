---
date: 2026-02-28T10:00:00
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - knowledge-infrastructure
  - standards
  - enterprise
authors:
  - totto
  - claude
---

# What Happens When Your Agent Needs Knowledge From Five Teams?

*Part 5 of the KCP series. Previous: [How Do You Tell an Agent "This Data Cannot Leave the Building"?](/blog/2026/02/28/how-do-you-tell-an-agent-this-data-cannot-leave-the-building/)*

<!-- more -->

You have added `knowledge.yaml` to your product repository. The agent navigates it well.
Then the first cross-team question arrives.

A developer asks: *how do I deploy this service?* The answer depends on four things:
local deployment configuration, the platform team's infrastructure conventions, the security
team's compliance requirements, and the shared engineering standards that govern API design.
Each of these lives in a separate repository. Each has its own `knowledge.yaml`. And in
KCP v0.3, each manifest is an island — there is no way to express that your deployment
guide depends on the platform team's architecture, or that your GDPR handling is governed
by the security team's policy.

RFC-0003 proposes exactly that: **cross-manifest federation**.

---

## The problem in concrete terms

Consider a mid-sized engineering organisation:

```
platform-team/knowledge.yaml       — infrastructure, deployment, observability
security-team/knowledge.yaml       — compliance, threat models, GDPR guides
product-alpha/knowledge.yaml       — feature docs, API guides, runbooks
shared-standards/knowledge.yaml    — org-wide conventions, ADRs, style guides
```

An agent helping a developer on product-alpha needs to know that the deployment guide
*depends on* platform-team's deployment architecture — that the GDPR handling *is governed
by* security-team's compliance policy — that API design *should follow* shared-standards'
conventions.

None of these relationships are expressible in v0.3. The agent must discover and load all
four manifests independently, with no way to understand the dependency ordering or
relationship types between them. It is navigating four separate maps with no connection
between them.

---

## Three additions, one pattern

RFC-0003 proposes a hub-and-spoke model. One manifest becomes the hub; it declares which
sub-manifests it federates and what role each plays. Three fields make this work.

### 1. The `manifests` block

A hub manifest declares its sub-manifests with labels and relationship types:

```yaml
kcp_version: "0.3"
project: acme-engineering-knowledge
version: 1.0.0

manifests:
  - id: platform
    url: "https://knowledge.platform.acme.com/knowledge.yaml"
    label: "Platform Engineering — infrastructure, CI/CD, observability"
    relationship: foundation    # this sub-manifest is foundational to hub units

  - id: security
    url: "https://knowledge.security.acme.com/knowledge.yaml"
    label: "Security & Compliance — GDPR, NIS2, threat models"
    relationship: governance    # this sub-manifest governs hub units

  - id: shared-standards
    url: "https://knowledge.standards.acme.com/knowledge.yaml"
    label: "Engineering Standards — ADRs, API conventions, style guides"
    relationship: foundation

  - id: product-alpha
    url: "https://knowledge.product-alpha.acme.com/knowledge.yaml"
    label: "Product Alpha — feature docs, API guides, runbooks"
    relationship: child         # this sub-manifest depends on hub context
```

The `relationship` values — `foundation`, `governance`, `child`, `peer`, `archive` — tell
the agent how to weight each sub-manifest. A `governance` manifest contains authoritative
policies. A `foundation` manifest provides context that hub units build on. An `archive`
manifest is historical; agents may skip it unless specifically requested.

### 2. `external_depends_on` on units

Individual units can declare cross-manifest dependencies:

```yaml
units:
  - id: product-deployment-guide
    path: ops/deployment.md
    intent: "How do I deploy product-alpha to production?"
    scope: project
    audience: [operator, developer, agent]
    depends_on: [product-architecture]        # local dependency (existing)
    external_depends_on:                      # cross-manifest (new)
      - manifest: platform                   # references manifests[].id
        unit: deployment-architecture
        required: false                      # advisory; continues if unresolvable

  - id: gdpr-data-handling
    path: compliance/data-handling.md
    intent: "How does product-alpha handle personal data under GDPR?"
    scope: project
    audience: [developer, operator, agent]
    external_depends_on:
      - manifest: security
        unit: gdpr-policy
        required: true                       # agent SHOULD warn if unresolvable
      - manifest: shared-standards
        unit: data-classification-guide
        required: false
```

`required: true` on an external dependency signals that the agent should surface a warning
if the cross-manifest unit cannot be resolved — not abort, but flag it. `required: false`
(the default) is silently skipped on network failure.

### 3. `external_relationships`

Typed edges across manifest boundaries, extending the existing `relationships` section:

```yaml
external_relationships:
  - from_unit: incident-response
    to_manifest: platform
    to_unit: alerting-runbook
    type: depends_on

  - from_manifest: security
    from_unit: gdpr-policy
    to_unit: onboarding-guide          # omitting to_manifest = this manifest
    type: governance

  - from_unit: api-design-guide
    to_manifest: shared-standards
    to_unit: rest-api-conventions
    type: context
```

The relationship vocabulary gains two new types for cross-manifest use: `depends_on` and
`governance`. The existing types — `enables`, `context`, `supersedes`, `contradicts` —
carry over.

---

## What you can do today: `x-external-ref`

RFC-0003 is not yet in the core spec. If you want cross-manifest navigation without
waiting, the `x-external-ref` extension convention works now:

```yaml
units:
  - id: deployment-guide
    path: ops/deployment.md
    intent: "How do I deploy this service?"
    x-external-ref:
      - manifest: "https://platform-team.example.com/knowledge.yaml"
        unit_id: deployment-architecture
        relationship: depends_on
```

Per the spec's extension rules, tools that understand `x-external-ref` use it; tools
that do not silently ignore it. When RFC-0003 is promoted, `x-external-ref` entries
migrate to `external_depends_on` mechanically.

---

## Hub-and-spoke, not arbitrary peer-to-peer

The deliberate constraint in RFC-0003 is the hub-and-spoke topology. Arbitrary
peer-to-peer cross-referencing — manifest A references manifest B without a hub — is
deferred. The reason is practical: it creates cycles that are hard to detect and trust
boundaries that are hard to reason about.

In the hub-and-spoke model, the hub author controls the federation graph. Cycle detection
extends across manifest boundaries using a visited URL set during fetching. The maximum
federation depth defaults to three levels (hub → sub-manifest → sub-sub-manifest → stop),
preventing runaway recursive fetches.

Whether sub-manifests should be able to declare their own `manifests` blocks — making the
topology a tree rather than a strict hub-and-spoke — is one of the open questions in
RFC-0003.

---

## The Synthesis connection

`synthesis export --format kcp` already generates a `knowledge.yaml` for a single
workspace. For multi-workspace Synthesis installations — the scenario that originally
motivated KCP, indexing 8,934 files across three workspaces — the natural extension is
a `synthesis federate` command that:

1. Generates per-workspace `knowledge.yaml` files
2. Generates a root hub manifest with a `manifests` block pointing to each
3. Infers `external_depends_on` entries from cross-workspace dependency data already
   in the Synthesis index

The cross-workspace dependency graph is already there. RFC-0003 would make it navigable
by any KCP-speaking agent, not just tools that speak the Synthesis MCP protocol directly.

---

## Open questions — your input matters

RFC-0003 has six open questions. The three most consequential:

**Hub-and-spoke only, or peer-to-peer too?** The RFC restricts federation to hub-and-spoke
for tractable cycle detection and clear trust boundaries. If your cross-team dependencies
do not fit a hub hierarchy, [comment on Issue #12](https://github.com/Cantara/knowledge-context-protocol/issues/12)
with the use case.

**Version pinning.** Should `manifests` entries support a `version_pin` field locking to a
specific remote manifest version? It prevents silent breakage when a sub-manifest changes —
but adds operational overhead for manifest authors who must update pins on every sub-manifest
update.

**Offline / air-gapped deployments.** The current proposal silently skips `required: false`
dependencies on network failure and warns on `required: true`. Should there be a
`cache_remote_manifests` option for storing fetched manifests locally? Enterprise
air-gapped deployments may need it.

---

Full RFC: [RFC-0003-Federation.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0003-Federation.md)

Spec and all RFCs: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
