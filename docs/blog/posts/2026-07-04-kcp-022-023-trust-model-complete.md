---
description: "The agentic web has no login page — so the only knowledge agents can consume is what publishers give away. KCP v0.22 and v0.23 add the missing half of the trust model: who may consume knowledge, and how they prove it."
date: 2026-07-04
series: "Knowledge Context Protocol"
categories:
  - Knowledge Context Protocol
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
tags:
  - kcp
  - trust
  - attestation
  - auth
  - did
  - ai-agents
  - agentic-web
  - open-source
  - knowledge-context-protocol
authors:
  - totto
  - claude
image: assets/images/kcp-022-023-01-missing-machinery.webp
---

# The Agentic Web Has No Login Page

Think about what makes the human web economically viable. Not the browser. Not HTML. It's the login page — and everything it implies. Paywalls, licenses, subscriptions, terms of access. The mundane machinery that lets someone publish valuable knowledge *without giving it away*. Remove that machinery and the web would contain only what people are willing to publish for free.

Now look at the agentic web. Agents consume knowledge from manifests, MCP servers, and context files across organisational boundaries — and there is no equivalent machinery. A knowledge source is either open to every agent that finds it, or it's locked behind a bespoke API that no standard agent can negotiate. Nothing in between. No standard way for a publisher to say *"this knowledge is for certified consumers only — prove who you are."*

The consequence is quiet but enormous: the knowledge layer of the agentic web contains only what publishers are willing to give away. Authoritative sources — legal data providers, regulatory interpreters, standards bodies, paid research — stay off it entirely. So agents answer compliance questions from scraped blog posts instead of authoritative guidance, because the authoritative guidance has no way to come online on terms its publisher can accept.

KCP v0.22 and v0.23, both shipping today, are the missing machinery.

<!-- more -->

![The missing economic machinery: the human web runs on logins, paywalls, licenses and subscriptions — the mundane infrastructure that lets publishers share valuable knowledge without giving it away. The agentic web has no equivalent: a knowledge source is either open to every agent or locked behind a bespoke API, so its knowledge layer contains only what publishers are willing to publish for free.](../../assets/images/kcp-022-023-01-missing-machinery.webp)

---

## Two questions, only one answered

The Knowledge Context Protocol has spent seven releases building a trust model for knowledge that agents load into context. v0.16 introduced signed manifests. v0.18 locked ingestion down with the trusted render pipeline. v0.19–v0.20 made knowledge expire — temporal validity, so agents stop acting on superseded guidance. v0.21 closed the composition and federation attack surfaces.

All of that answers one question: **is this knowledge what it claims to be?** Producer-side trust. The publisher signs, hashes, and dates the knowledge; the consumer verifies.

But there was a second question the protocol declared and never enforced: **who is allowed to receive it?**

A KCP manifest could always mark units `access: restricted`. The semantics were clear — this content is for authorised consumers. The enforcement was nonexistent. Who counts as authorised, how they prove it, what happens when they don't: unspecified. The field was a wish.

![Two questions of trust: producer-side trust — "is this knowledge what it claims to be?" — was answered across v0.16–v0.21 with signed manifests, the trusted render pipeline, content hashes and temporal validity. Consumer-side trust — "who is allowed to receive it?" — was declared via access: restricted but never enforced. One question answered, one a wish.](../../assets/images/kcp-022-023-02-two-questions.webp)

Here's what that looked like in practice.

---

## A scenario

A European MSP runs a compliance agent. Its job: verify whether a customer's data handling satisfies GDPR Article 5's data minimisation principle. The knowledge source is a KCP manifest from a legal data provider — authoritative, maintained interpretations of GDPR obligations. The provider's business is selling exactly this knowledge to certified compliance firms.

Some units are marked `access: restricted`. The publisher declared their intent. Before v0.22, that intent did nothing.

The bridge served restricted units like any others. An uncertified agent, a hobbyist, a competitor scraping the corpus — all got the same content as a paying, audited firm. The publisher had two options: publish and lose control, or stay off the agentic web. Most choose the second. That's the impoverished knowledge layer, one publisher at a time.

**Same scenario under v0.22.**

The agent queries `search_knowledge`. Restricted units come back in the results — but flagged `requires_attestation: true`, with the publisher's declared trusted providers. The agent calls `get_unit`. The bridge answers `attestation_required`: not an error, a gate. *Here are the identity providers we trust. Here is where you obtain a credential. Prove who you are.*

The agent authenticates with the provider — in this MSP's case, using its SPIFFE workload identity — and receives a signed credential. It presents that credential in the `attestation` argument on the next call. Content served.

**And under v0.23**, after serving the unit, the source issues a signed receipt: unit id, timestamp, the presented agent identity. The agent attaches it to the customer's compliance record. When an auditor reviews that record, they don't see "the agent consulted some GDPR guidance." They see a cryptographic receipt from the knowledge source itself proving which unit was served, when, and to whom.

![The GDPR compliance scenario in three acts: before v0.22, restricted units from the legal data provider are served to any agent that asks — certified firm, hobbyist and scraper alike. Under v0.22, the bridge answers attestation_required, the agent authenticates with its SPIFFE workload identity and presents the signed credential. Under v0.23, the source issues a signed access receipt the agent attaches to the customer's compliance record.](../../assets/images/kcp-022-023-04-gdpr-scenario.webp)

The `access: restricted` declaration now has teeth at three levels: the spec declares the contract, the bridge gates delivery, and the receipt proves the exchange happened.

---

## The mechanism: `trust.agent_requirements`

The core v0.22 addition is one block:

```yaml
trust:
  agent_requirements:
    require_attestation: true
    trusted_providers:
      - "https://auth.example.com"
    attestation_url: "https://auth.example.com/attest"
    attestation_jwks: "https://auth.example.com/.well-known/jwks.json"
    propagate_to_governed: true
```

This declares what an agent must prove about *itself* before a source serves restricted content — the consumer counterpart to `content_integrity`, which authenticates the producer. `trusted_providers` names the accepted identity providers. `attestation_url` is where an agent obtains a credential. The `jwks` URL describes what a valid credential looks like.

![The core mechanism: trust.agent_requirements is the consumer counterpart to content_integrity. require_attestation switches on the gate, trusted_providers names the accepted identity providers, attestation_url is where an agent obtains a credential, attestation_jwks describes what a valid credential looks like, and propagate_to_governed makes the requirement a floor for every governed source.](../../assets/images/kcp-022-023-05-agent-requirements.webp)

The critical design decision is what the spec does *not* do.

---

## Declare, never perform

KCP's load-bearing principle has always been: a manifest is data, never instructions. A manifest may influence what an agent *knows*, never what it *does*. v0.22 extends that principle into auth territory, where the temptation to violate it is strongest.

![The passive data doctrine extended into auth: a manifest is data, never instructions — it may influence what an agent knows, never what it does. A protocol that declared auth requirements and also performed auth would make every manifest a potential trigger for network calls to attacker-controlled URLs. KCP declares; it never performs.](../../assets/images/kcp-022-023-06-passive-data-doctrine.webp)

**The renderer never authenticates.** `kcp render` surfaces `agent_requirements` as data and marks restricted units `requires_attestation: true` — a flag, not a gate. It never dereferences `attestation_url`. The render pipeline is deterministic, network-free, LLM-free (conformance rules C1 and C7), and adding a live auth call would destroy those guarantees. The renderer can't attest on an agent's behalf, so it doesn't pretend to.

**The bridge gates, but never verifies.** Bridges are live MCP servers with a real client on the other end — they *can* gate delivery, and conformance rule C20 now says they must, on every retrieval path: `get_unit`, `read_resource`, `list_resources`. But the bridge checks that a credential is *presented*; it never calls the identity provider to verify one. Verification is between the agent and the IdP.

**Agents attest.** The party with the identity does the proving.

![Three layers, three jobs, no leakage: the renderer declares — surfaces agent_requirements as data and flags restricted units, never dereferencing attestation_url (conformance rules C1/C7 keep it deterministic, network-free, LLM-free). The bridge gates — conformance rule C20 blocks restricted content on every retrieval path until a credential is presented, but never calls the identity provider to verify it. The agent attests — verification happens between the agent and its IdP.](../../assets/images/kcp-022-023-07-three-layers.webp)

Three layers, three jobs, no leakage between them. This is the same discipline that kept KCP out of the [TrustFall class of vulnerabilities](2026-05-08-trustfall-and-why-kcp-is-passive-data.md) — config files that quietly became execution vectors because one layer took on another layer's job. A protocol that *declared* auth requirements and also *performed* auth would be a protocol whose manifests can trigger network calls to attacker-controlled URLs. KCP declares. It never performs.

---

## Speaking the identity languages agents actually use

Access control is only useful if agents can present identities they actually have. v0.22 promoted four additional `auth.methods` types into the spec:

| Type | What it means |
|------|--------------|
| `bearer_token` | Opaque bearer token — the simplest thing that works |
| `spiffe` | SPIFFE/SPIRE workload identity — the agent presents an SVID |
| `did` | W3C Decentralized Identifier authentication |
| `http_signature` | HTTP Message Signatures per [RFC 9421](https://datatracker.ietf.org/doc/html/rfc9421) — the mechanism Visa TAP and Mastercard Agent Pay use |

These join `api_key`, `oauth2`, and `oidc`. The range matters: from a hobbyist's API token, through zero-trust service-fleet identity, to the payment networks' agent authentication schemes. When the payment industry and a knowledge protocol converge on the same identity standards, agents can carry one identity across both — which is precisely what a functioning agentic economy requires.

![Speaking the identity languages agents actually use: bearer_token for the simplest thing that works, spiffe for zero-trust workload identity across service fleets, did for W3C decentralized sovereign identity, and http_signature per RFC 9421 — the same mechanism Visa TAP and Mastercard Agent Pay use for agent authentication. One identity, carried across knowledge and payment networks alike.](../../assets/images/kcp-022-023-08-identity-languages.webp)

And `propagate_to_governed` closes a long-open gap (#47): a governing manifest's attestation requirements become a floor for every source it governs. A regulator's hub manifest can require attestation once, and every federated corpus under it inherits the requirement. One policy, no per-source repetition.

---

## v0.23: the completion pass

v0.23 shipped the same day. No new gates, no new conformance rules — the enforcement was v0.22's job. This is the release that finishes the declarations and reconciles the paperwork.

![The v0.23 completion pass: per-unit auth overrides for multi-tenant sources, access receipts declared via trust.audit, publisher DIDs for cryptographically resolvable publisher identity, the require_delegation_proof field found and implemented, and an RFC drift audit that corrected the spec's own paperwork.](../../assets/images/kcp-022-023-09-completion-pass.webp)

**Per-unit `auth` override.** A unit can override the root auth method — multi-tenant sources with genuinely different access regimes per unit no longer need separate manifests.

**Access receipts.** `trust.audit.provides_access_receipts` declares the source issues verifiable receipts (`jws`, `vc`, or a spec URL) after serving restricted content. A capability of the source, not a requirement on the agent. This is what made the audit trail in the scenario above verifiable — not a log entry the agent wrote about itself, but signed proof from the knowledge source. For compliance chains, that distinction is everything.

![Anatomy of an access receipt: unit id, timestamp and the presented agent identity, signed by the knowledge source itself. Not a log entry the agent wrote about itself — cryptographic proof from the source of which unit was served, when, and to whom. The difference between "the agent consulted some guidance" and evidence an auditor can verify.](../../assets/images/kcp-022-023-10-access-receipt.webp)

**Publisher DID.** `trust.provenance.publisher_did` adds a cryptographically resolvable W3C DID alongside the human-readable `publisher` string. You can now verify that the entity behind a manifest controls the corresponding key pair — publisher identity at the same evidential level as content integrity.

**`require_delegation_proof`.** Existed in the delegation block's examples, missing from the field-reference table and every parser. Found, documented, implemented.

**RFC drift audit.** The pass also caught spec-vs-RFC drift: per-unit `delegation` and per-unit `compliance` had already been promoted into the spec in earlier releases, but the RFC headers still marked them pending. Corrected. Unglamorous work — and exactly the kind a protocol should do before declaring a story complete, because a spec that misdescribes itself is its own category of trust failure.

---

## The full model, seven releases on

| Concern | Question answered | Shipped |
|---------|------------------|---------|
| Signed manifests | Who published this? | v0.16 |
| Trusted render pipeline | Can I ingest this safely? | v0.18 |
| Per-unit content hash | Is the content what was signed? | v0.18 |
| Temporal validity + `as_of` | Is this still true? Was it true then? | v0.19–0.20 |
| Composition integrity (C17) | Are the included sources authentic? | v0.21 |
| Federation temporal (C18) | Is this *source* still relevant? | v0.21 |
| Consumer attestation (C19–C21) | Who may consume this? | v0.22 |
| Extended auth methods | How do agents prove identity? | v0.22 |
| Access receipts | Can the exchange be proven later? | v0.23 |
| Publisher DID | Is publisher identity cryptographic? | v0.23 |

Producer side: done. Consumer side: done.

![Completing the KCP trust model, on one page: the evolution from producer-side trust (v0.16–v0.21) through consumer-side trust (v0.22) to the completion pass (v0.23); the three-layer gating mechanism — renderer declares, bridge gates, agent attests; the four identity languages agents actually speak; and what it unlocks — authoritative sources onboarding, verifiable compliance audits, automated terms of access.](../../assets/images/kcp-022-023-00-overview-infographic.webp)

---

## What this actually unlocks

The point of all this is not security theatre for YAML files. It's the precondition for a knowledge economy on the agentic web.

A publisher with valuable knowledge can now express, in a standard machine-readable form: *here is my knowledge, here is who may consume it, here is how you prove you qualify, and here is the receipt I'll issue when you do.* An agent encountering that source for the first time can negotiate access with no bespoke integration — the manifest tells it everything, including where to go for credentials.

That's the shape of a market: declared terms, provable identity, verifiable receipts. The human web needed all three before anyone would put valuable content on it. The agentic web is no different.

![The precondition for an agentic knowledge economy: a publisher declares terms in machine-readable form, an agent proves identity with a credential it already carries, and the exchange produces a verifiable receipt. Declared terms, provable identity, verifiable receipts — the same three things the human web needed before valuable content came online.](../../assets/images/kcp-022-023-12-knowledge-economy.webp)

If you run restricted units in production, note that v0.22's bridge update is a behaviour change: all three bridges (TypeScript, Python, Java) now enforce C20, and agents that don't present attestation get gated content on upgrade. If you publish knowledge you've been keeping off the agentic web because you couldn't control who consumed it — `trust.agent_requirements` is now the mechanism that changes the calculus.

The next question — how knowledge flows between organisations that independently attest, each trusting their own providers — is RFC-0011 territory. Already drafted.

![What to do now, and what comes next: bridge operators should note the C20 behaviour change — all three bridges now gate restricted units on upgrade. Publishers with knowledge kept off the agentic web can adopt trust.agent_requirements. And the next frontier — cross-organisational trust between independently attesting parties — is RFC-0011, already drafted.](../../assets/images/kcp-022-023-13-roadmap.webp)

*→ [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)*
