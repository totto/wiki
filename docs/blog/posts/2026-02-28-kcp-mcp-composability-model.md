---
date: 2026-02-28
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - mcp
  - knowledge-infrastructure
  - standards
  - synthesis
authors:
  - totto
  - claude
---

# KCP + MCP: One Protocol for Structure, One for Retrieval

*The previous post in this series introduced KCP and why llms.txt does not scale to production
agent deployments. This post covers a different question: once you have both a knowledge manifest
and MCP tools, how do you decide which to use — and what happens when you get that decision wrong.*

<!-- more -->

## The decision an agent makes on every task

When an agent begins a task, it faces a choice it rarely gets explicit guidance on: should it
use what it already knows, or go and look for more?

This sounds trivial. It is not. An agent that queries too eagerly wastes tool calls on stable
facts that could have been pre-loaded. An agent that trusts pre-loaded knowledge too long will
confidently act on information that has gone stale. Both failure modes are common, and both have
the same root cause: the agent has no principled way to decide.

KCP and MCP together provide that principle. But only if you understand which layer handles which
problem.

---

## Three failure modes that look like model errors

![The KCP-MCP Composability Model](/assets/images/blog/kcp-mcp-composability-model.png)

**The narrative hallucination trap.** An agent reading a document that says "as of February 19th"
reports February 19th — when the actual date was February 17th. This is not a model error. The
model read the text accurately. The problem is that narrative prose has no machine-readable
freshness signal. The agent had no way to know the document was describing something that had
already changed. Structured metadata eliminates this: a `validated: 2026-02-17` field is not
ambiguous.

**The representation deficiency.** Agents reading unstructured text infer relationships that the
text does not actually state. Two modules described in adjacent paragraphs become "related" in
the agent's mental model even if they are independent. Topology that exists only as prose is
topology the agent will get approximately right and subtly wrong. Explicit `depends_on` fields
in a knowledge manifest remove the inference step.

**The over-invocation penalty.** Without guidance about what is stable, agents treat all
knowledge as uncertain and query for confirmation repeatedly. In benchmark testing, agents
without a knowledge manifest made 18+ tool calls on tasks that required 5–6. The overhead is
not just latency — each additional tool call is another opportunity to retrieve inconsistent
context.

---

## The three-layer solution

KCP and MCP solve different problems and operate at different times in a session. Conflating
them — or using only one — produces the failure modes above.

**Layer 1: KCP manifest (pre-session).** Before the task begins, the context window loads
structured knowledge from `knowledge.yaml`: dependency graphs, architectural decisions, naming
conventions, ROI metrics, onboarding documentation — the stable, documented facts that the agent
needs to operate. This happens once, before any tool is called.

**Layer 2: Decision heuristic (the logic).** A one-line protocol governs what happens next:

> *Trust pre-loaded context if it is fresh and in scope. Use MCP tools if context is stale or
> the query requires computation.*

This is not a rule that agents infer from instructions — it is a rule that should be explicit in
the system prompt or skill file. Without it, agents apply their own judgment about when to
re-query, and that judgment is inconsistent.

The `validated` field in the KCP manifest provides the freshness signal. An agent can refuse to
act on knowledge that has not been validated since a configurable threshold — for instance,
refusing to trust architectural decisions that are more than 72 days old without a verification
call. The staleness boundary is explicit rather than implicit.

**Layer 3: MCP tools (runtime).** When the agent needs something that changes — live dependency
analysis, caller graphs for unfamiliar codebases, real-time verification — it reaches for MCP
tools. These are the queries that cannot be pre-loaded because the answers depend on the current
state of the system.

The division is: stable facts go in the manifest, computed or current facts go through tools.

---

## What the benchmark shows

Testing the MCP+KCP combination against alternatives produced a consistent result:

| Condition | Avg tool calls | vs baseline |
|-----------|---------------|-------------|
| MCP + KCP (with decision heuristic) | 5.8 | −40% |
| MCP + KCP (standard) | 6.2 | −35% |
| Knowledge-only | 7.6 | −19% |
| MCP-only | 9.0 | baseline |

The 40% reduction in tool calls is not primarily a speed improvement — it is an accuracy
improvement. Fewer tool calls means fewer opportunities to retrieve inconsistent or stale
context mid-task. The agent that calls fewer tools is not lazier; it is operating from a more
reliable foundation.

The decision heuristic is the critical variable. MCP+KCP without the explicit heuristic performs
only 35% better than baseline. Adding the one-line protocol gets you the additional 5 points
and, more importantly, makes the agent's behaviour predictable rather than variable.

---

## The staleness threshold in practice

The `validated` field in KCP is an ISO-8601 timestamp that records when a human last confirmed
a knowledge unit was accurate:

```yaml
units:
  - id: auth-architecture
    path: docs/auth.md
    intent: "How does authentication work? Token flow, session management, edge cases."
    depends_on: [security-policy]
    validated: 2026-02-10
    triggers: ["authentication", "session", "token"]
```

An agent working on an authentication task loads this unit from the manifest. If the task begins
on February 28th and the validated date is February 10th, the agent knows the information is 18
days old. Whether to trust it depends on the staleness threshold configured for this system.

This is the mechanism that prevents the Mirror Test failure described in the previous post —
where an agent gave confident, fluent, wrong answers because it had no signal that the
documentation had drifted from the code. The validated field makes the drift visible.

---

## What this looks like in a Synthesis session

When Synthesis is connected as an MCP server and a `knowledge.yaml` exists in the workspace,
the three layers operate automatically:

1. Skills load the manifest into context before the session starts (Layer 1)
2. The system prompt includes the decision heuristic (Layer 2)
3. Synthesis tools (`search`, `relate`, `impact`, `graph`) handle runtime queries (Layer 3)

The agent arrives oriented — knowing the conventions, the dependencies, the validated
architecture — and reaches for live retrieval only when it needs something the manifest cannot
provide.

The result is what the benchmark shows: fewer tool calls, more reliable output, and a
predictable failure mode (stale manifest) rather than an unpredictable one (the agent guessing
when to trust what it knows).

---

*KCP spec and reference parsers: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)
— Apache v2, feedback welcome.*

*Previous in this series: [Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](/blog/2026/02/25/beyond-llms-txt-ai-agents-need-maps-not-tables-of-contents/)*
