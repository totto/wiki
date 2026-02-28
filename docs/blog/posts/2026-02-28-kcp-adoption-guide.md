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
  - claude-code
authors:
  - totto
  - claude
---

# Add knowledge.yaml to Your Project in Five Minutes

*A practical walkthrough of the KCP adoption gradient — from the minimum viable
manifest to a full knowledge graph. No theory. Just the steps.*

<!-- more -->

If you have not read the earlier posts in this series, the short version:
[KCP](https://github.com/Cantara/knowledge-context-protocol) is a `knowledge.yaml`
manifest you drop at the root of a project to make your knowledge navigable by AI agents.
It adds topology, intent, freshness, and selective loading — the things llms.txt cannot
express. You can start in five minutes and grow from there.

---

## Level 1: Minimal — five minutes, any project

The smallest valid `knowledge.yaml`:

```yaml
kcp_version: "0.3"
project: my-project
version: 1.0.0

units:
  - id: overview
    path: README.md
    intent: "What is this project and how do I get started?"
    scope: global
    audience: [human, agent]
```

That is it. Three root fields, one unit, five fields per unit. An agent connecting to this
via the MCP bridge can now find your README by asking "how do I get started?" rather than
guessing from a file name.

The `intent` field is the one that changes agent behaviour most. It is not a title — it is
the question this document answers, phrased as the agent would ask it. Write it that way.

**Validate it:**
```bash
# Python
pip install kcp
kcp validate knowledge.yaml

# Or just check the schema
kcp validate --strict knowledge.yaml
```

---

## Level 2: Personal site — add freshness and reading order

Once you have more than a handful of documents, two fields earn their weight immediately:
`validated` and `depends_on`.

`validated` is an ISO 8601 date recording when a human last confirmed the content was
accurate. Agents can be configured to distrust units older than a threshold — refusing to
act on architecture decisions that are 90 days stale, for instance, without a live
verification call.

`depends_on` tells the agent what to load first. An authentication guide that assumes you
have read the installation guide should declare that dependency. The agent loads in the
right order instead of guessing.

```yaml
kcp_version: "0.3"
project: wiki.example.org
version: 1.0.0
updated: "2026-02-28"

units:
  - id: home
    path: index.md
    intent: "Who is this person and what is this site about?"
    scope: global
    audience: [human, agent]
    validated: "2026-02-28"

  - id: about
    path: about/index.md
    intent: "What have they built, what do they believe, what are they doing now?"
    scope: global
    audience: [human, agent]
    validated: "2026-02-28"
    depends_on: [home]

  - id: cv
    path: about/cv.md
    intent: "What is their full professional history, credentials, and employment record?"
    scope: project
    audience: [human, agent]
    validated: "2026-02-28"
    depends_on: [about]

  # Agent-only: the machine-readable entry points
  - id: llms-index
    path: llms.txt
    intent: "What does this site contain? (machine-readable index)"
    scope: global
    audience: [agent]
    validated: "2026-02-28"
```

Note `audience: [agent]` on the llms.txt unit. Human readers do not need to be told about
it. Agents do.

Live reference: [wiki.totto.org/knowledge.yaml](https://wiki.totto.org/knowledge.yaml)

---

## Level 3: Multi-section knowledge base — add triggers and relationships

For a larger project — multiple documentation sections, a community wiki, an enterprise
codebase — two more fields become useful: `triggers` and `relationships`.

`triggers` are keywords or task contexts that make a unit relevant. They let the agent
load the right unit without reading everything:

```yaml
  - id: auth-architecture
    path: docs/auth.md
    intent: "How does authentication work? Token flow, session management, edge cases."
    scope: module
    audience: [developer, agent]
    validated: "2026-02-28"
    depends_on: [security-policy]
    triggers: [authentication, session, token, OAuth, login]
```

`relationships` express connections that do not fit into `depends_on` — context, supersedes,
enables:

```yaml
relationships:
  - from: software-architecture
    to: iam-architecture
    type: enables
  - from: enterprise-architecture
    to: software-architecture
    type: context
  - from: auth-v2
    to: auth-v1
    type: supersedes
```

The distinction matters: `depends_on` means "load this first." `enables` means "this makes
that possible." `context` means "this explains why that exists." An agent navigating the
graph can follow the edges to understand prerequisite order, background, and what has been
superseded.

Live reference: [cantara.github.io/wiki/knowledge.yaml](https://cantara.github.io/wiki/knowledge.yaml)
— 16 units covering IAM, microservices, agile, and enterprise architecture, with full
relationship graph.

---

## The adoption gradient

| Level | Fields used | Time to add | When to stop here |
|-------|-------------|-------------|-------------------|
| **Minimal** | `id`, `path`, `intent`, `scope`, `audience` | 5 min | Small projects, getting started |
| **Personal site** | + `validated`, `depends_on` | 30 min | Personal wikis, portfolios, small doc sites |
| **Multi-section** | + `triggers`, `relationships` | 1–2 hours | Community wikis, open source docs, team knowledge bases |
| **Enterprise** | + full relationship graph, role-based audience, cross-repo units | Ongoing | Large orgs, multiple repos, production agent deployments |

Start at the level that matches what you have. The manifest is valid at Level 1. Add fields
when they solve a problem you are actually experiencing, not before.

---

## Connect it to MCP

Once your `knowledge.yaml` exists, the bridge exposes it to any MCP-speaking agent:

```bash
pip install kcp-mcp   # or: npm install -g kcp-mcp
kcp-mcp knowledge.yaml
```

Claude Code config:

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

The agent can now call `resources/list` to see the full unit index, then load individual
units by intent rather than by filename. The previous post covers [how the decision model
works](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/) —
when to pre-load from the manifest versus when to reach for live MCP tools.

---

## Full field reference

All available unit fields, for reference:

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | required | Unique identifier within the manifest |
| `path` | required | Relative path to the content file |
| `intent` | required | The question this unit answers (one sentence) |
| `scope` | required | `global`, `project`, or `module` |
| `audience` | required | `human`, `agent`, `developer`, `architect`, `operator` |
| `validated` | recommended | ISO 8601 date of last human confirmation |
| `depends_on` | optional | IDs that should be loaded first |
| `triggers` | optional | Keywords that signal relevance |
| `supersedes` | optional | ID of the unit this replaces |
| `kind` | optional | `knowledge`, `schema`, `service`, `policy`, `executable` |
| `update_frequency` | optional | How often this content changes |

---

Spec, examples, parsers, and bridge implementations:
[github.com/cantara/knowledge-context-protocol](https://github.com/cantara/knowledge-context-protocol)

*This post is part of a series on knowledge infrastructure for AI agents.*
*Previous: [KCP and MCP: One Protocol for Structure, One for Retrieval](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/)*
