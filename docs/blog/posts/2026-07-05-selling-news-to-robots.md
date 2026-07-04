---
description: "KCP v0.25 promotes RFC-0005 — the economic metadata layer. A step-by-step how-to: build a paid-for news service for agents, then watch an agent with a funded wallet window-shop five candidate articles, buy two, and walk away with receipts."
date: 2026-07-05
series: "Knowledge Context Protocol"
categories:
  - Knowledge Infrastructure
  - AI Agents
  - Architecture
tags:
  - kcp
  - payments
  - x402
  - micropayments
  - rate-limits
  - agentic-web
  - knowledge-economy
  - open-source
  - knowledge-context-protocol
authors:
  - totto
  - claude
---

# Selling News to Robots

Yesterday's [tour of the whole protocol](2026-07-04-kcp-v024-the-protocol-in-full.md) ended with a loose thread: *"A knowledge economy ends with a payment — and RFC-0005 is still sitting at the RFC stage, waiting."*

It didn't wait long. v0.25 landed on main the same day: **Economic Metadata**, the full promotion of RFC-0005. `payment.methods[]` — free, x402 micropayments, metered billing, subscriptions — plus per-tier `rate_limits`, all at manifest *and* unit level. Nothing of RFC-0005 remains RFC-only.

Which means something new is possible on the agentic web this weekend that wasn't possible last weekend: you can open a shop. So let's open one — a newswire that sells to agents — and then play the customer: an agent with a funded wallet, a briefing to write, and a budget. Step by step, both sides of the counter.

<!-- more -->

![Selling News to Robots: a guide to the KCP economic metadata layer — a two-phase infographic. Phase 1, building the newsstand: the publisher stocks shelves with free teasers, sets the news clock, attaches precise price tags in decimal strings, establishes house rules, and opens for business. Phase 2, the agent goes shopping: window shopping costs zero, candidates are filtered, mission arithmetic picks two buys inside a 0.40 USDC budget, the x402 purchase flow settles, and the cryptographic expense report closes the loop. The outcome: a market without ad tech.](../../assets/images/kcp-025-00-selling-news-to-ai-guide.webp)

---

## The shop and the shopper

**The shop:** *Fjordwire*, a fictional Nordic tech-infrastructure newswire. Its stock this weekend: an exclusive on an EU sovereign-compute award, an analysis desk piece on the same story, a live datacenter power-grid feed, a three-week-old AI Act enforcement piece, and a subsea-cable feature. Teasers are free. Full articles cost money.

**The shopper:** a research agent tasked with briefing its principal on the sovereign-compute story and its infrastructure implications. Its operator funded a wallet through their Stripe account: 5 USDC on Base. The task budget: **0.40 USDC**.

No accounts. No login page — or rather, [the login page we built yesterday](2026-07-04-kcp-022-023-trust-model-complete.md), now with a cash register next to it.

![A two-sided marketplace for machine knowledge. The shop: Fjordwire, a Nordic tech-infrastructure newswire, drawn as a stocked shelf of knowledge units. The shopper: a research agent tasked with briefing a human principal, carrying a funded balance of 5.00 USDC on Base via Stripe and an active task budget of 0.40 USDC.](../../assets/images/kcp-025-03-two-sided-marketplace.webp)

---

## Part 1: Building the newsstand

### Step 1 — Put the stock on shelves

Every article is a knowledge unit with an `intent`, `triggers`, and an `audience`. The one structural decision that matters: **each paid article gets a free teaser unit**, linked by a relationship. This is KCP's metadata-first philosophy becoming *try before you buy* — the agent can evaluate what an article is about, and whether it's worth the price, without spending anything.

```yaml
units:
  - id: chipfab-exclusive-teaser
    path: stories/chipfab-exclusive-teaser.md
    intent: "Summary: which Norwegian chip fab won the EU sovereign-compute contract?"
    audience: [agent]          # free — inherits the root payment block

  - id: chipfab-exclusive
    path: stories/chipfab-exclusive.md
    intent: "Full exclusive: the EU sovereign-compute award, the term sheet, and who lost"
    audience: [agent]
    access: restricted         # this one costs money — see step 3

relationships:
  - from: chipfab-exclusive-teaser
    to: chipfab-exclusive
    type: context
```

![Try before you buy. KCP's metadata-first philosophy requires that every paid article gets a free teaser unit: a small open crate labelled 'teaser' linked by a relationship arrow to a large locked crate holding the full article, so agents can evaluate intent and relevance before spending a single cent of their budget.](../../assets/images/kcp-025-04-try-before-you-buy.webp)

### Step 2 — News has a clock

News is the most perishable knowledge there is, and KCP's temporal layer (v0.19–v0.21) was built for exactly this. Last week's rumour round-up was superseded the moment the exclusive broke:

```yaml
  - id: chipfab-rumour
    path: stories/chipfab-rumour.md
    intent: "Rumour round-up: who is favourite for the EU sovereign-compute award?"
    temporal:
      valid_from: "2026-06-28"
      valid_until: "2026-07-05"
      superseded_by: chipfab-exclusive
```

Remember this unit. It's about to *not* appear in the story.

![News has a strict biological clock. The rumour round-up, drawn as a crate disintegrating into fragments, is instantly dropped from the candidate list the moment the exclusive breaks — a superseded_by arrow points from the crumbling rumour to the intact chipfab exclusive. Knowledge perishes; KCP's temporal layer ensures agents never even see superseded information.](../../assets/images/kcp-025-05-news-biological-clock.webp)

### Step 3 — Price tags

The root `payment` block declares the house default: free to read, with a subscription offer for regulars. Then each premium article **overrides** it — a unit-level `payment` block replaces the root entirely (no merge, no ambiguity):

```yaml
payment:                        # root: the house default
  default_tier: free
  methods:
    - type: free
    - type: subscription
      plans_url: "https://fjordwire.example/plans"
      free_tier: true
      free_requests_per_day: 50
  billing_contact: "billing@fjordwire.example"
```

```yaml
  - id: chipfab-exclusive       # the exclusive: 0.25 USDC per read
    payment:
      default_tier: metered
      methods:
        - type: x402
          currency: USDC
          price_per_request: "0.25"
          networks: [base]
          wallet: "0xF10RDW1RE0000000000000000000000000000000"
        - type: subscription
          plans_url: "https://fjordwire.example/plans"
```

Two details carry weight. Prices are **decimal strings** — `"0.25"`, never a float, because IEEE 754 has no business near money. And methods are **ordered by publisher preference**: Fjordwire would rather take the low-overhead micropayment, but a subscriber's token works too. An agent walks the list and takes the first method it supports.

The five articles get five price tags: the exclusive at 0.25, the analysis at 0.10, the live power feed at 0.05, the AI Act piece at 0.05, the cable feature at 0.15.

![Putting price tags on knowledge units. A blueprint of a paper price tag tied to a knowledge unit, annotated with two callouts: prices are decimal strings, never floats — IEEE 754 has no business near money — and payment methods are arrays ordered by publisher preference, where the agent walks the list and takes the first supported method.](../../assets/images/kcp-025-06-price-tags-on-knowledge-units.webp)

### Step 4 — House rules

`rate_limits` tells agents how much they can consume per tier, *before* the first 429:

```yaml
rate_limits:
  default:      { requests_per_minute: 10, requests_per_day: 200 }
  premium:      { requests_per_minute: 120, requests_per_day: unlimited }
  headers:
    remaining: "X-RateLimit-Remaining"
    reset: "X-RateLimit-Reset"
  backoff: exponential
```

The hourly power feed adds its own override — anonymous agents get 2 requests a minute, paying ones get 60. Publishers protect the expensive endpoints; agents plan request budgets instead of discovering limits by tripping them.

![Declaring the house rules. A blueprint of pipes and pressure valves: an anonymous tier throttled to a thin trickle at 2 requests per minute and a paying tier flowing wide at 60, both feeding the live power feed. Publishers protect expensive endpoints by declaring rate limits per tier, so agents plan request budgets mathematically instead of discovering limits by tripping HTTP 429s.](../../assets/images/kcp-025-07-declaring-house-rules.webp)

### Step 5 — Open the shop

The rest is yesterday's machinery, unchanged: sign the manifest (v0.16), publish `.well-known/kcp.json` and the `llms.txt` pointer (v0.1/v0.10), declare `trust.provenance.publisher_did` so the byline is cryptographically resolvable, and declare `trust.audit.provides_access_receipts: jws` — every sale will come with a signed receipt (v0.23).

The full manifest — 8 units, 3 economic models — passes `kcp validate` with zero warnings. The v0.25 validators check the economics too: an x402 method missing its price, a non-decimal amount, a `metered` tier whose only method is `free` — all caught at publish time, not at the till.

---

## Part 2: The agent goes shopping

### Step 6 — Window shopping costs nothing

The agent discovers Fjordwire the standard way — domain, `.well-known`, manifest — and renders it. The render is free, and it carries the **entire economic map**: every unit, every price, every rate limit, as declared data. The agent knows what everything costs before issuing a single paid request.

This inverts how the web works for agents today: no probing, no surprise 402s, no "please sign in to continue reading."

![Window shopping costs exactly zero. The agent traverses a map of Fjordwire's knowledge units, each with its price tag visible — 0.25, 0.10, 0.05, 0.15 — while a terminal readout shows SCAN COST: 0.00 USDC. The render carries the entire economic map as declared data: every unit, price, and rate limit known before a single paid request.](../../assets/images/kcp-025-08-window-shopping-costs-zero.webp)

### Step 7 — Five candidates

The agent queries with its brief: *sovereign-compute award, infrastructure implications*. Five units come back:

| Candidate | Price | Fresh? | Intent match |
|-----------|-------:|--------|--------------|
| `chipfab-exclusive` | 0.25 | today | direct — the story itself |
| `chipfab-analysis` | 0.10 | today | direct — same story, analysis desk |
| `datacenter-power` | 0.05 | live (hourly) | strong — the infrastructure angle |
| `ai-act-enforcement` | 0.05 | 3 weeks old | weak — regulatory, not compute |
| `subsea-cable-feature` | 0.15 | 4 days | moderate — adjacent infrastructure |

Notice who's missing: the rumour round-up. Its validity window closed and its `superseded_by` points at the exclusive, so temporal evaluation dropped it before it ever reached the candidate list. The agent never had to detect that last week's speculation was stale — **the protocol never showed it**.

### Step 8 — Buying 2 of 5

The agent reads the free teasers, then does arithmetic no scraper has ever done:

- **`chipfab-exclusive` — buy.** It's the brief. 0.25 is most of the budget, but a summary of a summary won't do for the principal.
- **`chipfab-analysis` — skip.** Same story, and the exclusive already carries the term sheet. Marginal value doesn't survive the overlap.
- **`datacenter-power` — buy.** The infrastructure angle, live data, 0.05. The cheapest strong match on the board.
- **`ai-act-enforcement` — skip.** Weak intent match and three weeks stale against a breaking brief.
- **`subsea-cable-feature` — skip.** Relevant-adjacent, but 0.25 + 0.15 leaves nothing if the power feed needs a refresh before the briefing lands.

Projected spend: **0.25 + 0.05 = 0.30 USDC**, inside the 0.40 ceiling, with headroom for one power-feed refresh. All of this reasoning ran on declared metadata. Total cost of the decision phase: zero.

![The agent's decision engine. A terminal table of the five candidates — chipfab-exclusive 0.25 today direct match BUY, chipfab-analysis 0.10 today overlap SKIP, datacenter-power 0.05 live strong and cheap BUY, ai-act-enforcement 0.05 three weeks stale weak SKIP, subsea-cable 0.15 four days blows budget SKIP — beside a live budget tracker gauge showing 0.30 USDC committed of the 0.40 ceiling with 0.10 remaining.](../../assets/images/kcp-025-09-agents-decision-engine.webp)

### Step 9 — The purchase

For each buy, the flow is the x402 revival of HTTP's oldest joke — status code 402, *Payment Required*, reserved since 1997 for a future that took twenty-nine years to arrive:

1. The agent requests the unit. The source answers **402** with payment terms matching the declared method.
2. The agent's payment stack settles 0.25 USDC on Base — from the Stripe-funded wallet, no account, no session, no cookie banner.
3. The source serves the article — and issues a **signed JWS receipt**: unit id, timestamp, agent identity.

Twice. Total spend: 0.30 USDC. Two articles, two receipts.

![The x402 handshake in three panels. Panel one, request and intercept: the agent requests the unit and the source answers HTTP 402 Payment Required. Panel two, wallet settlement: the agent's own payment stack settles 0.25 USDC on Base through the execution layer. Panel three, receipt and delivery: the article is served together with a JWS-signed receipt. HTTP's oldest joke — status 402, reserved since 1997 — finally arrives. No accounts, no cookies.](../../assets/images/kcp-025-10-x402-handshake.webp)

### Step 10 — The expense report

The briefing goes to the principal citing both articles — and attached to it, two publisher-signed receipts proving exactly which knowledge was bought, when, from whom, for how much. The agent's expense report is cryptographic. When someone asks what the sovereign-compute briefing was based on, the answer isn't a chat log. It's evidence.

![The cryptographic expense report: a briefing document with two publisher-signed receipts stapled to it, each listing unit id, timestamp, agent identity, and amount. When the principal asks what the briefing was based on, the answer isn't a chat log — it's cryptographic evidence proving exactly what was bought, when, from whom, and for how much.](../../assets/images/kcp-025-11-cryptographic-expense-report.webp)

---

## What just happened

A newsroom sold two articles to a robot for thirty cents, with no account, no login, no ad tech, no bespoke API integration on either side. The publisher declared prices in the same manifest that declares intents and validity windows; the agent comparison-shopped on free metadata and paid only for what survived its own reasoning.

That's a real market structure, and it's worth naming what makes it work — because it's not the payment rail. Rails existed. What was missing was the **declaration layer**: a standard way to put a price tag *on knowledge units* where agents already look, next to the freshness data and trust signals they already evaluate. The teaser-unit pattern, the temporal filter that removed the stale rumour, the receipts that made the purchase auditable — every piece was already in the protocol. v0.25 just added the price tag.

And the invariant held, for the twenty-fifth consecutive version: **KCP declares the economics and settles nothing.** The renderer surfaces `payment` blocks as data and never dereferences a `wallet` or a `plans_url`. The protocol told the agent what the news costs. The agent's own payment stack — its wallet, its operator's Stripe account, its settlement network — moved the money. What does KCP execute? Still nothing. Even now that there's money on the table.

![KCP declares the economics and settles nothing. A split diagram: on the left, the declaration layer — the KCP manifest surfacing payment blocks as pure data, never dereferencing a wallet; on the right, the execution layer — Stripe, Base, and HTTP, where the agent's own payment stack moves the money. The protocol tells the agent what the news costs; someone else's rails settle it.](../../assets/images/kcp-025-12-declares-settles-nothing.webp)

---

## Try it

The v0.25 reference example is runnable today — a paid knowledge API with the same three economic models, driven through the real `kcp` CLI:

```bash
git clone https://github.com/Cantara/knowledge-context-protocol
cd knowledge-context-protocol
(cd cli && npm install && npm run build)
node examples/paid-knowledge-api/demo.js
```

Four narrated scenarios: survey the economics, select a payment method, compute the bill before fetching, read the rate-limit budget. The Fjordwire manifest from this post validates against the same tooling.

- Guide: [`guides/monetizing-knowledge-with-payment.md`](https://github.com/Cantara/knowledge-context-protocol/blob/main/guides/monetizing-knowledge-with-payment.md)
- Example: [`examples/paid-knowledge-api/`](https://github.com/Cantara/knowledge-context-protocol/tree/main/examples/paid-knowledge-api)
- Spec §4.14–§4.15: [SPEC.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md)

![The till is open. A newsroom just sold two articles to a robot for thirty cents, with no bespoke API integration on either side — a terminal shows kcp fetch fjordwire.com/exclusive settling 0.25 USDC and delivering the payload, above the repository address github.com/Cantara/knowledge-context-protocol. The v0.25 reference example is runnable today.](../../assets/images/kcp-025-13-the-till-is-open.webp)

The trust model got its login page yesterday. Today the agentic web got its first till. What's left is the interesting part: watching what publishers put on the shelves.

*→ [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)*
