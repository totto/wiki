---
date: 2026-03-02
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - knowledge-infrastructure
  - standards
  - synthesis
authors:
  - totto
  - claude
---

# KCP v0.1 to v0.5: How a Knowledge Standard Grows

KCP (Knowledge Context Protocol) has gone from a draft proposal to a v0.5 spec in one
week. This post walks through what each version added, why those decisions were
made, and where the spec is heading next.

The short version: every release promotes optional fields from community RFCs into the
normative core. The spec is a strict superset at each step — a manifest written for v0.1
is still valid under v0.5.

![The Evolution of KCP: From Minimal Draft to AI Knowledge Standard — v0.1 through v0.5 and Synthesis v1.20.0 implementation overview](/assets/images/blog/kcp-version-history-evolution.png)

<!-- more -->

---

## Why it matters that a spec evolves carefully

Most YAML config formats grow by accumulation — fields get added when someone needs them,
in whatever shape seemed natural at the time. KCP takes a different approach. Fields start
as RFC proposals, go through discussion, get validated in real-world benchmarks, and are
only promoted to the core spec when the pattern is proven stable.

The result: each version of KCP adds something you have already been using in practice.
There are no surprise breaking changes, no fields that were never adopted, no spec debt.

![Growth by accumulation vs strict superset model — formalise practice rather than leading it](/assets/images/blog/kcp-history-slide-formalise-practice.png)

---

## v0.1 — The minimal contract

The original spec defined five required fields per unit:

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier within the manifest |
| `path` | File or directory the unit points to |
| `intent` | What this unit is for (one sentence) |
| `scope` | What topics it covers |
| `audience` | Who should read it |

![v0.1 — The Minimal Contract: Which files matter, and why?](/assets/images/blog/kcp-history-slide-v01-minimal-contract.png)

That is the entire core. A valid v0.1 manifest is just a list of units with those five
fields and a `kcp_version: "0.1"` header.

The design was intentional minimalism. The question KCP answers is: *which files matter,
and why*. You can answer that with five fields per file. Everything else is optional
enrichment.

---

## v0.2 — Schema correctness

v0.2 shipped the same day as v0.3 — it was not a feature release. It fixed six
spec-alignment issues found during real-world adoption:

- `kind` was in the schema but not the spec (moved to RFC-0001 as an explicit extension)
- Relationship `additionalProperties` was too strict — unknown fields broke forward compat
- Date fields needed quoting guidance (YAML silently coerces unquoted dates to integers)

![v0.2 — Schema Correctness over Features: zero new fields, validate the schema against real manifests before locking in the next version](/assets/images/blog/kcp-history-slide-v02-schema-correctness.png)

No new fields. No new capabilities. Just a cleaner contract that held up when people
started writing manifests against it.

The lesson: write the schema, validate it against real manifests, fix the gaps before
locking in the next version.

---

## v0.3 — Descriptive metadata

v0.3 was the first real feature release. Seven new fields promoted from RFC-0001 and
GitHub issues #7, #8, #10, #13, #14, and #16:

**Unit-level fields:**

| Field | Example values | Purpose |
|-------|---------------|---------|
| `kind` | `guide`, `reference`, `policy`, `schema` | What type of content this is |
| `format` | `markdown`, `yaml`, `java`, `pdf` | File format for parsers and renderers |
| `content_type` | `text/markdown`, `application/pdf` | MIME type |
| `update_frequency` | `daily`, `weekly`, `on-release` | How often this unit changes |

**Root-level inheritable fields:**

| Field | Purpose |
|-------|---------|
| `language` | Primary language of the content (`en`, `nb`, etc.) |
| `license` | License that governs reuse |
| `indexing` | Hints for search and indexing tools |

![v0.3 — Descriptive Metadata: "Routing without reading." Unit-level and root-level fields, static YAML philosophy](/assets/images/blog/kcp-history-slide-v03-descriptive-metadata.png)

The promotion criterion for each field was the same: does it fit the static YAML manifest
philosophy? `kind` does — it is a stable declaration, not a computed property. Something
like "last verified by an agent" does not — it changes with each run and belongs in a
separate system.

Conformance levels were formally defined in v0.3:
- **Level 1:** The five required fields. Any valid manifest.
- **Level 2:** Adds `kind`, `format`, `language`. Enough for an AI agent to make routing
  decisions without reading the files.
- **Level 3:** Adds `license`, `update_frequency`, `indexing`. Enough for automated
  workflows that act on content based on its freshness and legal status.

![v0.3 Conformance Levels: Level 1 (Base), Level 2 (Routing), Level 3 (Governance)](/assets/images/blog/kcp-history-slide-v03-conformance-levels.png)

---

## v0.4 — The hints block

Every manifest written during the benchmark work used an undocumented pattern: a `hints`
block that told agents *how* to load a unit, not just *what* it contained. The `hints`
fields were being used before the spec formalised them.

RFC-0006 codified this pattern. v0.4 promoted it to the normative core on March 1.

The `hints` block adds per-unit loading instructions:

```yaml
units:
  - id: architecture-overview
    path: docs/ARCHITECTURE.md
    intent: System design and component relationships
    scope: architecture, components, dependencies
    audience: developers
    hints:
      load_strategy: always    # load unconditionally
      priority: critical       # before any query is answered
      density: high            # dense reference material, read carefully
      summary_available: true
      summary_unit: architecture-tldr
```

![v0.4 — The Hints Block: shifting from WHAT is in a file to HOW an agent should read it](/assets/images/blog/kcp-history-slide-v04-hints-block.png)

Root-level hints set defaults that units can override:

```yaml
hints:
  load_strategy: on_demand
  priority: normal
```

The key insight behind `hints`: KCP was already reducing tool calls by giving agents a
map. Hints let you give agents a *reading strategy* on top of the map. The benchmarks
showed 73–80% reductions with hints in place; we expect the numbers would be lower without
them.

![73–80% reduction in agent tool calls — proven in real-world benchmarks](/assets/images/blog/kcp-history-slide-v04-73-80-reduction.png)

---

## v0.5 — Trust and access metadata

v0.5 promoted five fields from four separate RFCs:

| Field | From | Values | Purpose |
|-------|------|--------|---------|
| `access` | RFC-0002 | `public`, `authenticated`, `restricted` | Who can read this unit |
| `sensitivity` | RFC-0004 | `public`, `internal`, `confidential`, `restricted` | Data classification |
| `deprecated` | — | boolean | Flag stale units; validator warns if no `supersedes` counterpart |
| `payment` | RFC-0005 | `free`, `metered`, `subscription` | Monetisation tier |
| `trust.provenance` | RFC-0004 | `publisher`, `publisher_url`, `contact` | Who published this manifest |

![v0.5 — Trust, Access, and Intent: "Advisory declarations, not enforcement mechanisms"](/assets/images/blog/kcp-history-slide-v05-trust-access.png)

These fields share a design principle: they are advisory declarations, not enforcement
mechanisms. KCP does not implement access control — it declares intent. An agent that
reads a unit marked `sensitivity: confidential` and sends it somewhere public is
misbehaving, but KCP has no runtime authority to stop it. That is explicitly out of scope.
Full auth, delegation, compliance, and x402 payment integration remain in their respective
RFCs pending further review.

v0.5 also adds `subManifests` — a list of child manifests that extend a root manifest.
This makes KCP composable across monorepos and federated repositories without requiring a
single authoritative manifest that needs to know about every file.

![v0.5 — Scale & Composability: subManifests allow KCP to scale across massive monorepos and federated repositories](/assets/images/blog/kcp-history-slide-v05-submanifests.png)

---

## Synthesis v1.20.0 — First full v0.5 implementation

Four phases, four PRs, merged March 1, 2026.

| Phase | What it does |
|-------|-------------|
| **Detection** | `YamlAnalyzer` identifies `knowledge.yaml` as KCP when: filename matches, `units` is a list, `project` or `id` key exists. Extracts all unit and relationship fields. |
| **Persistence** | V17 Flyway migration adds `kcp_manifests`, `kcp_units`, `kcp_relationships` tables. `KcpRepository` provides idempotent upsert/delete. Auto-triggers on scan and maintain. |
| **Export** | `synthesis export --format kcp` generates a v0.5-conformant `knowledge.yaml` from the Lucene index. Infers `format`, `kind`, `triggers`, `validated`, `updated` per unit. |
| **Knowledge graph** | `synthesis kg` surfaces KCP units as first-class nodes. ASCII groups by project. Mermaid adds pill nodes and `kcp-unit` edges. JSON adds `kcpUnits` and `kcpRelationships` arrays. |

![Real-World Proof: Synthesis v1.20.0 — the first tool that treats KCP as both input (index/query) and output (generated from an indexed workspace)](/assets/images/blog/kcp-history-slide-synthesis-proof.png)

The implementation is the first tool that treats `knowledge.yaml` as both input (index
and query it) and output (generate it from an indexed workspace). A workspace without a
KCP manifest can generate one. A workspace that already has one gets it indexed and
surfaced in the knowledge graph alongside the directories and source files it describes.

![The Synthesis v1.20.0 Pipeline: Detection → Persistence → Export → Knowledge Graph](/assets/images/blog/kcp-history-slide-synthesis-pipeline.png)

Over 40 new KCP-specific tests across four test classes. Zero regressions.
`synthesis kg --format json` now returns `kcpUnits` and `kcpRelationships` as top-level
arrays in every workspace that has a manifest.

---

## What is coming next

**AAIF submission.** KCP has been submitted to the [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) (Linux Foundation) for consideration as a neutral-governance project. The AAIF is the home of MCP and AGENTS.md — 146 member organizations including AWS, Anthropic, Google, Microsoft, and OpenAI. Acceptance would place KCP alongside the two other standards that describe how agents interact with tools (MCP) and codebases (AGENTS.md), completing the picture with how agents interact with knowledge.

**IANA well-known URI registration.** The `/.well-known/kcp.json` discovery endpoint
(§1.4) is documented and a formal IANA registration document is ready for submission to
`wellknown-uri-review@ietf.org`. This makes KCP discoverable via standard HTTP without
any prior knowledge of the repository structure — the same pattern used by OAuth
(`/.well-known/openid-configuration`) and security policies (`/.well-known/security.txt`).

![What's Next: Standardizing Discovery — /.well-known/kcp.json IANA registration](/assets/images/blog/kcp-history-slide-whats-next-discovery.png)

**opencode-kcp-plugin published.** The first KCP plugin for a major AI coding tool is live on
npm: [`opencode-kcp-plugin`](https://www.npmjs.com/package/opencode-kcp-plugin). It works with
[OpenCode](https://github.com/anomalyco/opencode) (114K stars), injecting the `knowledge.yaml`
knowledge map into the system prompt and annotating glob/grep results with KCP intent strings.
Install: `npm install opencode-kcp-plugin`. A PR adding `knowledge.yaml` to the OpenCode repo
itself is also [open for review](https://github.com/anomalyco/opencode/pull/15839).

**Framework PRs under review.** Four AI agent frameworks now have open PRs adding
`knowledge.yaml` manifests. If you maintain one of these repositories, or you use them
and want KCP adopted upstream, this is the moment to comment:

- [anomalyco/opencode #15839](https://github.com/anomalyco/opencode/pull/15839) — 73–80% reduction (+ plugin on npm)
- [microsoft/autogen #7329](https://github.com/microsoft/autogen/pull/7329) — 80% reduction
- [huggingface/smolagents #2026](https://github.com/huggingface/smolagents/pull/2026) — 73% reduction
- [crewAIInc/crewAI #4658](https://github.com/crewAIInc/crewAI/pull/4658) — 76% reduction

![Expanding the Ecosystem — framework PRs under review: AutoGen 80%, CrewAI 76%, smolagents 73%](/assets/images/blog/kcp-history-slide-ecosystem-prs.png)

**Cross-manifest relationships.** The current spec defines relationships within a single
manifest. Cross-manifest relationships — a unit in one repo depending on a unit in another
— are the next design challenge. `subManifests` lays the groundwork, but the relationship
semantics need to be specified carefully.

---

## The design principle that held across all five versions

Each release adds optional fields that were already in use. The spec formalises practice
rather than leading it.

This is what makes the strict-superset constraint worthwhile. A manifest you write today
for v0.5 does not break when v0.6 ships. A manifest written in February for v0.1 is still
valid. The cost of adoption does not compound with each version.

![The Cost of Adoption Does Not Compound — a manifest written in February for v0.1 remains 100% valid today](/assets/images/blog/kcp-history-slide-adoption-cost.png)

If you have not added a `knowledge.yaml` to your project yet, v0.5 is a good starting
point. The [five-minute adoption guide](./2026-02-28-kcp-adoption-guide.md) still applies —
start with the five required fields and add the rest when you need them.
