---
description: "You already know what an AI agent is: a model in a loop that reads context, follows skills, forms an answer, calls tools, checks with a human, and leaves a trail. Here's the claim — we now know how to build a genuinely new kind of agent, one that can answer for every one of those parts by construction, and the architecture is roughly 85–90% built. A defendable agent is self-evidencing: every organ emits a written, checkable verdict at the moment it decides. This is the complete picture — the KCP planner, grounding, and confidence and approval gates that are live today, plus the procedural plane, the conformance gate, and the pi-kcp reference runtime that finish it — with an honest account of the last stretch."
date: 2026-07-22T09:00:00
draft: false
image: assets/images/defendable-01-cover.webp
categories:
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
tags:
  - defendable-agents
  - kcp
  - agentic-development
  - governance
  - eu-ai-act
  - audit
  - provenance
  - human-in-the-loop
authors:
  - totto
---

# Your AI Agent Just Did Something. Can You Prove It Was Okay?

*A new kind of agent — the defendable agent — is roughly 85–90% built. Here's the complete picture, one organ at a time.*

On Tuesday, an AI agent called **Nora** followed the risk-assessment playbook, drafted an assessment for a customer account, and downgraded their status. On Wednesday the customer complained. On Thursday your compliance officer walks over: *What did Nora read? Why those documents and not the newer policy from March? What playbook did she follow — the current one? How sure was she? Which human signed off, under which policy?*

<!-- more -->

![Tuesday's autonomous action becomes Thursday's unanswerable audit: a flowchart of Nora's Tuesday — system trigger, data analysis, probabilistic assessment, threshold check, downgrade action — beside Thursday's five unanswerable questions: what did Nora read, why those documents and not the newer policy, what playbook did she follow, how sure was she, which human signed off and under which policy.](../../assets/images/da-nora-timeline.webp)

For nearly every AI agent deployed in 2026, the honest answer to all five is *"we can grep the logs and guess."* Fine when Nora summarizes meeting notes; not fine when she touches customer accounts, money, or medical records — and with the EU AI Act's record-keeping and human-oversight duties phasing in through 2026–27, "grep and guess" is turning from *embarrassing* into *illegal* for a growing class of systems.

This post is about the fix, and the fix is not a policy binder bolted onto an ordinary agent. It's a **different kind of agent** — one that can answer every one of those questions *by construction* — and the surprising part is how close it is. I'll defend a specific claim: **the architecture of a defendable agent is roughly 85–90% built, mostly as running code**, with a clearly-named last stretch and the reference runtime that ties it together.

What makes it a new *species* rather than an old agent in a compliance vest is one property: it is **self-evidencing.** Every part of it emits a written, checkable verdict *at the moment it decides* — not a log you reconstruct afterward, but a defense produced as a side effect of simply operating. No agent you run today does that. And to see how it's possible, we don't need a new abstraction — just a careful look at the thing you already picture when you hear the word "agent."

Grab a coffee. This one's a proper explainer.

---

## The agent you already picture

Close your eyes and picture an agent working. You already have the model:

> An agent is **a model, running in a loop**. Each turn it **reads some context**, leans on what it **remembers**, follows the **skills** you gave it, **forms an answer** with some confidence, **calls tools** to act, occasionally **checks with a human**, and **leaves a trail**.

![The anatomy of the agent you already picture in your head: a ring of nine organs — context (what it reads), skills (the playbook it follows), answer (the synthesis it forms), tools (the actions it takes), loop (the runtime driving it), human (the nearby oversight), trail (the record it leaves), confidence (how sure it is), and memory (what it carries forward).](../../assets/images/da-anatomy-circle.webp)

Nora is exactly this. And the uncomfortable secret of that familiar picture is that, in an ordinary agent, *not one of those organs can be defended.* A defendable agent is the same animal with a governor on every organ — each one turning a question you currently can't answer into a written verdict you can. Here's the whole tour on one page; the rest of the post is this table, slowed down:

| The organ | Ordinary agent | Defendable agent |
|---|---|---|
| The **context** it reads | fetched whatever matched | planner: 13 gates, each with a reason |
| The **skills** it follows | an unsigned file someone dropped in | governed unit + conformance check |
| The **answer** it forms | asserts, unverified | grounding: cite-or-it-didn't-happen |
| Its **confidence** | a vibe, unrecorded | a gate against your threshold |
| The **tools** it calls | any action, no scope | conformance: did it stay in bounds? |
| The **human** | `approved: true` | named reviewer + policy, durable |
| The **memory** it keeps | ungoverned | declared, gated, forgettable |
| The **loop** that drives it | a black box | a runtime that emits every verdict |
| The **trail** it leaves | logs to grep | an audit spine that exports itself |

Let's walk it. For each organ: what the ordinary agent can't answer, and how the defendable one does — with a note, honestly, on whether that governor is *live today* or *the last stretch.*

---

## A tour of the organs

![Every organ fails the Thursday audit — not a single part is defendable today: the same ring of nine organs, each drawn cracked and broken, annotated with what goes wrong — the retrieval layer fetched what matched with no opinion on whether it should have; a doctored playbook dropped into the shared library; pure LLM synthesis that may not follow from what it read; oversight decayed to an approved:true boolean that vanishes on server restart; a trail you cannot prove to a skeptic without trusting the agent's own account.](../../assets/images/da-every-organ-fails.webp)

### The context it reads — *live*

The ordinary agent's first move is to pull in material, and it has no opinion on whether it *should* have. Was `pricing-internal-2024.md` superseded in March? Restricted to finance? Expired?

The defendable agent's knowledge *declares its own rules* in a small `knowledge.yaml` beside the content — audiences, validity windows, what supersedes what, even per-read cost:

```yaml
units:
  - id: risk-policy-2026
    path: policies/risk-assessment.md
    audience: [agent, support-staff]
    supersedes: risk-policy-2024
    triggers: [risk, assessment, downgrade]
```

A **planner** — pure code, no LLM, no randomness — walks every unit through **13 gates in order** (`audience → not_for → temporal → deprecated → supersession → relevance → attestation → payment → access → strict → max_units → money_budget → context_budget`), each passing or failing *with a written reason*: `skipped risk-policy-2024: superseded by risk-policy-2026`. Same task + same manifest + same date = *identical plan, every time* — rerun it in front of an auditor and get the same answer. This is the agent-native ontology that general policy engines lack: gates that understand supersession, budgets, audiences, and time. **What did she read, and why — answered.**

![Context governance: knowledge stops being an undifferentiated pile of files and starts declaring its own rules. A knowledge.yaml manifest feeds a pure-code planner that routes every unit through a 13-gate filter gauntlet — audience, temporal, supersession and the rest — emitting a written rejection reason: 'rejected, superseded by March policy'. Identical inputs yield identical, auditable plans every time.](../../assets/images/da-context-funnel.webp)

### The skills it follows — *the last stretch*

This is the organ almost everyone forgets, and naming it is half the contribution. Nora didn't invent the downgrade — she ran a **playbook**, a reusable skill that tells her *how* to do a whole class of task. Where did it come from? Is it current? Did someone drop a doctored one into the shared library last Tuesday?

Knowledge is *declarative* — you **cite** it. A skill is *imperative* — you **execute** it. A stale document yields one bad citation; a stale or **poisoned skill reshapes many actions at once.** So in a defendable agent a skill is a *governed unit too*: it declares itself like knowledge (audience, validity, supersession, signature), its **selection runs through the same 13 gates** — a stale or unsigned playbook skipped *with a written reason* — and its execution is checked by the conformance gate below. The mechanism is the one we already built, aimed one organ over. *(Design: the [procedural plane](https://github.com/Cantara/knowledge-context-protocol/issues/132), with [kcp-agent#100](https://github.com/Cantara/kcp-agent/issues/100) and [kcp-harness#38](https://github.com/Cantara/kcp-harness/issues/38).)* **Which playbook, and was it authorized — answered.**

![The ungoverned plane, drawn as a balance scale: on one side declarative knowledge (you cite it; grounding catches errors); on the other, heavier side, imperative skills (you execute it; nothing checks it). A bad document yields one bad citation, but a poisoned playbook reshapes all actions. The roadmap fix: treat procedures as governed units through the same 13 gates.](../../assets/images/da-skills-seesaw.webp)

### The answer it forms — *live*

The synthesis step is pure LLM; it can assert things its sources don't support. Checking it, though, is disciplined. **Grounding** asks a *separate* verifier which loaded document supports each claim, then **pure code adjudicates**: the cited unit must have been loaded, and its content hash must match. A verifier that hallucinates a citation proposes into a void. *Attribution is a proposal; grounding is adjudicated.* Unsupported claims aren't deleted — they're **surfaced as gaps.** **Does what she said follow from what she read — answered.**

### Its confidence — *live*

Nora might have read exactly the right documents and still reached a shaky conclusion. A separate, post-synthesis gate settles it: the model's self-report ("0.92") is one proposal, an independent skeptic evaluator is another, and deterministic code takes the *minimum* and compares it to *your org's* threshold. A cocky self-report can't outvote the skeptic; no signal at all fails closed; every raw number is preserved so the threshold can be calibrated against real outcomes. **How sure, and who set the bar — answered.**

![Bounding the answer: on the left, grounding hash-compares each LLM claim against the loaded documents and surfaces any unsupported claim as a gap — attribution is a proposal, grounding is adjudicated. On the right, the confidence gate feeds the model's self-report (92%) and an independent skeptic evaluator (40%) into minimum-vote logic, compares the result against the organization's hard threshold (70%) and fails closed — a cocky model cannot outvote the skeptic.](../../assets/images/da-grounding-confidence.webp)

### The tools it calls, and the human — *approval live, conformance the last stretch*

Two governors meet at the moment of action. When policy demands a human — or a gate says *hold* — a durable **ticket** opens with a real state machine (`pending_review → approved | dismissed | expired`), and three rules make it evidence instead of theater: a rule-matched call is held *no matter what* (the human outranks the automation); `approved: true` alone is rejected — a resolution *requires a named reviewer and a policy citation*; and tickets *outlive the session*, so a human can answer three days later and the agent honors it on retry.

```
$ kcp-harness approvals approve 2d62d5a2 --reviewer "Kari N." --policy-ref POL-7.2
```

And the action itself is checked against the playbook it claimed to follow — the **conformance gate**, *grounding for actions*: deterministic code adjudicates that Nora's actual tool-call sequence stayed inside the declared scope of an authorized, current skill; deviations surface as gaps. *"I followed the approved procedure" is a proposal; conformance adjudicates it.* **Who allowed it, and did it stay in scope — answered.**

![Tools, conformance, and the human outrank: an action proposal reaches a decision point that either opens a durable ticket — locked behind a named reviewer plus a specific policy citation — or runs the conformance gate, which adjudicates that the actual tool-call stayed inside the bounds of the authorized playbook. A rule-matched call is held no matter what; approved:true alone is rejected.](../../assets/images/da-tools-conformance.webp)

### The memory it keeps — *the last stretch (earliest)*

What may be *remembered* — retention, provenance, right-to-forget — is the same shape of problem: declare it, gate it, evidence it. It's the earliest-stage organ, [named and scoped](https://github.com/Cantara/kcp-harness/issues/36), slotting into the same machinery.

### The loop that drives it — *the last stretch (the capstone)*

Everything above is enforced by **kcp-harness**, an MCP proxy — one door into the building, fail-closed. But a proxy governs at the *boundary*: it sees tool calls, not which skill was selected or what the model concluded. To govern the whole animal you must reach *inside the loop.* So the deepest piece is a **host-neutral runtime-depth contract** — the events a loop must expose (`skill_selected`, `plan_formed`, `conclusion` + `confidence`, `action_trace`, `verdict_emitted`, under one correlation id) to be fully governable ([knowledge-context-protocol#133](https://github.com/Cantara/knowledge-context-protocol/issues/133)). *The bet is the contract, not the vendor* — any runtime can implement it; the proxy stays the portable fallback.

![Reaching inside the runtime loop: a cutaway showing two depths. Level 1, proxy depth (shallow), catches data at the boundary — it sees tool calls but not reasoning, and is portable. Level 2, runtime depth (deep), embeds sensors inside the loop's gears to see skill-selection, conclusions, and action traces. The durable artifact is a host-neutral contract, not a single product; the reference implementation is a KCP wrapper around Pi.dev with the TerteForm sandbox.](../../assets/images/da-runtime-loop.webp)

**pi-kcp** — a Cantara project — is the reference implementation: a KCP runtime riding the [Pi.dev](https://pi.dev) agent loop (sandboxed by [TerteForm](https://github.com/Cantara/TerteForm)), where the planner, the gates, the memory, the skills, and the evidence spine finally compose into *one governed loop* instead of a toolbox you wire by hand. It is what turns "a set of governance libraries" into "a defendable agent." Offered as **one reference bet, not the only one** — Claude Code or a bespoke loop could implement the same contract. **Can anyone see inside the loop — yes, by design.**

### The trail it leaves — *live*

Underneath all of it, an append-only log where every stage lands as a structured event, mapped by an exporter onto compliance frameworks (SOC 2 and ISO 27001 today; [ISO 42001 and EU AI Act article-mapping](https://github.com/Cantara/kcp-harness/issues/37) next) and stitched toward [one evidence spine per action](https://github.com/Cantara/kcp-harness/issues/34). This is the payoff of the whole philosophy: **compliance artifacts as a side effect of normal operation.** Nobody writes the audit report — *operating* the agent writes it. **Can you prove all of it, later — answered.**

![Compliance artifacts emerge as a side-effect of normal operation: the agent's calls pass through the fail-closed kcp-harness proxy wall — a single entry point — into an append-only log; a KCP mapper turns the structured verdict events into SOC 2, ISO 27001, and EU AI Act compliance artifacts. Nobody writes the audit report; operating the agent is writing it.](../../assets/images/da-evidence-spine.webp)

One discipline runs through every organ — call them the four laws: *the model proposes, deterministic code adjudicates; fail closed; every verdict is binary with a written reason; evidence is generated at decision time, never reconstructed later.*

![The KCP philosophy: use probabilistic judgment where you must, use deterministic code everywhere you can. On the left the model proposes — subjective, probabilistic, black-box. On the right code adjudicates — deterministic, binary, fail-closed. The golden rule: every deterministic decision must write down its reason at the moment it decides; evidence is generated at decision time, never reconstructed later.](../../assets/images/da-kcp-bet.webp)

---

## State of the build — where the last 10–15% is

A picture this clean invites the fair question: *how much of it actually runs?* Transparently — because a completeness claim you can't check is just a claim:

**Live today, battle-tested across real client codebases:** the entire defendable-*decision* spine — the 13-gate planner (context), grounding (answer), the confidence gate (conclusion), durable approval tickets (the human), and the append-only audit log with SOC 2 / ISO 27001 export (the trail), all enforced through the fail-closed kcp-harness proxy. That's the majority of the animal, and it's not a demo: `npm i -g kcp-harness` and watch `audit.jsonl` fill.

**The last stretch — designed, filed as problem-statements-before-schemas, being built:** the **procedural plane** (skills as governed units) and its **conformance gate** — the one genuinely new gate; **runtime depth** — the host-neutral contract and **pi-kcp** as the runtime that composes everything into one loop; and **memory**, the earliest-stage organ.

Weight it by the spine and I'd honestly put us at **85–90% of a genuinely new kind of agent.** The core — govern the decision, evidence every step — is done and running. What remains extends the *same* discipline to two more organs and deepens it into the loop; none of it needs a new philosophy.

![The mended anatomy — one chain of evidence per action: the ring of organs with the shipped ones (context, answer, confidence, human, trail) drawn as solid boxes and the roadmap ones (skills, loop, memory) drawn dotted. Every governed organ leaves a written verdict, and the verdicts link into a single, cryptographically auditable evidence spine. Governance bounds decisions; it doesn't make the agent smarter — garbage in, well-cited garbage out.](../../assets/images/da-state-of-build.webp)

And the caveats that don't move with implementation status: it **doesn't make Nora smarter** (a well-governed mediocre conclusion is just *defensibly* mediocre); it **doesn't verify your knowledge is true** (a signed, current, *wrong* policy gets followed defensibly off a cliff); reviewer identity is asserted, not yet cryptographically proven ([#35](https://github.com/Cantara/kcp-harness/issues/35)); thresholds start as guesses with good bookkeeping ([kcp-dashboard#31](https://github.com/Cantara/kcp-dashboard/issues/31)); and it's per-agent while the world goes to fleets ([#36](https://github.com/Cantara/kcp-harness/issues/36)).

---

## Why this, and why now

You still want the ordinary toolbox — for the organs it guards. Observability is the flight recorder (records everything, judges nothing). Guardrails are the bouncer (catches PII and jailbreaks, blind to whether a *decision* was allowed). Sandboxes are the walls (coarse, no reasons, no evidence). Policy engines are a rulebook with no agent semantics. Evals are the bar exam (tells you the agent *tends* to behave, not what it did today). Human-in-the-loop degrades into cookie-consent theater. Every one guards a real organ; **none of them knows your policy, explains every decision, and produces evidence a skeptic can check** — and none has any opinion on the skills the agent runs. A defendable agent fills exactly that empty column. It doesn't replace the others; it's the organ they all leave undefended.

![The current enterprise security stack guards one organ at a time, leaving the anatomy exposed: a scorecard grid scoring observability, guardrails, permissions/sandbox, policy engines, evals and human-in-the-loop across four columns — stops bad things, knows your policy, explains itself, evidence for later. Every row fails at least one column, and a whole organ, the skills the agent follows, appears in nobody's remit at all.](../../assets/images/da-scorecard.webp)

And the timing isn't an accident. Agents got *hands* (the blast radius went from "awkward paragraph" to "production incident"), got *autonomy* (fleets running overnight, no human watching each step), and the *law caught up* (EU AI Act Articles 12 and 14 — real records, real oversight). "Trust us" stopped closing enterprise deals. Self-evidencing agents are the answer that survives an audit.

![Grep the logs and guess is transitioning from embarrassing to illegal: three overlapping circles meeting at 'the blast radius' — agents got hands (from copy-pasting text to filing tickets, calling APIs and moving money), agents got autonomy (long-running fleets working overnight; the implicit safety mechanism of human observation is gone), and the law caught up (EU AI Act and ISO/IEC 42001 mean 'trust us' no longer closes enterprise deals).](../../assets/images/da-why-now.webp)

### This isn't theoretical — it runs in a rig

The discipline has two surfaces. At **runtime**, KCP governs a deployed agent like Nora. At **development time**, the same four laws govern the agents that *build the software* — I run a rig I call **ExoCortex** across real client codebases: cross-model adversarial review, a verify-gate, end-to-end tests as the behavior truth, provenance on everything read. (More in ["Evidence isn't enough: the independence problem in agentic development"](/blog/2026/07/21/evidence-isnt-enough-the-independence-problem-in-agentic-development/).) And the skills organ? I hit it the hard way: ExoCortex already runs 561 skills as a **read-only mirror of `origin/dev` — never edited in place, synced only through a reviewed PR.** A governed skill corpus with provenance and versioning, *built by hand because the tooling didn't offer it yet.* Living proof the last stretch is real, and buildable.

---

## Come build the last 10%

Everything on the spine is running code, Apache-2.0:

- **Play in the browser** (no install): the [live governance dashboard demo](https://cantara.github.io/kcp-harness/demo-live-dashboard.html) — press **👤 Human-approval hold** and watch a ticket get requested, resolved by a named reviewer, and honored. Or the [agent thought-graph](https://cantara.github.io/kcp-dashboard/).
- **Run the narrated demos**: `git clone` [kcp-agent](https://github.com/Cantara/kcp-agent), then `node examples/demos.js` — nineteen scenarios driving the real planner, nothing mocked, including `second-opinion` (the confidence gate).
- **Govern an actual agent**: `npm i -g kcp-harness`, `kcp-harness init`, `kcp-harness integrate claude-code` (or cursor, copilot, windsurf, cline, continue, crush, openclaw, pi).
- **Argue with the last stretch**: the organs still being built are open problem statements, filed before any schema — the [procedural plane](https://github.com/Cantara/knowledge-context-protocol/issues/132), its [conformance gate](https://github.com/Cantara/kcp-harness/issues/39), and the [runtime-depth contract](https://github.com/Cantara/knowledge-context-protocol/issues/133). If a skill isn't the right atomic unit, or determinism is the wrong hill — come say so.

The intern is already hired. She started months ago; she's reading your documents, running your playbooks, and taking real actions today. The only open question is whether, on Thursday, your answer is a shrug — or a chain of written verdicts, one per organ, ending in a named human, a policy citation, and the current, authorized playbook she followed to get there.

You already knew what an agent was. Now you know what a *defendable* one is — and that it's most of the way here.

**Capability is abundant. Defensibility is scarce.**

![A gold KCP defendable ticket for one action — audit verdict: approved; authorized playbook named; a human owner; a timestamp; chain of evidence: verified; status: executed — the complete self-evidencing record of a single decision. The intern is already hired and taking real actions today; when the auditor walks over, your answer is either a shrug or a chain of written verdicts ending in a named human and an authorized playbook. Capability is abundant; defensibility is scarce.](../../assets/images/da-closing.webp)

---

*The KCP family: [knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol) (the spec) · [kcp-agent](https://github.com/Cantara/kcp-agent) (deterministic planner + reference agent) · [kcp-harness](https://github.com/Cantara/kcp-harness) (MCP compliance proxy) · [kcp-dashboard](https://github.com/Cantara/kcp-dashboard) (live visibility) — Apache-2.0, by [eXOReaction](https://www.exoreaction.com) under [Cantara](https://github.com/Cantara). The **pi-kcp** reference runtime is a separate [Cantara](https://github.com/Cantara) project.*
