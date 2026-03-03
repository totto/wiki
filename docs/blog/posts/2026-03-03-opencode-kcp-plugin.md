---
date: 2026-03-03
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - opencode
  - plugin
  - knowledge-infrastructure
  - context-window
authors:
  - totto
  - claude
---

# KCP Comes to OpenCode: The First AI Coding Tool Plugin

[kcp-commands](./2026-03-02-kcp-commands.md) recovers 33% of Claude Code's context window
by intercepting Bash tool calls. Today we are extending that same principle to
[OpenCode](https://github.com/anomalyco/opencode) — the 114K-star TypeScript alternative to
Claude Code.

The result is [`opencode-kcp-plugin`](https://www.npmjs.com/package/opencode-kcp-plugin): a plugin
that injects a `knowledge.yaml` knowledge map into every OpenCode session and annotates file
search results with intent descriptions. The mechanism is different from kcp-commands, and the
target is different, but the underlying idea is identical: give the agent a map so it does not
have to rediscover the territory on every session.

<!-- more -->

![Boosting AI Coding Efficiency: The OpenCode KCP Plugin — problem, mechanism, benchmark, and quick start](/assets/images/blog/opencode-kcp-plugin-overview.png)

---

## The problem in OpenCode sessions

OpenCode has an explore subagent. When you ask it to find something — "where is the skill
discovery logic?", "what controls MCP server registration?" — it navigates by grep, glob, and
read. Without any prior knowledge of the codebase, it issues multiple tool calls to triangulate
the answer.

That exploration is not wasted work. The agent gets there. But it gets there more slowly than
it needs to, and it uses context window space doing it. For a codebase with a known structure —
and the structure of an AI coding tool's internals is exactly the kind of thing you can document
once and reuse forever — the exploration overhead is avoidable.

The fix is the same one we applied to CLI commands: give the agent a manifest that maps keyword
intent to file path, and let it skip the search when the answer is already known.

---

## What the plugin does

The plugin uses two of OpenCode's plugin hooks.

**`experimental.chat.system.transform`** fires when OpenCode assembles the system prompt for a
session. The plugin appends a compact knowledge map derived from `knowledge.yaml`:

```
## Codebase Knowledge Map

This project has a `knowledge.yaml` manifest (KCP). Use this map to find
files directly before running glob/grep searches.
★ = load immediately  ·  space = load on demand

★ [readme] README.md
    What is OpenCode, how to install it, and what makes it different from Claude Code
    keywords: overview, install, getting started, features

★ [agents-md] AGENTS.md
    Coding style conventions, naming rules, and testing practices for this codebase
    keywords: style, naming, conventions, testing, code quality

  [config-schema] packages/opencode/src/config/config.ts
    Full config schema: providers, MCP servers, agents, skills, permissions, keybindings
    keywords: config, opencode.json, settings, schema, provider, MCP

  [agent-definitions] packages/opencode/src/agent/agent.ts  (after: config-schema)
    How agents (build, plan, explore, general) are defined, configured, and composed
    keywords: agent, build agent, plan agent, explore agent, subagent, permissions
...
```

For a 17-unit manifest, this section is approximately 800 tokens. The agent reads it before
any exploration begins. "Where is the skill discovery logic?" resolves to
`packages/opencode/src/skill/discovery.ts` in one lookup.

**`tool.execute.after`** fires after glob and grep results return. When a result line contains a
path that matches a KCP unit, the plugin appends the unit's intent description inline:

```
packages/opencode/src/skill/skill.ts  # KCP: How skills (SKILL.md files) are discovered
packages/opencode/src/skill/discovery.ts  # KCP: Remote skill fetching from URLs via index.json
```

The agent can identify the right file from the annotated result without reading both.

---

## The numbers behind this

The 73–80% tool call reduction figure comes from the benchmark we ran against three AI agent
framework repositories — AutoGen, smolagents, and CrewAI — before filing KCP integration PRs:

| Framework | Baseline tool calls | With KCP | Reduction |
|-----------|--------------------|-----------|----|
| AutoGen | ~140 | ~28 | 80% |
| CrewAI | ~95 | ~23 | 76% |
| smolagents | ~82 | ~22 | 73% |

The methodology: identical queries to agents without KCP (baseline) and with a `knowledge.yaml`
manifest (KCP condition). Tool-use counts from API `usage.tool_uses` metadata. Same model, same
session configuration, same queries.

The reduction is largest for explore-heavy workloads — exactly the scenario where OpenCode's
explore subagent is active. For tasks that do not involve file discovery, the overhead of reading
the 800-token knowledge map is recovered within the first avoided search.

---

## Install

The plugin is on npm:

```bash
npm install opencode-kcp-plugin
```

Add to your `opencode.json` or `.opencode/opencode.jsonc`:

```json
{
  "plugin": ["opencode-kcp-plugin"]
}
```

If there is no `knowledge.yaml` at your project root, the plugin registers no hooks and
adds zero overhead. It activates only when a manifest is present.

---

## Add a knowledge.yaml

The plugin needs a manifest to read. The minimum viable version is five fields per unit:

```yaml
kcp_version: "0.5"
project: my-project
version: 1.0.0
units:
  - id: readme
    path: README.md
    intent: "What is this project and how do I get started?"
    scope: global
    audience: [human, agent]
```

The [five-minute adoption guide](./2026-02-28-kcp-adoption-guide.md) covers the full field
set. `synthesis export --format kcp` will generate a `knowledge.yaml` from an existing
Synthesis index automatically — one command for a full manifest from an indexed workspace.

A `knowledge.yaml` for the OpenCode repo itself — 17 units covering the agent system, session
pipeline, skill system, plugin hooks, and MCP integration — is in
[PR #15839](https://github.com/anomalyco/opencode/pull/15839) awaiting review.

---

## How it relates to kcp-commands

kcp-commands and opencode-kcp-plugin solve the same problem at different points in the stack.

kcp-commands works at the **Bash tool boundary**: it intercepts shell command execution, injects
CLI syntax context before the command runs (Phase A), and filters noisy output after (Phase B).
It works in Claude Code via a `PreToolUse` hook. It has no awareness of the codebase structure —
it knows about commands, not files.

opencode-kcp-plugin works at the **session and file tool boundary**: it injects the codebase
structure map into the system prompt and annotates file search results. It works in OpenCode via
the plugin API. It has no awareness of CLI commands — it knows about files, not shell syntax.

The two are complementary. A developer using OpenCode gets codebase navigation improvements from
the plugin. A developer using Claude Code gets CLI efficiency from kcp-commands. Both use the
same underlying format — `knowledge.yaml` manifests with intent, triggers, and dependency
ordering — which is why a single `knowledge.yaml` at the project root benefits both tools.

---

## Source

The plugin source is in the knowledge-context-protocol repository:
[`plugins/opencode/`](https://github.com/Cantara/knowledge-context-protocol/tree/main/plugins/opencode)

It is 120 lines of TypeScript across two files: a manifest reader (`kcp.ts`) and the plugin
entry point (`index.ts`). The only dependency is `js-yaml`.

The [KCP spec](https://github.com/Cantara/knowledge-context-protocol) is Apache 2.0 and has
been submitted to the Agentic AI Foundation (Linux Foundation) for neutral governance alongside
MCP and AGENTS.md.

---

*This post is part of a series on knowledge infrastructure for AI agents.*
*Previous: [kcp-commands: Save 33% of Claude Code's Context Window](./2026-03-02-kcp-commands.md)*
