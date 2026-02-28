---
date: 2026-02-28
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - knowledge-infrastructure
  - standards
  - security
  - enterprise
authors:
  - totto
  - claude
---

# Who Let the Agent In?

*Part 7 of the KCP series. Previous: [The Agent Read the Whole Spec. It Didn't Need To.](/blog/2026/02/28/the-agent-read-the-whole-spec-it-didnt-need-to/)*

<!-- more -->

An agent reaches a unit in a `knowledge.yaml` manifest. No credentials. It loads the
content anyway, because nothing stopped it. Or it gets a 401 with no indication of what
credential to acquire, so it halts and asks the user. Or — in a multi-agent system — an
orchestrator delegates access to a sub-agent that has more permissions than the orchestrator
was ever granted.

These are not hypothetical failure modes. They are the current state of production agent
deployments: auth discovered reactively, delegation chains invisible, access constraints
expressed in system prompts that agents may or may not honour.

RFC-0002 proposes three additions that change this: a lightweight `access` field on units,
a structured `auth` block for the manifest, and a `delegation` block for multi-agent chains.

---

## The landscape (February 2026)

The agentic identity ecosystem has converged on a baseline without producing a single winner.
OAuth 2.1 is the floor — MCP requires it, A2A supports it, all major cloud platforms
implement it. Above that, the picture is fragmented: SPIFFE for workload identity,
W3C Verifiable Credentials for decentralised identity, HTTP Message Signatures (RFC 9421)
for Visa TAP and Mastercard Agent Pay, OIDC-A for delegation chain claims in tokens.

RFC-0002 does not pick a winner. It supports multiple auth schemes in a preference-ordered
list so that agents can select the first method they support. Publishers who only use
OAuth 2.1 declare one method. Publishers who support OAuth plus SPIFFE for zero-trust
workloads declare both. Unknown methods are silently ignored per the spec's extension rules.

---

## The `access` field

The smallest addition is also the most immediately useful. One field, three values:

```yaml
units:
  - id: public-overview
    path: README.md
    intent: "What is this project?"
    scope: global
    audience: [human, agent]
    # access omitted = "public" by default

  - id: internal-runbook
    path: ops/runbook.md
    intent: "How do I handle a production incident?"
    audience: [operator, agent]
    access: authenticated        # any valid credential for this source

  - id: customer-cohort
    path: reports/customer-cohort.md
    intent: "What does the Q1 customer cohort analysis show?"
    audience: [agent]
    access: restricted
    auth_scope: data-team        # named scope or role required
```

`public` (the default), `authenticated`, `restricted`. An agent reading the manifest knows
before fetching which units require credentials, what kind, and — via `auth_scope` — which
specific role or scope is needed. No 401 surprises. No loading content that should not have
been loaded.

---

## The `auth` block

When units require credentials, the root-level `auth` block describes how to acquire them:

```yaml
auth:
  methods:
    - type: oauth2
      flow: client_credentials
      token_endpoint: "https://auth.example.com/token"
      scopes: ["read:knowledge"]
      resource: "https://example.com/knowledge"   # RFC 8707 resource indicator

    - type: spiffe
      trust_domain: "example.com"

    - type: api_key
      header: "X-API-Key"
      registration_url: "https://example.com/register"
```

Methods are ordered by publisher preference. Agent tries each in sequence until one
succeeds — or surfaces the failure to its operator if none are supported.

For complex deployments, the `auth` block may appear on individual units to override the
root block for that unit. A partner documentation section served from a separate auth
domain is a clean use case:

```yaml
  - id: partner-api-docs
    path: partners/api.md
    access: restricted
    auth_scope: partner-portal
    auth:
      methods:
        - type: oauth2
          flow: client_credentials
          token_endpoint: "https://partners.example.com/token"
          scopes: ["partner:read"]
```

---

## The `delegation` block

This is where RFC-0002 addresses the multi-agent case. A human authorizes an orchestrator.
The orchestrator delegates to a sub-agent. The sub-agent accesses the knowledge source.
In current deployments, the knowledge source has no way to know the chain length, whether
permissions narrowed at each hop, or whether the access is auditable.

```yaml
delegation:
  max_depth: 3
  require_capability_attenuation: true
  require_delegation_proof: false
  human_in_the_loop:
    required: false
    approval_mechanism: oauth_consent
  audit_chain: true
```

**`max_depth`** limits chain length from human to resource. `max_depth: 1` means direct
human access or one directly-authorized agent only. `max_depth: 0` means humans only —
no agents.

**`require_capability_attenuation`** requires each hop to narrow, not expand, permissions.
An orchestrator that has `read:docs` cannot delegate `read:everything` to a sub-agent.
Based on the Google Zanzibar / Auth0 FGA attenuation model.

**`audit_chain`** requires W3C Trace Context headers so the full delegation chain can be
reconstructed from access logs. The lightest enforcement option — compatible with
OpenTelemetry, adds no agent complexity beyond including headers.

**`require_delegation_proof`** requires a verifiable delegation chain (XAA lineage token,
OIDC-A chain claim). The heavier option — appropriate for regulated environments.

For the most sensitive units, per-unit delegation constraints tighten the root defaults:

```yaml
  - id: patient-cohort
    path: reports/patient-cohort.md
    access: restricted
    auth_scope: clinical-staff
    delegation:
      max_depth: 1
      require_delegation_proof: true
      human_in_the_loop:
        required: true
        approval_mechanism: oauth_consent
```

This unit requires a human approval step, a short delegation chain, and a verifiable
proof of that chain. An agent that cannot satisfy these constraints cannot access
this unit — and the manifest tells it that before it tries.

---

## Known attacks addressed

The `delegation` block is not hypothetical hardening. Four active attack patterns in
multi-agent systems are addressed directly:

| Attack | Mitigation |
|--------|-----------|
| Agent Session Smuggling | `max_depth` limits chain length |
| Cross-Agent Privilege Escalation | `require_capability_attenuation` |
| EchoLeak (CVE-2025-32711, CVSS 9.3) | `audit_chain` + `require_delegation_proof` |
| Unauthorized autonomous access | `human_in_the_loop: required: true` |

EchoLeak — cross-agent data exfiltration via prompt injection, published in 2025 with a
CVSS score of 9.3 — is the most severe of these. `audit_chain: true` does not prevent
exfiltration on its own, but it makes the chain reconstructable from logs. Combined with
`require_delegation_proof`, it raises the bar significantly.

---

## Adoption gradient

RFC-0002 is designed to be adopted incrementally:

| Step | What to add | Time |
|------|-------------|------|
| Minimal | `access: authenticated` on protected units | 5 minutes |
| Basic | `auth` block with one OAuth 2.1 method | 1 hour |
| Enterprise | `delegation` block with `max_depth` and `audit_chain` | 1 day |
| Regulated | Per-unit `delegation` with `human_in_the_loop` | Project-level effort |

The `access` field works without the `auth` block. The `auth` block works without
`delegation`. Start at the level that matches the actual risk of your deployment.

---

## Open questions

**Granularity of `access`.** Three values (`public`, `authenticated`, `restricted`) covers
most cases. Should `confidential` or `internal` be distinct values? Or is
`access: restricted` + `auth_scope` sufficient for that level of nuance?

**`max_depth` vs named roles.** An integer hop count is simple. Should there also be named
delegation roles (`orchestrator`, `sub-agent`, `tool`) for expressing topology rather than
depth? Comments on [Issue #3](https://github.com/Cantara/knowledge-context-protocol/issues/3).

**Auth block on units.** The proposal allows per-unit `auth` overrides. Is there a
real-world use case that requires them, or does the root-level block cover all practical
scenarios?

---

Full RFC: [RFC-0002-Auth-and-Delegation.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0002-Auth-and-Delegation.md)

Spec and all RFCs: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
