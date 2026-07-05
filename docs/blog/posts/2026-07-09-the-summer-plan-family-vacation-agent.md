---
description: "Every agent demo books a trip; almost none can defend the booking. We give a travel agent a real family — a nut allergy, a wheelchair, a vegan teenager, a hard budget — and a knowledge landscape published by four independent parties: a signed tourism hub, a ferry authority mid-timetable-handover, an identity-gated accessibility registry, and a tour operator selling detail over x402. Then we plant the authoring bug that would hide the allergy information from exactly the family that needs it, and watch the tooling catch it twice. Ships as a runnable example in kcp-agent 0.4.0."
date: 2026-07-09T09:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Knowledge Infrastructure
  - AI Agents
tags:
  - kcp
  - kcp-agent
  - x402
  - travel
  - agentic-web
  - federation
  - supersession
  - agent-identity
  - not-for
  - knowledge-context-protocol
authors:
  - totto
  - claude
---

# The Summer Plan: A Family Vacation the Agent Can Defend

Travel is where every vibes-based agent demo lives. "Book me a weekend in Lisbon" is the canonical showcase prompt — because it looks consequential and is actually consequence-free. If the restaurant recommendation is stale, you eat somewhere else.

Now change the family. An eight-year-old with a severe nut allergy. A grandmother who uses a wheelchair. A teenager gone vegan. A hard budget. Suddenly the failure modes are not "mediocre tapas." They are a child in an emergency room and a grandmother stranded at a dock because the agent planned against a ferry timetable that expired three weeks ago.

This is exactly the terrain where "the model read some websites and sounded confident" stops being acceptable — and where the question from [the HR post](2026-07-08-hiring-by-the-book-regulated-hr-agent.md) returns in vacation clothes: **"Show me how you decided that."**

So we built it. A complete family-vacation knowledge landscape, published by four independent parties, shipped as a runnable example in [kcp-agent](https://github.com/Cantara/kcp-agent) — and a narrated demo that drives the real CLI with no mocks.

<!-- more -->

---

## Four publishers, one archipelago

The Larsen family books a week on **Fjordholm** (a fictional archipelago — every place, business, and measurement here is invented). The knowledge their travel agent plans over is not one website. It is four parties with four different trust postures, exactly like the real travel web:

| Party | Role | What it exercises |
|---|---|---|
| **Fjordholm Tourism Board** | Signed regional hub, the agent's entry point | ed25519-signed manifest, `not_for` written correctly, federation refs |
| **Fjordholm County Ferries** | Timetable authority | Temporal windows + supersession (§4.22): winter hands over to summer |
| **National Accessibility Registry** | Verified accessibility declarations | `agent_identity` on the federation edge — registered agents only |
| **Fjord Safari Co.** | Commercial tour operator | Anonymous-paid x402 (§4.11), budget arithmetic in skip reasons |

The tourism board signs its manifest. The ferry company is mid-season-handover: the winter timetable carries `valid_until: 2026-06-20` and `superseded_by: summer-timetable`. The accessibility registry only serves registered agents — its federation edge declares `agent_identity: required` with a credential hint. And the safari operator gives away an overview for free but sells the detailed family-tour page at 0.30 USDC per request over x402, no account needed.

None of this is exotic. It is the ordinary shape of commercial knowledge — some of it public, some of it seasonal, some of it credentialed, some of it for sale.

---

## Act one: the unprovisioned agent, and every closed gate in writing

First run: the family's agent has no registry credential and a too-tight budget ceiling of 0.10 USDC.

```text
$ kcp-agent plan "wheelchair accessible cabin near the ferry, nut allergy safe dining,
    and a fjord safari for the kids" \
    --manifest examples/summer/tourism --follow --as-of 2026-07-12 \
    --methods free,x402 --budget 0.10

Signature: ✓ ed25519 signature verified (envelope key) · key tourism-2026
● 1. allergen-dining (score 23)  docs/allergen-dining.md  free
→ registry needs registry_pat before fetch [acquire registry_pat]
● 1. summer-timetable (score 17)  timetables/summer-2026.md  free
· winter-timetable: expired 2026-06-20 (superseded by summer-timetable)
· family-safari: over budget: 0.3 would exceed remaining 0.1 of 0.1 USDC
```

Walk the gates:

- **The hub's signature verifies before anything is planned.** If the manifest bytes had been tampered with, the run would have failed closed — no plan, no load, no spend.
- **The allergy unit is top-ranked.** Its `not_for` is written correctly — it excludes *pollen forecasts* and *pet hair in rental cars*, named in their own words — so the unit is wide open to the question it exists to answer. Hold that thought for act three.
- **The grandmother's timetable problem is already solved.** The planner, evaluating as of July 12, skips the winter timetable with a written reason: `expired 2026-06-20 (superseded by summer-timetable)`. The agent *cannot* plan her onto a sailing that no longer runs, and the skip is in the plan for anyone to audit.
- **The accessibility registry is selected but not fetched.** The edge says registered agents only; the agent holds no `registry_pat`; the plan says so and names the acquisition step. No scraping, no guessing.
- **The safari does the budget arithmetic in public.** `0.3 would exceed remaining 0.1 of 0.1 USDC` is not a vibe — it is a number the family can check.

Every closed gate carries a written reason. That is the whole discipline.

---

## Act two: the provisioned family agent

Same task, same landscape — but now the agent is set up the way a real family agent would be: registered with the accessibility registry, and with a vacation-research budget of 0.60 USDC.

```text
$ kcp-agent plan "…" --manifest examples/summer/tourism --follow --as-of 2026-07-12 \
    --methods free,x402 --budget 0.60 --credentials registry_pat

═ federated: registry
● 1. cabin-accessibility (score 20)  registry/cabins.md  free
● 1. family-safari (score 22)  tours/family-tour.md  0.30 USDC/request
pay-per-request: family-safari → 0.30 USDC/request
```

The registry edge opens: the agent presents its credential, the federation is followed, and the *verified* accessibility declarations are selected — including the registry's most important line, which is about what it *doesn't* know: Old Pier Cabins has **no declaration on file**. Absence of evidence is the finding. A vibes-based agent would have paraphrased the cabin's own marketing copy ("charming historic access"); this one reports that nobody has verified anything, which is precisely what a wheelchair user needs to know before a non-refundable deposit.

And the safari detail is simply bought: 0.30 USDC against a 0.60 ceiling, committed to the spend ledger, receipt in the plan. Anonymous-paid x402 — no account creation, no newsletter, no dark pattern. The [robot newsstand](2026-07-05-selling-news-to-robots.md) economics, applied to a family's Saturday.

---

## Act three: the footgun that would have hidden the allergy unit

Here is the part we care about most, because it is the part that goes wrong silently.

The tourism board's allergen unit has navigation metadata: intents, triggers (`allergy`, `nut`, `allergen`, `vegan`, `dining`…), and a `not_for` list. In the shipping manifest the `not_for` is written correctly. But there is an authoring mistake so natural that we found 110 instances of it in a real production manifest during [the HR red-team](2026-07-08-hiring-by-the-book-regulated-hr-agent.md): writing the exclusion as a *negation of the unit's own topic*.

The demo's third act makes exactly that edit to a pre-publish draft:

```yaml
not_for: ["questions not about nut-free or allergen dining"]
```

Reads fine to a human. To a term-matching planner, that string *contains the unit's own vocabulary* — so the family's actual question, "nut allergy safe dining," matches the exclusion, and the planner does what deterministic planners do:

```text
· allergen-dining: not_for declares it does not serve
  'questions not about nut-free or allergen dining'
```

The allergy unit is now deterministically hidden from exactly the family that needs it. Determinism is not the safety property — determinism *plus auditability* is. The skip reason is written into the plan, so the failure is visible instead of silent. And since [kcp-agent 0.4.0](https://github.com/Cantara/kcp-agent/releases/tag/v0.4.0), it never gets that far:

```text
$ kcp-agent validate examples/summer/tourism-draft

⚠ unit 'allergen-dining': not_for 'questions not about nut-free or allergen dining'
  contains the unit's own vocabulary (allergen, dining, free, nut) — term matching
  will gate this unit against its most natural questions; name the excluded topic
  in its own words, never as a negation of this unit's topic ("non-X", "outside X")
```

The lint we promised in the HR post's red-team list, catching the bug in the travel domain it was never written for — before publication, where authoring bugs should die.

---

## Why a vacation, of all things

Because travel is the demo everyone has already seen done badly, and the special-preferences family is the honest version of it. The same machinery that made the HR agent defendable — signed manifests, temporal supersession, identity-gated federation, priced access, written skip reasons — is what stands between the Larsens and the two failure modes that matter. Nothing in this post is a compliance feature. It is just what knowledge infrastructure looks like when the consumer is an agent and the stakes are a child's allergy.

Everything runs from the shipping CLI, no mocks — the demo suite is CI, so every narrated claim above is a regression test:

```sh
npm install -g kcp-agent   # or: npx kcp-agent
node examples/demos.js summer
```

The world itself is small enough to read in ten minutes: [`examples/summer/`](https://github.com/Cantara/kcp-agent/tree/main/examples/summer) — four manifests, a handful of markdown files, one signature envelope, and one deliberately planted footgun.

The Larsens make the last sailing.
