---
description: "Five agent architectures walk into a comparison: Claude Code (the dominant IDE agent), Crush (Charm's model-flexible terminal agent), OpenClaw (the viral local-first personal assistant), kcp-agent (the deterministic knowledge planner), and pi-kcp (KCP governance running inside the Pi coding agent — the only entry that verifies its own execution against what was approved). They solve different problems — and the differences reveal what the industry still disagrees about."
date: 2026-08-14T15:00:00
draft: true
categories:
  - AI Agents
  - Architecture
tags:
  - claude-code
  - crush
  - openclaw
  - kcp-agent
  - kcp-harness
  - pi-kcp
  - comparison
  - agents
  - mcp
  - determinism
authors:
  - totto
  - claude
---

# Five Agents Compared

The agent landscape in mid-2026 has crystallized into distinct architectural philosophies. This post compares five entries. Four of them — Claude Code, Crush, OpenClaw, kcp-agent — are standalone tools, each successful, each widely discussed, representing fundamentally different answers to the question *"what should an agent be?"*

This is not a feature matrix. It's an architecture comparison. The interesting part isn't which one is "better" — it's what each one *assumes* about the problem, and where those assumptions diverge.

The fifth entry, pi-kcp, is a different kind of thing, and the difference is worth being precise about up front. It isn't a standalone product you'd install instead of the others — it's the KCP governance stack integrated into Pi, an independent coding-agent harness; you'd encounter it as part of choosing Pi as your coding agent. It gets full table presence anyway, because it does something none of the other four do: it verifies its own execution against what was approved — digesting what a gate approved for a tool call and, separately, what actually executed, keyed to the same call, and flagging divergence. Along the way it also settles a question the layering argument below would otherwise leave open: whether the deterministic knowledge layer really can be lifted out of one agent ecosystem and dropped into a completely different one. We'll get there.

<!-- more -->

![The Agent Architecture Fault Lines — probabilistic execution (model-centric, adaptive, non-deterministic) versus deterministic governance (rule-based, auditable, fixed), dissecting the five paradigms shaping the mid-2026 AI landscape](/assets/images/blog/five-agents-compared/cover-fault-lines.webp)
*Two shapes of agent, side by side: the unstructured probabilistic network and the linear deterministic gate cascade.*

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="https://github.com/totto/wiki/releases/download/media/The_Architectural_Divide.mp4" type="video/mp4">
</video>

![AI Agent Architectures 2026: The Battle for the Agentic Core — model-centric (Claude Code, Crush, OpenClaw) versus deterministic (kcp-agent, pi-kcp) contenders, technical specs, the major fault lines, the verification gap, and the layering diagram](/assets/images/blog/five-agents-compared/five-agents-architecture-comparison.webp)
*The whole comparison on one page, if you're skimming.*

## The five, at a glance

![The Mid-2026 Landscape: five answers to "what should an agent be?" — Claude Code (the model IS the agent), Crush (the terminal UX, model-flexible), OpenClaw (always-on, local-first reach), kcp-agent (navigation is a pure function), and pi-kcp (governance runs inside the host)](/assets/images/blog/five-agents-compared/five-answers-landscape.webp)
*Five different bets about what an agent fundamentally is — not a feature checklist, an architecture disagreement.*

| | **Claude Code** | **Crush** | **OpenClaw** | **kcp-agent** | **pi-kcp** |
|---|---|---|---|---|---|
| **One sentence** | Anthropic's IDE-integrated coding agent | Charm's model-flexible terminal agent | Local-first personal AI assistant across 20+ channels | Deterministic knowledge navigation planner | KCP governance embedded in the Pi coding agent, with execution-integrity verification |
| **Written in** | TypeScript | Go | TypeScript (Node.js) | TypeScript reference + Rust and Java planner ports, vector-conformant | TypeScript |
| **Primary job** | Write and edit code in a codebase | Write and edit code in a terminal | Execute tasks across apps, browsers, and system tools | Decide what knowledge an agent should read, and why | Govern a host agent's turns and verify what executed against what was approved |
| **Model dependency** | Claude (Anthropic only) | 30+ providers, switchable mid-session | Multiple (primarily OpenAI) | None for planning; optional model for synthesis | None of its own — governs whatever model Pi runs |
| **MCP support** | Client (consumes MCP tools) | Client + Server (full stdio/HTTP/SSE) | Registry-based | Server (exposes 5 tools to any MCP client) | None needed — hooks Pi's typed extension events directly |
| **Where it runs** | Terminal / IDE | Terminal (any OS including Android, FreeBSD) | Self-hosted gateway (local-first) | CLI, MCP server, library import, or native binary | Inside Pi, as an extension |
| **License** | Proprietary (Anthropic) | Open source | Open source | Apache-2.0 | Apache-2.0 |
| **GitHub stars** | N/A (proprietary) | ~27K | ~380K+ (most-starred repo on GitHub; the count fluctuates as bot-stars get purged) | ~modest (protocol-first, not viral) | ~0 (a weeks-old extension, not a product launch) |

*Star counts checked August 2026. Crush grew from ~25K to ~27K over the month; OpenClaw from ~347K to ~380K+ — nothing that changes either story. pi-kcp's count is exactly what you'd expect for a young extension to a niche host.*

---

## What each one actually does

![The Terminal, The IDE, and The Orchestrator — Claude Code's 217MB compiled binary with a hidden loop and Tengu-swarm subprocess spawner, Crush's model hot-swap and pure-Go POSIX shell interpreter, OpenClaw's local-first gateway architecture reaching 20+ messaging channels](/assets/images/blog/five-agents-compared/terminal-ide-orchestrator.webp)
*Three model-driven architectures, three different bets about what the interface should be — none of them touch navigation determinism.*

### Claude Code — the model IS the agent

Claude Code is the purest expression of the model-centric architecture. The LLM *is* the reasoning engine, the navigation system, the code writer, and the decision-maker. It decides which files to read, which tools to call, which changes to make. The human approves or rejects.

**Under the hood**: The loop itself is genuinely off-limits — it lives inside a compiled CLI binary of roughly 217 MB, and even Anthropic's own Agent SDK doesn't implement it. The SDK spawns the CLI as a subprocess and speaks a bidirectional control protocol over stdin/stdout; hooks and permission callbacks are IPC round-trips into a loop you cannot see. (One genuinely unusual power lives at that boundary: a permission callback can rewrite a tool call's input before execution, not just allow or deny it.) But real behavior is knowable, because a build of the CLI briefly shipped to npm with readable source in April 2026, and what it revealed sharpens the picture. The auto-approval system is not a static rule engine — it's an LLM classifier that reads your rules as natural language in three categories (`allow`: "run any read-only git command"; `soft_deny`: "modify files outside the project directory"; `environment`: facts about your setup for the classifier's benefit) and reasons about each tool call against them. There's even a meta-command, `claude auto-mode critique`, that runs a second model call to review your rule set for clarity, conflicts, and gaps — an LLM critiquing the rules you wrote for an LLM. Loop-runaway protection is `max_turns`: a ceiling, not a detector — it stops a runaway session but never notices oscillation, let alone diagnoses it. And multi-agent reaches beyond the documented subagents: a feature-gated coordinator mode (internal codename "Tengu swarms") manages leader/worker topologies, with workers running in separate tmux panes and a permission bridge propagating the leader's approvals downward.

**Strengths**: Deep IDE integration. The model sees your entire codebase and reasons about it fluidly. Hooks add a deterministic shell around the probabilistic core — `PreToolUse`, `PostToolUse`, `UserPromptSubmit` fire shell commands at fixed lifecycle points regardless of what the model decides. Skills package domain knowledge as loadable instruction sets. Subagents provide isolated context windows for parallel work.

**Architecture bet**: The model is smart enough to navigate. Give it the right context and instructions, and it will make good decisions. When it doesn't, hooks enforce guardrails deterministically. And the bet runs one layer deeper than navigation: in auto-mode, even the decision to allow a tool call is a model call.

**The gap**: Navigation decisions are opaque. Why did it read *this* file and not *that* one? You can ask it, but the answer is a post-hoc explanation from the model, not a reproducible decision trail. The hooks layer is deterministic, but the hooks don't decide *what* to read — they guard *how* the model acts on what it decided to read. The opacity is a deliberate trade, and it's worth naming what it buys: because the binary absorbs all loop complexity, thin clients stay forward-compatible across CLI versions — unknown message types are skipped, not errored on. What it costs: context compaction is unconfigurable, loop behavior is uninspectable, and when something goes wrong inside the loop, the only lever you were given is the `max_turns` ceiling.

### Crush — the terminal, model-flexible

Crush is Charm's answer: same category as Claude Code (agentic coding), but with radical model flexibility. You bring your own key, pick from 30+ providers (OpenAI, Anthropic, Google, Groq, Bedrock, Azure, self-hosted), and switch mid-session. LSP integration gives it language-server-grade code intelligence. The Go binary runs everywhere — including Android and FreeBSD.

**Under the hood**: The model isn't the only thing Crush treats as pluggable — it doesn't even own its agent loop. The loop lives in `charm.land/fantasy`, Charm's own LLM library; Crush steers it entirely from outside, through a `PrepareStep` callback that runs before every model call (drain user messages queued while the agent was busy, inject cache directives, record the turn) and a list of `StopWhen` predicates checked after every step. Two predicates do the heavy lifting. One is a context budget: stop 20,000 tokens before the limit on large-context models, at 20% remaining on small ones, then auto-summarize — with the current todo list folded into the summary so the resumed session knows where it was. The other is loop detection, and it's refreshingly literal: a SHA256 hash of `toolName + input + output` per step; if any identical hash appears more than five times in a ten-step window, the loop ends. That catches true oscillation — same call, same result, over and over — with essentially no false positives. It also means a loop whose output varies even slightly each round sails straight through, and when it does trigger, the loop just stops: no corrective message, no diagnosis. The shell tool is a quiet standout: not `os/exec` but a complete POSIX shell interpreter in pure Go (`mvdan.cc/sh/v3`), so `cd` and exported variables actually persist across tool calls — state that most agents' shell tools silently reset. Prompt caching is explicit and mechanical — cache markers placed on the last tool definition, the last system message, and the last two messages, worth a documented up-to-80% cost reduction on long sessions. And because models, tools, and the system prompt live in thread-safe `csync` containers, all three can be hot-swapped mid-session without a restart; the next `PrepareStep` simply picks up the new model. No one else in this comparison can do that.

**Strengths**: No vendor lock-in. The same tool works with whatever model your company approves. LSP-enhanced context means it gets code intelligence from real language servers, not from the LLM guessing at syntax trees. MCP support across all three transports (stdio, HTTP, SSE). `.crushignore` gives fine-grained control over what enters context.

**Architecture bet**: The model is interchangeable. The agent's value is the *interface* — the terminal UX, the LSP integration, the MCP plumbing — not which model sits behind it. Make the model a pluggable dependency, not an identity.

**The gap**: Same as Claude Code on navigation transparency — the model decides what to read and how to act. Crush gives you more *choice* of which model makes those opaque decisions, but the decisions remain opaque. No deterministic knowledge selection layer.

### OpenClaw — the local-first orchestrator

OpenClaw is architecturally different from the other entries. It's not a coding agent — it's a *personal assistant* that happens to be capable of coding. It runs as a self-hosted gateway on your own device, connects to 20+ messaging channels (WhatsApp, Telegram, Slack, Discord, iMessage, Teams, Signal, Matrix...), and executes multi-step workflows: browse the web, fill forms, manage your inbox, schedule meetings, run shell commands, call APIs.

**Strengths**: Channel breadth — it meets you wherever you already communicate. Local-first means your data stays on your device. The gateway architecture (sessions, channels, tools, events) provides a clean control plane. DM pairing and sandboxing enforce security boundaries. 100+ built-in skills cover common automation tasks.

**Architecture bet**: The agent should be *always-on and everywhere*, not confined to a terminal or IDE. The value is in orchestrating your digital life, not in code generation specifically. Local-first because trust requires control.

**The gap**: Knowledge selection is implicit — the model decides what's relevant from whatever context it has. No structured knowledge manifests, no temporal validity, no audit trail for *why* the agent chose to act on one piece of information rather than another. The security model (DM pairing, sandboxing) addresses *who can talk to the agent*, not *what the agent reads and why*.

A verification note, in fairness to the other entries: the Claude Code and Crush mechanics above come from actual source reads, and the KCP material below does too. OpenClaw's loop-level mechanics — how it detects oscillation, when and how it compacts context, what its permission internals actually do — have not been independently verified from source for this post. The description here is architecture-level, from documentation and observed behavior. That's a gap in this comparison, not necessarily in OpenClaw.

![The Model-Centric Bet — File Navigation, Code Generation, Tool Selection, and Orchestration all radiating from a single model core wrapped in imperative guardrails; the trade-off is extreme flexibility against complete opacity, because the loop itself is uninspectable](/assets/images/blog/five-agents-compared/model-centric-bet.webp)
*Claude Code, Crush, and OpenClaw share this shape underneath their differences: the model is the reasoning engine, navigator, and decision-maker, with guardrails wrapped around — not inside — that probabilistic core.*

### kcp-agent — the deterministic planner

kcp-agent inverts the architecture. The LLM is not the agent — it's an optional layer at the edge. The core is a pure-function planner that reads structured knowledge manifests (`knowledge.yaml`) and produces an inspectable, reproducible plan *before any content is loaded and before any model is called*.

![The Deterministic Inversion — the old way is probabilistic navigation, a model radiating chaotic read decisions across a pile of documents; the KCP way is knowledge.yaml through a pure function planner producing a byte-reproducible plan the LLM only executes, spending zero tokens on deciding what to read](/assets/images/blog/five-agents-compared/deterministic-inversion.webp)
*Navigation is a deterministic problem, not a language problem — the model never touches the decision of what to read.*

A framing note before the details: the loop mechanics that dominate the two entries above — oscillation detection, context compaction, prompt caching — mostly have no analogue here, because there is no loop. The planner is a single deterministic function evaluation: manifest in, plan out, done. Whatever loop exists belongs to the host agent consuming the plan. This part of the comparison is apples to a different fruit, on purpose.

A month is a long time in this repo. Since this comparison was first drafted, the KCP spec has moved from v0.21 to v0.32 (the reference agent is at npm v0.27.0), and the growth was in one specific direction: from governing *what an agent reads* to governing *what it may do*. Four RFCs landed in sequence: `kind: skill` and then `kind: playbook` mark units an agent could enact — a runbook, a procedure, a multi-step composition (RFC-0027); an explicit `load_eligible` grant is required before any of them is invoke-eligible, and eligibility deliberately does not compose — a grant on a playbook does not reach the units its steps name (RFC-0028); skills carry authority levels and a declared `action_scope` naming the tools, paths, and capabilities they may touch, with `action_scope.deny` as a blanket prohibition (RFC-0029); and a playbook's deny list unions with each step's — deny is final, an allow can never override it (RFC-0030). When something tries anyway, the spec's §17 now defines a normative `prohibited_attempt_events` wire format, so a refused attempt is an audit artifact, not a silent no.

**Strengths**: Navigation is deterministic — same task, same manifest, same date → same plan, byte for byte, forever. Every unit selected or skipped carries a structured reason. The decision trace walks all 14 gates (the `skill_eligibility` gate joined the cascade this cycle) and writes a per-gate verdict. Plans are diffable across time and replayable from saved artifacts, and reproducibility by independent implementations is no longer a promise: the Rust and Java planner ports ship from the same repo and must pass the same conformance vectors as the TypeScript reference. Beyond loading, the same fail-closed discipline now extends downstream — grounding verifies each claim in a synthesized answer against a loaded unit's pinned hash, and `assess()` gates whether a conclusion clears a confidence threshold before it is acted on. Zero tokens spent on navigation. Fail-closed on everything: unsigned manifests, unaffordable units, expired documents, missing attestations, ungranted skills.

**Architecture bet**: Navigation is not a language problem — it's a deterministic problem. The model should never decide what an agent reads. A pure function should, and the model should synthesize from exactly what the function selected. The past month extends the bet: what an agent may *do* shouldn't be a model decision either — it should be a declared, granted, deny-final scope.

**The gap**: It doesn't write code. It doesn't browse the web. It doesn't connect to WhatsApp. It does exactly one thing — decide what knowledge and which procedures an agent may use, and why — and delegates everything else. That's the point, but it means it's a *component*, not a complete agent. And its scorer is lexical by design: a unit is only findable through the words its manifest declares, which is reproducible and free, but means a badly-written manifest hides good content — the fix belongs to the publisher, not the planner. One more honest limit: kcp-agent plans and withholds; by itself it cannot stop a determined host agent from touching a file outside the plan. Enforcement at the tool-call boundary is a different job — which is exactly why the next tool exists.

### kcp-harness — the enforcement layer (new since the first draft)

![The Governance Enforcer: kcp-harness — Claude Code, Cursor, Copilot, and Crush all route their agent requests through the kcp-harness proxy firewall's four-stage pipeline (classify, govern, execute, audit) before reaching files, shell, or APIs, with the audit log exporting SOC 2, ISO 27001, and EU AI Act compliance evidence](/assets/images/blog/five-agents-compared/governance-enforcer-kcp-harness.webp)
*The agent cannot bypass governance because it only talks to the proxy's MCP interface — every tool call is classified, governed, executed, and audited, not just the ones the model remembers to check.*

kcp-harness didn't exist in the original version of this post, and it changes the shape of the KCP story enough to earn its own section. It's an MCP compliance proxy that sits between an agent and its tools. Every tool call flows through a pipeline that is literally numbered as steps in the source — classify → govern → execute → audit, with a conformance check wedged between the first two once a governed skill is active. A classifier decides whether a call targets governed knowledge (`Read("docs/api.md")` where `docs/` is governed? through the planner; `Read("package.json")`? pass through). The governor runs the same 14-gate cascade as kcp-agent, either against a cached approved plan or by auto-planning when the agent never asked. And everything — governed or not — lands in an append-only, hash-chained audit log, with an itemized budget ledger, temporal drift detection for long-running sessions, durable human-approval tickets (a resolution requires a named reviewer and a policy citation), and a confidence gate (`harness_assess`) that can route a low-confidence conclusion to a human before it's acted on. From that audit log it exports compliance evidence bundles mapped to SOC 2 Type II, ISO 27001:2022, ISO/IEC 42001, and EU AI Act controls.

Under the hood, held to the same standard as the entries above — this is from `proxy.ts`, `classifier.ts`, `governor.ts`, and `conformance.ts`, not the README:

Classification is six rules, applied in order, as a pure function. KCP's own tools are always governed (they are the governance layer); skill tools — `Skill`, `kcp_skill`, or anything a domain declares in its `skills` list — are governed as skill invocations; a tool a domain lists by name is governed outright; then a file path is extracted from known argument shapes (Read/Edit/Write/Glob/Grep plus common MCP filesystem tools) and matched against governed path prefixes, with `../` segments resolved first precisely to block traversal bypass and prefix matches anchored at directory boundaries; then URLs against URL prefixes; otherwise pass-through. Bash is the honest weak spot: path extraction from shell commands is a best-effort regex over `cat`/`cp`/redirect/`open("...")` patterns, and a sufficiently creative command evades it — which is exactly why the per-agent hook integrations exist to close the shell side door.

`govern()` tries modes in strict order, and the order is a policy statement. Mode 0: human-approval rules outrank every automated path — an approved plan must not bypass a rule that says a named human decides, and if the approval store is unreachable the call is blocked, because the harness cannot prove a human signed off. The ticket lifecycle is explicit: `approved` allows with the reviewer, timestamp, and policy citation attached to the decision; `pending_review` denies with the ticket id and an instruction to retry after approval; `dismissed` is a terminal block; `expired` or absent opens a fresh ticket carrying the required role and expiry. Mode 1: an already-approved plan covering the target. Mode 2: auto-plan against the domain's manifest on the fly, fail-closed on planner error. Mode 3 — new this cycle — covers a governed call with no extractable target at all: if a governed skill is active and its declared `action_scope` authorizes the tool by name (a simulator tool with no file argument, say), the call is approved as scope-conformant, adjudicated by the exact same pure function the conformance gate uses. Everything else: blocked. One asymmetry the source comments state plainly: `govern()` by itself never opens an approval ticket for an ordinary out-of-scope hold — that richer ticket-routing lives in the proxy — so a non-proxy host calling `govern()` directly gets fail-closed blocks, not held-for-human tickets.

Conformance is a pure, no-I/O adjudicator. Each declared dimension of a skill's `action_scope` is an allowlist — tools by exact name, paths by glob/prefix, capabilities — and deny is consulted before allow. Under a playbook, the effective denylist is the per-dimension union of the playbook's deny and the step skill's deny; a deny hit is final, never a grantable hold, and the verdict pins the exact deny entry that fired so the audit names the binding prohibition. A scope that declares nothing authorizes nothing, and even absence is fail-closed: a loaded skill with no declared scope becomes an empty scope, which holds every later governed action.

And a limitation stated in a source comment rather than buried: the harness does not track playbook step boundaries. An enacted playbook's `action_scope.deny` blankets every subsequent governed action until another playbook is enacted — there is no per-step enforcement yet. The comment's defense is correct as far as it goes — over-broad only in the direction union permits, more refused, never less — but "blanket deny, no step granularity" is the current truth.

The crucial architectural property: the agent can't bypass governance because it only talks to the proxy's MCP interface. kcp-agent makes decisions plannable; kcp-harness makes them enforceable at the tool-call boundary. One `kcp-harness integrate <agent>` command generates the wiring for nine hosts — Claude Code, Cursor, Copilot, Windsurf, Cline, Continue, Crush, OpenClaw, and Pi — each with its own config format and quirks.

**The gap**, stated with the same honesty as everyone else's: the harness governs what routes through it. An agent with direct, un-hooked filesystem or shell access can still walk around the proxy — the per-agent integrations exist precisely to close those side doors (Claude Code's uses `PreToolUse` hooks), but the guarantee is only as complete as the wiring. It's also young (v0.15.x), and a compliance bundle maps controls to evidence — it is not, by itself, an audit.

---

## The architectural fault lines

These tools disagree on six fundamental questions:

![Fault Line 1: Who Decides and Who Explains? — "ask the model" produces a post-hoc, non-reproducible speech bubble, while the 14-gate cascade produces a diffable, written verdict with a structured reason for why knowledge was selected or skipped](/assets/images/blog/five-agents-compared/fault-line-1-who-decides.webp)
*Only KCP produces a structured, re-derivable explanation for why knowledge was selected — prior to the model ever being invoked.*

### 1. Who decides what the agent reads?

| | Who navigates? |
|---|---|
| **Claude Code** | The model, guided by instructions (CLAUDE.md) and constrained by hooks |
| **Crush** | The model (any of 30+ providers), guided by LSP context and MCP tools |
| **OpenClaw** | The model, guided by skills and workspace configuration |
| **kcp-agent** | A pure function over declared metadata. The model is never consulted. |
| **pi-kcp** | The same pure function, transplanted — kcp-agent runs inside Pi, and Pi's model synthesizes from what it selected |

This is the deepest disagreement. Claude Code, Crush, and OpenClaw all assume the model is the right entity to decide what to read. kcp-agent assumes the opposite — that navigation should be deterministic and the model should only see what a function selected. pi-kcp carries that assumption into a different host unchanged.

### 2. Can you explain why?

| | Explainability |
|---|---|
| **Claude Code** | Ask the model (post-hoc); hooks provide lifecycle audit events |
| **Crush** | Ask the model (post-hoc) |
| **OpenClaw** | Ask the model (post-hoc); gateway logs provide event history |
| **kcp-agent** | Structured decision trace, diffable plans, byte-identical replay |
| **pi-kcp** | The same decision trace, plus a per-turn stage ledger recording a digest of what each governance stage actually saw |

Only the KCP entries — kcp-agent, and pi-kcp running it inside Pi — produce a deterministic, structured, reproducible explanation for why each piece of knowledge was selected or skipped. The others can explain after the fact, but the explanation is a model generation — non-deterministic, non-reproducible, non-diffable.

### 3. What's the trust model?

| | Trust boundary |
|---|---|
| **Claude Code** | The model decides trust; hooks enforce guardrails |
| **Crush** | The model decides trust; `.crushignore` controls context inclusion |
| **OpenClaw** | DM pairing, sandboxing, channel-level access control |
| **kcp-agent** | Manifest-declared trust: attestation, ed25519 signatures, credentials, audience gates — all evaluated deterministically before any content is loaded |

OpenClaw has the most sophisticated *user* trust model (who can talk to the agent). kcp-agent has the most sophisticated *knowledge* trust model (what the agent reads and under what conditions). pi-kcp doesn't get its own row here: it inherits kcp-agent's row wholesale — the manifests and the gates are the same.

### 4. Who bounds what the agent may do?

This fault line barely existed a month ago. It's where the KCP side moved fastest.

![Fault Line 2: The Boundary of Action — Claude Code's PreToolUse hook is an imperative bash function calling an LLM classifier to evaluate natural-language policy, while kcp-agent's policy.yaml is a declarative action_scope with an allowlist and a deny-final block that can never be overridden](/assets/images/blog/five-agents-compared/fault-line-2-boundary-of-action.webp)
*In KCP, a deny is final — it can never be overridden by an allow. Adjudication is a pure, no-I/O function, not a probabilistic classification.*

| | Action governance |
|---|---|
| **Claude Code** | Hooks and permission prompts — imperative guards you write yourself, at fixed lifecycle points; in auto-mode, the approval decision itself is an LLM classifier over natural-language rules |
| **Crush** | Per-tool permission prompts; no declared action model |
| **OpenClaw** | Sandboxing and channel access control — bounds the blast radius, not the individual action |
| **kcp-agent / kcp-harness** | Declared `action_scope` per skill (tools, paths, capabilities), explicit eligibility grants, authority levels, union'd deny lists where deny is final — adjudicated through the same 14-gate cascade, refused attempts emitted as normative `prohibited_attempt` audit events |
| **pi-kcp** | The same declarative `action_scope` conformance, adjudicated at Pi's native tool boundary — plus a check no one else makes: the executed call is verified against the approved call (see fault line 6) |

The distinction is declarative versus imperative. A Claude Code hook is a shell script that fires and does whatever you coded; an `action_scope` is a declaration the planner and harness adjudicate deterministically, with the verdict written down. Both are real governance. Only one of them produces an artifact a third party can re-derive. And Claude Code pushes the model-centric bet one layer deeper than either of the other two: in auto-mode the permission decision itself is a model call — an LLM classifier reasoning over your natural-language rules, with a second LLM on call to critique those rules for conflicts. Maximally flexible, and the exact opposite of re-derivable: the same tool call, under the same rules, can classify differently tomorrow.

### 5. What happens when the loop goes wrong?

This fault line only became answerable by reading real source, so the honest table has a hole in it:

![Fault Line 3: Catching the Doom Loop — Claude's max_turns is a hard ceiling that bounds damage but never notices oscillation, Crush's SHA256 hash-matching over a 10-step window catches byte-identical repeats with zero false positives, and KCP has no loop to protect because a plan is a single function evaluation](/assets/images/blog/five-agents-compared/fault-line-3-doom-loop.webp)
*Deterministic execution paths prevent oscillation by construction; model-based agents and detection systems rely on probabilistic bounds or post-hoc checks instead.*

| | Loop pathology handling |
|---|---|
| **Claude Code** | `max_turns` — a ceiling, not a detector. Bounds runaway sessions; never notices oscillation |
| **Crush** | SHA256 of every step's tool + input + output over a 10-step window; more than five identical hashes → hard stop |
| **OpenClaw** | Not source-verified here |
| **kcp-agent / kcp-harness** | No loop to protect — a plan is a single function evaluation. Runaway behavior belongs to the host agent; the harness's audit log is where you'd see it happening |
| **pi-kcp** | The loop is Pi's, but the governance failure mode is covered: Pi swallows handler exceptions, so a crashed gate would complete a turn ungoverned and silent — pi-kcp makes an ungoverned turn a detected, recorded fact, announced or blocked by configuration |

Crush's SHA256 detector is the strongest verified oscillation catch in this post, and its blind spot is honest and precise: the output must be byte-identical to count. Claude Code's `max_turns` bounds the damage without ever diagnosing it.

It's also worth a paragraph on a tool that isn't a full entry here: OpenCode (`sst/opencode`), whose source was read in the same exercise. It has the best verified answer to the context-overflow-mid-refactoring problem — automatic, structured compaction (goal, discoveries, accomplished, files touched) that replays the truncated user message afterward, so the task continues as if the compaction never happened — and the best debugging story of anything examined: every message part lands in SQLite as it happens, so you can query the agent's state mid-run. Its doom-loop detector (three identical calls in one response) does something neither Claude Code nor Crush does: it turns detection into a permission event, so the user can allow the repetition or feed back a correction the model then acts on. Cost control, meanwhile, goes to Crush's explicit caching. The pattern across the source reads: different tools have verifiably solved different corners of the same problem, and none has solved all of it.

### 6. Does anything verify the gate's verdict against what actually executed?

A permission gate answers "may this call run?". A separate question — one almost nobody asks — is whether the call that ran is the call that was approved. Between approval and execution there is a window, and in some hosts, code is allowed to mutate the call inside it.

![The Hidden Threat: Execution Integrity — Node A (gate approves input, user says yes) and Node B (tool executes input) sit on either side of a Window of Mutation (TOCTOU), where SDK callbacks in many hosts can legitimately rewrite tool inputs before execution](/assets/images/blog/five-agents-compared/hidden-threat-execution-integrity.webp)
*A permission gate answers "may this call run?" Almost nobody asks: "is the call that ran the exact call that was approved?"*

| | Execution-integrity verification |
|---|---|
| **Claude Code** | No — and the window is real: a permission callback can legitimately rewrite a tool call's input before execution. Nothing checks the executed input against the approved one |
| **Crush** | No — approval is a prompt, execution follows, nothing re-checks |
| **OpenClaw** | Not source-verified here |
| **kcp-agent** | Nothing to verify — a pure planner executes nothing |
| **kcp-harness** | Closest: the proxy itself executes the call it governed, which narrows the window by construction — but its own stated gap (it does not track playbook step boundaries) is the honest reason it doesn't fully cover this; governance stops at the tool-call boundary, with no independent re-check of what ran |
| **pi-kcp** | Yes, structurally: the input the gate approved is digested at decision time, the input that executed is digested under the same `toolCallId`, and divergence — or an execution with no recorded approval at all — marks the stage violated |

To be precise about what this is not: it is not capturing the model's self-reported reasoning. A model's stated account of what it did or why runs straight into the unfaithful-reasoning problem — stated chains of thought don't reliably match what the model actually computed — and is exactly the kind of evidence this comparison keeps refusing to accept. Execution-integrity verification is a mechanical, non-self-report check on the gap between intention and execution: the same evidentiary category as the harness's deterministic gate computation, no LLM ever asked to explain itself, applied at finer grain. And it exists because Pi's extension model makes the threat concrete — extensions may mutate a tool call between approval and execution, a TOCTOU-style bypass that a pure planner never sees and that tool-call-boundary governance doesn't catch.

---

## They compose, they don't compete

![Synthesis: They Compose, They Don't Compete — three layers stacked, The Model Agent (Claude/Crush, probabilistic and creative) on top of kcp-harness (tool boundary enforcement and immutable audit) on top of kcp-agent (deterministic knowledge selection), with the note that Claude Code already consumes kcp-agent as an MCP server](/assets/images/blog/five-agents-compared/synthesis-compose-not-compete.webp)
*The KCP stack doesn't replace the agents; it replaces the part of them that should never have been probabilistic.*

Here's the important part: these tools occupy different layers.

```
┌─────────────────────────────────────────────┐
│  Claude Code / Crush / OpenClaw / Pi        │ ← The agent: writes code,
│  (model-driven, probabilistic)              │   browses, orchestrates
├─────────────────────────────────────────────┤
│  kcp-harness (MCP compliance proxy)         │ ← The enforcement layer:
│  classify → govern → execute → audit        │   every tool call, logged
├─────────────────────────────────────────────┤
│  kcp-agent (planner core)                   │ ← The knowledge layer:
│  (deterministic, fail-closed, 14 gates)     │   decides what to read
├─────────────────────────────────────────────┤
│  Knowledge manifests (knowledge.yaml)       │ ← The publishers:
│  (declared metadata, signed, temporal)      │   structured knowledge
└─────────────────────────────────────────────┘
```

Claude Code already consumes kcp-agent as an MCP server:

```bash
claude mcp add kcp -- npx kcp-agent mcp
```

Now Claude Code's model still writes the code and orchestrates the workflow — but the *knowledge selection* is deterministic. The model calls `kcp_plan` or `kcp_load`, and the planner decides what to read. The model synthesizes from exactly what the planner selected. Same task tomorrow → same knowledge loaded → reproducible.

And with the harness in front, the arrangement stops being voluntary:

```bash
kcp-harness integrate claude-code    # or: crush, openclaw, cursor, copilot, windsurf, cline, continue, pi
```

Without the harness, a model that decides to `Read` a governed file directly simply does. With it, that read is classified, run through the gates, and either served, refused, or held for a named human — and either way it's in the hash-chained log. The deterministic planner doesn't replace any of these agents; it replaces the *part of them* that should never have been probabilistic. The harness is what makes that replacement stick.

---

## The fifth entry: pi-kcp, the one that verifies its own execution

Every layering diagram is a hypothesis until someone runs the experiment. The honest test of "they compose, they don't compete" isn't wiring kcp-agent into Claude Code — that's the home team integrating with the incumbent. The test is: take a different coding-agent harness, one with its own extension model, its own event lifecycle, its own quirks — and see whether the same deterministic layer slots in.

![Enter pi-kcp: Verifying Execution Integrity — dual-digest matching between the Approved Input Digest (captured exactly at decision time) and the Executed Input Digest (captured at the execution moment), joined by a shared toolCallId key, resolving to PASS on a match or VIOLATED on divergence](/assets/images/blog/five-agents-compared/enter-pi-kcp.webp)
*pi-kcp is the only architecture that digests what a gate approved and verifies it against what actually ran, keyed to the same tool call.*

That's what pi-kcp is. One thing should be said plainly about its kind: it is not a standalone product. It's the KCP stack — kcp-agent for plans, kcp-memory for recall, kcp-harness's conformance checking — integrated into Pi, an independent coding-agent harness, as an extension. You wouldn't install pi-kcp instead of Claude Code or Crush; you'd encounter it because you chose Pi. An earlier version of this post kept it out of the tables for exactly that reason, and that was the wrong call — categorical difference isn't lesser standing. pi-kcp does something no other entry here does: it verifies its own execution against what was approved, and that earns table presence on its own merits. The mechanics: humans get `/kcp` commands (`plan`, `recall`, `validate`, `health`); the agent gets automatic bounded recall injected before prompts; plans are requested from kcp-agent as structured JSON and rejected otherwise. Its philosophy is the layering — which is a philosophy, not the absence of one.

What makes it more than a demo is the decision its maintainers recorded at the end of July: pi-kcp became a **governed runtime**, not a demonstrator. Every model call and tool call in the host now flows through a seven-stage cycle — plan, load, synthesize, ground, assess, approve, act/observe — mapped onto Pi's typed extension events. The plan stage runs `kcp-agent plan --trace --json` and adjudicates every declared skill against all 14 gates before it shapes any action ("deprecated since 2026-01-01" is evidence; "skill not allowed" is not). At the tool boundary, the active skill's declared `action_scope` is checked against each native tool call using the same deterministic conformance decision the harness proxy makes — and because Pi allows extensions to mutate a call between approval and execution, pi-kcp digests the input the gate approved and compares it to what actually ran. Concretely: each stage records a digest of what it actually saw, not a restatement of what was intended — `plan` digests the system prompt Pi assembled, `load` the context as assembled, `approve` the tool input at the moment the gate decided, keyed by Pi's `toolCallId`, and `act` the input as executed, under the same key. If the two digests disagree — or a call reaches `act` with no recorded approval at all — the stage is recorded as violated, and a violated turn is not a governed turn. That's a gate that was overridden, which is worse news than a gate that never fired, and the reason string ranks it accordingly.

There's an engineering honesty in the details worth noticing. Pi swallows handler exceptions — a crashing gate doesn't stop a turn, it produces a turn that completes ungoverned and silent. So pi-kcp's refusals are return values (`{ block: true, reason }`), never exceptions; it catches its own errors so it can record them; and an ungoverned turn is itself a detectable, assertable fact, with a configurable response — `onUngoverned: "announce"` (the default: report the lapse loudly, keep the host usable) or `"block"` (fail the turn). Silence is never evidence of governance. The stage ledger even declares which stages each mode promises to run, and that guard earned its keep during development: when the maintainers first flipped full governance on by default, a turn with no tool calls had no tool boundary to govern — so every ordinary Q&A turn announced itself as ungoverned. A warning that fires during normal operation trains people to ignore it; the fix was scoping the ungoverned claim to the stages the active mode actually claimed. That defect and its fix are written up in the project's decision record, which is itself the right kind of receipt.

The gap, same standard as everyone else: pi-kcp is v0.8.x and Pi is a niche harness next to the four standalone entries above. Scope conformance engages by default only when a governed skill is active — an unscoped, general action passes conformance (it's still subject to approval and the other gates, but "ungoverned" and "checked and fine" are different states, and pi-kcp is at least careful to record which one you're in). Full seven-stage governance (`governance: "full"`) costs one kcp-agent subprocess per turn — 57ms mean, measured over 52–64ms; noise against a model call, but not free — and is opt-in; the default (`governance: "tool"`) enforces only the tool boundary, on the argument that a non-conformant call blocked is the enforcement that matters. Strict mode (`requireActiveSkill: true`, default false) exists for those who want tool calls held unless a governed skill is active. And governance can be switched off in-session — loudly, as a recorded decision, but off is off.

None of that weakens either of the two things pi-kcp brings to this comparison. As a peer entry: it is the only one of the five that verifies its own execution against what was approved — fault line 6, where every other cell reads "no" or "closest". And as a demonstration: the claim in the original draft — Crush *could* consume the planner, OpenClaw *could* via its registry — was a conditional, and pi-kcp discharges it: a second, independent agent ecosystem adopted the deterministic knowledge layer, at runtime depth, without the layer changing to accommodate it. That's what a layer boundary looks like when it's real.

---

## The comparison nobody wants to make

![The Matrix (The Comparison Nobody Wants to Make) — four rows across all five agents: byte-for-byte reproducible (unlikely for the first three, yes for kcp-agent and pi-kcp), navigation cost (tokens vs. zero), bounded actions (hooks/prompts/sandbox vs. declared action_scope), and executed-call verification, where pi-kcp alone scores a plain "Yes"](/assets/images/blog/five-agents-compared/the-matrix-comparison.webp)
*The four rows that matter most, distilled — the full 15-row table follows.*

| Dimension | Claude Code | Crush | OpenClaw | kcp-agent (+harness) | pi-kcp (in Pi) |
|---|---|---|---|---|---|
| **Same task, same answer tomorrow?** | Unlikely | Unlikely | Unlikely | Yes, byte for byte | Governed layers: yes (Pi's model: no) |
| **Why was X loaded?** | Ask the model | Ask the model | Ask the model | Structured 14-gate trace | Same 14-gate trace, run inside Pi |
| **Why was Y *not* loaded?** | Nobody knows Y existed | Nobody knows Y existed | Nobody knows Y existed | Written skip reason | Written skip reason |
| **Navigation cost** | Tokens, every time | Tokens, every time | Tokens, every time | Zero — no model call | Zero tokens (57ms subprocess in full mode) |
| **Injection surface for navigation** | Full context window | Full context window | Full context window | None — model never touches navigation | None |
| **Second implementation agrees?** | N/A | N/A | N/A | Rust and Java ports pass the same conformance vectors | Consumes the conformant reference planner as-is |
| **Temporal governance** | None | None | None | valid_from/valid_until, supersession, drift detection | Inherited from the planner |
| **Payment/budget enforcement** | None | None | None | Deterministic budget arithmetic, itemized ledger | Via the planner's gates |
| **Bounded actions?** | Hooks (imperative) | Prompts | Sandbox | Declared action_scope, deny-final, refused attempts logged | action_scope conformance at Pi's tool boundary |
| **Executed call verified against approved call?** | No — a callback can rewrite input, nothing re-checks | No | No | Closest — the proxy executes what it governs, but no step boundaries | Yes — approve/act digests under the same call id; divergence = violated |
| **Compliance evidence export?** | No | No | No | SOC 2 / ISO 27001 / ISO 42001 / EU AI Act bundles from the audit log | Per-turn stage ledger; no evidence bundles |
| **Writes code?** | Yes | Yes | Yes | No | The host does |
| **Browses the web?** | Via MCP | Via MCP | Yes (built-in) | No | The host does |
| **20+ messaging channels?** | No | No | Yes | No | No |
| **Model flexibility?** | Claude only | 30+ providers | Multiple | Model-free core | Inherits Pi's |

*(So many of pi-kcp's cells read "inherited" or "the host does" because it is the right-hand column running inside a different host — a consumer of the layer, not a reimplementation of it. The one cell nobody else fills is the execution-integrity row.)*

The last four rows matter. kcp-agent doesn't do what the others do — and the others don't do what kcp-agent does. That's not a limitation; that's a layer boundary.

---

## What this means

![The Era of the Governed Runtime — three numbered points on a faded diamond/hexagon backdrop: model flexibility and terminal UX are solved problems; the next frontier is the layer of governance, trust, execution integrity, and auditability; you can use all these tools, and soon you will have to](/assets/images/blog/five-agents-compared/era-of-governed-runtime.webp)
*Model flexibility and terminal UX are solved problems. The next frontier is governance, trust, execution integrity, and auditability — and governance proxies are already making that layer non-optional.*

The agent industry is consolidating around a model-centric architecture: the LLM decides everything, guardrails constrain it, and we hope for the best. Claude Code, Crush, and OpenClaw all share this assumption, differing mainly in *which model*, *which interface*, and *which channels*.

The KCP stack makes a different bet, and over the past month the bet doubled. First: the most important decision an agent makes — *what knowledge to read* — should never be left to a model. That decision should be deterministic, inspectable, reproducible, and defensible in front of anyone who asks. Second, and newer: the same holds for *what an agent may do* — a skill's scope should be declared, granted, and deny-final, with refused attempts logged in a normative wire format, and the whole thing enforced at the tool-call boundary by a proxy the agent cannot talk around. kcp-agent is the decision; kcp-harness is the enforcement; the manifests are the ground truth.

The bet is not that the other three are wrong. They're very good at what they do. The bet is that they're missing a layer — and that layer is where the governance, the trust, the audit trail, and the reproducibility live. A month ago that was an argument with one integration snippet as evidence. Today a second agent ecosystem runs the layer at runtime depth, and the harness will wire it into nine hosts with one command.

You can use all of them. In fact, you probably should.

---

*Sources:*

- [Crush — charmbracelet/crush on GitHub](https://github.com/charmbracelet/crush)
- [fantasy — Charm's LLM library that owns Crush's loop](https://github.com/charmbracelet/fantasy)
- [mvdan/sh — the pure-Go POSIX shell interpreter behind Crush's Bash tool](https://github.com/mvdan/sh)
- [OpenCode — sst/opencode on GitHub](https://github.com/sst/opencode)
- [OpenClaw — openclaw/openclaw on GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Explained — KDnuggets](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)
- [Claude Code Hooks Explained — Blake Crosley](https://blakecrosley.com/blog/claude-code-hooks-explained)
- [Claude Code Skills Guide — Totalum](https://www.totalum.app/blog/claude-code-skills-totalum)
- [kcp-agent — Cantara/kcp-agent on GitHub](https://github.com/Cantara/kcp-agent)
- [kcp-harness — Cantara/kcp-harness on GitHub](https://github.com/Cantara/kcp-harness)
- [pi-kcp — Cantara/pi-kcp on GitHub](https://github.com/Cantara/pi-kcp)
- [Knowledge Context Protocol specification (v0.32) — Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)
- [The AI Agent That Keeps the Receipts — wiki.totto.org](https://wiki.totto.org/blog/2026/07/22/the-ai-agent-that-keeps-the-receipts/)
