---
title: "Anti-Patterns & Pitfalls"
description: "The common ways teams build agents that only look defendable — reconstructed logs, a model in the scoring loop, mutable logs, classifier guardrails, missing pins, and weight-tuning to the answer."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# Anti-Patterns & Pitfalls

Most agents that fail an audit do not fail because someone was careless. They fail because a shortcut that felt reasonable at build time quietly removed the property that made the system defendable. The shortcut still runs. The demo still works. The gap only shows up when someone asks *why did it decide that, and can you prove it decided that way at the time?*

This page enumerates the anti-patterns I keep seeing, using the [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/) buyer-scoring stack — a deterministic engine scoring buyers in a regulated professional-services market — as the reference point. Each one comes with the fix.

## 1. Reconstructed logs

**The anti-pattern.** The agent does its work, and *afterwards* a separate routine writes a tidy log by re-reading the outputs. The log is a narrative assembled from results, not a record captured at the moment of decision. It reads well and it is fiction. If the scoring code changes between the decision and the reconstruction, the log describes a run that never happened.

**Why it is fatal.** A reconstructed log cannot show the inputs that were actually present, only what you can infer later. It has no independent value as evidence because the thing that produced it is the thing it is supposed to attest to.

**The fix.** Emit the audit event *inside* the governed operation, as a side effect of the decision itself, and make it append-only. In Lodestar every `buyer_scored` event carries the full variable trace at the instant of scoring — see [Audit Trail](/topics/defendable-agents/primitives/audit-trail/) and [Decision Traces](/topics/defendable-agents/primitives/decision-traces/).

```json
{
  "type": "buyer_scored",
  "sessionId": "sess_2026_07_08_a1",
  "sequence": 42,
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "b-8831", "name": "Buyer 8831" },
  "scoring": {
    "model": "buyer@2.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 }
    ],
    "layerScores": { "need": 78, "attractiveness": 61, "winnability": 70 },
    "total": 71,
    "band": "High"
  }
}
```

## 2. A model in the scoring loop

**The anti-pattern.** The composite score is produced by asking a language model to "weigh the factors and return a number". It feels flexible. It is not reproducible: the same buyer, scored twice, drifts.

**Why it is fatal.** You lose the one property that makes a decision defensible — that the same inputs yield the same output, every time, for anyone who re-runs it. See [Determinism vs Probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/).

**The fix.** Keep the model at the edge, never in the arithmetic. In Lodestar a layer score is the mean of its 1–5 variable scores times 20, and the BUYER score is a fixed weighted composite of three layers — Need 0.40, Attractiveness 0.25, Winnability 0.35 — computed by a pure function. The model may *propose* a variable score from unstructured signal; the composition is [Reproducible](/topics/defendable-agents/decisions/reproducibility/) code. See [Model at the Edge](/topics/defendable-agents/architecture/model-at-the-edge/).

> **Honest limit.** Determinism guarantees *process*, not *correctness*. If a variable is defined wrongly, the engine applies the mistake consistently — but visibly and reproducibly, which is exactly how you catch it. A model in the loop hides the mistake behind noise.

## 3. Editable, mutable logs

**The anti-pattern.** The audit log is a database row that can be updated, or a file the process rewrites. "We'll fix bad entries later." Once a record can be edited, none of the records can be trusted, because you can no longer prove any of them are original.

**The fix.** Append-only JSONL, one event per line, fsync on flush, monotonic sequence numbers per session. Never an update, never a delete. Corrections are *new* events (a `reanalysis_triggered` or `score_delta`) that reference the original. This is what satisfies ISO 27001 A.12.4 in the [control mapping](/topics/defendable-agents/compliance/control-mapping/) — and it is a directory-and-file discipline, not a policy note.

## 4. Classifier guardrails as the safety story

**The anti-pattern.** A prompt-injection classifier or a content filter sits in front of the agent and is treated as *the* control. When it passes, the agent runs with full authority.

**Why it is fatal.** A classifier is probabilistic; it fails open on the inputs it was not trained for, and an attacker only needs one. Guardrails describe intentions; they do not enforce boundaries. See [Why Guardrails Fail](/topics/defendable-agents/argument/why-guardrails-fail/).

**The fix.** Enforce at the harness, [fail-closed](/topics/defendable-agents/primitives/fail-closed-policy/): the agent can only touch declared domains, may only call `kcp_plan` and `kcp_load`, and every operation is charged against a budget ceiling that throws before it records. A classifier can still sit at the edge as defence in depth — it just is not the thing standing between the agent and your data.

```yaml
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000
  strict: true
  budget: { amount: 1000, currency: units }
  context_budget: 200000
```

> **Honest limit.** Fail-closed can be over-tuned into blocking legitimate work. If the ceiling or the domain list is too tight, real tasks stall. Governance is a dial you maintain, not a switch you flip once.

## 5. No temporal pin

**The anti-pattern.** A score is stored as a bare number with a timestamp of *when it was written*, not *what data it saw*. Months later nobody can tell whether it reflects current reality or a signal that decayed long ago — and in Lodestar signal freshness has a ~30-day half-life, so a stale score is not a rounding error, it is a different score.

**The fix.** Every score creates a pin — `{ scoredAt, dataAsOf, signalDates[], modelVersion, modelHash }` — and a [drift check](/topics/defendable-agents/primitives/drift-detection/) compares it against current state (DATA, MODEL, or TEMPORAL drift). See [Temporal Pinning](/topics/defendable-agents/primitives/temporal-pinning/).

> **Honest limit.** A pin detects staleness; it does not refresh the data. It tells you a decision is old, then you decide whether to reanalyze.

## 6. Weight-tuning to the answer

**The anti-pattern.** The stakeholder wanted a particular buyer to land in "Very high", so someone nudged the layer weights until it did. The engine is now a machine for producing the conclusion you already had.

**Why it is fatal.** Reproducibility is intact and worthless — you have made the model consistently confirm a bias, and the audit trail dutifully records it.

**The fix.** Treat weights and bands as versioned, declared artefacts governed as [KCP units](/topics/defendable-agents/kcp/declaring-governed-units/), changed through review with a rationale, never in-session to hit a target. See [Versioning Models](/topics/defendable-agents/decisions/versioning-models/) and [Layers, Weights & Bands](/topics/defendable-agents/decisions/layers-weights-bands/). A weight change should be a commit you can defend, not a knob you turned in a meeting.

---

The through-line: defendability is not something you add at the end, and it is not a feature you can demo. It is a set of properties — append-only capture, deterministic composition, temporal pinning, fail-closed enforcement, governed weights — that a shortcut removes silently. Governance is maintenance, not one-time setup. When in doubt, ask the audit question first: *if someone challenges this decision a year from now, what do I hand them?*
