---
description: "Every enterprise has the same documentation estate: an intranet nobody trusts, a wiki where the dev docs outrank the prod docs, crown-jewel recipes one bad link away from a press release, and HR pages that were never meant for a machine to read. We give a fictional dairy cooperative — Melkeveien SA, Norwegian for 'the Milky Way' — a complete KCP estate: one signed hub, eight domains, nine manifests. Then five agents with five very different jobs walk the same knowledge, and every closed door has a written reason: environment slicing, a 2027 regulation with a start date, audience targeting, HSM attestation for the formulations, an identity-gated ERP vendor, and a subscription that buys a premium rate tier. Ships as a runnable example in kcp-agent 0.5.0."
date: 2026-07-10T09:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Knowledge Context Protocol
  - AI Agents & the Agentic Web
tags:
  - kcp
  - kcp-agent
  - enterprise
  - federation
  - supersession
  - attestation
  - audience
  - not-for
  - environment-context
  - knowledge-context-protocol
authors:
  - totto
  - claude
image: assets/images/milky-way-02-tribal-knowledge-cannot-protect.webp
---

# The Milky Way: An Enterprise Documentation Estate the Agent Can Defend

Every company we have ever worked with has the same documentation estate. An intranet nobody fully trusts. A wiki where the sandbox instructions outrank the production ones because someone wrote them more enthusiastically. A quality manual with a regulation that isn't in force yet, sitting right next to the one that is. Crown-jewel R&D documents protected by nothing but a folder name. HR pages that were written for humans and are now being read by machines. And a vendor portal whose documentation is somebody's bookmark.

Ask "where is the current truth?" and the honest answer is *tribal knowledge* — the people who know which page is real, which one is stale, and which one you must never paste into a press release.

![Tribal knowledge cannot protect data from AI: an AI agent's search beam sweeping into the tangled ball of an enterprise wiki — draft policies, old docs, temp files, R&D secret sauce, salary guides, current law all knotted together — with four hazards called out: dev docs outranking production docs because they were written more enthusiastically, draft 2027 regulations sitting directly next to current law, crown-jewel R&D recipes protected by nothing but a folder name, and sensitive salary guides written for humans being scraped and synthesized by bots — every intranet relies on human tribal knowledge to avoid these landmines; agents expose them instantly](../../assets/images/milky-way-02-tribal-knowledge-cannot-protect.webp)

Now put an agent in that estate. Not one agent — five, with five different jobs: an audit-prep agent, a communications agent, an HR question, an R&D agent, and a sustainability reporter. The previous posts in this series gave one agent one gate at a time: [a newsstand](2026-07-05-selling-news-to-robots.md) sold it articles, [an HR world](2026-07-08-hiring-by-the-book-regulated-hr-agent.md) made it defend a hiring decision, [a family vacation](2026-07-09-the-summer-plan-family-vacation-agent.md) raised the stakes. This one is the enterprise case: **a whole estate, where classification, audiences, validity windows and vendor boundaries are machine-enforced manifest facts instead of tribal knowledge.**

So we built it. **Melkeveien SA** — a fictional farmer-owned dairy cooperative; *Melkeveien* is Norwegian for "the Milky Way" — publishes its entire documentation landscape as one signed federation, shipped as a runnable example in [kcp-agent 0.5.0](https://github.com/Cantara/kcp-agent/releases/tag/v0.5.0).

<!-- more -->

![Infographic — The Milky Way: defending the enterprise documentation estate. The group documentation hub of Melkeveien SA at the center, signed with ed25519 so tampered data causes fail-closed, radiating to every domain: the integration platform with machine-readable vendor gates and OpenAPI units, quality & food safety with date-based validity gating, R&D with secret formulations behind HSM attestation and not_for exclusions, people with audience [human] HR processes, brand & comms with the public CC-BY press kit, sustainability with CSRD overlap disambiguated by superseded_by, and Orion Business Systems behind identity, rate-limit tiers and subscriptions — plus the five agents' outcomes and the bottom strip on why KCP beats traditional retrieval: deterministic written reasons instead of hallucinated substitutes](../../assets/images/milky-way-00-defending-the-estate.webp)

---

## One signed hub, eight domains

The estate is nine manifests. The group documentation hub is signed with ed25519 and federates to eight domains, each with its own trust posture — exactly the shape of a real enterprise:

| Domain | Role | What it exercises |
|---|---|---|
| **Group Documentation Hub** | Signed entry point | ed25519-signed manifest, federation to 8 domains |
| **Integration Platform** | ERP/MES/logistics integrations | Rate-limit tiers, machine-readable OpenAPI unit, ADR supersession chain (§4.22) |
| **Dev Mirror** | Sandbox + mock data | `context: [dev]` on the federation edge — invisible to prod agents |
| **Quality & Food Safety** | HACCP, audits | Future regulation with `valid_from: 2027-01-01` — visible, dated, excluded |
| **R&D** | Formulations (crown jewels) | `access: restricted` + HSM attestation, `not_for` in the excluded topics' own words |
| **People** | HR processes | `audience: [human]` — the agent is turned away from the salary document |
| **Brand & Communications** | Press kit, guidelines | Public, CC-BY — where the comms agent legitimately lands |
| **Sustainability** | CSRD reporting | Annual handover: overlap window disambiguated by `superseded_by` |
| **Orion Business Systems** | External ERP vendor | `agent_identity` gate on the edge, subscription payment, premium rate tier |

![Mapping the Melkeveien architecture: one signed hub, eight domains, nine manifests — a hub-and-spoke diagram with the ed25519-signed group documentation hub at the center and spokes to the integration platform, dev mirror, quality & food safety, R&D vault, brand & communications, sustainability, people manifold, and Orion Business Systems as the external vendor — a complete fictional dairy cooperative with highly realistic enterprise boundaries](../../assets/images/milky-way-04-melkeveien-architecture.webp)

Everything is fictional — the cooperative, the Stjerneholmen plant, the vendor, the regulation, every number. But nothing is exotic. Every one of these gates is something an enterprise already *means* — in access-control spreadsheets, information-classification policies, and the heads of long-tenured employees. Here they are manifest facts a planner can enforce.

![Enforcing trust postures across eight domains, as one table: each domain's role, its KCP enforcement gate, and the operational impact — the signed hub's ed25519 validation means tampered bytes fail closed, the integration platform's rate-limit tiers and ADR chains mean machine-readable quotas, the dev mirror's context [dev] is invisible to prod agents, quality's valid_from temporal gating excludes future laws, R&D's HSM attestation plus not_for is a semantic topic firewall, people's audience [human] turns bots away, brand's CC-BY is the legitimate landing zone, and Orion's agent_identity edge carries subscription payments](../../assets/images/milky-way-05-trust-postures-eight-domains.webp)

---

## The audit agent: production context, and a regulation that isn't law yet

First job: prepare for the food safety authority's audit at the Stjerneholmen plant. The agent runs in production context, unprovisioned.

```text
$ kcp-agent plan "prepare for the food safety authority audit at the Stjerneholmen plant" \
    --manifest examples/milky-way/hub --follow --as-of 2026-07-06 --env prod

Signature: ✓ ed25519 signature verified (envelope key) · key milkyway-2026
· dev-mirror context ["dev"] excludes env 'prod'
→ vendor needs vendor_portal_token before fetch [acquire vendor_portal_token]
● 1. audit-checklist (score 22)  docs/audit-checklist.md  free
● 2. haccp-plan (score 18)  docs/haccp-plan.md  free
· hygiene-regulation-2027: not active until 2027-01-01
```

Four decisions, all in writing:

- **The hub's signature verifies before anything is planned.** Tampered bytes would have failed closed — no plan, no load, no spend.
- **The dev mirror never enters the plan.** Its federation edge declares `context: [dev]`; the agent runs with `--env prod`; the sandbox guide with its mock data is not merely down-ranked, it is *invisible* — with the reason written down. This is the answer to the oldest wiki failure there is: the enthusiastic sandbox page outranking the production one.
- **The vendor edge is named but not crossed.** Orion's documentation requires agent identity; the plan says which credential would open it (`vendor_portal_token`) instead of scraping around the gate.
- **The 2027 hygiene regulation is visible, dated, and excluded.** `not active until 2027-01-01` — the quality team can publish next year's regulation *today* without any risk of an agent citing it as current law. The [ferry timetable machinery](2026-07-09-the-summer-plan-family-vacation-agent.md) from the vacation post, wearing a lab coat.

![Agent 1, filtering by environment and time: the audit agent running with --env prod, its job to prepare for the food safety audit at the Stjerneholmen plant — the dev mirror edge is Blocked with the written reason 'context [dev] vs agent prod', and the quality docs are Filtered on 'valid_from: 2027-01-01'; the enthusiastic sandbox page is not down-ranked, it is invisible, and next year's hygiene regulation is visible and dated but strictly excluded from current law](../../assets/images/milky-way-06-filtering-by-environment-and-time.webp)

---

## The comms agent: turned away in the excluded topic's own words

Second job: draft the press release for the oat drink launch. This is the run that keeps compliance officers awake — because the estate *contains* the confidential formulations, and "oat drink" appears in both the press kit and the recipe file.

```text
$ kcp-agent plan "draft the press release for the oat drink launch" \
    --manifest examples/milky-way/hub --follow --as-of 2026-07-06 --env prod

· formulations: not_for declares it does not serve 'press releases'
● 1. press-kit (score 23)  docs/press-kit.md  free
```

R&D's formulations unit carries `not_for: ["press releases", "marketing copy", "supplier newsletters"]` — the excluded topics named *in their own words*, exactly the authoring discipline the [HR red-team](2026-07-08-hiring-by-the-book-regulated-hr-agent.md) established and the [vacation post's footgun](2026-07-09-the-summer-plan-family-vacation-agent.md) demonstrated the wrong way round. The comms agent's task contains "press release"; the exclusion matches; the crown jewels stay in the vault — and the agent lands on the brand team's CC-BY press kit, which is where it was always supposed to be.

The near-miss is the point. A retrieval system that had embedded the whole estate would happily have surfaced the sugar percentages to the press-release prompt, because they are *relevant*. Relevance was never the question. Whom the document serves is the question, and here it is a manifest fact.

![Agent 2, excluding topics in their own words: the comms agent's query 'draft an oat drink press release' hits the R&D vault node, whose not_for list — 'press releases', 'marketing copy' — matches the query term and returns Access Denied, while the arrow continues down to the CC-BY press kit node and Access Granted; exclusions are named in the authors' own words, the crown jewels stay in the vault, and the agent legitimately lands on public brand guidelines](../../assets/images/milky-way-07-excluding-topics-in-their-own-words.webp)

---

## The salary question: same estate, different reader

Third job is a single question asked twice. HR's salary-review document is marked `audience: [human]` — it describes a process involving managers and negotiations, written for employees, never meant to be paraphrased by a bot into something that sounds like policy.

```text
$ kcp-agent plan "how does the annual salary review work" --manifest examples/milky-way/people

· salary-review: audience ["human"] excludes role 'agent'

$ kcp-agent plan "how does the annual salary review work" --manifest examples/milky-way/people --role human

● 1. salary-review (score 25)  docs/salary-review.md  free
```

Same manifest, same question, same relevance score. The only thing that changed is who is asking — and the publisher decided that, not the reader. `audience` is the smallest gate in the protocol and possibly the most humane: it lets a documentation owner say *this page is for people* and have that mean something.

![Agent 3, the smallest and most humane gate: one HR policy document, two readers — the human user's path ends in Access Granted, the bot agent's path in Access Denied, with the KCP gate audience: [human] underneath and the verdict in large type: same document, same relevance, different identity; the publisher decides who reads the document, not the reader](../../assets/images/milky-way-08-the-smallest-most-humane-gate.webp)

---

## The R&D agent: the crown jewels, cold and warm

Fourth job: cut the sugar in the oat drink formulation and update the ERP recipe integration. This is the run that crosses the most gates, so we run it twice.

**Cold** — no attestation, no credentials:

```text
○ 1. formulations (score 27)  docs/formulations.md  free
   why: intent matches 3 term(s); triggers match 4 term(s); id/path matches 1 term(s);
   restricted: requires attestation the agent cannot present;
   access 'restricted': agent holds no credentials
```

Look at that line carefully, because it is the whole philosophy in one row. The formulations unit is **ranked first** — the planner is honest that this is the most relevant document in the estate — and it is **not load-eligible**, with both reasons written out. The hollow circle is the plan saying: *I know exactly what you need, and I can tell you exactly why you cannot have it.* No silent omission, no hallucinated substitute.

![The anatomy of a deterministic refusal: the hollow circle from the plan output, enlarged, with three callouts — no silent omissions, no hallucinated substitutes, absolute auditability — above the estate's rule in quotation marks: every document that is not loaded has a written reason you could read to an auditor](../../assets/images/milky-way-11-anatomy-of-a-deterministic-refusal.webp)

**Warm** — the agent presents attestation against the cooperative's HSM, carries the vendor credential, and can settle subscriptions:

```text
$ kcp-agent plan "cut the sugar in the oat drink formulation and update the ERP recipe integration" \
    --manifest examples/milky-way/hub --follow --as-of 2026-07-06 --env prod \
    --attest melkeveien-hsm --credentials sso_badge,vendor_portal_token --methods free,subscription

Trust: ✓ attestation required — agent can present it
● 1. formulations (score 27)  docs/formulations.md  free
═ federated: vendor
● 1. erp-integration-guide (score 25)  docs/erp-integration-guide.md  subscription
Budget: tier premium · unlimited req/min
```

Three doors open in one run. The HSM attestation satisfies R&D's `trust.agent_requirements`, and the restricted formulations flip from ○ to ●. The `vendor_portal_token` opens Orion's federation edge — the external vendor's documentation joins the plan on the vendor's terms, not via a scraped PDF. And the subscription does something quietly new for this series: it doesn't just buy *access*, it buys *class of service*. Orion's manifest declares rate-limit tiers — anonymous agents get 10 requests a minute, authenticated ones 300, subscribers unlimited — and the plan resolves the tier *before* the first request, so the agent designs its batch sizes inside the quota instead of discovering it at the 429.

![Agent 4, cold versus warm access to the crown jewels, in two columns: the cold run presents no credentials — R&D formulations ranked first for relevance but trust.agent_requirements met: FALSE, not load-eligible, and the Orion vendor edge locked; the warm run asserts complete credentials — HSM attestation confirmed flips the formulations to Loaded, and the vendor_portal_token opens the Orion edge into an authenticated rate tier](../../assets/images/milky-way-09-cold-vs-warm-crown-jewels.webp)

---

## The sustainability reporter: mid-handover, and the overlap decides itself

Fifth job, smallest and maybe most enterprise of all: scope 3 emissions for the sustainability report — asked on 2026-07-06, when the CSRD 2025 report (`valid_until: 2026-12-31`) and the CSRD 2026 methodology (`valid_from: 2026-07-01`) are **both valid**. Every enterprise has this overlap window; most wikis resolve it by whoever answers the Slack thread first.

```text
$ kcp-agent plan "scope 3 emissions for the sustainability report" \
    --manifest examples/milky-way/esg --as-of 2026-07-06

● 1. csrd-2026 (score 22)  docs/csrd-2026.md  free
· csrd-2025: superseded by csrd-2026 (successor active)
```

The 2025 report declares `superseded_by: csrd-2026`; the successor is active; precedence — not expiry — decides the overlap day, and the decision is written into the plan. The ESG team's restated emissions figures land in the report from the current methodology, deterministically, on the one day of the year when a human would have had to *know*.

![Agent 5, deterministic supersession in overlap windows: a 2026 timeline with the CSRD 2025 report (valid_until 2026-12-31) and the CSRD 2026 methodology (valid_from 2026-07-01) both valid on the July 6 query date, and the superseded_by: csrd-2026 arrow handing over between them — precedence, not expiry, deterministically resolves the overlap without a human Slack thread](../../assets/images/milky-way-10-supersession-in-overlap-windows.webp)

---

## Why a dairy cooperative, of all things

Because the enterprise documentation estate is the terrain where every "AI knowledge assistant" is being deployed right now, mostly by pointing an embedding model at the whole wiki and hoping. The Milky Way is what the alternative looks like: not one clever gate, but classification, audiences, validity windows, environments, attestation and vendor boundaries as *published, machine-enforced facts* — the same machinery that priced a newspaper article, defended a hiring decision, and got the Larsen family onto the right ferry, now running a whole company's knowledge at once.

![From tribal knowledge to cryptographic boundaries, side by side: the old way — a magnifying glass over the enterprise wiki's pile of draft policies, old docs, secret sauce, salary guides and current law, hoping the LLM figures out relevance; the KCP way — a circuit of machine-enforced validity, audience, and access gates; the verdict across the bottom: relevance is not the question — whom the document serves is the question](../../assets/images/milky-way-03-tribal-to-cryptographic-boundaries.webp)

Five agents walked the estate. The audit agent never saw the sandbox. The comms agent never saw the recipe. The salary document only spoke to humans. The crown jewels opened for hardware attestation and nothing less. The overlap year resolved itself. **And every document that was not loaded has a reason you could read to an auditor.**

![Publish machine-enforced facts, not just relevant text: the translation table from everyday enterprise to KCP implementation — access spreadsheets become cryptographic manifests, InfoSec policies become HSM attestations, 'for internal use' becomes audience: [human], and rollout dates become valid_from time gates — with the closing charge: the Milky Way runs entirely from the shipping CLI without mocks; stop pointing embedding models at wikis and hoping](../../assets/images/milky-way-12-machine-enforced-facts.webp)

Everything runs from the shipping CLI, no mocks — the demo suite is CI, so every narrated claim above is a regression test:

```sh
npm install -g kcp-agent   # or: npx kcp-agent
node examples/demos.js milky-way
```

The estate itself is small enough to read over coffee: [`examples/milky-way/`](https://github.com/Cantara/kcp-agent/tree/main/examples/milky-way) — nine manifests, seventeen short documents, one signature envelope. Or drive it over MCP with [the borrowed leash](2026-07-06-the-borrowed-leash-kcp-mcp-bridge.md), where a foreign agent gets the same gates and the same written reasons.

The oat drink ships with less sugar, and the recipe never left the vault.
