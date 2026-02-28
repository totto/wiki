---
date: 2026-02-28T11:00:00
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - compliance
  - gdpr
  - enterprise
  - knowledge-infrastructure
  - standards
authors:
  - totto
  - claude
---

# How Do You Tell an Agent "This Data Cannot Leave the Building"?

*Part 4 of the KCP series. Previous: [Add knowledge.yaml to Your Project in Five Minutes](/blog/2026/02/28/add-knowledge-yaml-to-your-project-in-five-minutes/)*

<!-- more -->

You have deployed an AI agent with access to your internal knowledge base. It can query
documentation, architectural decisions, operational runbooks. Useful. The problem arrives
in the second week, when someone asks: *how do we tell the agent which of this is
GDPR-regulated? Which cannot be sent to external LLM APIs? Which requires a human to
approve access first?*

Currently, the honest answer is: you cannot. Not in any machine-readable, standardised way
that the agent can act on. You can put instructions in the system prompt and hope they hold.
You can restrict access at the infrastructure level before the agent ever sees the data. But
there is no metadata layer in your knowledge manifest that says "this unit is MiFID2-regulated,
EEA-resident, do not cache, do not redistribute, require human approval."

RFC-0004 proposes exactly that layer.

---

## Two blocks, two concerns

The RFC adds two optional blocks to the `knowledge.yaml` manifest:

**`trust`** — provenance, content integrity, audit requirements, and agent access control:
who published this knowledge, has it been tampered with, what kind of agent may access it,
and what audit trail is required.

**`compliance`** — data residency, applicable regulations, sensitivity classification, and
processing restrictions: where may this knowledge be stored and processed, which laws govern
it, and what is the agent forbidden to do with it.

Both operate as root-level defaults with per-unit overrides. A manifest can declare that
all knowledge is GDPR-regulated, EEA-resident, and `confidential` by default — and then
individually mark a public README as `sensitivity: public` and trading algorithm
documentation as `sensitivity: restricted, no-external-llm, no-redistribution`.

---

## What it looks like in practice

A financial services firm deploying agents against its internal knowledge base:

```yaml
kcp_version: "0.3"
project: acme-financial-knowledge
version: 2.0.0

trust:
  provenance:
    publisher: "Acme Financial Services"
    publisher_did: "did:web:acme.com"
    contact: "knowledge-ops@acme.com"
  audit:
    agent_must_log: true
    require_trace_context: true   # W3C Trace Context — full access chain reconstructable

compliance:
  data_residency:
    regions: [EEA]
    hard_requirement: true        # legally mandatory, not advisory
  regulations: [GDPR, MiFID2, DORA]
  sensitivity: confidential

units:
  - id: overview
    path: README.md
    intent: "What does this knowledge base cover?"
    scope: global
    audience: [human, agent]
    compliance:
      sensitivity: public         # override: less restrictive than root default

  - id: customer-pii-schema
    path: data/customer-pii.md
    intent: "How is customer personal data structured and protected?"
    scope: module
    audience: [developer, agent]
    compliance:
      regulations: [GDPR, ePrivacy]
      sensitivity: confidential
      restrictions:
        - no-external-llm         # MUST NOT be sent to external LLM APIs
        - no-logging              # MUST NOT appear in agent logs
        - no-caching
        - audit-required
        - human-approval-required

  - id: security-runbook
    path: ops/security-runbook.md
    intent: "How do we respond to a security incident?"
    scope: module
    audience: [developer, agent]
    compliance:
      sensitivity: restricted
      regulations: [NIS2]
      restrictions:
        - no-external-llm
        - human-approval-required
```

The agent reading this manifest knows — before loading any content — that customer PII
documentation cannot go to an external LLM, cannot be cached, and requires human approval
to access. It knows the security runbook is NIS2-regulated and restricted. It knows the
EEA data residency requirement is legally mandatory, not advisory.

What it does with that information depends on the agent implementation. KCP declares. The
consuming system enforces.

---

## The advisory principle — and why it is the right call

This is the design decision most likely to prompt pushback, so it is worth being explicit:
**all KCP metadata is advisory**. The presence of a `no-external-llm` restriction in a
manifest is a declaration by the publisher. It is not a technical control that prevents
the agent from calling an external API.

This is intentional, and correct.

KCP is a metadata format, not a policy enforcement engine. It cannot inspect the agent
runtime, intercept API calls, or enforce data residency at the network level. Pretending
otherwise would produce false security — a `no-external-llm` field that organisations
trust as a control when it is actually just a flag.

The right architecture is: KCP declares the intent, compliance-aware agent frameworks and
infrastructure enforce it. Just as `robots.txt` does not technically prevent crawling but
establishes a standard declaration that compliant crawlers honour, KCP establishes a
standard declaration that compliant agents honour. The enforcement layer is separate —
and should be.

One exception: `data_residency.hard_requirement: true`. This is the only field in KCP that
approaches normative agent behaviour. Agents encountering it SHOULD refuse to process the
unit if they cannot confirm they are operating within the declared region. Even here,
enforcement depends on the agent implementation — but the signal is explicit that this is
a legal obligation, not a preference.

---

## NIST alignment

The NIST NCCoE AI Agent Standards Initiative (February 2026) identifies three requirements
that RFC-0004 addresses directly:

| NIST requirement | RFC-0004 response |
|-----------------|------------------|
| Logging and transparency: linking AI agent actions to their non-human entity | `trust.audit.require_trace_context` (W3C Trace Context) |
| Data governance: ensuring agents handle data in compliance with applicable laws | `compliance.regulations` + `compliance.data_residency` + `compliance.restrictions` |
| Trust verification: mechanisms for verifying agent trustworthiness | `trust.agent_requirements.require_attestation` + `attestation_url` |

The NIST comment period is open until April 2, 2026. RFC-0004 is structured to be
compliant with the NIST AI Risk Management Framework (Govern 1.6) and the EU AI Act data
requirements for high-risk systems.

---

## The regulation vocabulary

The `regulations` field uses a named vocabulary — GDPR, NIS2, DORA, MiFID2, HIPAA,
EU-AI-Act, SOC2, ISO27001, and others. Unknown values are silently ignored. Custom values
are permitted.

The intent is not to enumerate every possible regulation — it is to give compliance-aware
tooling a standardised signal it can act on without parsing free text. A tool that knows
`MiFID2` can apply MiFID2-specific rules without being told what MiFID2 requires.

---

## Open questions — your input matters

RFC-0004 is a Request for Comments. Three questions that need real-world feedback:

**Sensitivity level alignment.** The four levels (`public`, `internal`, `confidential`,
`restricted`) are intentionally aligned with common frameworks (ISO 27001, UK HMG) without
being locked to any one of them. Should they align explicitly with a specific standard? Or
does the current informal vocabulary serve a broader audience?

**`hard_requirement` scope.** Currently only `data_residency` has a `hard_requirement`
flag. Should other fields — regulations, restrictions — also support `hard_requirement`?
Or does this blur the advisory/normative boundary in ways that create false security?

**Per-unit content hashes.** `manifest_hash` covers the full manifest. Should there also
be per-unit hashes so agents can verify individual files without rehashing everything?

Comment on [Issue #5](https://github.com/Cantara/knowledge-context-protocol/issues/5)
(trust and audit) or [Issue #11](https://github.com/Cantara/knowledge-context-protocol/issues/11)
(compliance and data residency).

---

Full RFC: [RFC-0004-Trust-and-Compliance.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0004-Trust-and-Compliance.md)

Spec and all RFCs: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
