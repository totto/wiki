---
title: "Reference Architecture: The Inversion"
description: "Determinism at the core, the model at the edge. The three components of a defendable agent — planner, harness, model — and how a task becomes evidence you can defend to an auditor."
image: assets/images/kcp-agent-020-06-composes-with-mcp.webp
---

# Reference Architecture: The Inversion

Most agent architectures put the model in the middle. A language model receives a task, decides what to do, calls some tools, decides what to do next, and eventually emits an answer. The reasoning, the control flow, and the judgement all live in the same probabilistic box. When someone later asks *why* the system did what it did, the honest answer is a shrug and a token trace.

The defendable architecture inverts this. Determinism sits at the core; the model sits at the edge. Every consequential decision — every score, every band, every budget check — runs through pure functions that produce the same output for the same input, forever. The model is confined to the perimeter, where it is genuinely good: reading messy source text, extracting a signal, drafting prose. It never decides the outcome. It only proposes the inputs, and those inputs are recorded before they are used.

I call this the inversion because it reverses the default trust relationship. You do not trust the model and hope to audit it afterwards. You trust the deterministic core and let the model contribute only what the core can check. The argument for why this is the right trade lives in [determinism vs probabilism](/topics/defendable-agents/argument/determinism-vs-probabilism/); this page is about the shape of the thing.

## Three components

A defendable agent is three parts, and the boundaries between them are the whole point.

**The deterministic planner.** Pure scoring and planning functions with no I/O, no clock, no network. In the Lodestar example, a layer score is the mean of its 1-5 variable scores times 20, and a buyer score is the weighted composite of three layers — Need (0.40), Attractiveness (0.25), Winnability (0.35). Same eighteen variables in, same 0-100 total and priority band out, every time. See the [deterministic planner](/topics/defendable-agents/architecture/deterministic-planner/) for how these functions stay pure.

**The governance harness.** The layer that wraps every operation and enforces the rules an auditor cares about: fail-closed gating, an append-only audit trail, a budget ledger, temporal pins, and tenant isolation. Nothing consequential happens outside it. The [governance harness](/topics/defendable-agents/architecture/governance-harness/) page covers the enforcement machinery; [fail-closed behaviour](/topics/defendable-agents/architecture/fail-closed-behavior/) covers what happens when a rule trips.

**The model at the edge.** The language model, used for exactly the tasks a model is good at and nothing more. It reads a document and proposes a signal-strength of 4; the harness records that proposal, the planner consumes it deterministically. The [model at the edge](/topics/defendable-agents/architecture/model-at-the-edge/) page is honest about what this does and does not buy you — the model is still a model, and a confident wrong extraction is still wrong. Determinism guarantees the *process*, not the *correctness*: a bad variable is applied consistently, but visibly and reproducibly, which is precisely how you catch it.

The harness is configured, not coded. A single `harness.yaml` declares the governed domains and the policy that binds them:

```yaml
governance:
  domains:
    - manifest: knowledge.yaml
      paths: [scoring/**, planning/**]
      tools: [kcp_plan, kcp_load]
policy:
  fail_closed: true
  audit_all: true
  max_units: 1000          # session budget ceiling, in units
  strict: true
  budget: { amount: 1000, currency: units }
  context_budget: 200000   # tokens
audit:
  path: ./state/audit.jsonl
```

## From task to evidence

A governed operation follows the same four steps every time. First it records the budget cost and throws — emitting a `budget_exceeded` event — if the ceiling is breached. Then it runs the pure deterministic score. Then it creates a [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) capturing `scoredAt`, `dataAsOf`, the signal dates, and the model version and hash. Finally it emits an [audit event](/topics/defendable-agents/primitives/audit-trail/) carrying the full variable trace. A task does not merely produce an answer; it produces a defensible record of how the answer was reached.

## The auditor-questions table

The clearest way to see the inversion is to put an auditor's questions next to who answers them.

| Auditor asks | Model-in-the-middle | Defendable architecture |
| --- | --- | --- |
| Why this outcome? | Token trace, post-hoc | [Decision trace](/topics/defendable-agents/primitives/decision-traces/): every variable input and output, recorded |
| Would you get the same answer again? | No guarantee | Deterministic engine — same inputs, same output |
| What data was this based on, and when? | Usually unknown | Temporal pin: `dataAsOf` and signal dates |
| Who ran it, and under what limits? | Unlogged | Audit event `actor` + budget ledger `runningTotal`/`ceiling` |
| What stopped it doing the wrong thing? | A prompt, maybe | Fail-closed gate + budget ceiling, enforced |
| Can one tenant see another's results? | Depends on the prompt | Directory boundary, enforced by the harness |

The left column is a set of promises. The right column is a set of records. That difference is what [defendable means](/topics/defendable-agents/argument/what-defendable-means/).

## Where the reference implementations fit

Two components ground this architecture in running code. **kcp-agent** exposes the MCP tools `kcp_plan`, `kcp_load`, and `kcp_validate`, and reads a [KCP manifest](/topics/defendable-agents/kcp/manifest-basics/) that declares the scoring models as governed units — so the right model is selected deterministically and never silently swapped. **kcp-harness** is the enforcement layer configured by the `harness.yaml` above: it owns the audit trail, the budget ledger, and the pin map for a session. The image at the top of this page shows how that composition sits against MCP; the wiring itself is walked through in [wiring KCP, agent and MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/).

An honest caveat to close on. This architecture makes decisions reproducible, bounded, and auditable — it does not make them correct, and it is not a one-time setup. Temporal pinning tells you data is stale; it does not refresh it. Fail-closed gating, over-tuned, will block legitimate work. Governance here is maintenance, not installation. What you get for that ongoing cost is a system whose behaviour you can actually defend — which, for anything operating in a regulated professional-services market, is the difference between shipping and not.
