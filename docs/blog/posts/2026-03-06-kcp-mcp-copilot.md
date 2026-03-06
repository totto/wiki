---
date: 2026-03-06
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - mcp
  - copilot
  - claude-code
  - tools
authors:
  - totto
  - claude
---

# kcp-mcp v0.6.0: GitHub Copilot Gets KCP

A few days ago we prepared a roadmap for bringing KCP to GitHub Copilot users. Three phases,
estimated ten days. This is the post where I explain that we shipped all three phases today.

<!-- more -->

![Deploying KCP to the Enterprise Copilot Ecosystem — KCP Node to GitHub Copilot Node integration diagram](/assets/images/blog/kcp-copilot-slide-01-title.png)

---

## The problem we were solving

GitHub Copilot commands 20 million users and 90% adoption in the Fortune 100.

![The 20-Million User Enterprise Lockout — 90% Fortune 100 adoption, enterprise developers systemically locked out of Claude Code](/assets/images/blog/kcp-copilot-slide-02-lockout.png)

Enterprise developers in those organisations are not choosing Claude Code over Copilot.
They are locked out by IT policy, volume licensing agreements, and GitHub Enterprise bundles.
KCP's knowledge navigation and SDD methodology had no path into their workflow.

The fix was straightforward once MCP support in Copilot reached GA: build an MCP server that
exposes `knowledge.yaml` units as tools, not just resources. Tools let agents actively query
knowledge. Resources only let them browse.

---

## From passive browsing to active querying

The v0.5.0 kcp-mcp bridge already worked with Copilot — but passively. Agents could call
`resources/list` to enumerate all knowledge units, then `resources/read` to load one by URI.
That requires knowing what to look for in advance.

![Bridging the gap from passive browsing to active querying — kcp-mcp TypeScript bridge: Resources only (v0.5) vs MCP Tools (v0.6)](/assets/images/blog/kcp-copilot-slide-04-passive-to-active.png)

v0.6.0 adds active lookup. The agent says *"find me what's documented about authentication"* and
gets a scored result list back. It does not need to know the unit ids ahead of time.

---

## The plan said ten days. We shipped it in one session.

The NotebookLM planning deck estimated three phases across roughly ten days:

![A 10-Day Execution Roadmap: Phase 1 Active Lookup (v0.6.0, 2-3 days), Phase 2 MCP Prompts (1 day), Phase 3 Copilot Artifacts (2-3 days)](/assets/images/blog/kcp-copilot-slide-05-roadmap.png)

All three phases shipped in `kcp-mcp@0.6.0` today, in both the TypeScript and Java bridges.

---

## What v0.6.0 adds

### Three MCP tools

![Phase 1: Equipping agents with active lookup tools — search_knowledge, get_unit, get_command_syntax across TypeScript and Java bridges](/assets/images/blog/kcp-copilot-slide-06-tools.png)

**`search_knowledge`** — Find units by keyword. The agent calls this instead of loading the
entire manifest. Input: `{ query, audience?, scope? }`. Output: a JSON array of the top-5
matching units with id, intent, path, uri, and score.

**`get_unit`** — Fetch the full content of a unit by id. Input: `{ unit_id }`. Output: the
raw file content — markdown, YAML, JSON, whatever the unit contains.

**`get_command_syntax`** — Get compact CLI syntax for any command (requires `--commands-dir`).
Input: `{ command }` — e.g. `"git rebase"`, `"docker build"`, `"mvn"`. Output: the same
compact block that kcp-commands injects for Claude Code users.

### The scoring algorithm

When `search_knowledge` runs, it evaluates every unit in the manifest against a strict
scoring matrix:

![Search Mechanics: The Knowledge Scoring Algorithm — 10 pts exact id match, 5 pts trigger match, 3 pts intent match, 1 pt path match, returns top-5 JSON array](/assets/images/blog/kcp-copilot-slide-07-scoring.png)

Exact match on the unit `id`: 10 points. Term found in `triggers`: 5 points per match.
Term found in `intent`: 3 points. Term found in `path`: 1 point. Top 5 returned.

This keeps responses tight. An agent asking about authentication gets the authentication
units, not a dump of everything.

### Two MCP prompts

![Phase 2: Embedding KCP Methodology via Prompts — sdd-review and kcp-explore prompt templates](/assets/images/blog/kcp-copilot-slide-08-prompts.png)

**`/sdd-review`** — Review code or architecture using SDD (Skill-Driven Development) methodology
principles. Optional `focus` argument: `architecture`, `quality`, `security`, `performance`.
Invoke in Copilot Chat as `/sdd-review` or `/sdd-review focus=security`.

**`/kcp-explore`** — Navigate available knowledge units for a topic. Required `topic` argument.
Invoke as `/kcp-explore authentication` or `/kcp-explore deployment`.

### Zero-infra option: `--generate-instructions`

For locked-down environments where no MCP server can run:

![Phase 3: Bypassing infra limits with zero-footprint artifacts — knowledge.yaml → kcp-instructions-gen → .github/copilot-instructions.md](/assets/images/blog/kcp-copilot-slide-09-zero-infra.png)

```bash
npx kcp-mcp --generate-instructions knowledge.yaml > .github/copilot-instructions.md

# Agent-facing units only
npx kcp-mcp --generate-instructions knowledge.yaml --audience agent > .github/copilot-instructions.md
```

Commit the file. Copilot automatically injects its contents into every chat in the repository.
No server, no Node.js runtime, no configuration beyond committing a file.

---

## The 60/100 Rule

Not everything comes across. Phase B output filtering and full SDD skill graphs remain
Claude Code-exclusive. That is deliberate.

![The 60/100 Rule: Copilot gets native KCP value and basic SDD (60%); Claude Code adds Phase B output filtering and full SDD skill graphs (100%)](/assets/images/blog/kcp-copilot-slide-03-60-100-rule.png)

Copilot users get the knowledge layer: `search_knowledge`, `get_unit`, `get_command_syntax`,
the two methodology prompts, and `--generate-instructions`. That is meaningful value for
teams who cannot leave their current IDE.

Claude Code users keep Phase B (the output noise filter that recovers 33% of context window)
and the full SDD skill graph integration, which has no equivalent in the Copilot model.
The 40% gap is the conversion argument for enterprise teams who want to go further.

---

## Setup

### VS Code (Copilot)

Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "project-knowledge": {
      "type": "stdio",
      "command": "npx",
      "args": ["kcp-mcp@0.6.0", "knowledge.yaml"]
    }
  }
}
```

With kcp-commands syntax tool (284 bundled command manifests):

```json
{
  "servers": {
    "project-knowledge": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "kcp-mcp@0.6.0",
        "knowledge.yaml",
        "--commands-dir",
        "${workspaceFolder}/node_modules/kcp-commands/commands"
      ]
    }
  }
}
```

Reload VS Code. The server appears under **Copilot icon → MCP Servers**.

### Claude Code

```json
{
  "mcpServers": {
    "project-knowledge": {
      "command": "npx",
      "args": ["kcp-mcp@0.6.0", "knowledge.yaml"]
    }
  }
}
```

Full setup guide for all IDEs: [docs/guides/copilot-setup.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/docs/guides/copilot-setup.md).

---

## Java bridge

Both bridges ship at full parity. The Java bridge (`kcp-mcp` fat JAR) now includes
`KcpCommands`, `KcpInstructions`, and the same three tools and two prompts as the
TypeScript bridge. Pass `--commands-dir` and `--generate-instructions` to the Java CLI
exactly as you would to `npx kcp-mcp`.

```json
{
  "mcpServers": {
    "project-knowledge": {
      "command": "java",
      "args": ["-jar", "/path/to/kcp-mcp-0.6.0-jar-with-dependencies.jar", "knowledge.yaml"]
    }
  }
}
```

---

## Install

```bash
# npm (no install needed — just run)
npx kcp-mcp@0.6.0 knowledge.yaml

# or install globally
npm install -g kcp-mcp
```

Package: [npmjs.com/package/kcp-mcp](https://www.npmjs.com/package/kcp-mcp)
Source: [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)

---

*This post is part of the Knowledge Context Protocol series. Related:
[kcp-commands: Save 33% of Claude Code's Context Window](./2026-03-02-kcp-commands.md) ·
[Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](./2026-02-25-beyond-llms-txt-knowledge-context-protocol.md).*
