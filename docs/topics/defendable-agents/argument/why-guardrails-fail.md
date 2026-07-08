---
title: "Why Bolt-On Guardrails Fail"
description: "Classifier guardrails and safety-by-prompting lose slowly because you cannot police a probabilistic system with another probabilistic one. Determinism removes the attack surface instead."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Why Bolt-On Guardrails Fail

The dominant pattern for making an agent "safe" is to wrap it. You keep the probabilistic core and bolt something on: a prompt that begs the model to behave, a classifier that inspects inputs and outputs, a second model that judges the first. I have shipped systems like this. They feel like progress because you can demo a blocked attack. They fail in production for a reason that is structural, not tuning, and no amount of prompt engineering fixes it.

## The arms race you cannot win

A bolted-on guardrail is a filter sitting between an adversary and a model. Both the filter and the thing it protects are probabilistic. That means the guardrail has a false-negative rate, and the adversary gets unlimited retries to find one. Every published jailbreak, every prompt-injection payload smuggled through a fetched web page, every base64-and-roleplay trick is the same move: search the input space until the classifier's probability of catching this particular phrasing drops low enough.

You are defending with a coin that lands heads 99% of the time. The attacker flips it a thousand times. This is the [threat model](/topics/defendable-agents/argument/threat-model/) that bolt-on defences quietly assume away — they are tuned against the attacks that existed when they were trained, and the attack surface is the entire space of natural language.

Two things make the race unwinnable for the defender:

- **Asymmetry of retries.** One escape out of ten thousand attempts is a total breach. The defender must be right every time; the attacker must be right once.
- **Coupled failure modes.** Tighten the classifier and you raise false positives — legitimate work gets blocked, users route around the guardrail, and someone quietly disables it. Loosen it and the escapes return. There is no setting that is both safe and usable, only a slider between two kinds of failure. This is the same trap that over-tuned [fail-closed policy](/topics/defendable-agents/architecture/fail-closed-behavior/) falls into, except a fail-closed *gate* refuses deterministically; a classifier refuses on a guess.

## Classifier-on-top: what actually breaks

Concretely, the classifier-on-top architecture breaks in four predictable ways.

1. **It inspects text, not intent.** A payload that reads as benign but instructs the model to exfiltrate a tenant's confidential score passes the input filter and only reveals itself in behaviour the filter never sees.
2. **It has no memory of state.** The guardrail cannot know that this session has already spent its budget, already crossed a tenant boundary, or is scoring against a stale model, because those are facts about the *system*, not about the *string* it was handed.
3. **Its decisions are unauditable.** "The classifier returned 0.83, below threshold" is not a justification you can defend to an auditor twelve months later. There is no variable trace, no reproducible reason. Compare that to a real [decision trace](/topics/defendable-agents/primitives/decision-traces/).
4. **It drifts.** The base model updates, the attack distribution shifts, and the guardrail silently degrades. Nobody re-certifies it because it was sold as one-time setup, not [ongoing maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/).

## Constitutional versus bolted-on

There is a meaningful distinction between *constitutional* safety — where the model is trained so that the disposition to refuse harm is part of the weights — and *bolted-on* safety, where an external filter second-guesses an untrained core. Constitutional training is genuinely better than a classifier taped to the front door, because the behaviour is intrinsic rather than adversarially separable.

But it is still probabilistic. A trained disposition is a strong prior, not a proof. It lowers the escape rate; it does not make the rate zero, and it gives you nothing to show an auditor beyond "the model usually does the right thing." For a system that scores buyers, approves spend, or screens firms in a regulated professional-services market, "usually" is not a control. You cannot put a probability distribution in an evidence package. This is the gap between [what "defendable" means](/topics/defendable-agents/argument/what-defendable-means/) and what "safe-ish" delivers.

## Determinism removes the surface

The move that actually works is not a better guard. It is refusing to route the ungovernable decision through the model at all. The consequential act — the score, the tier, the spend approval — is computed by a pure function, and the model is pushed to [the edge](/topics/defendable-agents/architecture/model-at-the-edge/) where it drafts and summarises but never decides. See [determinism versus probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/) for the full argument.

When the decision is deterministic, there is no input space to search. A buyer score is a fixed weighted composite of eighteen variables across three layers, and the same inputs produce the same output every time:

```typescript
// Need 0.40, Attractiveness 0.25, Winnability 0.35 — pure, no model call
function buyerScore(layers: LayerScores): number {
  return Math.round(
    layers.need * 0.40 +
    layers.attractiveness * 0.25 +
    layers.winnability * 0.35
  );
}

function layerScore(variables: number[]): number {
  const mean = variables.reduce((a, b) => a + b, 0) / variables.length;
  return mean * 20; // 1-5 scores -> 0-100
}
```

There is no phrasing of a prompt that makes `0.40` become `0.90`. The [governance harness](/topics/defendable-agents/architecture/governance-harness/) gates access with a fail-closed policy that checks *state* — budget ceiling, tenant boundary, model version — not the wording of a request. What a guardrail tried and failed to police, the architecture simply removes.

## Honest limits

Removing the surface is not a claim of correctness. Determinism guarantees the *process*, not the answer: a badly chosen weight or a wrong variable is applied consistently to every buyer. The difference is that a deterministic wrong is *visible and reproducible* — it shows up identically in every [audit trail](/topics/defendable-agents/primitives/audit-trail/) and you can trace it back to the exact model version, which is how you catch it. A probabilistic wrong is different every time and blames the prompt.

And the model at the edge is still a model. Its drafts can still be wrong or injected; the point is that a bad draft cannot *decide* anything, because the deciding path never touches it. You have not eliminated probabilistic error. You have confined it to where it can be observed, bounded, and defended.

If you want the shape of the whole stack this argument leads to, start with the [architecture overview](/topics/defendable-agents/architecture/overview/).
