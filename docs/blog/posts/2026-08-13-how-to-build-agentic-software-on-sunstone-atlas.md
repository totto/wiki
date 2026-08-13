---
description: "A hands-on walkthrough of Sunstone Atlas's building blocks — Knowledge, Skills, Agents, Functions, Playbooks — using a real production system as the worked example. Add agents. Keep control."
date: 2026-08-13T09:00:00
draft: false
categories:
  - AI Agents
  - Engineering
tags:
  - sunstone-atlas
  - agentic
  - governance
  - playbooks
  - kcp
  - defendable-agents
authors:
  - totto
  - fable
  - claude
---

# How to Build Agentic Software on Sunstone Atlas

*Add agents. Keep control. A hands-on walkthrough of the building blocks, using a real production system as the worked example.*

Most "agentic" software today is an LLM in a loop with tool access and a prompt that says *please be careful*. That works right up until the agent is allowed to do something that costs money — approve an expense, send a quote, create an order — and someone from Risk or Compliance asks the only question that matters: **how do you know it stayed inside the rules, every time, and can you prove it?**

If the honest answer is "we trust the prompt," the deployment stops there.

Sunstone Atlas takes a different position: agents should be able to act autonomously *and* the system should be able to prove, after the fact, that letting them act was safe. Not with a gateway that blocks everything interesting, but with a substrate where every capability, every fact, every procedure, and every participant is a **signed, versioned artifact**, and every decision at runtime — model judgment, deterministic rule, or human sign-off — is a **cryptographically signed, replayable event on an append-only ledger**. Conformance + signing + grounding: defendable by construction, not by assurance.

<!-- more -->

This post walks through the actual building blocks and how they compose, using a real production build as the case study: a quote-control system for **Nordvik AS** — a (fictionalized) Norwegian B2B reseller that wins business through project quotes, often dozens of product lines per offer, sometimes under public-tender framework agreements. The architecture, the JSON shapes, and the governance mechanics below are real; the company, project names, and numbers are stand-ins.

Nordvik's problem is a classic one: quotes go out with the wrong rebate baked into the calculation, with the same product listed five or six times under different references, with the wrong environmental documentation attached. Each mistake is found late — in final review, or by the customer. The goal: **AI finds and proposes. A responsible human approves and sends.** And the system must be able to prove that's what actually happened, on every quote.

![Assurance vs. Evidence — LLM-in-a-loop relies on natural language prompts, an ephemeral context window, and unbounded execution; Sunstone Atlas replaces each with cryptographic charters, an append-only ledger, and a graduated trust ladder](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/assurance-vs-evidence.webp)
*The shift in one table: from hoping the model behaves, to proving it did.*

![Sunstone Atlas: Architecture of Governed AI — five core principles, the four-artifact data model, authority ceilings vs. the trust ladder, the three-path enactment runner, and the signing/cryptography layer](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/architecture-overview.webp)
*The full architecture at a glance — worth bookmarking, we'll unpack every box below.*

## The artifact model

Sunstone Atlas (the deployed engine is called **Canvas**) has four governed artifact classes, all stored as plain JSON, all validated by one conformance engine, and all moving through the same lifecycle: **draft → published (signed, versioned)**. A published version is permanent — a new publish adds a version file, it never rewrites one.

| Artifact | What it is |
|---|---|
| **Knowledge** | Declarative facts and context an agent grounds its reasoning in |
| **Agent** | A Knowledge unit that carries a `charter` — a bounded participant |
| **Skill** | An atomic capability with a declared action scope and authority ceiling |
| **Function** | A deterministic, non-LLM predicate — data, never code |
| **Playbook** | A composite, gated procedure wiring the others into steps |

Note that an Agent isn't a separate class. **What makes a Knowledge unit an Agent is the presence of a charter.** That's a deliberate statement about what an agent *is* here: not a process with a loop, but a body of grounded knowledge plus a signed contract about what it may see, propose, and never do.

Let's build up the Nordvik quote-control system one layer at a time.

## Knowledge: what the agent is allowed to know

The bottom layer is boring on purpose. Nordvik's product catalog, rebate agreements, and document-package requirements live as Knowledge units — versioned, published, signed. When an AI step later assesses a quote, the facts it reasons from come from here and from the run's declared inputs, not from whatever the model happens to remember about the world. The staging gateway's system prompt makes this a hard rule, not a hope: *ground every decision only in the policy provided — never use outside knowledge.*

This matters more than it sounds. Grounding is what turns "the model said so" into "the model applied *this* policy version to *these* facts" — which is the difference between an opinion and evidence.

## Skills: atomic capabilities with declared scope

A Skill declares one capability, what it touches, and — critically — what it must never touch:

```json
{
  "id": "check-rebate-against-confirmation",
  "kind": "skill",
  "intent": "Check that the rebate a quote is calculated with is exactly
             the rebate the supplier has confirmed. The three facts are
             laid before the deterministic gate: the match decision is
             made by Function 'price-rebate-gate', never by judgment.",
  "authority_level": "prepare",
  "action_scope": {
    "tools": ["read-quote", "read-supplier-confirmation"],
    "capabilities": ["flag-price-mismatch"],
    "deny": {
      "tools": ["send-quote-to-customer", "create-sales-order"]
    }
  }
}
```

Two things to notice. The `authority_level` — `"prepare"` — comes from a five-token scale: **observe → explain → suggest → prepare → commit**. A skill at `prepare` can get everything ready; it can never commit. And the `deny` list is a boundary, not a threshold: denies compose as a *union* across playbook and skill (never a narrowing), and removing one requires a new reviewed, signed version. Nothing in the system grants past a deny at runtime.

## Agents: charter-bound participants

Here is the AI judgment agent from the Nordvik build — the one that reads a whole quote and assesses whether it hangs together. It's a Knowledge unit with a charter:

```json
{
  "id": "quote-coherence-agent",
  "kind": "knowledge",
  "intent": "Assess in free text whether a quote is coherent and complete
             before it goes to supplier confirmation and final approval:
             right products against the customer's request, no contradictions
             between price, document package and delivery terms.",
  "charter": {
    "authority": "Nordvik AS — Sales",
    "decision_basis": "model_judgment",
    "scope": {
      "read": ["quote", "product-catalog", "document-package",
               "supplier-confirmation"],
      "propose": ["propose-ready-for-approval", "flag-issue-for-clarification"],
      "never": ["send-quote-to-customer", "create-sales-order",
                "modify-policy", "escalate-authority"]
    },
    "rules": [
      {
        "id": "COHERENCE-1",
        "text": "A quote with no flagged issues is proposed ready for the
                 responsible seller's approval; any flagged issue sends it
                 back for clarification before it can be sent.",
        "decision": "propose-ready-for-approval or flag-issue",
        "control": { "mode": "review_after",
                     "authority_required": "responsible-seller" }
      }
    ],
    "escalate_when": ["one or more issues flagged as unresolved"],
    "authority_required": "responsible-seller"
  }
}
```

The charter's `scope` is the enforcement surface. When this agent runs, its proposal is conformance-checked against these lists **by exact match**: a proposed action on the `never` list is an automatic DENY, and anything *not exactly on the propose list* is a deny too — allow is enumerated, never inferred. The model can phrase its reasoning however it likes; the only actions that can survive the gate are the two it's chartered to propose.

![Layer 2: Agents are charter-bound participants — Knowledge Unit + Signed Charter = Agent. Propose (read_knowledge, generate_plan, request_approval, log_action) is enumerated; Never (delete_knowledge, execute_unapproved, override_deny, access_external) is exact; everything else is automatically denied](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/charter-bound-participants.webp)
*Allow is enumerated. Never is exact. Everything else is automatically denied — the same shape as the charter JSON above.*

### The trust ladder

Notice `control.mode: "review_after"` on the rule. This is the graduated-autonomy mechanism, and it's worth being precise about because it's commonly confused with authority levels.

`authority_level` is a **ceiling** — authored per assessed risk, composed lowest-of across playbook, step, and skill, never something an agent climbs. The trust ladder is a separate field: `control.mode`, per rule, moving **block → review_after / sample → monitor**. A new agent starts with heavy oversight (every decision blocked pending review, or reviewed after the fact). As a track record accrues — a configured window, a minimum count of clean decisions, a maximum deviation count, all conjunctive — a rule becomes *eligible* to graduate one rung looser:

![Graduated Autonomy trust ladder activation curve — Block, then Review After/Sample, then Monitor, climbed as a clean track record of decisions accrues; one deviation or human overturn drops the rule straight back to Block](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/trust-ladder-activation-curve.webp)
*Not the same ladder as the authority ceiling above — this one is earned and can be lost. Climbed slowly, one clean-decision window at a time; dropped instantly on the first deviation.*

```json
"graduation": { "mode": "manual", "window": "P30D",
                "min_clean_decisions": 3, "max_deviations": 1 }
```

Three properties make this defensible rather than decorative:

- **The authored charter never changes.** Graduation lives entirely in a separate append-only governance ledger per agent; the effective control mode is computed by replaying that ledger. A machine mutating a governed artifact would break the platform's one absolute rule.
- **Regression is instant and asymmetric.** One deviating decision — or one after-the-fact review where a human overturns the agent's call — regresses the rule immediately, undoing the most recent graduation. Loosening is earned slowly, one rung at a time; tightening is immediate.
- **A high-stakes playbook can opt out entirely.** Setting `x_canvas.control_regime: "authored_only"` forces the authored control modes for that playbook's runs, ignoring any earned relaxation. The extension namespace can only ever *narrow*, never grant.

### Clearance: no run without a human sign-off — pinned to content

Before an AI agent's judgment steps can dispatch at all, the agent must be **cleared**: staged on an isolated gateway, exercised with at least one real test run, then signed off by a human whose role matches the charter's `authority_required`. The clearance event pins a hash of the charter's actual content. Edit the charter afterward and the clearance goes *stale* — the next run refuses to start (HTTP 409, before a single event is written) until a human re-clears against the current content. Grant-once-drift-forever is structurally impossible.

![Content-pinned human clearance — before edit, the charter's hash matches a signed CLEARED stamp and runs freely; after any edit to the charter, the hash breaks and the next run attempt returns HTTP 409: STALE until a human re-clears against the new content](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/content-pinned-clearance.webp)
*Edit the charter, and the old clearance simply stops matching — there's no code path where a stale grant survives.*

## Functions: decisions that replay byte-for-byte

Anything that *can* be decided deterministically *should* be — because a deterministic decision can be re-evaluated later against the recorded facts and reproduce itself exactly. An LLM decision can be attested; it can never be replayed. Functions are the replayable half.

![Layer 3: Functions — a predicate expression tree (AND / exists / == over user.status and transaction.amount) balanced against byte-for-byte replayability: a past fact weighed against a past decision, fail-closed evaluation that escalates to a human instead of defaulting or guessing](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/functions-byte-for-byte.webp)
*No eval, no regex, fail-closed — a Function is data, not code, which is exactly what makes it replayable months later.*

A Function is a predicate expressed as a JSON tree in a small, closed language — comparisons, membership, existence, boolean composition. Never code, never `eval`, deliberately no arithmetic or regex. Here's the gate that checks a quote's rebate against what the supplier actually confirmed:

```json
{
  "id": "price-rebate-gate",
  "kind": "function",
  "inputs": [
    { "name": "rebate_confirmed",        "type": "boolean", "required": true },
    { "name": "quoted_rebate_percent",   "type": "number",  "required": true },
    { "name": "confirmed_rebate_percent","type": "number",  "required": true }
  ],
  "expression": {
    "op": "and",
    "clauses": [
      { "op": "==", "left": { "fact": "rebate_confirmed" }, "right": true },
      { "op": ">=", "left": { "fact": "quoted_rebate_percent" },
                    "right": { "fact": "confirmed_rebate_percent" } },
      { "op": "<=", "left": { "fact": "quoted_rebate_percent" },
                    "right": { "fact": "confirmed_rebate_percent" } }
    ]
  },
  "tests": [
    { "name": "45% quoted vs 45% confirmed matches",
      "facts": { "rebate_confirmed": true, "quoted_rebate_percent": 45,
                 "confirmed_rebate_percent": 45 }, "expect": true },
    { "name": "unconfirmed rebate stops regardless of number match",
      "facts": { "rebate_confirmed": false, "quoted_rebate_percent": 45,
                 "confirmed_rebate_percent": 45 }, "expect": false },
    { "name": "missing confirmation status fails closed, never guessed",
      "facts": { "quoted_rebate_percent": 45,
                 "confirmed_rebate_percent": 45 }, "expect": "not_evaluable" }
  ]
}
```

Evaluation is three-valued and fail-closed: a missing fact or type mismatch is `not_evaluable` — never a default, never a guess — and `not_evaluable` escalates the step to a human. The `tests` array is the publish gate itself: a Function cannot be published unless every one of its own vectors passes, including at least one `true`, one `false`, and (as here) explicit coverage of the fail-closed cases. Harder publish gate, lighter run gate.

## Playbooks: the composed, gated procedure

Now the composition layer. Nordvik's top-level playbook, `quote-control`, wires everything above into one governed procedure. Its shape, abbreviated:

```json
{
  "id": "quote-control",
  "kind": "playbook",
  "authority_level": "prepare",
  "action_scope": {
    "deny": {
      "tools": ["create-sales-order", "execute-payment",
                "send-quote-to-customer"],
      "paths": ["orders/**", "payments/**"]
    }
  },
  "x_canvas": {
    "run_inputs": [
      { "name": "quote_id", "type": "string",  "required": true },
      { "name": "score",    "type": "number",  "required": true },
      { "name": "quoted_rebate_percent", "type": "number", "required": false }
    ]
  },
  "steps": [
    { "id": "auto-check-score",     "uses": "check-price-and-documentation" },
    { "id": "requirements-control", "x_canvas": { "invokes":
        { "playbook": "quote-requirements-control",
          "bind": { "quote_id": "run.quote_id" } } } },
    { "id": "product-control",      "x_canvas": { "invokes":
        { "playbook": "quote-product-control", "...": "..." } } },
    { "id": "documentation-control","x_canvas": { "invokes":
        { "playbook": "quote-documentation-control", "...": "..." } } },
    { "id": "coherence-check",      "x_canvas":
        { "performer": "quote-coherence-agent" } },
    { "id": "supplier-confirmation","x_canvas":
        { "decision_owner": "Supplier", "autonomy_mode": "human_in_loop",
          "outputs": [
            { "name": "rebate_confirmed", "type": "boolean", "required": true },
            { "name": "rebate_percent",   "type": "number" },
            { "name": "valid_until",      "type": "string" } ] } },
    { "id": "price-control",        "x_canvas": { "invokes":
        { "playbook": "quote-price-control",
          "bind": {
            "rebate_confirmed":
              "steps.supplier-confirmation.rebate_confirmed",
            "confirmed_rebate_percent":
              "steps.supplier-confirmation.rebate_percent" } } } },
    { "id": "delivery-control",     "x_canvas": { "invokes":
        { "playbook": "quote-delivery-control", "...": "..." } } },
    { "id": "seller-approval",      "escalation": "requires_approval",
      "x_canvas": { "decision_owner": "Responsible seller",
                    "autonomy_mode": "human_in_loop",
                    "control_form": "pre_approval" } }
  ]
}
```

Several design moves here are worth stealing regardless of platform:

**The deny list at the top makes the playbook's non-goals structural.** This entire procedure — nine steps, four sub-playbooks, an AI judgment, deterministic gates — is *incapable by declaration* of creating an order, executing a payment, or sending the quote. The only step that commits anything is `seller-approval`, and that step is a human. This is the shape of "AI finds and proposes; a responsible person approves and sends" expressed as data rather than as a code-review comment.

**The composite score is a pre-filter, not the control.** The first step runs a fast 0–100 check score against a published threshold gate — cheap early triage. But the score carries no control weight for any dimension: price, product, documentation, and delivery are each decided structurally in their own chained sub-playbook, whatever the score says. One opaque number never stands in for four real checks.

**Each sub-playbook has its own gates and its own ledger.** `quote-price-control`, for instance, runs two Function-gated steps (`price-rebate-gate`, `price-purchase-band-gate`) and ends in a human-set verdict (OK / RISK / CRITICAL) — as its own child run with its own signed event chain, referenced from the parent by `child_run_id`. Sub-playbooks conclude verdicts; only the parent's terminal human step can approve anything.

**Data flow is declared and validated, not discovered.** Look at the `bind` on `price-control`: it consumes `steps.supplier-confirmation.rebate_confirmed` — the recorded output of the *human* confirmation step upstream. The validator checks every such reference at author time: it must point to a declared run input or to a field an upstream dependency actually produces. The human confirmation is never repeated by the machine — it is *re-verified*: the deterministic gate checks that the quote actually uses the rebate the supplier confirmed. And because a model-judgment step's referencable outputs are a fixed four-field shape (`outcome`, `proposed_action`, `confidence`, `citation`), there is no schema surface through which a model-*extracted* value — an amount, a date read out of free text — can launder itself into a downstream deterministic decision.

![Layer 4: Playbooks and structural non-goals — sub-playbooks, AI judgments, and deterministic gates wired together inside a non-goals deny list; if "create order" sits on the top-level deny list, the entire procedure is mathematically incapable of executing a payment or sending a quote](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/playbooks-structural-non-goals.webp)
*The deny list wraps the whole procedure, not just one step — every sub-playbook, every AI judgment, every gate inside it inherits the same non-goals.*

## Enactment: what actually happens at run time

Publishing a playbook makes it a signed, inert artifact. Enactment makes it run. Every step dispatches on the performer's `decision_basis`:

- **`human`** → the step immediately emits a signed `escalation-raised` event and waits. A pause-for-input gate by design, not a failure mode.
- **`deterministic`** → the exact *published* Function version bound to each charter rule is fetched and evaluated against the declared facts. Any missing input or `not_evaluable` result escalates the whole step — no partial credit.
- **`model_judgment`** → the request goes to an **isolated staging gateway**: a separate service, own OS user, own budget, loopback-only, never the production instance. The model gets the step description and the run's recorded facts — no tools, no browsing, one grounded verdict call. Its proposal passes the conformance check against the charter's propose/never lists, then an **asymmetric confidence gate**: low confidence can downgrade an auto-approve to a human escalation, but no amount of confidence can ever upgrade an escalation to an approval. Confidence only ever makes the outcome more cautious.

![Enactment: the append-only ledger — human, deterministic, and model-judgment paths all resolve into dual-signed blocks on a verified chain; AI decisions carry two signatures, one for who decided (the gateway's embedded receipt) and one for what belongs on the chain (the engine's conformance signature)](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/enactment-append-only-ledger.webp)
*Current state is never held in memory — it's reconstructed by replaying this chain, which is why a restarted server always reasons its way back to the identical answer.*

Every decision becomes a signed event on the run's append-only ledger: `run-initiated`, `judgment-decision`, `deterministic-decision`, `escalation-raised`, `human-approval`, through to `run-completed`. A judgment event is **dual-signed** — the gateway's embedded receipt attests *who decided* (the real model call, the real conformance check); the engine's wrapper signature attests *what belongs on this run's chain*. Nothing about a run's state is held in memory: current state is always reconstructed by replaying the ledger, so a restarted server reasons its way to the identical answer.

And the ledger is checkable, not just readable: a verify endpoint re-evaluates every deterministic decision's pinned Function version against its recorded facts (byte-for-byte reproduction) and re-checks that every upstream fact a decision consumed still matches the signed event that produced it — catching a substituted fact, not merely a bad recomputation.

One production war story that shows the gates are real: while wiring the Nordvik UI to the engine, the team discovered that a run of `quote-control` **would not start at all** — a 409 before any event was written — because the coherence agent had been staged but not yet cleared. The fix was not a config flag; it was a human with the `responsible-seller` role recording a signed clearance, once, after a real test run. The team deliberately refused to script that sign-off into the deployment automation: forging the human signature from infrastructure-as-code would hollow out exactly the thing the platform exists to prove.

## The worked flow, end to end

![The end-to-end composition — Lead, Dedup, Build Quote, Quote-Control Run, Customer Accepts; the Quote-Control Run expands into AI Check (proposes), Human Step (records supplier confirmation), and Function Check (mathematically re-verifies) — the AI is an accountable employee, only the terminal human step has authority to send](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/end-to-end-composition.webp)
*Zoomed into the one box that does the governed work — everything either side of it is ordinary application flow.*

Composed, the Nordvik system runs five stages:

1. **A lead arrives** and is scored by a published Function (`lead-tier-a-gate`: score ≥ 70). Deterministic, replayable, no judgment involved.
2. **Deduplication** — is this the same opportunity as an existing one? Flagged for a human; the machine proposes, never merges.
3. **A seller builds the quote** — say `NV-2026-0231`, a 40-line project quote for a municipal customer's fit-out at Verkstedveien 12.
4. **The `quote-control` run**: pre-filter score → requirements register (roughly fifty requirement lines under a framework agreement, each Function-gated, concluding GO / GO-WITH-ADJUSTMENTS / NO-GO) → product control (duplicate-reference and canonical-ID gates — the "same product five times" failure mode, caught structurally) → documentation-package completeness gate plus AI review of whether each attached document covers what's actually offered → the AI coherence check (behind staging, clearance, and conformance) → the supplier confirms the rebate as a recorded human step (45%, freight included, valid until a stated date) → price control re-verifies the quote against that confirmation (guide price 240 000 NOK × 0.55 = 132 000 NOK expected purchase price, checked within ±0.5%) → delivery-terms and validity control → **seller approval**: the one step, in the entire tree of runs, with authority to send.
5. **The customer accepts; an order is created** — outside the deny-scoped playbook, by a human, with the full signed chain behind it. One "verify the chain" click replays it.

## What this actually bought

No superlatives — just what's concretely different from the LLM-in-a-loop version of the same system:

- **The mistake that costs money is structurally impossible for the AI to make.** Sending the quote and creating the order sit on a deny list and behind a human-only terminal step. This isn't prompt engineering; it's a signed artifact a reviewer can read in thirty seconds.
- **Every check that can be deterministic is, and replays byte-for-byte.** The rebate mismatch that used to surface in final review is now caught by a published Function version whose decision can be re-executed against the recorded facts months later.
- **The AI is accountable in the ways an employee is.** Chartered scope, a human clearance pinned to the charter's content, oversight that relaxes only against a measured track record and snaps back on the first deviation.
- **"Prove it" has a mechanical answer.** Not logs — a chained, signed, replayable ledger where the human approval, the supplier confirmation, and the model's proposal are the same class of evidence.

![Unlocking the AI 10x: from risk veto to proven autonomy — the governed substrate's four artifact classes, the three-class trust ladder from blocked to fully autonomous, and measured evidence: grounding lifts auto-approval from 23% to 59% with zero optimistic errors across 10,000 simulations](/assets/images/blog/how-to-build-agentic-software-on-sunstone-atlas/proven-autonomy-evidence.webp)
*This isn't a projection. The "grounding lifts auto-approval 23%→59% at zero optimistic errors" figure is a measured benchmark, and the same governance model shown here is what actually runs Mynder's own compliance platform in production today: 210 knowledge units, 43 skills, 12 playbooks.*

Honest caveats: this is a single-tenant substrate today (flat files, one instance per tenant), identity on the ledger is a typed name rather than an authenticated principal, and there is deliberately **no tool-execution layer yet** — agents propose; integrations that act are separate, later work, and the conformance/deny machinery is designed to gate them when they land. Those are named limitations, not fine print.

The pattern to take away is the composition: **facts you can cite, capabilities with declared scope, agents with charters, deterministic gates wherever determinism is possible, judgment only behind staged clearance, and a human at exactly the steps where a mistake becomes irreversible** — all of it signed, all of it replayable. That's what it takes to answer the Risk Committee's question with evidence instead of assurance.

If you want the fuller architectural picture — the argument for determinism-at-the-core, the threat model, and worked tutorials from an empty repo up — see the [Defendable Agents field guide](/topics/defendable-agents/).

*Sunstone Atlas is built by Sunstone Tech AS / eXOReaction. If you're evaluating governed agent substrates and want to go deeper on any of the mechanics above, get in touch.*
