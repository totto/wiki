---
title: "Reproducibility Guarantees"
description: "Why the Lodestar scoring engine is built as pure functions, what reproducibility does and does not guarantee, and how model hashing and golden-master tests detect change."
image: assets/images/kcp-agent-020-05-claims-with-receipts.webp
---

# Reproducibility Guarantees

A score you cannot reproduce is an opinion with a timestamp. The whole point of a [defendable agent](/topics/defendable-agents/argument/what-defendable-means/) is that when someone challenges a decision months later — a buyer, an auditor, a colleague who thinks the ranking is wrong — you can re-run the exact computation and get the exact same number back. Not "roughly the same". The same. That property is not free; it is engineered, and it is engineered by keeping the model out of the arithmetic.

## Pure functions all the way down

The Lodestar scoring engine is a set of pure functions. Given the same inputs it returns the same outputs, every time, on any machine, forever. No clock reads inside the function. No network calls. No random seeds. No global mutable state. The variable scores go in, the layer means and the weighted composite come out.

A buyer layer score is the mean of its 1-5 variable scores times 20, giving a 0-100 layer score. The composite is a fixed weighting of three layers — Need at 0.40, Attractiveness at 0.25, Winnability at 0.35 — and the band is a lookup on the total. There is nothing in that description that varies between two runs.

```typescript
// Pure: no I/O, no Date.now(), no Math.random(), no hidden state.
function layerScore(variables: number[]): number {
  const mean = variables.reduce((a, b) => a + b, 0) / variables.length;
  return mean * 20; // 1-5 mean -> 0-100
}

function buyerScore(need: number[], attractiveness: number[], winnability: number[]) {
  const layers = {
    need: layerScore(need),
    attractiveness: layerScore(attractiveness),
    winnability: layerScore(winnability),
  };
  const total =
    layers.need * 0.40 +
    layers.attractiveness * 0.25 +
    layers.winnability * 0.35;
  return { layers, total, band: band(total) };
}

function band(total: number): string {
  if (total >= 85) return "Very high";
  if (total >= 70) return "High";
  if (total >= 55) return "Interesting but with gaps";
  if (total >= 40) return "Lower priority";
  return "Not prioritized now";
}
```

The [governance harness](/topics/defendable-agents/architecture/governance-harness/) is where the impure things live: budget recording, temporal pinning, audit emission, reading the current data. The pure engine is called from inside the harness but knows nothing about it. This separation is the reproducibility guarantee; this page is about proving the arithmetic never drifts underneath you.

## Determinism is not correctness

Here is the honest limit, stated plainly: reproducibility guarantees **process**, not **truth**. A pure function will apply a wrong variable weight just as faithfully as a right one. If `signal-freshness` is miscalibrated, every score inherits that error identically. Determinism does not save you from being wrong.

What it does is make wrongness **visible and reproducible**, which is the only condition under which you can catch it. A stochastic pipeline that returns 72 today and 68 tomorrow hides its bugs inside noise — you can never tell whether the variance is the model thinking or the model breaking. A deterministic engine has no noise to hide in. When a number changes, something changed, and the [append-only audit trail](/topics/defendable-agents/primitives/audit-trail/) tells you exactly what — down to the decision trace for the score that moved. Determinism is what turns "the score feels off" into "variable 4 moved from 3 to 5 because the input freshness changed on this date". This is the line the whole [determinism-versus-probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/) argument turns on.

## modelHash: detecting the swap

Pure functions guarantee that the *same code* gives the same output. They do not, by themselves, tell you whether the code is the same. That is what the model hash is for.

Every score creates a temporal pin, and the pin carries `modelVersion` and `modelHash` alongside the data timestamps. The hash is a content hash of the scoring model definition — its variables, weights, bands, and the layer structure — declared as a governed [Knowledge Context Protocol (KCP)](/topics/knowledge-context-protocol/) unit so it is selected deterministically and never silently swapped.

```json
{
  "scoredAt": "2026-07-08T09:14:22Z",
  "dataAsOf": "2026-07-07T00:00:00Z",
  "signalDates": ["2026-07-05", "2026-06-28"],
  "modelVersion": "buyer-1.4.0",
  "modelHash": "sha256:9f2c1e…a740"
}
```

If two pins for the same entity carry different hashes, the model changed between them — even if the version string was left untouched by mistake. That is [model drift](/topics/defendable-agents/primitives/drift-detection/), and it forces a reanalysis. The hash is what makes [versioning models](/topics/defendable-agents/decisions/versioning-models/) enforceable rather than aspirational: you cannot quietly re-tune a weight and pretend last quarter's scores were computed the same way.

## How to test reproducibility

Two tests, run in every build.

**Idempotence.** Score the same fixture twice in the same process and assert byte-for-byte equality on the full trace — every variable, every layer score, the total, and the band. If this ever fails, some hidden state or clock read has crept into the pure path.

```typescript
test("scoring is idempotent", () => {
  const input = loadFixture("buyer-fixture-01.json");
  const a = buyerScore(input.need, input.attractiveness, input.winnability);
  const b = buyerScore(input.need, input.attractiveness, input.winnability);
  expect(a).toEqual(b);
});
```

**Golden-master.** Keep a committed set of input fixtures paired with their expected output traces — the golden files. On every run, re-score the fixtures and diff against the golden. A matching diff is a green build. A non-matching diff is a *decision point*: either you introduced a regression, or you deliberately changed the model and must bump `modelVersion`, regenerate the goldens, and record why in the commit. The test does not judge which; it refuses to let the change happen silently.

```bash
# Regenerate goldens ONLY as a deliberate, reviewed act.
npm run score:goldens -- --update
git diff --stat test/goldens/   # this diff is the changelog for the model
```

Golden-master tests are the mechanism behind the ISO 27001 A.14.2 reproducibility control in the [compliance mapping](/topics/defendable-agents/compliance/control-mapping/): the deterministic engine plus a committed golden set *is* the evidence that scoring is reproducible. Use the same fixtures in an in-memory audit log to prove the emitted trace matches the computed trace end to end — the pattern is walked through in [reproduce a decision](/topics/defendable-agents/examples/reproduce-a-decision/).

## What you actually get

Reproducibility gives you three things and withholds a fourth. You get **replay** — any past score recomputed exactly. You get **change detection** — the model hash catches every swap, intended or not. You get **defensibility** — a challenged decision becomes a re-run, not an argument. What you do not get is **correctness**; the [model at the edge is still a model](/topics/defendable-agents/architecture/model-at-the-edge/), and a faithfully-reproduced wrong answer is still wrong. But it is a wrong answer you can find, name, and fix — which is more than any probabilistic pipeline will ever offer you.
