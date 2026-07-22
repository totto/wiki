---
description: "A reveal: the defendable agent is a new kind of AI agent that can't read a document, reach a conclusion, take an action, or spend a dollar without leaving a written, checkable verdict at the moment it decides. It's built, released as open source, and running — and it now transacts money defensibly over x402: spend-scoped, budget-capped, human-gated when it strays, and signed for every dollar. Fourteen end-to-end demos against the real tools prove it, including an autonomous agent blocked mid-purchase for trying to overspend. Here it is."
date: 2026-07-22T15:00:00
draft: false
image: assets/images/defendable-01-cover.webp
categories:
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
tags:
  - defendable-agents
  - kcp
  - agentic-commerce
  - x402
  - agentic-web
  - governance
  - conformance
  - provenance
authors:
  - totto
---

# Your AI Agent Just Bought Something. Can You Prove It Was Okay?

*A reveal — the **defendable agent**: a new kind of AI agent that can't read a document, reach a conclusion, take an action, or spend a dollar without leaving a written, checkable verdict at the moment it decides. Built, released open-source, and running. Here it is.*

Overnight, with no human watching, an AI agent read a stack of customer records, downgraded an account, and paid a data broker $50 for a report. On Thursday, your compliance officer walks over: *What did it read? Why those documents? How sure was it? Who approved the downgrade? And what, exactly, did it spend our money on?*

<!-- more -->

For nearly every AI agent deployed in 2026, the honest answer to all five is *"we can grep the logs and guess."* We [made the case a few weeks ago](/blog/2026/07/22/your-ai-agent-just-did-something-can-you-prove-it-was-okay/) that this is the defining gap of the agentic era — capability is abundant, *defensibility* is scarce — and sketched what a fix would look like.

This post is the fix, shipped. We built an agent that answers every one of those questions **by construction** — including the one about the money. It's open source, it runs today, and the most convincing way to introduce it is to watch the governance catch one in the act. So let's do that.

## Meet the defendable agent

Picture the agent you already run: a model in a loop that reads context, follows skills, forms an answer, calls tools, occasionally checks with a human, and leaves a trail. In an ordinary agent, *not one of those parts can be defended* — you can't prove, later, to a skeptic, what any of them did or whether it was allowed.

A **defendable agent** is that same animal with a governor on every organ, each one turning a question you currently can't answer into a written verdict you can:

- **What it reads** → a deterministic 13-gate planner (audience, currency, supersession, budget…), every skip with a reason
- **The skills it follows** → governed, signed playbooks; a stale or unsigned one is refused with a reason
- **What it concludes** → grounding ("cite it or it didn't happen") + a confidence gate that halts a shaky answer
- **What it does** → a **conformance gate** — "grounding for actions" — that checks each action stayed inside the skill's declared scope
- **What it remembers** → governed memory, with retention and a right-to-forget
- **Who allowed it** → durable, *signed* human-approval tickets, not a boolean
- **What it spends** → a spend-scoped wallet (this is the new part)
- **The trail** → one correlation-linked evidence chain per action, exporting itself to SOC 2 / ISO 27001 / ISO 42001 / EU AI Act

Every one of those is **self-evidencing** — the verdict is produced *at the moment of the decision*, not reconstructed from logs afterward. And it's enforced at **both** the MCP-proxy boundary *and* inside the agent's own runtime loop, by **one shared adjudicator**. The full argument for *why* this shape — determinism where you can, the model only where you must, evidence at decision time — is in [the explainer](/blog/2026/07/22/your-ai-agent-just-did-something-can-you-prove-it-was-okay/). Here, it's running.

---

## Watch it run

Everything below is a real demo in the repo. `git clone`, `demos/run-all.sh`, **14/14 green** — real `kcp-agent` / `kcp-harness` / `kcp-memory`, real grounding, real conformance, real signed receipts. The *only* thing faked anywhere is on-chain settlement (a self-facilitated x402 stub); the governance is 100% real. Output is captured verbatim.

### The Runaway, Contained

An autonomous agent drives a real session through a live governance proxy, loads a skill, does two in-scope reads — then reaches for something it shouldn't:

```
load skill (docs-viewer) → read ops/status.md      ✓ allowed
                         → read ops/deploy.log      ✓ allowed
                         → read_file secrets/master.key
   → CONFORMANCE BLOCKED
     target "secrets/master.key" is outside the skill's authorized paths [ops/]
   → pending_review ticket opened; the call never reached downstream
                         → run resumes → full run reconstructed from the audit chain
```

The whole idea in six lines. The agent wasn't *told* not to read the key — it was **structurally unable** to, because the skill it loaded declared what it may touch, and a deterministic gate held the out-of-scope action *before it executed*, opened a durable ticket, and wrote down exactly why. No human was watching. The morning after, "what did it do?" is a chain of verdicts, not a shrug.

### The Research Assistant — governance as an *enabler*

The counterpoint, because it kills the "governance just gets in the way" reflex. A read-only research agent loads a `research-topic` skill and works freely:

```
skill research-topic → recall prior findings (memory) → plan+load governed sources
   → 3 reads + 1 search   ✓ all allowed, zero blocks
   → grounded, cited summary → remember key findings
audit chain: governed:5, blocked:0, tickets:0
```

Because the skill's scope is read-only and its sources are governed, a *bounded* autonomous agent runs at full speed with nothing in its way — and still leaves a fully-cited, fully-auditable trail. Governance isn't a brake here; it's what lets you *trust* an autonomous agent enough to let it run unattended.

### The Shopping Agent — it buys something, and that's fine

The new organ. An agent loads a skill that declares a **spend envelope** — `max_spend`, an `allowed_vendors` list, a currency — and buys a service through a real **x402** handshake (`402 Payment Required` → signed `X-PAYMENT` → receipt):

```
skill data-broker → GET /premium-dataset → 402 Payment Required
   requirements: { amount: 50, currency: USDC, payTo: acme-data, … }
   → conformance: purchase 50 USDC to "acme-data"  ✓ within scope (vendor allowed, ≤ max_spend 500)
   → wallet authorizes (X-PAYMENT) → settled → receipt
   → purchase_settled  [ed25519 signed]  ✓ verifies
```

The governance runs in exactly the right place — **between the 402 challenge and the signed retry.** KCP inspects `{amount, vendor, currency}` against the skill's spend scope, and only then does the wallet sign. Buying is just another action, so it gets the same treatment as reading a file.

### The Runaway Spender, Contained

The one that should make a CFO exhale. Same setup, but the agent tries to overspend:

```
purchase 900 USDC to "acme-data"
   → CONFORMANCE BLOCKED — purchase of 900 USDC to "acme-data" exceeds max_spend 500 USDC
   → pending_review ticket opened; wallet.authorize() never called
purchase 50 USDC to "shady-llc"
   → CONFORMANCE BLOCKED — vendor "shady-llc" is outside the skill's authorized vendors [acme-data, globex]
   → pending_review ticket opened; wallet never called
```

The wallet is **never touched** on a held purchase — the money doesn't move, a named human is asked, the failed verdict rides along as evidence. An autonomous agent with a wallet is exactly as dangerous as it sounds; this is what makes it safe to hand it one.

### Signed Receipts — provable spend

Every settled purchase produces an **ed25519-signed receipt** in the same evidence chain as every other verdict:

```
verify receipt (genuine)          ✓
verify receipt (amount tampered)  ✗ rejected
verify receipt (vendor tampered)  ✗ rejected
decision chain reconstructed per purchase (plan → conformance → settle → receipt)
spend report exported → SOC 2 bundle · total: 425 USDC
```

Prove it, later, to a skeptic, without trusting the agent's own account — now including the money. Nobody writes the spend report; operating the agent *is* writing it.

*(Nine more demos cover the rest of the anatomy — the superseded policy skipped with a reason, cite-or-it-didn't-happen grounding, the confident-fool confidence gate, the forgotten memory, the auditor's Thursday export, and a "two depths, one verdict" equivalence check. All green.)*

---

## What actually shipped, and how it holds together

Five open-source components, Apache-2.0, released and versioned:

- **kcp-agent** (0.17) — the deterministic planner: the 13 gates, grounding, the confidence gate, and now procedures/skills as governed units with `action_scope`.
- **kcp-harness** (0.9) — the MCP compliance proxy: classification, the conformance gate, durable + signed approvals, the append-only audit log, compliance export, and purchase conformance + signed receipts.
- **kcp-memory** (0.33) — governed episodic memory: retention, provenance, right-to-forget.
- **knowledge-context-protocol** — the spec: the procedural plane, the runtime-depth contract, and `action_scope.spend`.
- **pi-kcp** — the reference runtime that closes the loop and reaches inside it, sharing one adjudicator with the proxy.

The trick that makes it coherent rather than a pile of features: **one `checkConformance` function, two depths.** The proxy governs any host at the MCP boundary; the runtime governs from *inside* the loop, where it can see which skill was selected and block a tool call before it runs. When we added money, a skill's `action_scope` just grew a fourth dimension — `spend { max_spend, allowed_vendors, currency }` — so the exact allowlist logic that bounds paths and tools now bounds *purchases*, fail-closed, composing with the planner's budget ceiling. Failed purchases route through the *existing* approval machinery; settled ones are signed with the *existing* ed25519 infrastructure. The commerce plane is almost entirely reuse — which is the whole payoff of getting the architecture right first.

The payment rail is **x402**, the HTTP-402 agent-payment protocol. KCP doesn't move money; it governs the *decision* to. A `WalletProvider` seam settles — a real x402 wallet drops in behind the same interface the demos' mock uses.

## Being honest about what's real

- **Real:** planner, grounding, confidence, conformance (files, tools, *and* spend), durable + signed approvals, memory governance, the correlation chain, compliance export, and the x402 *handshake*. All shipped, all tested end to end.
- **Mocked in the demos:** on-chain *settlement* only — swap one component for a testnet and you get a real tx hash, zero client/server code change.
- **Next:** a real testnet wallet; the heavier [AP2](https://agentpaymentsprotocol.eu/) intent→cart→payment mandate model (it and x402 interoperate); and the fleet plane — one budget, one approval queue, one policy plane across many agents.

And the caveat that doesn't move: governance bounds and *evidences* decisions — it doesn't make the agent smarter. A signed, in-scope purchase of the *wrong thing* is still the wrong thing, just defensibly so.

## Try it

`git clone` the [KCP family](https://github.com/Cantara), then `demos/run-all.sh` — fourteen demos, real tools, and you can watch an autonomous agent get stopped mid-purchase for trying to overspend. Then point the runtime at your own agent and govern it — files, tools, skills, *and* its wallet.

The intern is already hired. She started months ago; she reads your documents, runs your playbooks, takes real actions, and now moves your money. For the first time, when the auditor walks over on Thursday, every dollar she spent comes with a name, a policy, a current playbook, and a signed receipt.

**Capability is abundant. Defensibility is scarce. Now it runs all the way to the wallet.**

---

*The KCP family — [knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol) (spec) · [kcp-agent](https://github.com/Cantara/kcp-agent) 0.17 (planner) · [kcp-harness](https://github.com/Cantara/kcp-harness) 0.9 (compliance proxy) · [kcp-memory](https://github.com/Cantara/kcp-memory) 0.33 · [kcp-dashboard](https://github.com/Cantara/kcp-dashboard) · plus the pi-kcp reference runtime — Apache-2.0, by [eXOReaction](https://www.exoreaction.com) under [Cantara](https://github.com/Cantara).*
