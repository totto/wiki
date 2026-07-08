---
title: "Verifying Defendability"
description: "How to test a defendable agent: golden-master determinism, audit-completeness, budget-ceiling enforcement, drift detection, and tenant isolation, wired into a conformance matrix."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Verifying Defendability

A claim of defendability is worthless until it is tested. "Defendable" is not a
posture you assert in a slide; it is a property you can demonstrate on demand,
with a suite that fails loudly the moment the property stops holding. This page
sets out how I test the Lodestar stack — the categories, the concrete assertions,
and the conformance matrix that ties each test back to a control.

If you have not read
[what defendable means](/topics/defendable-agents/argument/what-defendable-means/),
start there. This page assumes you already accept the goal and want to know how
to prove you have hit it.

## Five test categories

Verification splits cleanly into five buckets. Each maps to a mechanism in the
stack, and each has a distinct failure signature.

| Category | What it proves | Mechanism under test |
|---|---|---|
| Determinism (golden-master) | Same inputs produce byte-identical scores | Pure scoring engine |
| Audit-completeness | Every governed operation emits an event | Append-only log |
| Budget enforcement | Work stops at the ceiling, fail-closed | Budget ledger |
| Drift detection | Stale or re-versioned scores are flagged | Temporal pinning |
| Tenant isolation | Confidential state never crosses a boundary | Per-tenant directories |

## Golden-master determinism

The scoring engine is a set of pure functions:
[reproducibility](/topics/defendable-agents/decisions/reproducibility/) is the
whole point. A golden-master test freezes a known input, records the expected
output once, and fails on any divergence. Because a Buyer score is a weighted
composite of three layers — Need (0.40), Attractiveness (0.25),
Winnability (0.35) — the fixture must pin every one of the 18 variables.

```typescript
import { scoreBuyer } from "../src/scoring/buyer";
import goldenInput from "./fixtures/buyer-001.input.json";
import goldenOutput from "./fixtures/buyer-001.output.json";

test("buyer score is a pure function of its inputs", () => {
  const first = scoreBuyer(goldenInput);
  const second = scoreBuyer(goldenInput);

  // idempotent
  expect(first).toEqual(second);
  // matches the frozen golden master
  expect(first.total).toBe(goldenOutput.total);
  expect(first.band).toBe(goldenOutput.band);
  expect(first.layerScores).toEqual(goldenOutput.layerScores);
});
```

The `total` and `band` are not independent assertions — a band of `"High"`
must correspond to a `total` in `[70, 85)`. I assert both so a broken band
boundary cannot hide behind a correct total.

The honest limit here is worth stating plainly: determinism guarantees
**process, not correctness**. If `signal-freshness` is computed with the wrong
half-life, the golden master will happily lock in the wrong number. What the
test buys you is that the error is *visible and reproducible* — you change the
decay function, the golden master breaks, and you are forced to look. That is
how you catch a wrong variable, not how you prevent one.

## Audit-completeness

The rule is absolute: every governed operation emits exactly one audit event.
A test harness that uses the in-memory log writer can assert this directly.
Drive an operation, then interrogate the log.

```typescript
test("buyer_scored emits a complete decision trace", () => {
  const session = newTestSession();        // in-memory audit log + ledger
  session.scoreBuyer(goldenInput);

  const events = session.audit.events();
  expect(events.map(e => e.type)).toContain("buyer_scored");

  const ev = events.find(e => e.type === "buyer_scored")!;
  expect(ev.scoring.variables).toHaveLength(18);   // full trace, no gaps
  expect(ev.scoring.total).toBeGreaterThanOrEqual(0);
  expect(ev.temporal.dataAsOf).toBeDefined();       // provenance pinned
  expect(ev.budget.cost).toBe(5);                   // buyer_scoring = 5 units
});
```

Completeness has two halves. First, *presence*: the operation must produce an
event at all. Second, *fidelity*: the event must carry the full variable trace,
the temporal pin, and the budget line — a
[decision trace](/topics/defendable-agents/primitives/decision-traces/) with a
missing variable is a hole in the record. I test both, because a system that
logs "buyer scored" with no variables is auditable in name only.

## Budget-ceiling enforcement

The ledger checks the ceiling **before** it records. A budget test asserts that
the boundary is fail-closed, not fail-open: the operation over the ceiling must
throw and emit `budget_exceeded`, and it must *not* have produced a score.

```typescript
test("work stops at the ceiling and fails closed", () => {
  const session = newTestSession({ ceiling: 8 });   // room for one buyer score

  session.scoreBuyer(goldenInput);                  // +5 => runningTotal 5
  expect(() => session.analyseFirm(goldenFirm))     // firm_analysis = 10
    .toThrow(/budget/i);                            // 5 + 10 > 8

  const types = session.audit.events().map(e => e.type);
  expect(types).toContain("budget_exceeded");
  expect(types).not.toContain("firm_analysis_complete"); // no partial work
});
```

See [budget and bounding](/topics/defendable-agents/primitives/budget-and-bounding/)
for the full cost table. The subtle case a good test catches: `runningTotal + cost`
must exceed the ceiling to be rejected, so an operation that lands the total
*exactly* on the ceiling should be accepted. Test the boundary at
`ceiling - 1`, `ceiling`, and `ceiling + 1`; off-by-one errors live here.

## Drift detection

[Temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/)
records a pin at score time; the drift check compares it against current state.
The recommendation logic has four arms, and each deserves a test: two or more
drift reasons recommend `reanalyze`; model drift alone recommends `reanalyze`;
a single non-model reason recommends `monitor`; no drift is `ok`.

```typescript
test("model version change alone triggers reanalyze", () => {
  const pin = { dataAsOf: "2026-06-01", modelVersion: "1.3.0",
                scoredAt: "2026-06-15", maxAgeDays: 30 };
  const now = { currentDataAsOf: "2026-06-01", modelVersion: "1.4.0",
                today: "2026-06-20" };

  const result = checkDrift(pin, now);
  expect(result.reasons).toEqual(["MODEL"]);
  expect(result.recommendation).toBe("reanalyze");
});
```

Again the honest limit: drift detection tells you a score is stale. It does not
refresh the underlying data — that is a separate operation you must schedule and
pay for out of the same ledger.

## Tenant isolation

Isolation is a directory boundary, not a policy note, so I test it as one.
Shared signal data is visible to every tenant; confidential scores and plans
must never appear in another tenant's state directory.

```typescript
test("confidential scores stay in their tenant directory", () => {
  const a = harness.session({ tenant: "tenant_a" });
  a.scoreBuyer(goldenInput);

  const bFiles = fs.readdirSync(stateDir("tenant_b"));
  expect(bFiles).not.toContain(`${goldenInput.buyerId}.score.json`);
  // and the reverse read is refused, not empty
  expect(() => harness.session({ tenant: "tenant_b" })
    .loadScore(goldenInput.buyerId)).toThrow(/not found|forbidden/i);
});
```

For the boundary model see
[multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/).

## The conformance matrix

Individual tests are necessary but not sufficient. What an auditor wants is a
single artefact that maps every control to the test that exercises it and the
last time that test passed. I generate one from the suite:

| Control | Mechanism | Test id | Status |
|---|---|---|---|
| Audit logging (ISO 27001 A.12.4) | Append-only JSONL | `audit.completeness` | pass |
| Decision trace (SOC 2 CC7.2) | Full variable trace | `audit.fidelity` | pass |
| Reproducibility (ISO 27001 A.14.2) | Deterministic engine | `scoring.golden` | pass |
| Data provenance (ISO 27001 A.8.1) | Temporal pinning | `drift.recommend` | pass |
| Budget enforcement (SOC 2 CC6.1) | Cost ceiling | `budget.failclosed` | pass |
| Tenant isolation (ISO 27001 A.9.4) | Per-tenant state | `tenant.boundary` | pass |

This matrix is the seam between engineering and
[evidence packages](/topics/defendable-agents/compliance/evidence-packages/) —
each row is a control, a mechanism, and a green test that produced a record.
Run the suite in CI on every commit and the matrix is never more than one push
out of date.

A closing caution: passing the suite proves the mechanisms hold, not that the
system is correct or that governance is done. Verification is
[maintenance, not one-time setup](/topics/defendable-agents/compliance/operating-and-maintenance/) —
the tests decay the moment a variable, a weight, or a boundary changes and no
one updates the golden master.
