---
title: "Example: A Regulatory Q&A Agent"
description: "A worked example of a regulatory Q&A agent that answers every question with a provenance chain: each claim traces to a declared, temporally-pinned source unit, and stale rules are flagged."
image: assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp
---

# Example: A Regulatory Q&A Agent

Most "ask the documents" agents fail the only test that matters in a regulated setting: *where did that answer come from, and is the rule still in force?* A fluent paragraph with no traceable source is worse than no answer, because it reads as authoritative while being unaccountable. This page walks through a regulatory Q&A agent inside Lodestar — the example system for a regulated professional-services market — that refuses to answer without a provenance chain, and flags any rule that may have gone stale.

The design goal is narrow and honest: the agent does not *know* the rules. It selects declared source units deterministically, pins them in time, and answers only from what it selected. Every claim in the output points back to a governed unit and the date that unit was valid.

## Regulatory sources as declared KCP units

Each authoritative source — a statute section, a supervisory circular, an internal compliance policy — is a governed KCP unit with its own validity window. Nothing is embedded implicitly in a prompt. If a source is not declared, the agent cannot cite it, and if it cannot cite it, it will not use it. This is the same [manifest discipline](/topics/defendable-agents/kcp/manifest-basics/) used elsewhere in the stack, applied to knowledge rather than scoring models.

```yaml
kind: manifest
metadata:
  name: regulatory-corpus
  version: 4.2.0
  domain: compliance-qa
  description: Declared regulatory sources for the Q&A agent
  temporal:
    valid_from: "2026-01-01"
    refresh_interval: "P30D"
units:
  - id: reg.retention.records
    path: sources/records-retention-2025.md
    tags: [retention, records, in-force]
    description: Client-record retention obligations and minimum periods
  - id: reg.conflict.screening
    path: sources/conflict-screening-2024.md
    tags: [conflicts, screening, in-force]
    description: Mandatory screening steps before accepting a mandate
  - id: reg.marketing.restrictions
    path: sources/marketing-restrictions-2023.md
    tags: [marketing, restrictions, review-due]
    description: Permitted communications to prospective buyers
```

Declaring sources this way is described in [declaring governed units](/topics/defendable-agents/kcp/declaring-governed-units/). `kcp-agent` exposes `kcp_plan`, `kcp_load`, and `kcp_validate` as MCP tools; the harness only grants the Q&A domain those two read tools, `kcp_plan` and `kcp_load`. It cannot write, and it cannot reach any unit outside its declared paths — a [fail-closed boundary](/topics/defendable-agents/primitives/fail-closed-policy/), not a polite instruction.

## Deterministic selection, then answer

Selection is a pure function of the question tags and the manifest — not a similarity guess re-rolled per call. Given the same question and the same corpus version, `kcp_plan` returns the same units in the same order every time. The [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) then phrases the answer, but it may only phrase from the loaded units. The provenance chain is built by the harness, not asserted by the model.

Here is what one answer looks like on the wire — the prose the user reads is backed by a structured chain:

```json
{
  "question": "How long must client records be retained after a mandate closes?",
  "answer": "Client records must be retained for a minimum of ten years after the mandate is formally closed.",
  "provenance": [
    {
      "claim": "minimum retention period is ten years",
      "unit": "reg.retention.records",
      "corpusVersion": "4.2.0",
      "validFrom": "2026-01-01",
      "dataAsOf": "2026-06-15",
      "modelHash": "sha256:9f1c…a2"
    }
  ],
  "temporal": {
    "scoredAt": "2026-07-08T09:12:04Z",
    "sourceDates": ["2025-11-02"],
    "drift": []
  }
}
```

No provenance entry, no claim. If the model tries to state something the loaded units do not support, there is no unit to attach, and the harness drops the claim rather than emitting an unbacked assertion. That is the whole point: the [decision trace](/topics/defendable-agents/primitives/decision-traces/) is the answer's backbone, not an afterthought bolted on for auditors.

## Temporal drift flags stale rules

Every answer creates a temporal pin — `{scoredAt, dataAsOf, sourceDates[], modelVersion, modelHash}` — exactly as scoring operations do. On the next question touching the same unit, the [drift check](/topics/defendable-agents/primitives/temporal-pinning/) compares the live corpus against the pin:

| Drift reason | Trigger | Recommendation |
|---|---|---|
| DATA | `currentDataAsOf > pin.dataAsOf` | monitor (single non-model reason) |
| MODEL | corpus/model version changed | reanalyze |
| TEMPORAL | age in days > 30 | monitor |
| Two or more reasons | any combination | reanalyze |

So a marketing-restrictions source tagged `review-due` that has aged past its refresh interval surfaces as a TEMPORAL flag on the answer; if the corpus version has also moved, that is two reasons and the agent recommends reanalysis rather than serving the old rule silently. The user still gets an answer, but with a visible "this rule may be stale" banner and the date it was last valid.

## Worked exchange

> **Q.** "Can we send a follow-up email to a buyer who has not yet responded?"
>
> **A.** "Permitted, subject to a documented opt-out in the first communication." — source `reg.marketing.restrictions`, valid from 2023, `dataAsOf` 2026-03-01.
> **Notice:** TEMPORAL drift — this source is 128 days past its 30-day refresh window. Recommendation: monitor; confirm against the current circular before relying on it.

The agent answered, cited, and warned — in one pass. Every part of that exchange lands in the [append-only audit log](/topics/defendable-agents/primitives/audit-trail/) as a governed event carrying the question, the selected units, the provenance chain, and the drift verdict, which is what makes the exchange reproducible months later. See [reproduce a decision](/topics/defendable-agents/examples/reproduce-a-decision/) for how that replay works.

## Honest limits

This design guarantees **traceability, not correctness**. If a declared source itself contains a wrong or outdated rule, the agent will cite it faithfully and consistently — the error is applied visibly, with a date attached, which is how a reviewer catches it, but the agent will not catch it for you. Temporal pinning *detects* staleness; it does not *refresh* the corpus — someone still has to update the source unit and bump the manifest. And the model at the edge remains a model: it can still phrase a supported claim awkwardly or over-generalise within the bounds of a loaded unit. Governance here is maintenance — keeping sources declared, dated, and refreshed — not a one-time setup. For the broader argument on why traceable process beats confident fluency, see [what defendable means](/topics/defendable-agents/argument/what-defendable-means/).
