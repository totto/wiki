---
title: "Multi-Tenancy & Isolation"
description: "How Lodestar separates shared public data from per-tenant confidential decisions using per-tenant state directories the governance harness owns, not a policy note."
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# Multi-Tenancy & Isolation

Most agent systems that serve more than one customer end up with a single pile of state and a hopeful comment somewhere saying "we filter by tenant ID". That comment is a promise, not a boundary. The first bug in the filter, the first forgotten `WHERE` clause, the first prompt that talks the model into reading the wrong record, and one buyer's confidential scores land in front of a competitor. In [Lodestar](/topics/defendable-agents/reference/case-study-lodestar/) I refused to build isolation as a promise. It is a boundary you can point at on disk.

## The shared/confidential split

The key observation is that not all data is confidential. Lodestar operates in a regulated professional-services market where the raw signals — public events, company records, market movements — are the same for everyone. Every tenant watching the same firms sees the same events. There is nothing secret about a public filing.

What is confidential is what each tenant *does* with that shared data: which buyers they prioritise, how they score them, the go-to-market plans they generate. That is the tenant's strategy, and it must never leak.

So the data cleanly divides in two:

| Class | Examples | Visibility |
|-------|----------|------------|
| **Shared** | signals, company/firm records, public market events | Every tenant sees the identical stream |
| **Confidential** | buyer scores, match scores, account tiers, go-to-market plans, playbooks | One tenant only, never crosses |

The shared side can be one dataset because there is nothing to protect. The confidential side must be physically partitioned. Trying to keep both in one store and separating them with query predicates is exactly the fragile design I wanted to avoid.

## Isolation is a directory boundary, not a policy note

Here is the design decision that matters. Per-tenant confidential state does not live in a shared database column tagged with a tenant ID. It lives in an isolated per-tenant state directory, and the [governance harness](/topics/defendable-agents/architecture/governance-harness/) enforces which directory a session may touch.

```yaml
# harness.yaml — a session is bound to exactly one tenant's state root
governance:
  domains:
    - manifest: knowledge.yaml
      paths: ["models/**"]
      tools: [kcp_plan, kcp_load]
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000
  strict: true
  budget: { amount: 1000, currency: units }
  context_budget: 200000
audit:
  path: state/tenant-a/audit/session.jsonl
tenant:
  id: tenant-a
  state_root: state/tenant-a
```

```text
state/
├── tenant-a/
│   ├── audit/          # this tenant's append-only log
│   ├── pins/           # this tenant's temporal pins
│   ├── ledger/         # this tenant's budget ledger
│   └── decisions/      # scores, tiers, plans — confidential
├── tenant-b/
│   ├── audit/
│   ├── pins/
│   ├── ledger/
│   └── decisions/
└── shared/
    └── signals/        # public events — read-only, identical for all
```

A [governed session](/topics/defendable-agents/architecture/overview/) resolves `state_root` once, at start, and every write it makes — the [audit log](/topics/defendable-agents/primitives/audit-trail/), the [budget ledger](/topics/defendable-agents/primitives/budget-and-bounding/), the [temporal pins](/topics/defendable-agents/primitives/temporal-pinning/) — is rooted under that path. There is no code path that writes a decision to a directory the session was not bound to, because the session never holds a handle to another tenant's root. A leak would require constructing a path outside `state_root`, which is the kind of thing a path check catches and refuses, fail-closed, rather than a filter you hope was written correctly.

This is the difference between a boundary and a note. A `WHERE tenant_id = ?` clause is code you must get right on every single query. A directory root resolved once is a boundary the whole session inherits. You cannot forget to apply it, because nothing hands you the ability to escape it.

## Control mapping

This satisfies **ISO 27001 A.9.4** (access control to information and systems): tenant confidential state is segregated by construction, and the segregation is auditable — you can list the directories and see that tenant B's session never opened tenant A's root. It is recorded, not asserted. See the full [control mapping](/topics/defendable-agents/compliance/control-mapping/) for how this sits alongside audit logging and access gating.

## Cross-tenant leakage risks — and where they actually live

Being honest about a security boundary means naming the ways it can still fail.

- **The shared side is a fan-in channel.** Every tenant reads the same signal stream, so anything that pollutes shared data reaches everyone. A poisoned signal is a cross-tenant blast radius. This is where a prompt injection lands — see [catch an injection](/topics/defendable-agents/examples/catch-an-injection/). The mitigation is that shared data is read-only to sessions and the deterministic engine only consumes declared variables; a hostile string in a signal cannot reach into another tenant's decisions because decisions are computed, not narrated.
- **Aggregate leakage.** Even with directories sealed, cross-tenant *statistics* — "how many tenants scored this firm Very high" — can leak strategy if exposed. Lodestar simply does not compute cross-tenant aggregates in a tenant session; there is no code that reads two roots.
- **Model swaps.** If tenant A's session silently loaded tenant B's scoring model you would get a subtle correctness leak. Models are declared as [governed KCP units](/topics/defendable-agents/kcp/declaring-governed-units/) and selected deterministically, so the model in play is pinned and recorded, never ambient.
- **The audit log is the check.** Because every write carries `sessionId` and lands in the tenant's own log, you can prove after the fact that no session touched a foreign root. Isolation you can verify beats isolation you assert.

## Honest limits

A directory boundary is only as strong as the process that owns the filesystem. If two tenants share an OS user and one can read the other's directory, the boundary is administrative, not cryptographic — for hard separation you put tenants in separate trust domains, not just separate folders. And multi-tenancy is not a feature you switch on once; it is [maintenance](/topics/defendable-agents/compliance/operating-and-maintenance/). Every new operation that writes state is a new chance to write it to the wrong root, so the harness has to remain the only thing that resolves paths. The moment application code starts computing its own state paths, the boundary is back to being a promise.

The rule I keep: the harness owns the root, sessions inherit it, and nothing else is allowed to name a path. Everything else about tenancy follows from that.
