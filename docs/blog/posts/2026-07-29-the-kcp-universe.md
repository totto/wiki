---
description: "The complete map of the Knowledge Context Protocol universe — twelve repositories, 1,012 commits and 88 releases in July alone. What each piece does, what landed this month, what it enables, and exactly where to start. Written for people arriving for the first time and for people who have been here since February."
date: 2026-07-29T18:00:00
draft: false
series: "Knowledge Context Protocol"
categories:
  - Knowledge Context Protocol
  - AI Agents & the Agentic Web
  - Governance, Trust & Compliance
  - Knowledge Infrastructure
tags:
  - kcp
  - kcp-agent
  - kcp-harness
  - pi-kcp
  - sunstone-atlas
  - governance
  - playbooks
  - getting-started
authors:
  - totto
  - claude
---

# The KCP Universe: Everything, and What July Changed

In July 2026, twelve repositories in the Knowledge Context Protocol ecosystem took **1,012 commits** and shipped **88 releases**. The specification went from v0.22 to v0.30.3 — sixteen releases in a single month.

That is either a lot of noise or a lot of signal, and the only honest way to tell you which is to show you the whole thing.

This is the complete map. If you have never heard of KCP, start at the top and it will make sense. If you have been following since February, skip to [July in focus](#july-in-focus) — that is where everything new is.

<!-- more -->

![The KCP Universe — 12 repositories, 1,012 commits, and the shift from relevance to authority](/assets/images/kcp-universe/title-kcp-universe.webp)

---

## The problem, stated once

![Relevance is not authority — RAG guesses, KCP proves](/assets/images/kcp-universe/relevance-is-not-authority.webp)

An AI agent reading your codebase has no idea what is true.

It finds a design document from March and a design document from June, and nothing in either tells it which one is current. It finds a runbook that was superseded in April, and follows it. It finds an internal API guide that was written for a version that no longer exists. It reads all of them with exactly equal confidence, because a file is a file.

Retrieval-augmented generation does not fix this. RAG finds *relevant* text. It has no concept of *authoritative* text. Relevance and authority are different questions, and only one of them has an answer that can be checked.

**KCP is the other answer.** It is a small, boring YAML file — `knowledge.yaml` — that sits in your repository and says, for each unit of knowledge: what it is for, who it is for, when it stops being true, what supersedes it, what it is allowed to touch, and a content hash proving it has not changed since someone stood behind it.

An agent that reads a KCP manifest does not have to guess. It can ask, and get an answer with a reason attached.

That is the whole idea. Everything below is what it took to make it real.

---

## The map

Twelve repositories. Here is what each one is, in the order you would meet them.

![Ecosystem topology — the spec at the centre, enforcement points in the inner orbit, tooling and organisational scale further out](/assets/images/kcp-universe/ecosystem-topology-12-repositories.webp)

| Repository | What it is | July |
|---|---|---|
| **knowledge-context-protocol** | The specification, JSON schemas, and conformance vectors. The thing everything else implements. | 163 commits · 16 releases |
| **kcp-agent** | The reference deterministic planner. Given a task and a manifest, decides which units to load — and shows its reasoning through 14 gates. | 183 commits · 27 releases |
| **kcp-harness** | Governance enforcement at proxy depth. Sits in front of an agent's MCP tools and adjudicates every call against declared authority. | 113 commits · 17 releases |
| **pi-kcp** | Governance enforcement at *runtime* depth — inside the agent's own turn, where it actually acts. | 81 commits · 8 releases |
| **kcp-memory** | Cross-session episodic memory. What you and the agent did last Tuesday, retrievable today. | 44 commits · 3 releases |
| **kcp-commands** | The first thing to install. Token-efficient command wrappers — immediate savings, no protocol knowledge needed. | 47 commits · 2 releases |
| **kcp-skill** | Skills as portable, governed artifacts rather than editor-specific files. | 38 commits · 4 releases |
| **kcp-dashboard** | See what is happening. Manifest health, load decisions, drift. | 64 commits · 1 release |
| **kcp-triage** | Knowledge for external APIs you do not control — turn someone else's docs into a governed manifest. | 48 commits · 2 releases |
| **kcp-playground** | A place to try things without consequences. | 7 commits |
| **Synthesis** | Workspace intelligence. Indexes an entire codebase and answers questions across it. | 193 commits · 8 releases |
| **Sunstone Atlas** | The newest, and the most ambitious: a governed substrate for an entire organisation. Design phase. | 31 commits · born 23 July |

If that table looks like a lot, here is the compression: **a spec, three enforcement points, and a set of tools that make the spec pleasant to live with.**

### What a manifest actually looks like

![The atomic unit of trust — each knowledge.yaml field answers a question an agent would otherwise guess at](/assets/images/kcp-universe/atomic-unit-of-trust-knowledge-yaml.webp)

Before going further, the concrete thing. This is a real unit from `kcp-agent`'s own manifest — the one fully-formed governed procedure in the ecosystem today:

```yaml
  - id: navigator-skill
    path: skills/kcp-navigator/SKILL.md
    kind: skill
    intent: "Portable skill packaging the plan-first, fail-closed KCP
             navigation discipline for agents that drive the CLI themselves"
    scope: project
    audience: [agent]
    triggers: [skill, navigator, discipline, plan first]
    load_eligible: true
    action_scope:
      tools: ["shell.exec"]
      capabilities: ["kcp.navigate"]
```

Read it as a series of answers to questions an agent would otherwise guess at:

- `intent` — *what is this for?* Not a summary of the text; a statement of purpose the planner matches tasks against.
- `audience: [agent]` — *is this for me?* A human-facing onboarding doc and an agent-facing runbook are different artifacts, and pretending otherwise is how agents end up reading marketing copy.
- `kind: skill` — *is this knowledge, or is it a procedure?* This one line is what makes the unit governable as an action rather than a fact.
- `load_eligible: true` — *may this be loaded at all?* Eligibility is separate from relevance. A unit can be perfectly relevant and still not permitted.
- `action_scope` — *what may it touch?* The declared authority. When this skill is active, a tool call outside `shell.exec` is refused, in-loop, with the reason.

Knowledge units are simpler — most have no `kind` and no `action_scope`, because a document does not act. Add `valid_until` and a unit expires on its own. Add `supersedes` and the old one steps aside without anyone having to remember to delete it.

That is the whole surface area. It is deliberately small enough to write by hand.

---

## The tools, in a bit more depth

**`kcp-commands`** is the entry drug and the only piece with an instant payoff. It wraps frequently-used shell commands with token-efficient filtering — a measured 33% of context window saved per session, because 84% of an agent's Bash calls are well-known tools whose output can be compressed without loss. It runs as a hook in about 12ms. You do not need to know what KCP is to benefit.

**`kcp-agent`** is where the protocol becomes a decision. Give it a task and a manifest and it produces a plan: which units to load, which to skip, and *why* for each — adjudicated through fourteen gates (audience, not_for, temporal, deprecated, supersession, relevance, skill eligibility, attestation, payment, access, strict, max units, money budget, context budget). Ask for `--trace --json` and you get every gate's verdict with a written reason. It runs in about 57 milliseconds against a real manifest, which is the number that makes per-turn governance affordable at all.

**`kcp-harness`** enforces at **proxy depth**. It sits in front of an agent's MCP tools and adjudicates every call against the active skill's declared authority using a deterministic decision function — plus grounding (does this claim cite a loaded, hash-pinned unit?), confidence assessment, spend envelopes for pay-per-request sources, and signed receipts.

**`pi-kcp`** enforces at **runtime depth**, inside the agent's own turn. See below — it is the piece that changed most this month.

**`kcp-memory`** gives agents episodic recall across sessions with provenance, so "what did we decide about the migration last Tuesday" has an answer that includes where the answer came from. Memories carry temporal validity: an expired one is skipped, not silently served.

**`kcp-dashboard`** shows manifest health, load decisions and drift, because a governance system you cannot observe is a governance system you are trusting rather than checking.

**`kcp-triage`** solves the problem of knowledge you do not own. You cannot add a `knowledge.yaml` to someone else's API docs — triage turns external documentation into a governed manifest you can.

**`kcp-skill`** treats skills as portable governed artifacts rather than files that only mean something inside one editor.

**`Synthesis`** is the outlier: not KCP itself, but workspace intelligence. It indexes an entire codebase — thousands of files — and answers structural questions across it. It is how you find out what you already have.

---

## July in focus

The month, compressed:

| Date | What |
|---|---|
| 4 Jul | v0.22 → v0.25.1 — the trust model completes; five spec releases in a day |
| 5 Jul | `kcp-agent` — the reference planner ships |
| 6 Jul | the MCP bridge — KCP reaches tools it does not own |
| 14 Jul | v0.26 — manifest signature refresh |
| 23 Jul | **Sunstone Atlas** begins: knowledge / skill / playbook as the three artifact classes |
| 27 Jul | v0.28 **Implementation Parity** · v0.29 **`kind: playbook`** (RFC-0027) |
| 28 Jul | v0.30 **eligibility grants** (RFC-0028) + `grant_request_events` |
| 29 Jul | v0.30.3 · **pi-kcp 0.5.0** — the governed runtime, on by default |

![The July momentum — implementation parity, the procedural plane, eligibility grants, parse diagnostics](/assets/images/kcp-universe/july-momentum-four-shifts.webp)

Four things in that list changed what the protocol can do that changed what the protocol can do. They are related, and they arrived in an order that turns out to be the argument.

### 1. Implementation Parity (v0.28, 27 July)

KCP is implemented more than once on purpose. The spec repository carries three bridges — **TypeScript, Java, and Python** — and the reference planner adds a **Rust** port alongside its TypeScript and Java ones. For most of its life, "the spec says X" and "the implementations do X" were separate claims, and the second was taken on trust.

v0.28 closed that. Conformance vectors are shared across implementations, so a behavioural difference between the Java parser and the Python one is a **test failure**, not a discovery someone makes in production six weeks later.

The work to get there is worth quoting, because it was not flattering: one of the commits in that release is titled *"record the real bridge state — three spec versions of drift."* Parity was not achieved by declaring it. It was achieved by measuring the gap first and writing the number down.

This is unglamorous and it is the most important thing in the list. A protocol with three implementations that disagree is not a protocol; it is three programs with a shared vocabulary.

### 2. The procedural plane — `kind: playbook` (v0.29, 27 July, RFC-0027)

Until July, KCP governed **knowledge**: facts, documents, things that are true. A unit could say "I am about deployment, I am for agents, I expire in August."

v0.29 added the other half. Knowledge units describe *what is true*. **Skills** describe *how to do one thing*. **Playbooks** describe *how to accomplish a goal* — a composed, gated sequence of skills with checkpoints.

The difference that matters: a playbook run emits a **signed decision chain**. Not "an agent did some things and here is a log," but "here is cryptographic evidence that this procedure ran, in this order, with each step checked against what it was authorised to do."

For anyone who has sat through a compliance audit, that sentence is the entire product.

### 3. Eligibility grants (v0.30, 28 July, RFC-0028)

Governance that can only say *no* is a brake. The interesting question is how something gets to say *yes* — safely, revocably, with a record.

v0.30 introduced grants: a unit can be made eligible under specific conditions, that eligibility composes, and — via `grant_request_events` — the *asking* is itself part of the audit trail. You can see not just what was permitted, but what was requested and refused.

### 4. Parse diagnostics — a typo is no longer silent

![The invisible bug — before July a misspelled field parsed cleanly and left the unit ungoverned forever](/assets/images/kcp-universe/invisible-bug-silent-failures.webp)

My favourite, because it is so small and so telling.

Before July, a misspelled field in a manifest was simply ignored. You wrote `audiance:` instead of `audience:`, and the manifest parsed cleanly, and your unit was quietly ungoverned forever. Nothing failed. Nothing warned. It just did not work, invisibly.

Now it tells you.

There is a theme running through this entire project, and that is it: **the difference between something that is fine and something that has not been checked is invisible unless you build the machinery to see it.** Almost every hard bug in this ecosystem has been a version of that sentence.

---

## The runtime: pi-kcp 0.5.0

![Proxy depth versus runtime depth — the same adjudicator, two places it can act](/assets/images/kcp-universe/enforcement-proxy-vs-runtime-depth.webp)

Shipped today, and it deserves its own section because it is where the protocol stops being a description and starts being a thing that intervenes.

`kcp-harness` governs at **proxy depth** — in front of an agent's MCP tools. That is airtight for everything the agent reaches *through the proxy*. But a coding agent also reads files, runs shell commands, and fetches URLs through its own harness's native tools, which never touch the proxy at all.

`pi-kcp` closes that gap by living inside the agent's turn. In 0.5.0 it runs the full governed cycle — plan, load, synthesize, ground, assess, approve, act — as one sequence across eight of the host's lifecycle events, recording a decision for every stage against one correlation id.

Three things it does that I think are genuinely new.

**It cannot fail silently.** The host swallows exceptions thrown by extensions — every dispatch site wraps handlers in `try`/`catch` and carries on. So a governance gate that *crashes* does not stop anything; it produces a turn that completes ungoverned and looks completely normal. pi-kcp therefore never signals refusal by throwing. Refusal is a returned value. The gate catches its own errors in order to *record* them. And a stage that never reported is a recorded fact, announced in the session:

```text
## KCP — turn 4 completed ungoverned

stage never reached the ledger: load, synthesize, ground

Actions this turn were not covered by the governance guarantee.
```

**It records what ran, not what was approved.** The host hands the pre-call and post-call hooks the *same arguments object*, and explicitly invites extensions to modify a call by mutating it in place. So a call can change *after* the gate approved it. pi-kcp digests the input the gate decided on, digests what actually executed, and compares:

```text
turn 4 — UNGOVERNED: approval was not honoured at: act
  approve     ok        tool=bash toolCallId=call_a1 inputDigest=1df8bcca…
  act         violated  toolCallId=call_a1 approvedDigest=1df8bcca… executedDigest=2911155a…
```

An audit trail that records the decision and stops there is a record of *intent*. This one records what happened.

**It comes in three strengths.**

![The governed runtime — seven stages, the approved-versus-executed delta, and three modes](/assets/images/kcp-universe/governed-runtime-pi-kcp-050.webp)

| Mode | What runs | Cost |
|---|---|---|
| `full` | all seven stages, including a per-turn planner trace that gates which skills may load | one planner call per turn (~57ms, measured) |
| **`tool`** (default) | conformance at the tool boundary, integrity on the result | **zero subprocesses** |
| `off` | no cycle, no records | — |

`tool` is the default because it is the enforcement that matters — a non-conformant call blocked, a mutated call caught — with no new dependency and no per-turn cost.

A detail I want to keep, because it nearly went wrong: turning the cycle on by default initially made **every ordinary question-and-answer turn announce itself as ungoverned**. A turn that answers a question without using a tool never reaches the approve or act stages, and the accounting counted them missing. A warning that fires during normal operation is not a warning — it teaches people to ignore the real one. Those stages are conditional now, closed out with a reason. The alarm is reserved for turns where the cycle genuinely did not run.

---

## What this enables: Sunstone Atlas

![The artifact trinity — knowledge, skill, playbook as the three governed classes](/assets/images/kcp-universe/artifact-trinity-sunstone.webp)

The clearest answer to "so what?" was born on 23 July, six days before this post.

**Sunstone Atlas** is a governed substrate for an entire organisation — and it is built on exactly the three artifact classes the protocol grew this month:

| Class | Is | Governance gives |
|---|---|---|
| **Knowledge** | facts — *what is true* | provenance, confidence, freshness, conformance |
| **Skill** | a capability — *how to do one thing* | `action_scope`, signed, versioned |
| **Playbook** | a procedure — *how to accomplish a goal* | who may run it, per-step conformance, a signed receipt of the **whole run** |

That is not a coincidence, and it is the reason to pay attention to July specifically. The spec grew `kind: playbook` on 27 July. Sunstone was designed on the assumption that Knowledge / Skill / Playbook are the three things an organisation has. **The protocol and the first system built on it converged in the same month**, from opposite directions.

![The autonomy dividend — a chokepoint caps autonomy, a signed substrate compounds it](/assets/images/kcp-universe/autonomy-dividend.webp)

Sunstone's design document contains the best one-line statement of what this whole universe is for:

> A **chokepoint gateway** inspects traffic and blocks — it sees calls, not meaning, and it caps autonomy: every action is suspect, gated at the choke. Sunstone binds each decision to an approved, versioned knowledge substrate, conformance-checks it, and signs it. Because the action is defendable *by construction*, the agent can safely be granted **more** autonomy.
>
> **The gateway says *no*. Sunstone says *yes, provably*.**

That inversion is the thesis. Governance is usually sold as the brake. Here it is the thing that lets you take your foot off it — because an agent whose actions come with signed evidence that they stayed in bounds can be trusted with more, not less. The design calls this the **autonomy dividend**, and it earns higher autonomy tiers against a track record of grounded, conformant, signed decisions.

---

## Fifteen things you can run

![Executable scenarios — out of bounds, cite or it didn't happen, the auditor's Thursday, the runaway spender](/assets/images/kcp-universe/prove-it-executable-scenarios.webp)

Abstractions about governance are cheap. The pi-kcp repository ships **fifteen executable demos**, each one a scenario that either works or does not, and most of them need nothing installed beyond the repo itself.

They are the fastest way to understand what any of this means. A selection:

**The Superseded Policy.** A retired policy sits in the manifest next to its replacement. The planner's supersession gate skips it *and writes down why*. Run it twice and the output is byte-identical — determinism is the point, because a governance decision you cannot reproduce is not evidence.

**Out of Bounds.** The flagship. A skill declares `action_scope`. An in-scope call passes; an out-of-scope call is blocked with the harness's own written reason, and the deviation is surfaced as a gap rather than swallowed.

**The Auditor's Thursday.** One `correlationId` threads a whole task, reconstructs as a full decision chain, and exports as **SOC 2 / ISO 27001 / ISO 42001 / EU AI Act** evidence bundles. This is the demo to show a compliance officer.

**Cite or it didn't happen.** A claim grounds to a loaded, SHA-pinned unit. An unsupported claim becomes a visible gap. A claim citing a unit that was never loaded fails closed. Hallucination becomes a *detectable event* rather than a vibe.

**The Confident Fool.** An agent reports 0.92 confidence in itself. An independent skeptic reports 0.35. They are min-aggregated against a 0.70 threshold, and the work is **held**. The no-signal case also fails closed — silence is not confidence.

**Two Depths, One Verdict.** The same `checkConformance` adjudicator runs at proxy depth (`kcp-harness serve`) and at runtime depth (pi-kcp), on the same action — and returns an *identical* verdict and reason. That is the entire argument for having two enforcement points instead of two competing policies.

**The Research Assistant.** Governance as **enabler**, and my favourite for arguing with sceptics: a bounded read-only agent runs autonomously through the proxy, performs many in-scope reads and searches, is blocked **zero** times, and produces a grounded, cited summary with one clean audit chain. The guarantee is what let it run unattended.

**The Runaway Spender, Contained.** A purchase over `max_spend` and a purchase to a disallowed vendor are both held in-loop, each opens a real approval ticket, and **the wallet is never authorised**. Money is the case where "we noticed afterwards" is worthless.

**The Governed Composition.** The newest: a `kind: playbook` promotion spanning `observe → prepare → commit`. An ungranted playbook fails closed exactly as an ungranted skill does, a superseded one is dropped, and **no step exceeds the playbook's ceiling** — a step cannot quietly out-scope the procedure that contains it.

Sunstone Atlas has its own set — ten browser-based demos including a board-buyer walkthrough, a CISO governance view, an enforceability argument, and an orchestration simulation of a governed agent team.

---

## An honest accounting

![The adoption gap — skill files to one declared procedure, zero playbooks, and one repo five versions behind](/assets/images/kcp-universe/honest-accounting-adoption-gap.webp)

!!! warning "Correction, 30 July 2026 — the 65 was wrong, and the anatomy of the miscount is the point"
    This section originally claimed **65 skill files**. The real number is **24**. The 65 came
    from a naive `find` that counted 26 duplicates inside stale `.claude/worktrees/` copies and
    12 files in `examples/governed-skills/` — several of which are *deliberately* non-conformant
    negative test fixtures (`poisoned-playbook`, `ungranted-skill`). Counting a negative test
    fixture as a governance gap inverts its meaning. The slide above still shows the wrong
    figure; the sentence below is corrected. On a post about measurement, the miscount and its
    cause stay visible rather than quietly rewritten.

    The ratio the section actually argued from — many skill files, **one** governed — was right,
    and naming it publicly had a consequence: within 48 hours, **all 24 real skills across six
    repositories were declared as governed procedures**, each verified against the planner. What
    an honest map triggers is a story for the next post.

I would rather you got this from me than found it yourself.

Across the nine core repositories there are **24 real `SKILL.md` files** *(originally misstated as 65 — see the correction above)*. At publication, exactly **one** of them was declared in a manifest as a governed procedure, with `kind: skill`, `load_eligible`, and a declared `action_scope`: `kcp-agent`'s own `navigator-skill`.

Ask the planner about any of the others and it said, accurately: *"not a governed procedure."*

**Zero playbooks are declared in any repository's own manifest.** The spec shipped `kind: playbook` two days ago, and it is exercised — demo 15 runs a real governed composition end to end — but no repo yet governs its own procedures with one.

And `Synthesis` — the largest repository in the ecosystem by July commit count — is still on `kcp_version: 0.25` while everything else is on 0.30.

So the protocol is currently ahead of its own adoption, in its own house. That is not a scandal — v0.29 is two days old, and the correct order is *spec, then implementations, then adoption*. But it is the real state, and a map that only shows the finished parts is a brochure.

August is for closing that gap. If you want to watch something concrete, watch the number of declared playbooks go from zero.

---

## Where to start

![Where to start — four routes in, by how much time you have](/assets/images/kcp-universe/where-to-start.webp)

**If you want a result in ten minutes**, install `kcp-commands`. It wraps common commands to be far more token-efficient — a measured **33% of the context window saved per session** — and requires you to understand nothing about the protocol. It is the only entry point with an immediate, measurable payoff.

**If you want to understand the idea**, write a `knowledge.yaml` for one repository you know well. Six units. Give each an `intent`, an `audience`, and where relevant a `valid_until`. Then run `kcp-agent plan "some task" --manifest knowledge.yaml --trace --json` and read the gate verdicts. Watching a planner explain in fourteen gates why it did or did not load your document is the moment the concept lands.

**If you want the governance story**, read the pi-kcp user guide and turn the cycle on in `tool` mode. It costs nothing and it will block the first genuinely out-of-bounds thing your agent tries.

**If you are evaluating this for an organisation**, the relevant artifacts are `kcp-harness` for proxy-depth enforcement, pi-kcp for runtime depth, and the Sunstone Atlas design document for where it goes at organisational scale.

**If you want to argue with me about it**, that is what AgentPilsen is for. We restart after the summer break this Thursday, and I would genuinely rather be told this is over-engineered by someone who has run demo 3 than agreed with by someone who has not.

The objection I most want to hear is the one Sunstone's own design document records as the strongest from the field: *that chokepoint governance at the tool call is good enough, and a signed substrate is over-engineering.* I think the answer is the autonomy dividend — but I would like to lose that argument properly if I am going to lose it.

---

## What July actually was

A thousand commits is not a plan. It is what happens when a small set of ideas turn out to be load-bearing and you keep pulling on them.

The ideas, as far as I can tell after a month of this:

1. **Relevance is not authority.** Retrieval solved the first and pretended it had solved the second.
2. **A claim nobody checked is indistinguishable from a claim that is true.** Every serious bug this month was a version of that.
3. **Governance that can only refuse is a brake. Governance that can prove is an enabler.**

The third one took the longest to see, and it is the one I would defend hardest. It is why the protocol grew playbooks and grants in the same month, and why the first platform built on it treats a signed decision chain as a product rather than a compliance chore.

Everything is open source except Sunstone Atlas. Break it and tell me what broke — the most useful contributions this month were not features, they were people demonstrating that something I believed was true was not.

If you read one thing beyond this post, make it demo 10: the same adjudicator, at two depths, returning the same verdict. Everything else is an elaboration of that.

---

*Written with Claude Code, which also wrote most of pi-kcp 0.5.0 and found the bug where every ordinary turn would have announced itself as ungoverned. The commit and release counts in this post were measured on 29 July 2026 with `git rev-list --count` across the twelve repositories, not estimated.*

*The diagrams were generated by NotebookLM from this post and then checked against it — which is the same discipline the post argues for, applied to itself. Two things were corrected in the process: a fabricated document stamp (a wrong date and an author group that does not exist) was removed from four slides, and a companion infographic was held back because four of its six repository figures did not match the measured ones. A picture of a number is still a claim.*
