---
title: "Tutorial 7: Multi-Tenant Isolation"
description: "Separate shared public data from per-tenant confidential scores and plans using per-tenant state directories the governance harness enforces, then prove the boundary with a test."
image: assets/images/kcp-024-00-from-domain-to-receipt.webp
---

# Tutorial 7: Multi-Tenant Isolation

By this point in the field guide you have a governed session that scores buyers, records a budget ledger, and writes an append-only audit log. In this tutorial we make Lodestar serve more than one tenant at a time without letting one tenant's confidential decisions leak into another's.

The distinction that carries the whole design is this: **the raw signal graph is shared, the decisions made on top of it are not.** Every tenant operating in the same regulated professional-services market sees the same public events — a firm posts a mandate, a company changes its registration, a buyer publishes a tender. That data is public by construction (see [data minimisation](/topics/defendable-agents/compliance/control-mapping/) — Lodestar processes public data only). But the moment a tenant scores a buyer, that score, its variable trace, and any generated plan become confidential. Two tenants can look at the identical signal and arrive at wildly different Winnability assessments, and neither is allowed to see the other's.

Isolation here is a **directory boundary, not a policy note.** We do not write "please don't read the other tenant's scores" in a comment and hope. The harness resolves each tenant to a distinct state directory, and a governed operation physically cannot address a path outside its tenant's root.

## The layout

Shared, read-only data lives once. Per-tenant confidential state lives under a tenant root, one directory per tenant.

```bash
lodestar/
  shared/
    signals/            # public events, shared graph — every tenant reads this
    companies/          # public registration + firm data
  tenants/
    acme/
      state/
        scores/         # confidential buyer/match scores
        plans/          # confidential GTM plans, playbooks
        pins/           # temporal pins for this tenant's decisions
        audit.jsonl     # this tenant's append-only log
      harness.yaml
    globex/
      state/
        scores/
        plans/
        pins/
        audit.jsonl
      harness.yaml
```

Each tenant gets its own harness, its own audit log, its own budget ledger, and its own map of temporal pins. Nothing about a governed session spans tenants. If you have read [Tutorial 3](/topics/defendable-agents/tutorials/03-governed-session/), this is the same governed session you already built — instantiated once per tenant, rooted at a different directory.

## A tenant config

The `harness.yaml` for a tenant points its writable paths at the tenant root and its read-only domains at the shared graph. The `state_root` is the load-bearing line: everything the session writes is resolved relative to it.

```yaml
tenant: acme
state_root: ./tenants/acme/state

governance:
  domains:
    - manifest: ./shared/knowledge.yaml   # shared, read-only signal + model units
      paths:
        - ./shared/signals
        - ./shared/companies
      tools: [kcp_plan, kcp_load]

policy:
  fail_closed: true
  audit_all: true
  max_units: 64
  strict: true
  budget:
    amount: 1000
    currency: units
  context_budget: 200000

audit:
  path: ./tenants/acme/state/audit.jsonl   # under state_root — never shared
```

Two things to notice. First, the `domains` block references the shared manifest and shared paths — the signal graph and the [scoring-model KCP units](/topics/defendable-agents/kcp/declaring-governed-units/) are declared once and loaded read-only by every tenant, so a model is selected deterministically and never silently swapped per tenant. Second, `audit.path` and everything derived from `state_root` sit under `tenants/acme/`. The globex config is identical except every path says `globex`.

## Proving isolation with a test

A boundary you have not tested is a boundary you are guessing about. The test does two things: it confirms two tenants scoring the same shared signal write to separate state, and it confirms a session rooted at one tenant cannot write into another's directory.

```typescript
import { GovernedSession } from "../src/session";
import { readFileSync, existsSync } from "node:fs";

test("tenants share signals but isolate scores", async () => {
  const signal = loadSharedSignal("sig-4417");   // same public event for both

  const acme = new GovernedSession({ config: "tenants/acme/harness.yaml" });
  const globex = new GovernedSession({ config: "tenants/globex/harness.yaml" });

  const a = await acme.scoreBuyer("buyer-88", signal);
  const g = await globex.scoreBuyer("buyer-88", signal);

  // Same input, deterministic planner — but confidential outputs land apart.
  expect(a.total).not.toBeUndefined();
  await acme.end();
  await globex.end();

  // Each tenant's decision is only in its own audit log.
  const acmeLog = readFileSync("tenants/acme/state/audit.jsonl", "utf8");
  const globexLog = readFileSync("tenants/globex/state/audit.jsonl", "utf8");
  expect(acmeLog).toContain("buyer-88");
  expect(globexLog).toContain("buyer-88");
  expect(acmeLog).not.toContain("globex");
});

test("a session cannot write outside its tenant root", async () => {
  const acme = new GovernedSession({ config: "tenants/acme/harness.yaml" });
  await expect(
    acme.persistPlan("buyer-88", { path: "../globex/state/plans/leak.json" })
  ).rejects.toThrow(/outside tenant root|fail_closed/);
  expect(existsSync("tenants/globex/state/plans/leak.json")).toBe(false);
});
```

The second test is the one that matters. `persistPlan` resolves the requested path against `state_root` and rejects anything that escapes it. Because `fail_closed: true`, an out-of-root write is not clamped or sanitised into a "safe" location — the operation throws and emits an audit event. That is the [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) doing exactly its job.

## Why the boundary is a directory, not a filter

You could imagine tagging every score with a `tenantId` and filtering reads by it. That works right up until a query forgets the filter, and then you have a silent cross-tenant leak with no trace. A directory boundary fails loudly instead: a mis-rooted path either does not exist or is refused. The tenant isolation control in the [compliance mapping](/topics/defendable-agents/compliance/control-mapping/) (ISO 27001 A.8.3) is satisfied by per-tenant state, not by a `WHERE` clause you have to remember to write.

## Honest limits

Directory isolation protects confidential *outputs* — scores, pins, plans, logs. It does not encrypt them, and it does not defend against a process that runs with credentials to more than one tenant root. If your deployment gives one operating account write access across `tenants/`, isolation is only as strong as that account's discipline; treat cross-tenant access as a privileged, separately audited path. And the shared graph is genuinely shared: if a public signal is wrong, every tenant scores on the same wrong input. That is by design — determinism guarantees process, not correctness — but it means a bad shared record has blast radius across all tenants at once. Isolation is maintenance, not a one-time switch: every new writable path you add to a session has to be rooted, or it becomes the next leak.

---

Next, [Tutorial 8: Evidence Export](/topics/defendable-agents/tutorials/08-evidence-export/) turns a tenant's audit log and pins into a defensible evidence package. For the reasoning behind sharing data but isolating decisions, see [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/) and the [Lodestar case study](/topics/defendable-agents/reference/case-study-lodestar/).
