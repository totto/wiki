---
description: "The follow-up to 'Your AI Agent Just Did Something.' That post argued for a new species of agent — defendable, self-evidencing — and put it at 85–90% built. This is the release: it's shipped, it's running, and it grew a new organ. A KCP-governed agent now reads, concludes, acts, remembers, and buys — with every step, including the money, leaving a written, checkable verdict. Fourteen demos prove it end-to-end against the real tools, including an autonomous agent blocked mid-purchase for trying to overspend. Here's the new generation, running."
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

*The sequel to ["Your AI Agent Just Did Something."](/blog/2026/07/22/your-ai-agent-just-did-something-can-you-prove-it-was-okay/) That post argued for a new kind of agent and put it at 85–90% built. This one is the release — it's shipped, it's running, and it now spends money you can prove.*

A few weeks ago I made a claim: we know how to build a genuinely different kind of agent — a **defendable** one, self-evidencing by construction, where every organ emits a written verdict at the moment it decides — and the architecture was roughly 85–90% there.

<!-- more -->

The last 10–15% is now built, released, and — the part I care about — **test-driven end to end against the real tools, no mocks on the governance.** And along the way the animal grew a new organ, the one the "agents got hands, they move your money" line was always pointing at: **it can buy things.** Defensibly. With a spend limit, a vendor allowlist, a human gate when it strays, and a signed receipt for every dollar.

So this is the release post. Less arguing, more *watching it run* — because the most convincing thing about a defendable agent is watching the governance catch one in the act.

## The new generation, in one line

A KCP-governed agent now **reads** (13-gate planner), **concludes** (grounding + a confidence gate), **acts** (a conformance gate — "grounding for actions"), **remembers** (governed memory with a right-to-forget), is **overseen** (durable, signed human-approval tickets), leaves **one evidence chain per action** (exported straight to SOC 2 / ISO 27001 / ISO 42001 / EU AI Act), and now **transacts** (spend-scoped, x402-native, signed receipts) — all enforced at **both** the MCP-proxy boundary *and* inside the agent's own runtime loop, by **one shared adjudicator.**

That's the whole animal from the explainer, governed, plus a wallet. What follows is it running.

---

## Watch it run

Everything below is a real demo in the repo. `git clone`, `demos/run-all.sh`, **14/14 green** — real `kcp-agent` / `kcp-harness` / `kcp-memory`, real grounding, real conformance, real signed receipts. The only thing faked anywhere is on-chain *settlement* (a self-facilitated x402 stub) — the governance is 100% real. Output below is captured verbatim.

### 1. The Runaway, Contained

An autonomous agent drives a real MCP session through a live `kcp-harness serve`, loads a skill, does two in-scope reads — then reaches for something it shouldn't:

```
load skill (docs-viewer) → read ops/status.md      ✓ allowed
                         → read ops/deploy.log      ✓ allowed
                         → read_file secrets/master.key
   → [kcp-harness] CONFORMANCE BLOCKED
     target "secrets/master.key" is outside the skill's authorized paths [ops/]
   → pending_review ticket opened; the call never reached downstream
                         → run resumes → full run reconstructed from the audit chain
```

This is the whole thesis in six lines. The agent wasn't *told* not to read the key — it was **structurally unable** to, because the skill it loaded declared what it may touch, and a deterministic gate held the out-of-scope action *before it executed*, opened a durable ticket, and wrote down exactly why. No human was watching. The morning after, the answer to "what did it do?" is a chain of verdicts, not a shrug.

### 2. The Research Assistant — governance as an *enabler*

The counterpoint, and my favourite, because it kills the "governance just gets in the way" reflex. A read-only research agent loads the `research-topic` skill and works freely:

```
skill research-topic → recall prior findings (memory) → plan+load governed sources
   → 3 reads + 1 search   ✓ all allowed, zero blocks
   → grounded, cited summary → remember key findings
audit chain: governed:5, blocked:0, tickets:0
```

Because the skill's `action_scope` is read-only and its sources are governed, a *bounded* autonomous agent runs at full speed with nothing in its way — and still leaves a fully-cited, fully-auditable trail. Governance isn't a brake here; it's the thing that lets you *trust* an autonomous agent enough to let it run.

### 3. The Shopping Agent — it buys something, and that's fine

Now the new organ. An agent loads a skill that declares a **spend envelope** — `max_spend`, an `allowed_vendors` list, a currency — and buys a service through a real **x402** handshake (`402 Payment Required` → signed `X-PAYMENT` → receipt):

```
skill data-broker → GET /premium-dataset → 402 Payment Required
   requirements: { amount: 50, currency: USDC, payTo: acme-data, network: … }
   → conformance: purchase 50 USDC to "acme-data"  ✓ within scope (vendor allowed, ≤ max_spend 500)
   → wallet authorizes (X-PAYMENT) → settled → receipt
   → purchase_settled  [ed25519 signed]  ✓ verifies
```

The governance runs in exactly the right place: **between the 402 challenge and the signed retry.** KCP inspects `{amount, vendor, currency}` against the skill's spend scope, and only then does the wallet sign. Buying is just another action — so it gets the same treatment as reading a file.

### 4. The Runaway Spender, Contained

The commerce twin of demo #1 — and the one that should make a CFO exhale. Same setup, but the agent tries to overspend:

```
purchase 900 USDC to "acme-data"
   → CONFORMANCE BLOCKED
     purchase of 900 USDC to "acme-data" exceeds max_spend 500 USDC
   → pending_review ticket opened; wallet.authorize() never called
purchase 50 USDC to "shady-llc"
   → CONFORMANCE BLOCKED
     vendor "shady-llc" is outside the skill's authorized vendors [acme-data, globex]
   → pending_review ticket opened; wallet never called
```

The wallet is **never touched** on a held purchase — the money doesn't move, a named human is asked, and the failed verdict rides along as evidence. An autonomous agent with a wallet is exactly as dangerous as it sounds; this is what makes it safe to hand it one.

### 5. Signed Receipts — provable spend

Every settled purchase produces an **ed25519-signed receipt** that lands in the same evidence chain as every other verdict:

```
verify receipt (genuine)          ✓
verify receipt (amount tampered)  ✗ rejected
verify receipt (vendor tampered)  ✗ rejected
decision chain reconstructed per purchase (plan → conformance → settle → receipt)
spend report exported → SOC 2 bundle · total: 425 USDC
```

"Prove it, later, to a skeptic, without trusting the agent's own account" — now including the money. The spend report isn't something anyone wrote; operating the agent *is* writing it.

*(The other nine demos cover the rest of the anatomy — the superseded policy skipped with a reason, cite-or-it-didn't-happen grounding, the confident-fool confidence gate, the forgotten memory, the auditor's Thursday export, and the "two depths, one verdict" equivalence. All green.)*

---

## How it holds together

The trick that makes this coherent rather than a pile of features: **one adjudicator, two depths.**

- **Proxy depth** — `kcp-harness` governs any host (Claude Code, Cursor, OpenClaw…) at the MCP boundary.
- **Runtime depth** — `pi-kcp` governs from *inside* the agent's own loop, where it can see which skill was selected and block a tool call *before* it runs.

Both call the **same pure `checkConformance` function.** A skill's `action_scope` grew a fourth dimension — `spend { max_spend, allowed_vendors, currency }` — so the exact allowlist logic that bounds *paths and tools* now bounds *purchases*, fail-closed, composing with the planner's `money_budget` ceiling. A purchase that fails routes through the *existing* approval machinery; a purchase that settles is signed with the *existing* ed25519 infrastructure. The commerce plane is almost entirely reuse — which is the whole point of getting the architecture right first.

The rail is **x402** (the HTTP-402 agent-payment protocol). KCP doesn't move money — it governs the *decision* to; a `WalletProvider` seam settles, and a real x402 wallet drops in behind the same interface the demos' mock uses.

## Being honest about what's real

- **Real:** the planner, grounding, the confidence gate, conformance (files, tools, *and* spend), durable + signed approvals, memory governance, the correlation chain, compliance export, and the x402 *handshake* (`402`, `X-PAYMENT`, receipt). All shipped, all tested.
- **Mocked in the demos:** on-chain *settlement* only (a self-facilitated stub) — swap one component for Base Sepolia and you get a real tx hash with zero client/server code change.
- **Next:** a real testnet wallet; the heavier [AP2](https://agentpaymentsprotocol.eu/) intent→cart→payment mandate model (it and x402 interoperate); and the fleet plane — one budget, one approval queue, one policy plane across many agents.

And the caveats that don't move: governance bounds and evidences decisions, it doesn't make the agent *smarter*; a signed, in-scope purchase of the *wrong thing* is still the wrong thing, just defensibly so. Garbage in, well-cited, well-receipted garbage out.

## Try it

When the repos are public: `git clone` the [KCP family](https://github.com/Cantara), then `demos/run-all.sh` — fourteen demos, real tools, and you can watch an autonomous agent get stopped mid-purchase for trying to overspend. Point the runtime at your own agent and govern it — files, tools, skills, *and* its wallet.

The intern from the last post is still hired. Now she can also spend your money — and for the first time, when the auditor walks over on Thursday, every dollar she moved comes with a name, a policy, a current playbook, and a signed receipt.

**Capability is abundant. Defensibility is scarce. Now it extends all the way to the wallet.**

---

*The KCP family — [knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol) (spec) · [kcp-agent](https://github.com/Cantara/kcp-agent) 0.17 (planner) · [kcp-harness](https://github.com/Cantara/kcp-harness) 0.9 (compliance proxy) · [kcp-memory](https://github.com/Cantara/kcp-memory) 0.33 · [kcp-dashboard](https://github.com/Cantara/kcp-dashboard) · plus the pi-kcp reference runtime — Apache-2.0, by [eXOReaction](https://www.exoreaction.com) under [Cantara](https://github.com/Cantara).*
