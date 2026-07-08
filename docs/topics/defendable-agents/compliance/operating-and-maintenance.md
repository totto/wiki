---
title: "Operating & Maintaining One"
description: "Governance is maintenance, not a one-time build: nightly drift scans, model review cadence, signing-key rotation, audit-log retention and integrity, and clear ownership."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Operating & Maintaining One

A defendable agent is not something you build once and hang on the wall. The
whole point of the machinery — the append-only log, the temporal pins, the
deterministic scoring engine — is that it keeps telling you the truth about
itself as the world drifts underneath it. That only works if someone keeps it
running. Governance is maintenance. If nobody owns the upkeep, the controls
quietly rot and you are left with a system that *looks* governed and isn't.

Here is what operating a Lodestar-style deployment actually costs, week to week.

## The nightly drift scan

Every score in the system carries a temporal pin: `{scoredAt, dataAsOf,
signalDates[], modelVersion, modelHash}`. Pins do nothing until you check them.
The nightly job walks every live pin, compares it against current state, and
records the recommendation. See [temporal pinning](/topics/defendable-agents/primitives/temporal-pinning/)
for the pin structure and [drift detection](/topics/defendable-agents/primitives/drift-detection/)
for how the reasons combine.

The rule is fixed and deterministic:

- **DATA drift** if `currentDataAsOf > pin.dataAsOf`
- **MODEL drift** if the model version changed since the pin
- **TEMPORAL drift** if `ageInDays > maxAgeDays` (default 30)

Two or more reasons, or model drift alone, means reanalyse. A single
non-model reason means monitor. Nothing means the score still stands.

```bash
# cron: nightly at 02:00, fail-closed, results written to the audit log
0 2 * * *  lodestar drift-scan \
  --harness /etc/lodestar/harness.yaml \
  --max-age-days 30 \
  --emit reanalysis_triggered,monitoring_check \
  --budget-op reanalysis   # 5 units each, ledger-enforced
```

Two honest caveats. First, the scan **detects** staleness; it does not
**refresh** data. A `reanalysis_triggered` event is a to-do, not a fix — if the
upstream signal feed is down, every pin will keep flagging DATA drift and the
scan will cheerfully re-flag it forever. Second, reanalysis spends budget. Each
`reanalysis` operation costs 5 units against the session ceiling, so a scan over
a large book can exhaust a [budget ceiling](/topics/defendable-agents/primitives/budget-and-bounding/)
and start emitting `budget_exceeded`. That is correct fail-closed behaviour, but
you must size the ceiling for the maintenance load, not just the interactive one.

## Model review cadence

The scoring models are declared as governed KCP units, selected by manifest and
pinned by hash, so they are never silently swapped (see
[declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/)).
That gives you a clean seam for review. On a fixed cadence — quarterly is a
sensible default — the model owner sits down with the last quarter's decision
traces and asks the only question that matters: are the variables still measuring
what we think they measure?

Remember the limit here. Determinism guarantees **process, not correctness**. A
mis-specified variable — say a `signal-freshness` decay that is too aggressive
for your sector — is applied *consistently* to every buyer. That is a feature:
the error is visible in every trace and reproducible on demand, which is exactly
how the review catches it. But no amount of governance turns a wrong weight into
a right one. The review is where human judgement earns its keep. When it decides
a variable or weight must change, that is a model version bump, which the next
drift scan will surface as MODEL drift across every affected pin — so the change
propagates loudly, not quietly. Bump discipline is covered in
[versioning models](/topics/defendable-agents/decisions/versioning-models/).

## Key rotation and log integrity

The [audit trail](/topics/defendable-agents/primitives/audit-trail/) is
append-only JSONL, one event per line, fsynced on flush. Append-only is a
property you have to *keep*, not one you get for free. Two operational duties
protect it:

- **Signing-key rotation.** Each day's log segment is sealed and signed at
  rotation. Rotate the signing key on a fixed schedule (90 days is typical) and
  on any suspected compromise. Old keys are retained read-only so historic
  segments stay verifiable — you never destroy the means to check yesterday's
  log just because today's key is new.
- **Integrity verification.** A separate job re-hashes sealed segments and
  checks the chain, so tampering or truncation is caught by a machine on a
  schedule rather than by an auditor eighteen months later.

```yaml
# retention.yaml — log lifecycle, separate from harness.yaml
audit:
  path: /var/lib/lodestar/audit
  segment: daily            # one sealed file per day
  fsync_on_flush: true
retention:
  hot_days: 90              # queryable on fast storage
  archive_years: 7          # sealed, signed, write-once
  verify_cron: "30 3 * * *" # nightly re-hash + chain check
signing:
  rotate_days: 90
  retain_old_keys: true     # historic segments stay verifiable
```

Set retention to match the obligation you are defending — the compliance mapping
ties the log to ISO 27001 A.12.4 and the per-session records to GDPR Art. 30, and
those regimes carry their own minimums. The
[evidence packages](/topics/defendable-agents/compliance/evidence-packages/)
page shows what you export from these segments when someone asks you to prove a
decision.

## Who owns it

Controls with no owner are decoration. Name people, not teams-in-the-abstract:

| Duty | Owner | Cadence |
|---|---|---|
| Nightly drift scan health | Platform on-call | Daily |
| Model review & version bumps | Model owner | Quarterly |
| Signing-key rotation | Security | 90 days |
| Log integrity + retention | Security | Nightly / audited |
| Ceiling & cost review | Product owner | Monthly |
| Tenant isolation checks | Platform | Per release |

The last row is not optional either: [multi-tenancy](/topics/defendable-agents/primitives/multi-tenancy/)
isolation is a directory boundary the harness enforces, and boundaries are worth
re-testing after every change that touches state paths.

## Maintenance is not optional

Every mechanism in this stack degrades if left alone. Pins accumulate staleness.
Models drift out of alignment with the market. A [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/)
that once protected you can, over-tuned, start blocking legitimate work — and the
only way you learn that is by watching the `budget_exceeded` and gate-denial
events and reacting. None of this is a defect. It is the honest shape of running
a real system: the governance is the maintenance, and the maintenance is the job.
If you are not prepared to fund the upkeep, you do not have a defendable agent —
you have a very well-documented one that used to be true.

For where this sits in the whole, see the
[case study](/topics/defendable-agents/reference/case-study-lodestar/) and the
[anti-patterns](/topics/defendable-agents/reference/anti-patterns/) that
maintenance is meant to keep you out of.
