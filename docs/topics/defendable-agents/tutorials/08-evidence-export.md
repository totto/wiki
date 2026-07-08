---
title: "Tutorial 8: Exporting Evidence for an Auditor"
description: "Assemble a self-contained evidence package from the audit log: the decision trace, the temporal pin, the budget ledger and the model version, then map each field to a control."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Tutorial 8: Exporting Evidence for an Auditor

By this point you have a governed session that scores buyers, records every spend, and pins every decision in time. The tutorials up to here built the machinery. This one turns that machinery into something an auditor can hold: a self-contained evidence package for a single decision, assembled entirely from records the system already wrote.

The premise is simple. When someone asks "why did Lodestar prioritise this buyer, on what data, at what cost, under which model?", you should not have to reconstruct anything. Every fact of the answer is already on disk. Your job here is selection and packaging, not investigation.

If you have not done the earlier tutorials, at least skim [Tutorial 4: The Audit Log](/topics/defendable-agents/tutorials/04-audit-log/) and [Tutorial 6: Temporal Drift](/topics/defendable-agents/tutorials/06-temporal-drift/) — this page assumes you have those records to draw from.

## What an auditor actually needs

An auditor is not asking you to prove the score is *right*. They are asking you to prove the process is *accountable*: that the decision was made the way you say it was, on the data you say it was, and that you can show it again. For one decision, that reduces to four artefacts:

| Artefact | Answers | Source |
|---|---|---|
| Decision trace | Which variables, which scores, which band? | `buyer_scored` event |
| Temporal pin | What data, how old, which model version/hash? | `temporal` block on the event |
| Budget ledger | What did it cost, under what ceiling? | `budget_spend` entries |
| Model manifest | Which model version produced it, and is it declared? | KCP unit + `modelHash` |

Each of those maps to a control. The [control mapping](/topics/defendable-agents/compliance/control-mapping/) page holds the full table; the [evidence packages](/topics/defendable-agents/compliance/evidence-packages/) page describes the format an assessor expects. Here we build one by hand.

## Step 1 — select the events for one decision

The [append-only audit log](/topics/defendable-agents/primitives/audit-trail/) is JSONL: one event per line, one session's events in order. To isolate a decision, filter by `sessionId` and the `entity.id` of the buyer, then keep the events that carry the trace and the money.

```bash
#!/usr/bin/env bash
set -euo pipefail

LOG="audit/session-2026-07-08.jsonl"
SESSION="sess_8f21"
ENTITY="buyer_5567"
OUT="evidence/${ENTITY}"

mkdir -p "$OUT"

# 1. The decision trace + temporal pin (the buyer_scored event)
jq -c --arg s "$SESSION" --arg e "$ENTITY" \
  'select(.sessionId==$s and .entity.id==$e and .type=="buyer_scored")' \
  "$LOG" > "$OUT/decision.jsonl"

# 2. Every budget line touching this entity
jq -c --arg s "$SESSION" --arg e "$ENTITY" \
  'select(.sessionId==$s and .entity.id==$e
          and (.type=="budget_spend" or .type=="budget_exceeded"))' \
  "$LOG" > "$OUT/budget.jsonl"

# 3. Session envelope: start + end give the ceiling and the run boundary
jq -c --arg s "$SESSION" \
  'select(.sessionId==$s and (.type=="session_start" or .type=="session_end"))' \
  "$LOG" > "$OUT/session.jsonl"
```

Nothing here mutates the log. The log is fsync-flushed and append-only; you are reading past-tense facts, never editing them.

## Step 2 — the decision trace itself

A single `buyer_scored` line already contains the whole story. This is what one looks like, pretty-printed:

```json
{
  "timestamp": "2026-07-08T09:14:22.301Z",
  "sessionId": "sess_8f21",
  "sequence": 47,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer_5567", "name": "Buyer 5567" },
  "decision": {
    "action": "score_buyer",
    "justification": "Composite 78.4 over three weighted layers",
    "outputs": { "total": 78.4, "band": "High" }
  },
  "scoring": {
    "model": "buyer-scoring@2.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 4 },
      { "id": "competitive-position", "score": 3 },
      { "id": "relationship-proximity", "score": 5 }
    ],
    "layerScores": { "Need": 81, "Attractiveness": 72, "Winnability": 80 },
    "total": 78.4,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-07-06T00:00:00Z",
    "scoredAt": "2026-07-08T09:14:22.301Z",
    "signalDates": ["2026-07-05", "2026-07-01"],
    "modelVersion": "2.3.0",
    "modelHash": "sha256:9c1f...e4a2"
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 132, "ceiling": 1000 },
  "durationMs": 38
}
```

The layer maths is checkable by hand — Need is the mean of its six 1-5 variables times 20, and the composite is `0.40·Need + 0.25·Attractiveness + 0.35·Winnability`. An auditor with a calculator can reproduce `78.4` from the numbers on the page. That is the point of a [deterministic engine](/topics/defendable-agents/decisions/reproducibility/): the trace is not a summary of the decision, it *is* the decision.

## Step 3 — assemble a self-contained package

The package must survive being emailed to someone with no access to your systems. So it pins the model too — not the name, the hash — and includes a manifest that maps every field to its control.

```bash
# Resolve the model unit + hash the actual model file
MODEL_VER=$(jq -r '.scoring.model' "$OUT/decision.jsonl")
cp "models/buyer-scoring.yaml" "$OUT/model.yaml"
sha256sum "$OUT/model.yaml" > "$OUT/model.sha256"

cat > "$OUT/manifest.json" <<JSON
{
  "package": "evidence/${ENTITY}",
  "decision": "buyer_5567 scored ${MODEL_VER}",
  "generatedAt": "$(date -u +%FT%TZ)",
  "generatedBy": "totto@exoreaction.com",
  "contents": {
    "decision.jsonl": "Decision trace (SOC 2 CC7.2)",
    "budget.jsonl":   "Budget enforcement record (SOC 2 CC6.1)",
    "session.jsonl":  "Processing record (GDPR Art. 30)",
    "model.yaml":     "Model version, declared KCP unit (ISO 27001 A.14.2)",
    "model.sha256":   "Reproducibility hash (ISO 27001 A.14.2)"
  },
  "provenance": "temporal pin embedded in decision.jsonl (ISO 27001 A.8.1)"
}
JSON

tar -czf "evidence/${ENTITY}.tar.gz" -C evidence "${ENTITY}"
sha256sum "evidence/${ENTITY}.tar.gz"
```

The final `sha256sum` gives the package its own tamper-evident fingerprint. Record it in your handover note; if the tarball is altered later, the hash no longer matches.

## Step 4 — map fields to controls

The auditor rarely reads JSON for pleasure. They want a crosswalk from artefact to control, and the manifest above is that crosswalk. In prose:

- **Decision trace** (`scoring.variables`, `layerScores`, `total`, `band`) satisfies the decision-trace control — full inputs and outputs, SOC 2 CC7.2.
- **Temporal pin** (`temporal`) satisfies data provenance — you can show exactly how old the underlying signals were, ISO 27001 A.8.1.
- **Budget ledger** (`budget_spend`) satisfies budget enforcement — the operation cost against a hard ceiling, SOC 2 CC6.1.
- **Model hash** (`modelHash` + `model.sha256`) satisfies reproducibility — the deterministic engine plus the exact model bytes, ISO 27001 A.14.2.

For the fuller narrative an assessor reads alongside the package, point them at [verifying defendability](/topics/defendable-agents/compliance/verifying-defendability/).

## Honest limits

This package proves the decision was made as recorded — process, not correctness. If a variable was scored on a flawed rule, the trace shows that flaw applied faithfully; the export makes the mistake *visible and reproducible*, which is how you catch it, but it does not tell you the score was wise. The temporal pin proves the data's age, not its accuracy, and it does not refresh anything. And the tarball hash is only tamper-*evident*: it detects change, it does not prevent it. Store the package where the [governed session](/topics/defendable-agents/architecture/governance-harness/) already keeps its logs, and treat evidence export as a repeatable step in operating the system, not a scramble you improvise the week an audit lands.
