---
title: "Determinism vs Probabilism"
description: "Where determinism belongs in a defendable agent and where the model belongs: navigation, trust, time and budget are algorithms; synthesis and vocabulary are language tasks."
image: assets/images/kcp-agent-020-04-defeating-prompt-injection.webp
---

# Determinism vs Probabilism

The single most consequential design decision in a defendable agent is where you draw the line between the parts that must be reproducible and the parts that are allowed to improvise. Get the line right and you can defend every action the system took. Get it wrong — usually by letting the model do a job an algorithm should have done — and you have quietly traded accountability for convenience.

I draw the line the same way every time. **Navigation, trust, time and budget are algorithms. Synthesis and vocabulary are the model's job.** Everything else follows from that.

## What "deterministic" buys you

A deterministic function is a pure function: the same inputs produce the same outputs, always, with no hidden state and no sampling. The scoring engine behind Lodestar, my running example throughout this guide, is exactly that. A layer score is the mean of its 1–5 variable scores times 20, giving a 0–100 layer score. A buyer score is a fixed weighted composite of three layers — Need at 0.40, Attractiveness at 0.25, Winnability at 0.35 — and the priority band is a threshold lookup: `>=85` is "Very high", `>=70` is "High", and so on down. Feed the same eighteen variables in and you get the same band out, on any machine, next year, in front of an auditor.

That reproducibility is the whole point. It is what lets you [reproduce a decision](/topics/defendable-agents/examples/reproduce-a-decision/) months later and defend it, and it is what makes the [audit trail](/topics/defendable-agents/primitives/audit-trail/) worth keeping. I go deeper on the trade-offs in [what defendable means](/topics/defendable-agents/argument/what-defendable-means/); here I only want to fix which side of the line each concern lives on.

## The four things that must stay algorithmic

| Concern | Why it must be deterministic | The mechanism |
|---|---|---|
| **Navigation** — which knowledge unit, which model version, which document | Selection over declared metadata is a lookup, not a judgement. A model that "decides" which scoring model to use can silently swap it. | KCP `kcp_plan`/`kcp_load` over a declared manifest |
| **Trust** — is this input allowed, is this tenant isolated | Access boundaries are policy. A probabilistic gate is an open door on the runs where it feels generous. | Fail-closed gating; per-tenant state directories |
| **Time** — is this score stale | Staleness is arithmetic over dates, not intuition. | Temporal pinning with a 30-day-half-life decay |
| **Budget** — can I afford this operation | Cost ceilings are counting. You do not want a model estimating whether it is over budget. | The budget ledger, checked before every operation |

Take budget as the sharpest case. The ledger records a fixed cost per operation — `buyer_scoring` costs 5 units, `firm_analysis` 10, `signal_detection` 1 — and checks the ceiling *before* it records:

```typescript
record(op: string, entityId: string, cost = COST[op]): LedgerEntry {
  if (this.runningTotal + cost > this.ceiling) {
    return { accepted: false, reason: "budget_exceeded", op, cost };
  }
  this.runningTotal += cost;
  const entry = { seq: this.seq++, timestamp: now(), operation: op,
                  entityId, cost, currency: "units", runningTotal: this.runningTotal };
  this.entries.push(entry);
  return { accepted: true, ...entry };
}
```

When it returns `accepted: false` the governed operation throws and emits a `budget_exceeded` audit event. There is nothing to argue with. See [budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/) for the full ledger, and [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/) for how the same discipline applies to time.

## What the model is actually good at

None of this means the model has no job. It has the *hard* job. Turning a firm's public signals into a 1–5 `signal-relevance` score is genuinely a language task — it requires reading unstructured text and mapping it onto a vocabulary. Writing the justification that accompanies a decision, drafting a playbook, summarising why a buyer moved bands: all synthesis, all language, all work no lookup table can do. That is the [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/): the model produces the *variables*, and the deterministic engine composes them into the *decision*. The composition is the part you have to defend, so the composition is the part that must be reproducible.

This split is why I distinguish navigation from synthesis so firmly. If you want the deeper treatment of synthesis as its own discipline, [synthesis](/topics/synthesis/) and the [Knowledge Context Protocol](/topics/knowledge-context-protocol/) cover how the model's language work is fed by declared, governed context rather than a free-for-all retrieval.

## Why handing navigation to an LLM subtracts accountability

Here is the failure I see most often. A team lets the agent decide, in natural language, which scoring model to apply, which tenant's data it is looking at, or whether a stale score is "probably fine". Each of those is a navigation, trust or time decision dressed up as a reasoning step. The moment the model owns it, three things you were counting on evaporate:

- **Reproducibility.** The choice was sampled, so re-running yields a different path. Your [reproducibility](/topics/defendable-agents/decisions/reproducibility/) guarantee is gone.
- **The audit trail.** The decision trace records *what the model said*, not *why the correct unit was selected* — because nothing selected it deterministically.
- **Fail-closed behaviour.** A probabilistic gate cannot fail closed; it fails *soft*, letting through whatever the current sampling happened to favour. That is precisely the crack a prompt injection walks through — see [catch an injection](/topics/defendable-agents/examples/catch-an-injection/).

Giving navigation to a model does not add intelligence to those decisions. It subtracts the record.

## The honest limits

Determinism guarantees **process, not correctness**. If a variable is wrong — a mis-scored `signal-relevance`, a weight that should have been 0.30 — the deterministic engine applies that error to every buyer, consistently. What determinism buys you is that the error is *visible and reproducible*, which is exactly how you catch it: a consistent, inspectable mistake is findable in a way a stochastic one never is. Temporal pinning tells you a score is stale; it does not refresh the data. Fail-closed gating, over-tuned, blocks legitimate work. And the model at the edge is still a model — it will produce a confident wrong `1–5` from time to time, which is why its output is a *variable feeding a transparent composite*, not a decision in itself.

The discipline is not "never use the model". It is: **let the model speak, but never let it navigate.** Everything downstream of that line — the [governance harness](/topics/defendable-agents/architecture/governance-harness/), the audit log, the whole [architecture overview](/topics/defendable-agents/architecture/overview/) — exists to keep the line honest.
