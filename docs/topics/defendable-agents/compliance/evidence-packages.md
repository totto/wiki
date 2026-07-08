---
title: "Auditor Evidence Packages"
description: "How to assemble a self-contained evidence package an auditor can verify offline — decision traces, temporal pins, budget ledger, model versions, signatures, and a manifest."
image: assets/images/kcp-agent-020-07-governance-imperative.webp
---

# Auditor Evidence Packages

An auditor rarely gets — or wants — a login to your running system. What they want is a folder they can open on a laptop, in a room, with no network, and satisfy themselves that a particular decision was made the way you say it was. If your defence depends on someone re-running the live agent, you have no defence; the live agent has moved on. So the deliverable is not access. It is a **self-contained evidence package**: everything needed to understand and reproduce a decision, sealed and portable.

I have shipped these for the Lodestar system — a scoring engine for a regulated professional-services market, matching buyers to firms. The parts below are exactly what goes in the box.

## What goes in a package

A package is the intersection of what the [audit trail](/topics/defendable-agents/primitives/audit-trail/), the [decision traces](/topics/defendable-agents/primitives/decision-traces/), the budget ledger, and [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) already record. You are not generating new artefacts for the auditor; you are extracting and sealing the ones the [governed session](/topics/defendable-agents/architecture/governance-harness/) produced at decision time.

| Artefact | Source | What it proves |
|---|---|---|
| Session audit log (`.jsonl`) | Append-only log, fsync on flush | The sequence of events, actors, and justifications |
| Decision traces | `buyer_scored` / `match_scored` events | The 18 (or 21) variable inputs, layer scores, total, band |
| Temporal pins | Per-session pin map | `dataAsOf`, `signalDates[]`, `modelVersion`, `modelHash` at scoring time |
| Budget ledger | Session ledger entries | Every operation, its cost, and the running total against the ceiling |
| Model manifest + source | Governed KCP unit | The exact scoring model, versioned and hashed |
| Package manifest | Assembled at export | The index, hashes, and signature over everything above |

The decision trace is the load-bearing part. A [score is not a number](/topics/defendable-agents/decisions/anatomy-of-a-score/); it is a mean of 1-5 variable scores per [layer, times 20, then weighted](/topics/defendable-agents/decisions/layers-weights-bands/). If the trace carries all 18 Buyer variables and their layer scores, the auditor can recompute the total with a calculator. That is the point.

## The package manifest

The manifest is the first file an auditor opens. It names every artefact, pins the model, and carries a signature over the content hashes so tampering is detectable.

```json
{
  "package": "lodestar-evidence-2026-07-08",
  "generatedAt": "2026-07-08T09:14:22Z",
  "sessionId": "sess_4f1a9c",
  "decision": {
    "type": "buyer_scored",
    "entity": { "type": "buyer", "id": "buyer_20481" },
    "total": 78,
    "band": "High"
  },
  "model": {
    "unit": "scoring.buyer",
    "version": "3.2.0",
    "hash": "sha256:9b2c…e17a"
  },
  "artifacts": [
    { "path": "audit/session.jsonl",  "sha256": "sha256:41d0…" },
    { "path": "traces/buyer_20481.json", "sha256": "sha256:aa93…" },
    { "path": "pins/buyer_20481.json",   "sha256": "sha256:0f7b…" },
    { "path": "ledger/session.jsonl",   "sha256": "sha256:c55e…" },
    { "path": "model/buyer-3.2.0.yaml", "sha256": "sha256:9b2c…" }
  ],
  "chainOfCustody": [
    { "at": "2026-07-08T09:14:22Z", "actor": "harness-export", "action": "assembled" },
    { "at": "2026-07-08T09:14:23Z", "actor": "release-key",    "action": "signed" }
  ],
  "signature": {
    "alg": "ed25519",
    "keyId": "lodestar-release-2026",
    "value": "base64:MEUCIQ…"
  }
}
```

The signature is computed over the sorted list of artefact hashes plus the manifest metadata, not over the raw bytes of every file — so verification is one hash-and-compare per file, then one signature check. The `keyId` maps to a public key the auditor holds out of band. See [trust and attestation](/topics/defendable-agents/primitives/trust-and-attestation/) for how the signing key is provisioned and rotated; a package is only as trustworthy as the key that sealed it.

## Reproducibility instructions

The [deterministic engine](/topics/defendable-agents/decisions/reproducibility/) is what makes an offline package meaningful: the scoring functions are pure, so the same inputs and the same model version yield the same total, byte for byte, on the auditor's machine. Include a short, literal recipe:

```bash
# 1. Verify integrity: every artifact hash matches the manifest
lodestar-verify manifest.json            # checks sha256 + ed25519 signature

# 2. Reproduce the score from the trace, offline
lodestar-score \
  --model model/buyer-3.2.0.yaml \
  --inputs traces/buyer_20481.json \
  --expect 78
# -> layer scores: Need 74.0  Attractiveness 68.3  Winnability 89.5
# -> composite: 0.40*74.0 + 0.25*68.3 + 0.35*89.5 = 78  ✓  band "High"
```

If the recomputed total does not match the trace, the package is invalid and that itself is a finding. Bundle the verifier binary (or its hash and a build recipe) in the package — an auditor should never have to trust a tool they downloaded separately.

## Chain of custody

Chain of custody answers "who touched this, and when, between the decision and my desk." The audit log already timestamps and attributes every event to an actor. The manifest's `chainOfCustody` block extends that past export: assembled by the harness, signed by the release key, and — once handed over — countersigned or hash-logged by the recipient. Keep it short and append-only. Because the underlying log is append-only with fsync-on-flush, you can also prove the events were not reordered after the fact: sequence numbers are monotonic and gaps are visible.

## Honest limits

An evidence package proves **process, not correctness**. If variable `signal-relevance` was scored 4 when a careful human would have said 2, the package reproduces that 4 faithfully and consistently — the error is preserved, visible, and traceable, which is exactly how a reviewer catches it, but the package does not tell you the score was wrong. Temporal pins prove what the data's `dataAsOf` was; they do not prove the data was accurate, only that it was current as of that instant. And the model at the edge that mapped raw signals to variable scores is still a model — the package makes its output auditable, not infallible.

Practically: a package is a snapshot. It defends one decision at one time. Standing up the export path is a day of work; keeping keys rotated, hashes honest, and the verifier building is ongoing — [governance is maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/), not a one-time setup. Once the packages assemble cleanly, they slot straight into your [control mapping](/topics/defendable-agents/compliance/control-mapping/) as the record behind each control, and become the raw material for [verifying defendability](/topics/defendable-agents/compliance/verifying-defendability/) end to end.
