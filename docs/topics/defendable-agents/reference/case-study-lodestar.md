---
title: "Case Study: Lodestar (Deep)"
description: "A full anonymized walkthrough of Lodestar, a governed competitive-intelligence scoring system in a regulated professional-services market, from pipeline to compliance."
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# Case Study: Lodestar (Deep)

Lodestar is the system this whole field guide is reverse-engineered from. It is a competitive-intelligence and scoring engine operating in a regulated professional-services market: it watches public signals about buyers, scores how worthwhile each buyer is to pursue, and produces go-to-market plans for the firms selling into that market. The real system is proprietary and the domain is sensitive, so everything here is anonymised. What is not anonymised is the mechanics — the numbers, weights, event shapes, and control mappings are exactly what runs.

I built Lodestar the way I have built systems for four decades: assume the interesting failures happen where nobody is looking, and instrument for that. When a model recommends spending real commercial effort on one buyer over another, "the AI said so" is not an answer anyone can defend. That is why Lodestar is a *defendable* agent — the model at the edge turns noisy inputs into typed ones, and every consequential decision downstream is a deterministic, logged, reproducible function of those declared inputs. If the term is new, [what defendable means](/topics/defendable-agents/argument/what-defendable-means/) is the one-page definition; this page is the worked example.

## Why defendable matters here

The buyers are large, the pursuit costs are real, and the market is regulated, so decisions can be audited after the fact by people who were not in the room. A buyer excluded from pursuit is a commercial decision with a paper trail requirement. A confidential score leaking across tenant boundaries is an incident. The [threat model](/topics/defendable-agents/argument/threat-model/) is not "the model hallucinates a fact" so much as "we cannot show why we did what we did." Defendability is the product requirement, not a nice-to-have.

## The pipeline

Lodestar runs a linear pipeline of governed operations, each with a fixed cost in budget units:

| Stage | Operation | Cost (units) |
|---|---|---|
| Detect public signal | `signal_detection` | 1 |
| Score a buyer | `buyer_scoring` | 5 |
| Analyse a firm's fit | `firm_analysis` | 10 |
| Score buyer/firm match | `match_scoring` | 5 |
| Assign account tier | `account_tiering` | 2 |
| Generate GTM plan | `gtm_plan` | 10 |
| Produce a playbook | `playbook_generation` | 5 |

The model reads noisy public events and turns them into structured, typed inputs. From that point on, nothing is improvised — the scoring is arithmetic.

## Deterministic scoring

A buyer score is a weighted composite of three layers. Each layer score is the mean of its 1-5 variable scores times 20, giving 0-100:

```typescript
// layer score: mean of 1-5 variable scores, scaled to 0-100
const layerScore = (vars: number[]) =>
  (vars.reduce((a, b) => a + b, 0) / vars.length) * 20;

// buyer composite
const buyer =
  0.40 * need +          // 6 vars: signal-strength, signal-freshness, ...
  0.25 * attractiveness + // 6 vars: mandate-value, strategic-value, ...
  0.35 * winnability;     // 6 vars: competitive-position, relationship-proximity, ...

const band =
  buyer >= 85 ? "Very high" :
  buyer >= 70 ? "High" :
  buyer >= 55 ? "Interesting but with gaps" :
  buyer >= 40 ? "Lower priority" :
                "Not prioritized now";
```

Eighteen variables across three layers for buyers; twenty-one across four layers for the match score. `signal-freshness` is itself a pinned function of time — a stepped decay with a roughly 30-day half-life, so a three-day-old signal scores 5 and a ninety-day-old one scores 1.5. Same inputs, same outputs, every time. The [anatomy of a score](/topics/defendable-agents/decisions/anatomy-of-a-score/) page walks the full arithmetic; [variable design](/topics/defendable-agents/decisions/variable-design/) covers why each variable exists.

## The governance layer in practice

Every operation runs inside a governed session that shares one audit log, one budget ledger, and one map of temporal pins. The order is fixed and non-negotiable:

1. **Record the budget spend** first. The ledger checks the ceiling *before* recording; if `runningTotal + cost` exceeds the session ceiling (Lodestar defaults to 1000 units), the operation throws and emits a `budget_exceeded` event. See [budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/).
2. **Run the pure deterministic score.**
3. **Create a temporal pin** — `{scoredAt, dataAsOf, signalDates[], modelVersion, modelHash}`. Later, [drift detection](/topics/defendable-agents/primitives/drift-detection/) compares that pin against current state and recommends monitor or reanalyse.
4. **Emit an append-only audit event** carrying the full variable trace: every variable id and score, the layer scores, the total, the band, the temporal context, and the budget position.

The audit log is JSONL, one event per line, fsync on flush. A single `buyer_scored` line looks like this:

```json
{
  "timestamp": "2026-07-08T09:14:22Z",
  "sessionId": "sess_4f2a",
  "sequence": 37,
  "type": "buyer_scored",
  "actor": "scoring-agent",
  "entity": { "type": "buyer", "id": "b_881", "name": "[redacted]" },
  "scoring": {
    "model": "buyer/1.4.0",
    "variables": [
      { "id": "signal-strength", "score": 4 },
      { "id": "signal-freshness", "score": 4.5 }
    ],
    "layerScores": { "need": 78, "attractiveness": 66, "winnability": 71 },
    "total": 72.6, "band": "High"
  },
  "temporal": { "dataAsOf": "2026-07-07", "scoredAt": "2026-07-08T09:14:22Z" },
  "budget": { "cost": 5, "runningTotal": 190, "ceiling": 1000, "remaining": 810 }
}
```

The whole harness is configured declaratively — fail-closed, audit-all, ceiling, context budget — as described in [governance-harness](/topics/defendable-agents/architecture/governance-harness/) and the [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) primitive. The scoring models themselves are declared as governed [KCP](/topics/knowledge-context-protocol/) units, so a model is selected deterministically and never silently swapped ([declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/)).

## Multi-tenancy

Several firms use Lodestar over the same market. Signal and company data is shared — every tenant sees the same public events, because they are public. Scores and plans are confidential and live in isolated per-tenant state directories. The isolation is a directory boundary enforced by the harness, not a policy note in a document. That distinction is the whole point of [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/): a boundary you can `ls`.

## Compliance mapping

Each control is satisfied by a mechanism *and* a record, never by a claim:

| Control | Mechanism | Record |
|---|---|---|
| Audit logging (ISO 27001 A.8.15) | append-only JSONL | the log |
| Decision trace (SOC 2 PI1.5) | full variable inputs/outputs | scoring block |
| Data provenance (ISO 27001 A.5.12) | temporal pinning | pins |
| Reproducibility (ISO 27001 A.8.32) | deterministic engine | re-run |
| Access boundaries (SOC 2 CC6.1) | fail-closed gating | denied events |
| Tenant isolation (ISO 27001 A.8.3) | per-tenant state | directories |

The full table lives in [control-mapping](/topics/defendable-agents/compliance/control-mapping/).

## The org angle

Lodestar is what happens when domain expertise stops living in people's heads and becomes infrastructure. The eighteen variables and their weights *are* the encoded judgement of the people who know this market — versioned, reviewable, and applied identically to every buyer. That is the argument in [the governance gap](/topics/defendable-agents/argument/the-governance-gap/): governed expertise scales; tribal knowledge does not.

## Honest limits

Determinism guarantees process, not correctness. If a variable weight is wrong, Lodestar applies it wrongly to *every* buyer — but visibly, reproducibly, and in the log, which is exactly how you catch and fix it. Temporal pinning detects staleness; it does not refresh the underlying data. Fail-closed, over-tuned, will block legitimate work. And the model at the edge is still a model. Governance is maintenance, not a one-time setup — see [operating and maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/). None of this makes Lodestar right. It makes Lodestar defendable, which is a different and more honest claim.
