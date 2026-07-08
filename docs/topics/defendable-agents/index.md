---
title: "Defendable Agents"
description: "A field guide to defendable agents — AI agents whose every decision is declared in advance, reproducible, and evidenced. The argument, the architecture, the governance primitives, tutorials, worked examples, and compliance mapping."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Defendable Agents

**A defendable agent is one whose every decision can be defended — declared in advance, reproducible byte-for-byte, and backed by evidence you can put in front of an auditor, a regulator, or a board.** Not "the model seemed confident." A plan, a trace, a signed record.

Most agents being built today cannot do this, and it is not a policy gap — it is an architecture gap. When the model decides everything mid-flight — what to read, what to trust, what to spend — the result is unreproducible, unauditable, and injectable *by construction*. You cannot bolt governance onto improvisation after the fact.

This is a **field guide** to the alternative: determinism at the core, the model at the edge. It runs from the argument through the architecture, the governance primitives, hands-on tutorials, worked examples, and the compliance mapping — anchored throughout by an anonymised real-world system, *Lodestar*.

> The agentic web everyone is racing to build has a governance-shaped hole in it. Agents are about to read our regulations, spend our money, and brief our boards — and the dominant architecture cannot answer *"why did you do that?"* with anything better than a transcript. Improvisation doesn't testify well.

New here? Start with **[How to Read This Guide](/topics/defendable-agents/orientation/how-to-read/)**.

---

## Part I · The Argument

<div class="grid cards" markdown>
- :material-alert-circle-outline: **[The Governance Gap](/topics/defendable-agents/argument/the-governance-gap/)** — why you can't govern an improviser
- :material-scale-balance: **[What "Defendable" Means](/topics/defendable-agents/argument/what-defendable-means/)** — declared, reproducible, evidenced
- :material-target: **[Threat Model](/topics/defendable-agents/argument/threat-model/)** — the failures this defends against
- :material-function-variant: **[Determinism vs Probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/)** — where each belongs
- :material-shield-off-outline: **[Why Bolt-On Guardrails Fail](/topics/defendable-agents/argument/why-guardrails-fail/)** — the arms race you lose slowly
</div>

## Part II · Reference Architecture

<div class="grid cards" markdown>
- :material-sitemap-outline: **[The Inversion](/topics/defendable-agents/architecture/overview/)** — determinism at the core
- :material-cog-outline: **[The Deterministic Planner](/topics/defendable-agents/architecture/deterministic-planner/)**
- :material-shield-check-outline: **[The Governance Harness](/topics/defendable-agents/architecture/governance-harness/)**
- :material-robot-outline: **[Where the Model Lives](/topics/defendable-agents/architecture/model-at-the-edge/)**
- :material-transit-connection-variant: **[From Task to Evidence](/topics/defendable-agents/architecture/data-flow/)**
- :material-lock-outline: **[Fail-Closed Behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/)**
</div>

## Part III · Governance Primitives

<div class="grid cards" markdown>
- :material-view-grid-outline: **[The Primitives](/topics/defendable-agents/primitives/overview/)** — at a glance
- :material-lock-check-outline: **[Fail-Closed Policy](/topics/defendable-agents/primitives/fail-closed-policy/)**
- :material-notebook-outline: **[The Append-Only Audit Trail](/topics/defendable-agents/primitives/audit-trail/)**
- :material-file-tree-outline: **[Decision Traces](/topics/defendable-agents/primitives/decision-traces/)**
- :material-cash-multiple: **[Budget & Bounding](/topics/defendable-agents/primitives/budget-and-bounding/)**
- :material-clock-outline: **[Temporal Pinning](/topics/defendable-agents/primitives/temporal-pinning/)**
- :material-trending-down: **[Drift Detection](/topics/defendable-agents/primitives/drift-detection/)**
- :material-certificate-outline: **[Trust & Attestation](/topics/defendable-agents/primitives/trust-and-attestation/)**
- :material-account-multiple-outline: **[Multi-Tenancy & Isolation](/topics/defendable-agents/primitives/multi-tenancy/)**
</div>

## Part IV · Deterministic Decisions

<div class="grid cards" markdown>
- :material-numeric: **[Anatomy of a Defensible Score](/topics/defendable-agents/decisions/anatomy-of-a-score/)**
- :material-file-document-outline: **[The Scoring-Model Manifest](/topics/defendable-agents/decisions/scoring-model-manifest/)**
- :material-layers-outline: **[Layers, Weights & Bands](/topics/defendable-agents/decisions/layers-weights-bands/)**
- :material-tune: **[Designing 1–5 Variables](/topics/defendable-agents/decisions/variable-design/)**
- :material-repeat: **[Reproducibility Guarantees](/topics/defendable-agents/decisions/reproducibility/)**
- :material-source-branch: **[Versioning Decision Models](/topics/defendable-agents/decisions/versioning-models/)**
</div>

## Part V · KCP Integration

<div class="grid cards" markdown>
- :material-map-outline: **[The KCP Manifest](/topics/defendable-agents/kcp/manifest-basics/)**
- :material-format-list-checks: **[Declaring Governed Units](/topics/defendable-agents/kcp/declaring-governed-units/)**
- :material-connection: **[Wiring kcp-agent as MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/)**
- :material-share-variant-outline: **[Federation & Dogfooding](/topics/defendable-agents/kcp/federation-and-dogfood/)**
</div>

## Part VI · Tutorials — build one end to end

<div class="grid cards" markdown>
- :material-folder-outline: **[0 · Project Layout](/topics/defendable-agents/tutorials/00-project-layout/)**
- :material-shield-edit-outline: **[1 · Your First harness.yaml](/topics/defendable-agents/tutorials/01-first-harness/)**
- :material-calculator-variant-outline: **[2 · A Deterministic Scoring Model](/topics/defendable-agents/tutorials/02-scoring-model/)**
- :material-console-line: **[3 · The Governed Session](/topics/defendable-agents/tutorials/03-governed-session/)**
- :material-notebook-edit-outline: **[4 · The Append-Only Audit Log](/topics/defendable-agents/tutorials/04-audit-log/)**
- :material-cash-lock: **[5 · Enforcing a Budget Ceiling](/topics/defendable-agents/tutorials/05-budget-ceiling/)**
- :material-clock-alert-outline: **[6 · Temporal Pinning & a Drift Report](/topics/defendable-agents/tutorials/06-temporal-drift/)**
- :material-account-lock-outline: **[7 · Multi-Tenant Isolation](/topics/defendable-agents/tutorials/07-multi-tenant/)**
- :material-export-variant: **[8 · Exporting Evidence for an Auditor](/topics/defendable-agents/tutorials/08-evidence-export/)**
</div>

## Part VII · Worked Examples

<div class="grid cards" markdown>
- :material-chart-line: **[A Buyer-Scoring Pipeline](/topics/defendable-agents/examples/buyer-scoring-pipeline/)**
- :material-cash-check: **[A Spend-Approval Agent](/topics/defendable-agents/examples/spend-approval-agent/)**
- :material-gavel: **[A Regulatory Q&A Agent](/topics/defendable-agents/examples/regulatory-qa-provenance/)**
- :material-history: **[Reproducing a Decision](/topics/defendable-agents/examples/reproduce-a-decision/)**
- :material-shield-bug-outline: **[Catching an Injection at the Gate](/topics/defendable-agents/examples/catch-an-injection/)**
- :material-account-check-outline: **[A Compliant Screening Agent](/topics/defendable-agents/examples/compliant-screening-agent/)**
</div>

## Part VIII · Compliance & Assurance

<div class="grid cards" markdown>
- :material-clipboard-check-outline: **[Control Mapping: SOC 2 / ISO 27001 / GDPR](/topics/defendable-agents/compliance/control-mapping/)**
- :material-package-variant-closed: **[Auditor Evidence Packages](/topics/defendable-agents/compliance/evidence-packages/)**
- :material-test-tube: **[Verifying Defendability](/topics/defendable-agents/compliance/verifying-defendability/)**
- :material-wrench-clock-outline: **[Operating & Maintaining One](/topics/defendable-agents/compliance/operating-and-maintenance/)**
</div>

## Part IX · Case Study & Reference

<div class="grid cards" markdown>
- :material-compass-outline: **[Case Study: Lodestar](/topics/defendable-agents/reference/case-study-lodestar/)**
- :material-toolbox-outline: **[Starter Kit & Reference Configs](/topics/defendable-agents/reference/starter-kit/)**
- :material-alert-outline: **[Anti-Patterns & Pitfalls](/topics/defendable-agents/reference/anti-patterns/)**
- :material-help-circle-outline: **[FAQ](/topics/defendable-agents/reference/faq/)**
</div>

---

## Where this sits

Defendable agents are what you get when you point the [Knowledge Context Protocol](/topics/knowledge-context-protocol/) at a governance problem instead of a discovery problem. The same substrate that makes knowledge *navigable* is what makes an agent's decisions *defensible* — and the same encoded expertise that makes an organisation resilient ([Skill-Driven Development](/topics/skill-driven-development/)) is also its audit trail. **Compound and defendable are the same infrastructure seen from two angles.**

This guide is itself published as KCP-navigable knowledge — an agent can discover every page through [the site's root manifest](/knowledge.yaml). We build what we describe.

*The thesis in narrative form is on the [blog](/blog/); this is the reference.*
