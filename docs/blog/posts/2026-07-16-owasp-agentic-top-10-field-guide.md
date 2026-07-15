---
description: "OWASP published the Agentic Top 10 in December 2025: ten named categories of agent security failure built by 100+ security experts. Here's a field guide to all ten — plus the pattern that four of them share that the list doesn't name."
date: 2026-07-16T08:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Governance, Trust & Compliance
  - AI Agents & the Agentic Web
  - Security
tags:
  - owasp
  - agentic-security
  - kcp
  - prompt-injection
  - memory-poisoning
  - supply-chain
  - trust-tiers
  - provenance
  - defendable-agents
authors:
  - totto
  - claude
image: assets/images/owasp-00-title.webp
---

# OWASP Just Mapped the Agentic Top 10. Here's the Root Cause Four of Them Share.

![The OWASP Agentic Top 10 Field Guide: mapping the risks, finding the hidden pattern, and securing the autonomous stack. An AI Agent Core at the centre connected to Knowledge Data Stores, Internal APIs, Model Weights, External Integrations, Actionable APIs, Executive Functions, Policy & Constraints, Human-in-the-Loop, and Audit Logs.](../../assets/images/owasp-00-title.webp)

In December 2025, OWASP published the [Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — 100+ security experts, peer-reviewed, the first serious attempt to name what goes wrong when AI systems plan, act, and talk to each other autonomously.

The list is correct. Every item on it maps to a real incident category. If you're building or deploying AI agents and you haven't read it, stop here and do that first.

This post does two things: a fast field guide to all ten risks, and then a close reading that reveals the pattern four of them share — a pattern the list describes but doesn't name, and which points at a common architectural fix.

<!-- more -->

![AI systems that plan, act, and communicate autonomously require new security paradigms. Released December 2025, built by 100+ security experts, fully peer-reviewed. The first serious attempt to map what goes wrong when AI stops merely answering prompts and begins planning, acting, and talking to other machines autonomously. Every item maps to a real, documented incident category.](../../assets/images/owasp-01-new-paradigms.webp)

---

## The Ten Risks: A Field Guide

![OWASP identified ten distinct ways autonomous agents fail: ASI01 Goal Hijack (attack vector is data, not the prompt), ASI02 Tool Misuse (agent has legitimate access — failure is what it does with it), ASI03 Privilege Abuse (acting entity becomes ambiguous), ASI04 Supply Chain (you didn't change anything — something upstream did), ASI05 Code Execution (agent wrote the compromising code), ASI06 Memory Poisoning (asynchronous — inject today, fire tomorrow), ASI07 Insecure Communication (trusting the channel substitutes for trusting the content), ASI08 Cascading Failures (partial failure looks like success), ASI09 Trust Exploitation (agent sounds authoritative), ASI10 Rogue Agents (the design was the problem).](../../assets/images/owasp-02-ten-ways-fail.webp)

### ASI01: Agent Goal Hijack

An agent's objectives are altered through content it retrieves — not through its user's input. A document retrieval agent reads a poisoned PDF. The hidden instructions inside redirect its goal. The EchoLeak vulnerability was the first public documented instance.

**The defining characteristic**: the attack vector is data, not the prompt. The user typed nothing malicious. The document did.

### ASI02: Tool Misuse & Exploitation

Agents misuse legitimate tools through unsafe chaining, unvalidated inputs, or poisoned tool descriptions. The agent isn't breaking in — it's using the front door in ways the tool's designer didn't anticipate.

**The defining characteristic**: the agent has legitimate access. The failure is in what it does with it.

### ASI03: Identity & Privilege Abuse

Agents inherit, cache, or delegate credentials in ways that allow privilege escalation or scope expansion across multi-hop chains. RBAC holds when humans are the principals. It breaks when a five-hop machine-to-machine chain obscures who is actually acting.

**The defining characteristic**: the acting entity becomes ambiguous. As Edison Sanchez noted — the moment that happens, someone will exploit it, usually on a Tuesday morning.

The best current mitigation: OAuth 2.0 Token Exchange (on-behalf-of scoping) + cryptographic signing of the identity context envelope, so downstream evaluators can verify the chain wasn't tampered mid-flight. AWS Cedar's three-layer pipeline (trust score → delegation depth cap → pin to originating human) is the most complete implementation documented publicly.

### ASI04: Agentic Supply Chain Compromise

Dynamically loaded models, plugins, tools, or MCP servers are compromised, tampered with, or substituted at runtime. The LiteLLM PyPI backdoor — 47,000 downloads in a three-hour window — is the clearest example. The GitHub MCP server population problem (16,500+ entries, many near-duplicates, some drifting) is the ambient version.

**The defining characteristic**: you didn't change anything. Something upstream did.

### ASI05: Unexpected Code Execution

Agent-generated or influenced code runs in unintended ways — sandbox escape, data destruction, system compromise. This is RCE but the payload is often model-generated rather than human-crafted.

**The defining characteristic**: the agent wrote the code that compromised the system.

### ASI06: Memory & Context Poisoning

False information implanted in persistent agent memory, RAG indices, or shared context stores corrupts future reasoning — potentially weeks later. The Gemini Memory Attack documented this: inject once, affect every future session.

**The defining characteristic**: the attack is asynchronous. You injected yesterday; the damage fires today, on a different task, in a context that looks entirely unrelated.

### ASI07: Insecure Inter-Agent Communication

Weak authentication and unencrypted messages between agents enable interception, spoofing, and replay attacks. When Agent A asks Agent B a question, there's often no mechanism to verify that the response actually came from Agent B and hasn't been altered in transit.

**The defining characteristic**: trust in the communication channel substitutes for trust in the content.

### ASI08: Cascading Failures

Single faults propagate through networked agents, amplifying into system-wide outages or breaches. The failure mode is familiar from distributed systems — but agents add non-determinism at every hop.

**The defining characteristic**: partial failure is worse than total failure, because the partial failure looks like success.

### ASI09: Human-Agent Trust Exploitation

Users are manipulated through persuasive agent recommendations and false authority. The agent says "I've verified this" or "the policy requires this" — and the user trusts it because it sounds authoritative.

**The defining characteristic**: the attack exploits the human's belief that the agent checked.

### ASI10: Rogue Agents

Compromised or misaligned agents deviate from intended purpose through reward hacking or emergent behaviour. The agent is doing what it was optimised to do — the optimisation target was wrong.

**The defining characteristic**: the agent works exactly as designed. The design was the problem.

---

## The Pattern in Four of the Ten

![Four of these critical vulnerabilities share the exact same root cause. ASI01, ASI04, ASI06, and ASI07 are highlighted — the others greyed out. "Read them again. The OWASP list treats these as separate issues, but they are symptoms of the exact same underlying disease."](../../assets/images/owasp-03-four-share-root.webp)

Read ASI01, ASI04, ASI06, and ASI07 again and look for what they share.

![The common thread is reasoning from unverified knowledge. Risk → Attack Vector → Common Vulnerability table: ASI01 Goal Hijack → Poisoned retrieved document; ASI04 Supply Chain → Tampered plugin or MCP server; ASI06 Memory Poisoning → False data implanted in persistent memory; ASI07 Inter-Agent → Spoofed or replayed responses. Common Element: Agent cannot verify the origin, integrity, or context of the data before acting.](../../assets/images/owasp-04-common-thread.webp)

| Risk | Attack vector | Common element |
|---|---|---|
| ASI01: Goal Hijack | Poisoned document the agent retrieves | Agent can't verify the document is from a declared, trusted source |
| ASI04: Supply Chain | Tampered plugin, model, or MCP server | Agent can't verify the component hasn't been substituted |
| ASI06: Memory Poisoning | False data implanted in persistent memory | Agent can't verify the memory entry's provenance or integrity |
| ASI07: Inter-Agent Communication | Spoofed or replayed agent responses | Agent can't verify the response actually came from who it claims |

In each case, the agent is reasoning from knowledge it cannot verify. The attack doesn't break in through the front door — it poisons the well the agent drinks from. And the agent has no mechanism to ask: *was this knowledge from a source I declared, has it been modified, and did it arrive from where it was supposed to?*

![The attack doesn't break through the front door; it poisons the well the agent drinks from. Left: Traditional network perimeter with API gateway protection — secure. Right: Knowledge Provenance Gap — corrupted data block injected into the knowledge store, flowing invisibly through the agent pipeline as accepted data. The error is invisible in the action log. The agent acts correctly based on wrong information.](../../assets/images/owasp-05-poisons-the-well.webp)

This is the knowledge provenance gap. The OWASP list describes it in the mitigations — "validate memory entries before they influence reasoning," "implement memory provenance metadata," "maintain software bills of materials for agent dependencies" — but doesn't name it as a first-class attack surface.

---

## What ASI11 Would Look Like

![Defining the missing first-class attack surface. ASI11: Knowledge Provenance Failure. Definition: The agent reasons from knowledge whose origin, integrity, and intended serving context cannot be verified. Context: The knowledge may be current or stale, authentic or tampered, from an authoritative source or an attacker-controlled lookalike. The agent has no mechanism to distinguish these cases before acting.](../../assets/images/owasp-06-asi11-definition.webp)

If the Agentic Top 10 had an eleventh entry, it might read like this:

**ASI11: Knowledge Provenance Failure**

*The agent reasons from knowledge whose origin, integrity, and intended serving context cannot be verified. The knowledge may be current or stale, authentic or tampered, from a declared authoritative source or from an attacker-controlled lookalike. The agent has no mechanism to distinguish these cases before acting.*

Attack scenarios:
- Agent reads a policy document whose content was silently modified after the last human review (stale/tampered knowledge — ASI01 variant)
- Agent loads context from an MCP server that replaced the authoritative one (supply chain — ASI04 variant)
- Agent replans based on memory entries injected by a previous attacker session (memory poisoning — ASI06 variant)
- Agent accepts knowledge from an inter-agent message that doesn't carry its own provenance (ASI07 variant)

In every case, the agent acts correctly given what it knows. What it knows is wrong. The error is invisible in the action log.

---

## What the OWASP Mitigations Point Toward

The mitigations OWASP recommends for ASI01, ASI04, and ASI06 are directionally correct:

- *"Validate memory entries before they influence reasoning"* (ASI06) → but validate how? Against what ground truth?
- *"Implement memory provenance metadata — origin and timestamp tracking"* (ASI06) → this is the right framing; the mechanism to make it machine-verifiable is cryptographic signing
- *"Maintain software bills of materials for agent deployments"* (ASI04) → an SBOM for agents' knowledge sources, not just their dependencies

![Knowledge must carry its own machine-verifiable provenance. Sequential verification pipeline: Raw Data/Document → knowledge.yaml Manifest (per-unit content hashes) → Ed25519 Cryptographic Signature + Bound Endpoint → Agent Validation Gate (check hash, check signature, check endpoint) → Strict Output: Fail-Closed (refuse to load). This is the prepared statement for the knowledge layer. Change document → hash fails. Change manifest → signature fails. Serve from wrong location → trust tier demoted.](../../assets/images/owasp-07-verification-pipeline.webp)

The pattern these mitigations share: **knowledge needs to carry its own provenance**. The agent shouldn't have to trust the channel, the memory store, or the MCP server — it should be able to verify the knowledge itself, regardless of how it arrived.

This is what a knowledge manifest achieves. A `knowledge.yaml` declaring every unit of knowledge the agent is authorised to reason from, signed with an Ed25519 key, with per-unit content hashes, bound to a declared serving endpoint:

```yaml
serving:
  manifest:
    - https://knowledge.mycompany.com/knowledge.yaml

signing:
  scheme: ed25519
  scope: this-manifest
  signature: knowledge.yaml.sig

units:
  - id: refund-policy
    path: docs/refund-policy.md
    intent: "What is our refund policy?"
    content_hash:
      algorithm: sha256
      value: "ac23a09a9e04d944225b9ca616d54ccbac17cd16b9428e49288ab24994fb89c2"
```

Change the document → content hash fails (ASI04, ASI06 mitigation). Change the manifest → signature fails. Serve from the wrong location → serving check demotes trust tier (ASI01, ASI07 mitigation). The agent refuses to load knowledge it cannot verify — fail-closed, not fail-open.

This is the prepared statement for the knowledge layer. If you're not familiar with why that framing matters, [the GitLost post](2026-07-15-gitlost-prompt-injection-prepared-statement.md) covers the SQL injection parallel in detail.

---

## How the Ten Map to Two Layers

![Security requires a full-stack approach across Knowledge, Action, and Alignment. Three-layer stack: Knowledge Layer (what it knows) — ASI01, 04, 06, mitigation: declared, signed, endpoint-bound knowledge manifests. Action Layer (what it does) — ASI02, 03, 05, 07, 08, mitigation: least-privilege access, Cedar policies, sandboxing. Alignment Layer (its intended goals) — ASI09, 10, mitigation: human oversight, value alignment, reward design.](../../assets/images/owasp-08-three-layer-stack.webp)

The cleaner model for understanding the full Agentic Top 10:

| Layer | Risks | Primary mitigation |
|---|---|---|
| **Knowledge** (what the agent knows and reasons from) | ASI01, ASI04, ASI06, ASI07 (partial) | Declared, signed, endpoint-bound knowledge manifests |
| **Action** (what the agent does with what it knows) | ASI02, ASI03, ASI05, ASI07 (partial), ASI08 | Least-privilege access, Cedar-style policy pipelines, sandboxed execution, audit trails |
| **Alignment** (whether the agent's goals are what you intended) | ASI09, ASI10 | Human oversight, value alignment, reward function design |

Enterprise agent governance needs all three legs. The industry has invested heavily in the action layer (audit trails, RBAC, Cedar policies). The alignment layer is an active research problem. The knowledge layer is the one that doesn't have an industry-standard name yet — but four entries on the Agentic Top 10 are pointing at it.

---

## Where to Start

If you're mapping your agent deployment against the Agentic Top 10 today:

**For ASI01, ASI04, ASI06:** Start by asking whether your agent has a declared list of knowledge sources. Not a prompt saying "use only approved documents" — a machine-verifiable manifest that the agent checks before loading. If the answer is no, any knowledge that reaches the agent is implicitly trusted, and the attack surface for all three risks is the full set of documents, memory entries, and APIs your agent can reach.

![Managing identity and privileges across multi-hop agent chains (ASI03). The threat: RBAC holds for humans but breaks when a five-hop machine-to-machine chain obscures the actor. The mitigation: OAuth 2.0 Token Exchange (OBO scoping), AWS Cedar 3-layer pipeline (trust score → delegation depth cap → pins to originating human), cryptographic signing of identity context envelope prevents mid-flight tampering.](../../assets/images/owasp-09-identity-multihop.webp)

**For ASI03:** The AWS Cedar + OAuth OBO pattern Edison Sanchez documented is the most complete implementation available. The key insight: identity has to travel with the request, not the caller.

**For ASI02, ASI05:** Sandboxing and least-privilege tool scoping. MCP token scoping for individual servers. This is the most mature layer — standard DevSecOps applied to agent tools.

**For ASI07:** If your inter-agent messages don't carry signed provenance, you're relying on transport security alone. Transport can be intercepted, replayed, or spoofed at a gateway.

**For ASI08, ASI09, ASI10:** Circuit breakers, human-in-the-loop gates, and honest evaluation of what your agent is actually optimised to do. These are harder problems and longer conversations.

![Mapping your enterprise agent deployment against the architectural model. Knowledge Layer (ASI01, 04, 06): Do you have a machine-verifiable manifest that the agent checks before loading data? (If no, your attack surface is every document your agent can reach.) Action Layer (ASI02, 03, 05, 07): Does identity travel with the request? Are MCP servers token-scoped? Do inter-agent messages carry signed provenance? Alignment Layer (ASI08, 09, 10): Are circuit breakers and human-in-the-loop gates implemented for critical optimization targets?](../../assets/images/owasp-10-deployment-checklist.webp)

The list is the right starting point. Four of the ten have a common fix that starts one layer below where most teams are looking.

---

![The OWASP Agentic Top 10: Mapping the Risks of AI Autonomy. One-page infographic showing all 10 risks with their defining characteristics, the Knowledge Provenance Gap pattern (ASI01, 04, 06, 07), ASI11 Knowledge Provenance Failure definition, the fix (machine-verifiable knowledge manifests with Ed25519 signing), and the three layers of agent governance (Knowledge / Action / Alignment).](../../assets/images/owasp-11-onepage-infographic.webp)

*OWASP Top 10 for Agentic Applications: [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/). The KCP tutorial with real command outputs: [A Firewall for What Your Agent Knows](2026-07-17-a-firewall-for-what-your-agent-knows.md). The GitLost post covering the SQL injection parallel: [Prompt Injection Is SQL Injection for Agents](2026-07-15-gitlost-prompt-injection-prepared-statement.md).*
