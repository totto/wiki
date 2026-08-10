---
description: "You've signed what your agent knows. Now govern what it does — from inside the turn. pi-kcp binds every native tool call to the declared authority of the skill it runs under: an allowlist of tools and paths in knowledge.yaml, adjudicated deterministically, blocked with a written reason. This tutorial walks three real demos: an in-scope pass and two out-of-scope blocks, a bounded research agent that runs freely with zero blocks, and the same violation caught at proxy depth and runtime depth with a byte-identical verdict. Every output in this post is real."
date: 2026-08-10T09:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Governance, Trust & Compliance
  - AI Agents & the Agentic Web
  - Knowledge Context Protocol
tags:
  - kcp
  - pi-kcp
  - kcp-harness
  - tutorial
  - action-scope
  - conformance
  - runtime-governance
  - audit-trail
  - defendable-agents
authors:
  - totto
  - claude
image: assets/images/blog/the-skill-is-the-security-boundary/title-hero.png
---

# The Skill Is the Security Boundary

![The Skill Is the Security Boundary — deterministic, declarative governance for defendable AI agents with pi-kcp](/assets/images/blog/the-skill-is-the-security-boundary/title-hero.png)

When your agent loads a skill, it loads a playbook — and, implicitly, an author's idea of what that playbook should be allowed to touch. A deploy skill means the deploy scripts. A research skill means the research corpus. But in almost every agent harness today, that idea stays implicit: the skill shapes the agent's *behavior* while the agent keeps its *entire* toolbelt. The deploy skill can read `/etc/shadow`. The research skill can call out to the network. Nothing binds the actions to what the skill claimed to be.

![The illusion of implicit boundaries — an agent with an active "deploy" skill still holds a robotic arm that can reach network access and /etc/shadow, because nothing binds the claim to the action](/assets/images/blog/the-skill-is-the-security-boundary/illusion-of-implicit-boundaries.png)

[pi-kcp](https://github.com/Cantara/pi-kcp) makes the binding explicit. A governed skill declares its authority — an allowlist of tools and path prefixes called an `action_scope` — in the same `knowledge.yaml` that already governs what the agent knows. At runtime, inside the turn, every native tool call taken under that skill is adjudicated against the declaration. In scope: it runs. Out of scope: it is held, fail-closed, with a written reason naming the violating target and the authorized scope it fell outside of. Deterministic. No LLM in the loop.

This is the hands-on follow-up to the *Policy vs. Enforcement* post from earlier today, which named both `kcp-harness` and `pi-kcp` but didn't show the mechanics. Below are the mechanics — three worked demos, real outputs pasted from real runs, ending with the one that motivated the LinkedIn post: the same out-of-scope action, checked at two different depths of the stack, producing a byte-identical verdict.

<!-- more -->

## What pi-kcp is, in one paragraph

![Explicit binding through pi-kcp — the same robotic arm now locked to its declared scope, with deterministic, fail-closed, no-LLM-in-the-loop badges](/assets/images/blog/the-skill-is-the-security-boundary/explicit-binding-through-pi-kcp.png)

`pi-kcp` is an extension for the [Pi coding agent](https://github.com/earendil-works) that makes a Pi agent **defendable**. It gives the agent KCP memory recall and deterministic knowledge plans through a small `/kcp` command surface — and, since the runtime-depth milestone, it governs what the agent actually *does*: it learns which skill an action is being taken under and blocks any native tool call that falls outside that skill's declared authority, using the same deterministic decision function the `kcp-harness` proxy uses. Every governed turn carries one correlation id, so you can reconstruct exactly why the agent read what it read. It runs on stock Pi — no MCP client required.

## Quickstart

You need Pi (`@earendil-works/pi-coding-agent` ≥ 0.80.6) and Node ≥ 20 (Bun for development). Clone [Cantara/pi-kcp](https://github.com/Cantara/pi-kcp), then:

```bash
bun install
bun run build
bun run smoke          # verifies /kcp registers on both source and built extension
pi -e ./dist/src/index.js
```

That gives you the `/kcp` command surface:

```text
/kcp help                 Show the command list
/kcp health               Check configuration, kcp-memory, and kcp-agent discovery
/kcp recall <query>       Add episodic memory to the next turn
/kcp plan <intent>        Add a deterministic knowledge plan to the next turn
/kcp validate             Validate the project's knowledge.yaml
/kcp init                 Create knowledge.yaml (won't overwrite an existing file)
/kcp govern <full|tool|off|status>  Set how much of the governed cycle runs
/kcp evidence [n]         Show the stage record for the last n governed turns
```

Start with `/kcp health`. It reports whether your `.pi/kcp.json` is valid, whether the kcp-memory daemon is reachable, and where (if anywhere) the kcp-agent CLI was found. The satellite tools are optional and degrade gracefully: recall is fail-open (memory down means the prompt goes through unchanged), and `/kcp plan` needs the `kcp-agent` CLI only if you use it. The governance we're about to exercise needs none of them.

## Declaring a governed skill

Governance is driven entirely by `knowledge.yaml` — the same manifest KCP already uses to declare knowledge units. A **skill** is a unit with `kind: skill` and an `action_scope`:

```yaml
kcp_version: "0.29"
project: my-app
version: 1.0.0
language: en

units:
  # A normal knowledge unit (documentation the planner may load).
  - id: architecture
    path: docs/architecture.md
    intent: "How the service is structured and deployed."
    scope: project
    audience: [agent, developer]
    triggers: [architecture, deploy, layout]

  # A governed skill: kind: skill + action_scope defines its authority.
  - id: deploy
    path: .pi/skills/deploy/SKILL.md
    intent: "Deploy the service to staging."
    scope: project
    audience: [agent]
    triggers: [deploy, release, ship]
    kind: skill
    action_scope:
      tools: [read, bash]                     # only these tools are authorized
      paths: [src/deploy, scripts/deploy.sh]  # only these paths/prefixes
      capabilities: [deploy]                  # optional capability allowlist
```

The semantics are worth stating precisely, because they're the whole contract:

- Each declared dimension is an **allowlist**. If `tools` is declared, the action's tool must be a member. If `paths` is declared, every path (or URL prefix) the action reaches must sit under an authorized prefix.
- A dimension you **don't** declare does not constrain that facet.
- A scope that declares **nothing** authorizes nothing — every action under that skill is held. Fail-closed is the default posture, not the exception.

![The Allowlist Vault — an action_scope of tools and paths funnels write_file and execute requests to a block, while an authorized read_file request reaches the vault](/assets/images/blog/the-skill-is-the-security-boundary/allowlist-vault.png)

Run `/kcp validate` before relying on it. Authoring conventions for skill units — what a *good* `action_scope` looks like, an SK001–SK008 linter, and conformance vectors with expected verdicts — live in [Cantara/kcp-skill](https://github.com/Cantara/kcp-skill); `npx kcp-skill-lint knowledge.yaml` lints your manifest's skill units.

At runtime, the cycle per turn is short: a fresh W3C `traceparent` correlation id is minted at `turn_start`; when the agent loads a skill by reading its `SKILL.md`, that read is recognized and the skill becomes *active*; from then on, every native `tool_call` is mapped to an action (tool name plus its `path`/`file_path`/`url` targets), the active skill's `action_scope` is resolved from `knowledge.yaml`, and kcp-harness's deterministic `checkConformance` adjudicates before the call runs.

![Inside the turn: the enforcement cycle — turn starts, skill loads, action intent forms, then the gate (checkConformance against knowledge.yaml) routes to execute or hold with a written reason](/assets/images/blog/the-skill-is-the-security-boundary/enforcement-cycle.png)

One deliberate design point: enforcement is scoped, not blanket. When **no** skill is active, conformance is not applicable and the call passes through to Pi's other gates and approval — conformance bounds a *skill's* actions; it does not govern general, unscoped ones. For high-assurance autonomous agents that should only ever act within a declared skill, set `requireActiveSkill: true` and no-skill calls fail closed too.

Now the three demos. All of them live in the repo under `demos/` and run without an LLM — the point is that the decisions are deterministic.

## Use case 1 — the allowlist in action: one pass, two blocks

![Proof 1: the allowlist in action (Demo 3) — a read_file request inside ops/ passes, a read_file request to secrets/master.key is blocked as a path mismatch, a fetch request is blocked as a tool mismatch](/assets/images/blog/the-skill-is-the-security-boundary/proof1-allowlist-in-action.png)

Demo 3 feeds three actions straight into the real `checkConformance` export from `kcp-harness`, under a skill scoped to `tools: [read_file, write_file]` and `paths: [ops/, deploy/]`. The core is a two-line use of the real API:

```js
import { checkConformance } from "kcp-harness";
const scope = { tools: ["read_file", "write_file"], paths: ["ops/", "deploy/"] };
checkConformance({ tool: "read_file", paths: ["/etc/shadow"] }, scope); // → passed:false
```

Run it:

```bash
cd demos
node 03-out-of-bounds-conformance/run.mjs
```

**Action 1 — in scope.** `read_file "ops/service.conf"` sits under an authorized prefix, with an authorized tool:

```json
{
  "gate": "conformance",
  "passed": true,
  "reason": "action \"read_file\" on ops/service.conf is within the active skill's declared action_scope",
  "evidence": { "tool": "read_file", "scopeTools": ["read_file","write_file"], "scopePaths": ["ops/","deploy/"], "target": "ops/service.conf" }
}
```

Note the verdict pins the checked target as `evidence.target`. A pass is not a silent no-op — it's a record of what was checked and against what.

**Action 2 — out of scope by path.** Same authorized tool, wrong target:

```json
{
  "gate": "conformance",
  "passed": false,
  "reason": "target \"/etc/shadow\" is outside the skill's authorized paths [ops/, deploy/]",
  "evidence": { "tool": "read_file", "scopeTools": ["read_file","write_file"], "scopePaths": ["ops/","deploy/"], "target": "/etc/shadow" }
}
```

**Action 3 — out of scope by tool.** The skill never declared any network tool, so a fetch is held regardless of destination:

```json
{
  "gate": "conformance",
  "passed": false,
  "reason": "tool \"WebFetch\" is outside the skill's authorized tools [read_file, write_file]",
  "evidence": { "tool": "WebFetch", "scopeTools": ["read_file","write_file"], "scopePaths": ["ops/","deploy/"], "target": "WebFetch" }
}
```

Look at what the reasons do: they name the violating target *and* surface the authorized scope as the gap. That's not cosmetic. Inside a Pi session, a blocked call surfaces to the agent as exactly that written reason —

```text
target "/etc/passwd" is outside the skill's authorized paths [src/deploy, scripts/deploy.sh]
```

— which means the agent can correct course (take an in-scope action instead), and the human reviewing the evidence later can see *why* an action was held without reverse-engineering anything. This is "grounding, but for actions": every verdict carries its own justification.

![Grounding for actions: the written reason — the blocked-call error naming secrets/master.key as out of scope and the authorized paths, surfacing to both the agent (to self-correct) and the human reviewer (to see why without reverse-engineering an LLM's thoughts)](/assets/images/blog/the-skill-is-the-security-boundary/grounding-written-reason.png)

## Use case 2 — governance as an enabler: the research assistant

It's tempting to read all of this as a machine for saying no. Demo 9 shows the other half, and honestly the more important one: **a well-declared scope is what lets a bounded agent run autonomously at all.**

![Proof 2: governance as the enabler (Demo 9) — a research bot runs freely inside its declared box with zero blocks and zero approval tickets, every one of its actions a signed, approved receipt](/assets/images/blog/the-skill-is-the-security-boundary/proof2-governance-as-enabler.png)

The setup: a deterministic, read-only research agent loads a `research-topic` skill whose `action_scope` permits read/search tools over `research/`, `docs/`, and `knowledge/` — and no writes. The governed tool surface literally has no write tool. The agent then does its work, every step a real MCP `tools/call` through the `kcp-harness serve` proxy:

```bash
cd demos
node 09-research-assistant/run.mjs
```

```text
governed tool surface: … read_file, search_files, Skill   (read-only — no write tool exists)

Autonomous read-only run (each step is a real MCP tools/call through the proxy):
  ✅ ALLOW load research skill    → [downstream] skill "research-topic" loaded
  ✅ ALLOW read market scan       → # Market scan — governed autonomous agents (Q3 2026)
  ✅ ALLOW read architecture      → # Architecture — the proxy sits between the agent and its tools
  ✅ ALLOW read glossary          → # Glossary
  ✅ ALLOW search corpus          → research/market-scan.md: first for an audit trail: every autonomous
```

Every action allowed. Zero blocks. Zero approval tickets — nothing needed a human, because nothing left the declared box. The agent then grounds a short cited summary against the units it actually read:

```json
{
  "status": "grounded",
  "grounded": [
    { "claim": "The harness is a Model Context Protocol proxy that adjudicates governed calls before forwarding them.", "unitId": "architecture-doc", "sha256": "c96d8d3cd6f3…" },
    { "claim": "Buyers ask first for an audit trail of every autonomous action.", "unitId": "market-scan", "sha256": "386c2d5ce357…" }
  ],
  "gaps": []
}
```

And the whole run reconstructs as one clean audit chain — a `skill_loaded` event plus one conformance verdict per action, all approved:

```text
  # 1 session_start        approved   session_start
  # 3 skill_loaded         approved   kind: skill with explicit eligibility grant
  # 5 conformance_verdict  approved   action "read_file" on research/market-scan.md is within the active skill's declared action_scope
  # 7 conformance_verdict  approved   action "read_file" on docs/architecture.md is within …
  # 9 conformance_verdict  approved   action "read_file" on knowledge/glossary.md is within …
  #11 conformance_verdict  approved   action "search_files" on research/ is within …
  #12 session_end          approved   session_end
```

```json
{ "sessions": 1, "events": 12, "governed": 5, "blocked": 0, "budgetExceeded": 0, "drifts": 0, "signatureBlocked": 0 }
```

This is the trade you're actually making when you declare an `action_scope`. Without it, "let the agent run unattended" is a judgment call someone has to defend later with nothing in hand. With it, the question changes shape: the agent ran freely, *and* here is the chain showing that every single action it took was inside the authority we declared for it, with zero holds. Autonomy with receipts is a much easier thing to say yes to than autonomy on trust — and the agent isn't slowed down one bit inside its box.

![The trade-off: trust vs. receipts — implicit boundaries and human-in-the-loop judgment calls on the left, explicit code-bound rules, zero human bottlenecks, a single clean trace-id audit chain, and provable enterprise-readiness on the right](/assets/images/blog/the-skill-is-the-security-boundary/trust-vs-receipts.png)

## Use case 3 — two depths, one verdict

Now the demo that ties directly back to *Policy vs. Enforcement*. That post's claim was that a policy is only as good as the enforcement point that carries it — and that KCP's enforcement is the *same decision* wherever you mount it. Demo 10 proves it mechanically.

![Proof 3: two depths, one verdict (Demo 10) — external tools through the MCP proxy hook and native Pi tools through the runtime hook both feed the same checkConformance function, producing byte-identical verdict receipts](/assets/images/blog/the-skill-is-the-security-boundary/proof3-two-depths-one-verdict.png)

The same out-of-scope action — `read_file "secrets/master.key"` under a skill scoped to `paths: [ops/]` — is driven through two completely different depths of the stack:

- **(a) Proxy depth** — through the real `kcp-harness serve` MCP proxy, sitting between the agent and its tool server. The proxy resolves the skill's `action_scope` and adjudicates with `checkConformance`.
- **(b) Runtime depth** — through pi-kcp's real `HarnessConformanceChecker`, the seam its Pi extension wires at the `tool_call` boundary *inside the turn*. It resolves the same skill's `action_scope` from the same manifest and calls the same pure `checkConformance`.

```bash
cd demos
node 10-two-depths-one-verdict/run.mjs
```

Proxy depth blocks it in-loop:

```text
(a) PROXY DEPTH — spawning: kcp-harness serve --config <config>
  proxy tool result: ⛔ HELD — [kcp-harness] CONFORMANCE BLOCKED: target "secrets/master.key" is outside the skill's authorized paths [ops/]
```

```json
{ "skillId": "deploy-skill", "passed": false,
  "reason": "target \"secrets/master.key\" is outside the skill's authorized paths [ops/]",
  "tool": "read_file", "target": "secrets/master.key", "ticketId": "…" }
```

Runtime depth, same action, same manifest:

```text
(b) RUNTIME DEPTH — pi-kcp HarnessConformanceChecker over the SAME action + manifest
  ran via: REAL pi-kcp HarnessConformanceChecker (transpiled from src/harness-conformance.ts)
```

```json
{ "passed": false, "reason": "target \"secrets/master.key\" is outside the skill's authorized paths [ops/]" }
```

Same `passed`. Same written reason, byte for byte. The demo's verdict block asserts it:

```text
  ✔ proxy depth BLOCKED the out-of-scope action in-loop
  ✔ runtime depth also holds the action (passed:false)
  ✔ SAME passed verdict at both depths
  ✔ SAME written reason at both depths (identical adjudication)
  ✔ the shared reason names the violating target + the authorized scope
✅ Demo 10 — Two Depths, One Verdict: ALL CHECKS GREEN
```

Why this matters: proxy depth and runtime depth have different coverage profiles. The proxy governs any agent whose tools flow through MCP — you don't need to touch the agent. The runtime hook governs Pi's *native* tool calls — the ones that never cross an MCP boundary at all. In a real deployment you may want both, and the thing you must not have is two enforcement points that interpret the same policy differently. Here the policy is one `action_scope` in one `knowledge.yaml`, the adjudicator is one pure function, and the verdict is provably identical regardless of where the action was observed. Policy and enforcement stay one artifact. That's the claim from the LinkedIn post, now with the mechanics attached.

![The danger of split-brain enforcement — the same knowledge.yaml action_scope must never feed two engines that disagree, one passing and one failing the same action; policy and enforcement must remain a single unified artifact](/assets/images/blog/the-skill-is-the-security-boundary/split-brain-enforcement-danger.png)

## What governance costs, and the dials you have

Runtime governance in pi-kcp has three modes, set in `.pi/kcp.json` or switched mid-session with `/kcp govern <full|tool|off>`:

| Mode | What runs | Cost |
|---|---|---|
| `"full"` | all seven stages, including the per-turn planner trace that gates skill selection | one `kcp-agent` invocation per turn (~57ms); requires kcp-agent |
| `"tool"` | the governance boundary: conformance at `tool_call`, integrity at `tool_result` | no subprocess, no kcp-agent dependency |
| `"off"` | no cycle, no records | — |

![The cost & dials: governance modes — full runs all seven stages at ~57ms per subprocess and requires kcp-agent, tool runs conformance at tool_call only with no subprocess overhead, off runs no cycle or records](/assets/images/blog/the-skill-is-the-security-boundary/governance-modes-cost-dials.png)

Two subtleties. First, `"off"` is not "no enforcement": the conformance check at `tool_call` predates the cycle and still runs in every mode — `"off"` means pi-kcp keeps no turn record and makes no liveness claim. Second, a turn is judged against what its mode promised: `"tool"` mode is never reported as ungoverned for stages it never claimed to run.

*Lowering* the mode mid-session is announced in the session — weakening a guarantee is a governance decision, so it leaves the same trace a lapse does rather than happening quietly. Raising it is not announced; strengthening needs no alibi.

There's one more dial worth knowing: `gateFailurePosture` decides what the runtime does when its *own* gate breaks — a stage errored and it can no longer establish what is authorized. `"announce"` (the default) reports the lapse prominently and keeps the host usable; `"block"` fails closed and refuses tool calls for the rest of the turn. Use `"block"` where a turn that cannot be governed must not act.

![Failure postures: when the gate breaks — a cracked lock branching to "announce" (reports the lapse, keeps the host usable) or "block" (fails closed, refuses tool calls for the rest of the turn)](/assets/images/blog/the-skill-is-the-security-boundary/failure-postures-gate-breaks.png)

And the evidence is always one command away: `/kcp evidence [n]` prints the stage record for the last n governed turns — a bounded 20-turn inspection window, not storage. Durable, exportable evidence belongs to the harness's append-only audit log, which `kcp-harness export` turns into SOC 2 Type II, ISO 27001, ISO/IEC 42001, or EU AI Act artifacts. Because pi-kcp shares the harness's decision function and correlation scheme (the join key is the W3C trace-id, threaded through recall, plan, and every conformance decision in a turn), runtime-depth decisions line up with proxy-depth audit.

![From turn record to enterprise audit — a single turn record, keyed by a W3C trace-id, feeding SOC 2 Type II, ISO 27001, ISO/IEC 42001, and EU AI Act artifacts](/assets/images/blog/the-skill-is-the-security-boundary/turn-record-to-enterprise-audit.png)

## The boundary was always there — now it's written down

Every skill you hand an agent already *implies* a boundary; the author had one in mind. pi-kcp just refuses to leave it implied. The declaration is a few lines of YAML in a manifest you likely already have. The enforcement is a pure function with no model in the loop. The verdicts are written reasons that name the target and the scope. And the same declaration produces the same verdict whether it's checked at an MCP proxy in front of the agent or at the `tool_call` boundary inside it.

The [previous post in this series](2026-07-17-a-firewall-for-what-your-agent-knows.md) put a firewall on what your agent *knows*. This is the other half: the skill your agent acts under now carries its authority with it — declared, enforced, and accounted for. Not because we've stopped trusting the agent, but because "the research skill only ever touched the research corpus" is something you should be able to *show*, not just believe. Now you can, in one audit chain, with zero blocks when the agent behaves — and a written reason when it doesn't.

![The boundary was always there. Now it's written down. — a hand-wave thought bubble ("the agent should only touch the research files...") turned into a declared action_scope of paths: [research/], with links to the pi-kcp repo, kcp-skill repo, and the live playground](/assets/images/blog/the-skill-is-the-security-boundary/closing-boundary-written-down.png)

---

*pi-kcp, kcp-harness, and kcp-skill are open source (Apache-2.0): [pi-kcp](https://github.com/Cantara/pi-kcp) · [kcp-skill](https://github.com/Cantara/kcp-skill). Eleven of the demos also run live in your browser — the real decision code, signed receipts and all — at [cantara.github.io/pi-kcp/playground](https://cantara.github.io/pi-kcp/playground/).*
