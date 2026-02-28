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
  - claude-code
authors:
  - totto
  - claude
---

# KCP and MCP: One Protocol for Structure, One for Retrieval

*The [previous post](/blog/2026/02/25/beyond-llms-txt-ai-agents-need-maps-not-tables-of-contents/)
introduced KCP and why llms.txt does not scale to production agent deployments. This post covers
what happens when you connect a `knowledge.yaml` manifest to a live MCP server — and why the
combination changes how agents behave.*

<!-- more -->

## It works today

Drop a `knowledge.yaml` in your project. Install the bridge. Add four lines to your MCP config.
Every agent that speaks MCP — including Claude Code — can now navigate your structured knowledge
without loading everything at once.

**Python:**
```bash
pip install kcp-mcp
```

**TypeScript:**
```bash
npx kcp-mcp knowledge.yaml
```

**Claude Code config** (`.mcp.json` or `~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "project-knowledge": {
      "command": "kcp-mcp",
      "args": ["knowledge.yaml"]
    }
  }
}
```

That is the whole setup. The bridge exposes each knowledge unit as an MCP resource. The agent
calls `resources/list` to see the manifest, then loads units by URI — `knowledge://{project}/{unit-id}`.
It loads what it needs, when it needs it, with freshness metadata intact.

The bridge implementations — Python, TypeScript, and Java — are in the
[KCP repository](https://github.com/Cantara/knowledge-context-protocol/tree/main/bridge).
Apache v2.

---

## What the agent sees

![The KCP-MCP Composability Model](/assets/images/blog/kcp-mcp-composability-model.png)

When the bridge is running, the agent has access to structured knowledge units — not a flat
text dump. Each resource carries the metadata that makes it navigable:

| MCP field | What it provides |
|-----------|-----------------|
| `title` | The unit's `intent` — the question this unit answers |
| `description` | Intent + triggers + depends_on — when to load it and what it needs |
| `annotations.priority` | Scope weight: `global=1.0`, `project=0.7`, `module=0.5` |
| `annotations.audience` | Whether this unit is for humans, agents, or both |

A synthetic manifest resource at `knowledge://{slug}/manifest` returns the full unit index as
JSON — the recommended entry point. The agent gets a navigable map of what exists and what each
unit answers, before loading any content.

---

## Why this matters: three failure modes it prevents

**The narrative hallucination trap.** An agent reading a document that says "as of February 19th"
reports February 19th — when the actual date was February 17th. Not a model error. The text had
no machine-readable freshness signal. A `validated: 2026-02-17` field is unambiguous; narrative
prose is not.

**The representation deficiency.** Agents reading unstructured text infer relationships that the
text does not state. Two modules described in adjacent paragraphs become "related" in the agent's
model even if they are independent. Explicit `depends_on` fields remove that inference step.

**The over-invocation penalty.** Without guidance about what is stable, agents treat all knowledge
as uncertain and query repeatedly for confirmation. In benchmark testing, agents without a
knowledge manifest made 18+ tool calls on tasks that required 5–6.

---

## The decision rule

KCP and MCP operate at different times. Conflating them — or using only one — produces the
failure modes above.

The manifest (KCP) loads before the session starts: stable facts, dependency graphs,
architectural decisions, naming conventions. The MCP tools handle runtime queries: live
dependency analysis, caller graphs, current state. The boundary between them fits in one line:

> *Trust pre-loaded context if it is fresh and in scope. Use tools if context is stale or the
> query requires computation.*

The `validated` field in each knowledge unit provides the freshness signal. An agent can be
configured to distrust units older than a threshold — say, 72 days — and fall back to a live
tool query rather than acting on stale context. The staleness boundary is explicit rather than
left to the agent to infer.

---

## What the benchmark shows

| Condition | Avg tool calls | vs baseline |
|-----------|---------------|-------------|
| MCP + KCP (with decision heuristic) | 5.8 | −40% |
| MCP + KCP (standard) | 6.2 | −35% |
| Knowledge-only | 7.6 | −19% |
| MCP-only | 9.0 | baseline |

The 40% reduction in tool calls is primarily an accuracy improvement, not a speed improvement.
Fewer tool calls means fewer opportunities to retrieve inconsistent or stale context mid-task.
The decision heuristic — made explicit rather than inferred — accounts for the difference between
the 35% and 40% results.

---

## Getting the bridge

- **Python**: [bridge/python](https://github.com/Cantara/knowledge-context-protocol/tree/main/bridge/python) — `pip install kcp-mcp`
- **TypeScript**: [bridge/typescript](https://github.com/Cantara/knowledge-context-protocol/tree/main/bridge/typescript) — `npx kcp-mcp`
- **Java**: [bridge/java](https://github.com/Cantara/knowledge-context-protocol/tree/main/bridge/java) — Maven jar

KCP spec, RFCs, and reference parsers: [github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)

---

*Previous in this series: [Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](/blog/2026/02/25/beyond-llms-txt-ai-agents-need-maps-not-tables-of-contents/)*
