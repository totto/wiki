---
title: "Control Mapping: SOC 2 / ISO 27001 / GDPR"
description: "Each defendable-agent primitive mapped to the audit control it satisfies, with the concrete mechanism and the record you export as evidence — satisfied by mechanism, not by claim."
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Control Mapping: SOC 2 / ISO 27001 / GDPR

An auditor does not want to hear that your agent "takes governance seriously". They want a control, a mechanism that enforces it, and a record they can inspect after the fact. Most AI systems fail at the second and third steps: the control exists as a paragraph in a policy document, the mechanism is a prompt instruction the model may or may not follow, and the record is a chat log nobody can reconstruct. That gap is the whole subject of [the governance gap](/topics/defendable-agents/argument/the-governance-gap/).

The defendable-agent stack is built so that every control an enterprise auditor cares about is satisfied by a running mechanism, and every mechanism leaves a record you can pull on demand. This page is the map. It is the document I hand an auditor first, because it lets them tie each clause they are checking to a file on disk.

## The point: satisfied by mechanism, not by claim

Read the table below with one question in mind for each row: *if I deleted the policy sentence, would the control still hold?* For a defendable agent the answer is yes. Audit logging is not a promise to log — it is an append-only writer with `fsync` on flush that the [governed session](/topics/defendable-agents/architecture/governance-harness/) cannot bypass. Reproducibility is not a claim that scores are consistent — it is a [deterministic engine](/topics/defendable-agents/decisions/reproducibility/) of pure functions where the same inputs always yield the same outputs. The control is the code path, and the evidence is what that path wrote down.

## The mapping

| Control | Mechanism (what enforces it) | Record (what you pull) | Clause |
|---|---|---|---|
| Audit logging | Append-only JSONL log, one event per line, `fsync` on flush | The session audit file, every event with sequence + timestamp | ISO 27001 A.12.4 |
| Decision trace | Full variable inputs and outputs captured per score | The `scoring.variables[]` and `decision` block on each event | SOC 2 CC7.2 |
| Data provenance | Temporal pinning on every score | The `temporal` pin: `dataAsOf`, `scoredAt`, `signalDates[]` | ISO 27001 A.8.1 |
| Reproducibility | Deterministic scoring engine (pure functions) | Re-run of the pinned model + inputs, byte-identical result | ISO 27001 A.14.2 |
| Access boundaries | Fail-closed gating on every governed operation | `session_start` config + any denied/`budget_exceeded` events | SOC 2 CC6.1 |
| Processing records | Per-session governed logs | The session log as an Article 30 processing record | GDPR Art. 30 |
| Data minimization | Public-data-only inputs + declared audience | The KCP manifest audience + input provenance | GDPR Art. 5(1)(c) |
| Tenant isolation | Per-tenant state directories | The directory boundary + per-tenant log paths | ISO 27001 A.9.4 |
| Budget enforcement | Operation cost ceiling checked before recording | The [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/) entries + `budget_spend` events | SOC 2 CC6.1 |

Each row is a full page elsewhere in this guide. The [audit trail](/topics/defendable-agents/primitives/audit-trail/), the [decision traces](/topics/defendable-agents/primitives/decision-traces/), and [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) are the three primitives an auditor will spend most of their time in.

## For each row: mechanism plus the record you pull

The record is the part people underestimate. A control is only defendable if the evidence survives the moment — you must be able to reconstruct a decision months later. In the Lodestar example, a buyer-scoring event on the audit log carries everything three separate controls need at once:

```json
{
  "timestamp": "2026-03-11T09:14:02.412Z",
  "sessionId": "sess-4417",
  "sequence": 128,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "buyer-9021", "name": "[redacted]" },
  "decision": {
    "action": "score_buyer",
    "justification": "Composite of Need/Attractiveness/Winnability layers"
  },
  "scoring": {
    "model": "buyer-scoring@2.3.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 },
      { "id": "buying-journey-stage", "score": 3 }
    ],
    "layerScores": { "need": 78, "attractiveness": 66, "winnability": 71 },
    "total": 73,
    "band": "High"
  },
  "temporal": {
    "dataAsOf": "2026-03-10T00:00:00Z",
    "scoredAt": "2026-03-11T09:14:02.412Z",
    "signalDates": ["2026-03-08T00:00:00Z"]
  },
  "budget": { "cost": 5, "currency": "units", "runningTotal": 340, "ceiling": 1000 }
}
```

One line satisfies four rows of the table. The `scoring.variables[]` block is the SOC 2 CC7.2 decision trace. The `temporal` block is the ISO 27001 A.8.1 provenance record. The `model` field pinned to `buyer-scoring@2.3.0` is what makes the ISO 27001 A.14.2 reproducibility re-run possible — feed the same model version and the same variable scores back through the [deterministic engine](/topics/defendable-agents/decisions/anatomy-of-a-score/) and you get `73 / "High"` again, every time. The `budget` block is the SOC 2 CC6.1 ceiling record. When an auditor asks "show me how this buyer was prioritised", you hand them this line and the [reproduce-a-decision walkthrough](/topics/defendable-agents/examples/reproduce-a-decision/).

## Adapt the clause numbers

The clause numbers in the table are the ones I map to most often, but they are not load-bearing. Your auditor may be working from a different framework — NIST, a sector regulator, an internal control catalogue. The mapping still holds, because it is anchored to the *mechanism*, not the citation. Re-label the right-hand column and the middle two columns do not move. A useful exercise before an audit is to sit with the assessor, take their control list, and point each item at a mechanism in this table. Where nothing points, you have found a real gap rather than a documentation gap. The full [evidence packages](/topics/defendable-agents/compliance/evidence-packages/) page shows how to bundle the records once the mapping is agreed.

## Honest limits

This table proves *process*, not *correctness*. If a variable is designed wrong — say `signal-freshness` decays too slowly — the deterministic engine will apply that error consistently to every buyer. The control mapping does not catch the mistake; it makes the mistake *visible and reproducible*, which is how you catch it on review. Temporal pinning tells you data is stale; it does not refresh the data. Fail-closed gating can be over-tuned until it blocks legitimate work. And the model at the edge is still a model. None of these controls make the agent right. They make it *answerable* — which is the bar an audit actually sets. Governance is maintenance, not a one-time setup; the mapping is only true as long as you keep [operating and maintaining it](/topics/defendable-agents/compliance/operating-and-maintenance/).
