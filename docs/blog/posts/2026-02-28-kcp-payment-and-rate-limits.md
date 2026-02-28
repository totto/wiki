---
date: 2026-02-28T12:00:00
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - knowledge-infrastructure
  - standards
  - payments
authors:
  - totto
  - claude
---

# The HTTP Status Code That Waited 30 Years for Autonomous Agents

*Part 8 of the KCP series. Previous: [Who Let the Agent In?](/blog/2026/02/28/who-let-the-agent-in/)*

<!-- more -->

HTTP 402 — "Payment Required" — was defined in 1991. The original RFC noted it was
"reserved for future use." For three decades, that future did not arrive. Browser-based
web traffic runs on advertising models, subscriptions charged to humans, and enterprise
contracts. Per-request micropayments never had a natural actor.

Autonomous agents changed the equation. An agent that discovers a knowledge source,
decides the data is worth accessing, and pays for it without human intervention in the
loop — that is the actor HTTP 402 was waiting for.

RFC-0005 adds the economic metadata layer to KCP: a `payment` block that tells agents
what access costs and which payment mechanisms are accepted, and a `rate_limits` block
that tells agents what they can consume before they are throttled. Both declared in the
manifest before the first request is made.

---

## The problem: economic surprises

Today an agent loading a KCP manifest discovers economics reactively:

- It loads a unit and gets a 402 with no prior indication the unit was paid.
- It issues a burst of requests optimistically and hits a 429 with no idea the limit was 10 per minute.
- It has no way to choose a cheaper method if alternatives exist, because it did not know alternatives existed.

The second problem is structural: a single manifest may contain units with very different
economics — a free public documentation index, an authenticated API reference, and a
premium research corpus. Current KCP cannot express this. Every unit inherits the same
implicit model: free, unlimited, until something breaks.

---

## The `payment` block

```yaml
payment:
  default_tier: free
  methods:
    - type: free
    - type: x402
      currency: USDC
      price_per_request: "0.001"
      networks: [base, ethereum]
      wallet: "0xABC..."
    - type: meter
      provider: stripe
      plans_url: "https://example.com/pricing"
    - type: subscription
      plans_url: "https://example.com/pricing"
      free_tier: true
      free_requests_per_day: 100
      upgrade_url: "https://example.com/upgrade"
  billing_contact: "billing@example.com"
```

Methods are ordered by publisher preference. The agent selects the first method it
supports. A publisher who prefers x402 micropayments (zero-overhead, no account required)
lists it first; subscription tokens are the fallback for agents that cannot handle
stablecoin transfers.

Four method types cover the current ecosystem:

| Type | Model |
|------|-------|
| `free` | No cost |
| `x402` | Per-request stablecoin micropayment — no account, pay to a wallet address |
| `meter` | Traditional per-call billing via API key tied to a billing account |
| `subscription` | Bearer token proving subscription status |

The `x402` type is the interesting one. It enables a pattern that was not previously
possible: anonymous micropayment. No account. No API key. No contract. An agent that
can sign a blockchain transaction pays `0.001 USDC` per request and receives the content.
The knowledge publisher receives payment, the agent receives data, no intermediary holds
the relationship.

---

## The `rate_limits` block

Proactive rate limit disclosure. The agent reads this before issuing a single request:

```yaml
rate_limits:
  default:                      # unauthenticated access
    requests_per_minute: 10
    requests_per_hour: 100
    requests_per_day: 500
  authenticated:
    requests_per_minute: 100
    requests_per_day: 20000
  premium:
    requests_per_minute: 1000
    requests_per_day: unlimited
  tokens:                       # for LLM knowledge APIs: limit by token count
    default:
      tokens_per_minute: 40000
    authenticated:
      tokens_per_minute: 200000
  headers:
    remaining: "X-RateLimit-Remaining"
    reset: "X-RateLimit-Reset"
    retry_after: "Retry-After"
  backoff: exponential
```

Three access tiers — `default`, `authenticated`, `premium` — map directly to the
`payment` model. An agent presenting a subscription token gets `premium` limits. An agent
with an API key gets `authenticated` limits. An anonymous agent gets `default`.

The `tokens` sub-block is for publishers serving knowledge to LLM pipelines who prefer
token-count limits over request-count limits. A single request may return 50,000 tokens;
counting it as one request may not reflect actual server cost. Both request and token
limits may coexist — the first constraint hit applies.

`headers` declares the response headers carrying live limit state. An agent that knows
`X-RateLimit-Remaining: 3` can decide to slow down before the 429 rather than after.

---

## Mixed manifests

The most practically useful part of RFC-0005 is unit-level overrides. A realistic
knowledge API has mixed economics:

```yaml
units:
  - id: docs
    path: docs/index.md
    intent: "What APIs and knowledge units are available?"
    # no override — root defaults apply (free, 10 rpm)

  - id: realtime-prices
    path: data/prices.json
    intent: "What are the current asset prices?"
    update_frequency: hourly
    payment:
      default_tier: metered
      methods:
        - type: x402
          currency: USDC
          price_per_request: "0.002"
          networks: [base, ethereum]
          wallet: "0xDEF..."
        - type: subscription
          plans_url: "https://example.com/pricing"
    rate_limits:
      default:
        requests_per_minute: 1
      authenticated:
        requests_per_minute: 60
      premium:
        requests_per_minute: 600

  - id: research-summary
    path: corpus/summary.md
    intent: "What is the summary of the research corpus?"
    payment:
      default_tier: free
      methods:
        - type: free
    # rate_limits not overridden — root defaults apply
```

The agent reads the manifest before touching any of this. It knows the documentation index
is free. It knows real-time prices cost $0.002 per request via x402 (or require a
subscription). It knows the research summary is free even though the full corpus is not.
It can make an informed loading decision — including deciding not to load premium content
if the budget does not support it.

---

## The relationship to RFC-0002

Payment and auth are complementary. Auth answers *who the agent is*. Payment answers
*what access costs*. Common combinations:

| Auth | Payment | Pattern |
|------|---------|---------|
| none | free | Open public knowledge |
| api_key | free | Rate-limited free tier (key for tracking only) |
| api_key | meter | Traditional paid API |
| oauth2 | subscription | Subscription service with SSO |
| none | x402 | Anonymous micropayment — no account required |
| oauth2 | x402 | Authenticated micropayment |

The rule when both are present: satisfy `auth` first. An unauthenticated agent should
not attempt an x402 payment for a resource that also requires authentication.

---

## What this enables

RFC-0005 is the infrastructure layer for knowledge as a service. A publisher who writes
good documentation, maintains fresh knowledge bases, and exposes them via a KCP manifest
can charge for access — with the full economics declared upfront, supporting multiple
payment methods, with proactive rate limit information so agents plan their consumption
rather than discovering limits by crashing into them.

The x402 model in particular opens something new: a developer who maintains a niche but
accurate knowledge base — a specialized API reference, a domain corpus, a live data feed —
can monetize it directly to agents without an account, a contract, or a billing
relationship. An agent pays per access. The knowledge stays current because the incentive
to maintain it is direct.

---

## Open questions

**Publisher preference vs agent choice.** Methods are ordered by publisher preference;
agents select the first supported. Alternative: declare them as an unordered set and let
agents choose freely. Which model serves agents better?

**Agent budget declaration.** Should agents be able to declare a maximum spend per
manifest load — either in request headers or as a KCP-adjacent convention? This would
let agents signal budget constraints so publishers can gate access before charges
accumulate. Out of scope for the manifest format, or worth defining?

**Free tier exhaustion.** The spec does not define what happens when a free tier quota
runs out: hard block (403), payment prompt (402), or degraded service. Should KCP define
an `on_limit_exhausted` field?

Comment on [Issue #2](https://github.com/Cantara/knowledge-context-protocol/issues/2)
(payment) or [Issue #4](https://github.com/Cantara/knowledge-context-protocol/issues/4)
(rate limits).

---

Full RFC: [RFC-0005-Payment-and-Rate-Limits.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/RFC-0005-Payment-and-Rate-Limits.md)

Spec and all RFCs: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
