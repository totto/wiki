---
date: 2026-03-13
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - discovery
  - federation
  - standards
authors:
  - totto
  - claude
---

# KCP v0.10: Pre-Invocation Discovery

An agent is about to call a knowledge server. It has no idea what that server
knows, how sensitive the content is, or whether the answer will fit in its
remaining context window. So it calls blindly and hopes for the best.

v0.10 fixes that with RFC-0007: a normative query vocabulary that lets agents
ask before they invoke.

<!-- more -->

---

## The query vocabulary

RFC-0007 defines a request/response shape for pre-invocation capability
discovery. Before calling `get_unit` or `search_knowledge`, an agent can issue a
query with structured constraints:

- **terms** -- what topics to match against
- **audience** -- filter to units relevant to this consumer role
- **sensitivity_max** -- reject anything above this classification level
- **max_token_budget** -- only return units that fit in the remaining window

The response is a scored ranked list. Scoring follows the same algorithm the
kcp-mcp bridge already uses internally: trigger matches score 5 points, intent
matches 3, id and path matches 1 each. The difference is that this is now
specified normatively -- any conformant implementation returns the same ranking
for the same query.

The practical effect: an agent with 12K tokens remaining does not waste half of
them discovering that the unit it fetched is 40K tokens of restricted content it
cannot use. It asks first.

---

## Federation version pinning

v0.9 added federation -- declaring sub-manifests and cross-manifest
dependencies. What it did not add was a way to say "I depend on v2.1 of that
manifest, not whatever version happens to be live."

v0.10 adds two fields to `manifests[]` entries:

- **`version_pin`** -- the expected version string (e.g. `"2.1.0"`)
- **`version_policy`** -- how strictly to enforce it: `exact`, `minimum`, or
  `compatible`

Validators emit a WARNING on mismatch, never reject. This is intentional.
Federation is advisory. Breaking a build because an upstream manifest bumped a
patch version would defeat the purpose.

---

## Instruction file bridge

A new guide (`guides/instruction-file-bridge.md`) documents how to use
`knowledge.yaml` as the single source of truth for vendor-specific instruction
files: `CLAUDE.md`, `.github/copilot-instructions.md`, `.github/agents.json`.

One manifest, multiple outputs. The CI workflow from the
[kcp-mcp Copilot post](./2026-03-06-kcp-mcp-copilot.md) already demonstrated
`--generate-all`. The bridge guide formalises the mapping rules.

---

## `kcp init`

The adopting guide now specifies `kcp init` -- a command that scans a project and
bootstraps a `knowledge.yaml` with discovered artifacts. Three levels of detail
(`--level 1|2|3`) and a `--scan` flag for deeper file inspection. Markdown
headings become candidate triggers. OpenAPI files get `kind: schema`
automatically.

Not a runtime feature -- a spec for tooling authors. But it closes the
"where do I start?" gap that comes up in every adoption conversation.

---

## What did not change

537 tests across all parsers and bridges. Zero breaking changes. A manifest
written for v0.1 is still valid under v0.10. That strict-superset constraint
continues to hold.

---

Spec, changelog, and updated parsers:
[github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)

*This post is part of the Knowledge Context Protocol series. Previous:
[The Front Door and the Filing Cabinet: A2A Agent Cards Meet KCP](./2026-03-08-a2a-cards-and-kcp.md).*
