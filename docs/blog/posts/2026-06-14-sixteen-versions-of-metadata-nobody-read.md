---
description: "63 regulatory manifests with full KCP v0.21 metadata -- hashes, signatures, temporal validity. Then a benchmark showed agents were not reading any of it."
date: 2026-06-14T14:00:00
draft: false
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - synthesis
  - kcp
  - temporal
  - verification
  - compound-developer
  - regulatory-compliance
  - practitioner-notes
authors:
  - totto
  - claude
image: assets/images/blog/sixteen-versions-metadata/slide-01.png
---

# Sixteen Versions of Metadata Nobody Read

*Practitioner notes on shipping a feature that was already a no-op, in two different ways.*

The Mynder regulatory knowledge base has 63 fragment manifests covering 101 units of EU regulation — GDPR, NIS2, the EU AI Act, DORA, Norwegian and Swedish data protection law. Every unit carries temporal validity (`valid_from`, `valid_until`, `superseded_by`), per-unit content hashes (sha256), `not_for` audience filtering, content structure declarations, and Ed25519 JWS signatures. All of it declared in KCP v0.21.

Synthesis — the workspace intelligence tool that indexes and searches this corpus — was reading it at v0.5 feature level.

Sixteen spec versions of metadata, sitting in the files, being dutifully indexed and completely ignored by the tool whose job was to understand them. The corpus was "searchable" but not "knowledge-aware." You could find GDPR articles by keyword. You could not ask what was in effect in 2022 and get a time-correct answer.

![Sixteen Versions of Metadata Nobody Read: a circuit board blueprint showing KCP v0.21, Temporal Validity, and Ed25519 JWS Signatures as three input connectors feeding into a central processor — but the connection is broken with an X. Diagnostic: the gap between organized data and intelligent infrastructure.](/assets/images/blog/sixteen-versions-metadata/slide-01.png)

<!-- more -->

---

## The gap

KCP moved fast this spring. Temporal validity landed in v0.19. Point-in-time queries in v0.20. Content hashes in v0.18. Audience filtering earlier still. Each release was designed, specified, implemented in the bridges, and validated against real manifests.

Synthesis consumed those manifests through its own indexer. The indexer read the YAML, extracted the text content, built a Lucene index, and served search results. It did this correctly. It also did this while ignoring every field added after v0.5 — temporal blocks, hash declarations, `not_for` rules, `content_structure`, discovery provenance. The metadata was parsed, stored in the database, and never consulted at query time.

![The Asymmetry Between Data and Engine: the Mynder Regulatory Corpus (KCP v0.21) — 63 fragment manifests, 101 units of EU regulation, valid_from/valid_until, sha256 content hashes, not_for audience filtering — feeds text extraction through to the Synthesis Indexer (v0.5 logic). Temporal metadata and hash metadata flow only to Database Storage, never to the indexer at query time. The metadata was parsed, stored, and entirely ignored at query time. The corpus was searchable, but not knowledge-aware.](/assets/images/blog/sixteen-versions-metadata/slide-02.png)

This is not an unusual failure mode. The ingestion path and the query path are different code, maintained at different cadences. The ingestion path gets updated when the schema changes — you have to, or parsing fails. The query path only gets updated when someone asks a question it can't answer. Nobody had asked the question yet.

![Why Ingestion Evolves While Queries Stagnate: two-column comparison. Ingestion path: a cycle of Schema Updates → Parse YAML → Update Ingestion Logic → Schema Updates (KCP v0.18–v0.21) — must update or parsing crashes. Query path: a linear pipeline of Extract Text → Build Lucene Index → Serve Results — the path only updates when a question fails; nobody had asked the question.](/assets/images/blog/sixteen-versions-metadata/slide-03.png)

So we asked it: `synthesis search "GDPR" --as-of 2017-01-01`.

![The Query That Broke the Illusion: terminal output shows `synthesis search GDPR --as-of 2017-01-01` returning `[System]: Returning 20 results for GDPR`. A timeline below marks 2017-01-01 (Query Date) on the left and 2018-05-25 (GDPR valid_from) on the right — every single result should have been excluded; the temporal data was in the database; the query never checked it.](/assets/images/blog/sixteen-versions-metadata/slide-04.png)

Twenty results. GDPR's `valid_from` is 2018-05-25. Every one of those results should have been excluded. The temporal metadata was in the database. The query never checked it.

---

## The fix, and why it was a fix twice

PR #345 (Synthesis 1.36.0) added the full v0.21 feature set to the query path: temporal filtering with `--as-of`, content hash verification, `not_for` audience exclusion, health signals for integrity problems (hash mismatches, expired units with no successor, dangling `superseded_by` references). A proper implementation, tested, merged.

Then we ran the same query again.

`synthesis search "GDPR" --as-of 2017-01-01` — twenty results.

![Fixing the Logic Did Not Fix the System: PR #345 (Synthesis 1.36.0) checked off --as-of temporal filtering, hash verification, and audience exclusion — a proper implementation, tested and merged. The execution: synthesis search GDPR --as-of 2017-01-01. The reality: 20 results. The logic was there. So why did the system still act like it wasn't?](/assets/images/blog/sixteen-versions-metadata/slide-05.png)

PR #346 (Synthesis 1.37.0) is the more interesting story. The temporal filtering code from #345 worked correctly — in the MCP handler. Two bugs made it a no-op in practice:

**Bug 1: Annotate but don't filter.** The MCP handler evaluated temporal validity and annotated each result with `active: false` for units outside the query window. It did not remove them. The code comment — I am not paraphrasing — said: *"not removed — the consumer decides."* The consumer, in this case, was a CLI that printed every result it received.

**Bug 2: The CLI never called the handler.** The `--as-of` flag was declared in picocli, captured from the command line, stored in a field, and never passed anywhere. The CLI search path bypasses the MCP handler entirely — it calls Lucene directly. The flag existed as a user-facing promise with no implementation behind it.

Two independent paths to the same no-op. The MCP handler had the logic but didn't act on it. The CLI had the flag but didn't use the logic. A feature that appeared to work from the code structure, that appeared to work from the CLI help text, and that did nothing.

![Two Independent Paths to a Total No-Op: flowchart showing --as-of 2017 branching into two paths. Left path (MCP Handler): evaluates temporal validity, tags active:false — code comment says "not removed — the consumer decides" — result reaches Filter but nothing is removed. Right path (The CLI): picocli captures the --as-of flag, then bypasses to Lucene Direct — flag captured, logic bypassed entirely. Both paths reach Final User Output unfiltered. The handler had the logic but didn't act on it. The CLI had the flag but didn't use the logic. A feature that appeared to work, but did nothing.](/assets/images/blog/sixteen-versions-metadata/slide-06.png)

---

## The actual fix

The fix is a SQL query: `getInactiveFilePaths()`. A UNION of two result sets — file paths from manifests whose temporal window excludes the query date, and content paths from individual units whose temporal window excludes it. Both the CLI and the MCP handler now call this before printing results. Inactive paths are excluded, not annotated.

![Rewiring the Circuit at the Root: getInactiveFilePaths() sits between both the MCP Handler and the CLI. It runs a UNION query combining Inactive Manifests and Inactive Units, producing a set of paths that are now strictly excluded at the SQL level — not politely annotated. The loop is closed.](/assets/images/blog/sixteen-versions-metadata/slide-07.png)

The validation:

```bash
synthesis search "GDPR" --as-of 2017-01-01
# 0 results. GDPR valid_from: 2018-05-25.

synthesis search "GDPR" --as-of 2019-01-01
# Full corpus. All units active.
```

---

## The EU AI Act test

The regulatory corpus already has unit-level temporal overrides for the EU AI Act's phased rollout — three chapters with different effective dates:

- Prohibited practices: 2025-02-02
- GPAI and governance: 2025-08-02
- High-risk obligations (Article 6+): 2026-08-02

![Validation — The EU AI Act Temporal Override: a Gantt-style timeline chart showing three EU AI Act chapters against 2025–2027. For a query date of 2025-10-01: Prohibited practices (valid from 2025-02-02) — Access Granted. GPAI and governance (valid from 2025-08-02) — Access Granted. High-risk obligations / Article 6+ (valid from 2026-08-02) — Excluded. Synthesis now understands that Article 6 requirements do not exist before August 2026.](/assets/images/blog/sixteen-versions-metadata/slide-08.png)

This means:

```bash
synthesis search "AI Act high-risk" --as-of 2025-07-01
# Returns only the prohibited-practices chapter.
# Article 6 requirements (valid_from: 2026-08-02) excluded.

synthesis search "AI Act high-risk" --as-of 2026-09-01
# Full corpus. All phases active.
```

Synthesis now understands that Article 6 high-risk classification requirements come into force in August 2026 and correctly excludes them from queries asking about earlier dates. This is not a demo — it is what makes the difference between "an AI searched some files" and "an AI answered from verified, time-correct regulatory knowledge."

---

## New health signals

1.36.0 also added four KCP integrity health checks:

![Upgrading to Observable Integrity: table of four KCP health signals. K001: Content hash mismatch — file changed without manifest update, or signed against different content. K002: Expired unit, no successor — valid_until is past, superseded_by is null (maintenance oversight). K003: Dangling reference — superseded_by ID missing from corpus. K004: Rumored verification — manifest claims verified but sha256 is absent or wrong. These signals transform a passive collection of files into active infrastructure with observable health.](/assets/images/blog/sixteen-versions-metadata/slide-09.png)

- **K001** — Content hash mismatch. The file on disk doesn't match the sha256 declared in the manifest. Either the file changed without updating the manifest, or the manifest was signed against different content.
- **K002** — Expired unit with no successor. `valid_until` is in the past and `superseded_by` is null. This is almost always a maintenance oversight — the replacement exists but wasn't linked.
- **K003** — Dangling `superseded_by`. The referenced unit ID doesn't exist in the corpus. Broken chain.
- **K004** — Rumored verification status. A manifest claims `verified` but the content hash is absent or doesn't match. The claim cannot be substantiated.

These surface in `synthesis health` and in the MCP `health` tool. They are the kind of signals that turn a knowledge base from "a collection of files" into "infrastructure with observable integrity."

---

## What this is actually about

The [Organized Truths](/blog/2026/06/11/organized-truths/) post described building a corpus where agents reason from source text instead of training-data vibes. That corpus was already built — 63 manifests, 101 units, full temporal metadata, signed.

But the tool reading it was still in vibes mode. It had the text. It had the metadata. It used the text and ignored the metadata. The organized truth was organized in the files and disorganized in the query engine.

![Moving from "Vibes" to Infrastructure: two-column comparison. Left — Training-Data Vibes: a tangled graph of raw text, metadata, declarations all disorganized; the AI searches raw text, metadata exists in files but is disorganized in the query engine, the tool ignores the data's declarations. Right — Organized Truths: a clean grid of verified source, corpus dictation, enforced rules, structured metadata; the AI reasons from verified source text, the corpus dictates when knowledge is valid, the engine enforces the corpus rules. The distinction is not the data itself. It is the tool honoring what the data declares.](/assets/images/blog/sixteen-versions-metadata/slide-10.png)

The sixteen-version gap is a reminder: infrastructure is not just the data and not just the tool. It is the tool *honoring* what the data declares. A temporal validity field that gets parsed but never evaluated is not infrastructure. It is a comment in YAML syntax.

With 1.37.0, the loop closes. The corpus declares when knowledge is valid. The tool respects that declaration at query time. An agent asking "what GDPR rules applied in 2022?" gets a time-correct answer — not because the agent understands temporal validity, but because the infrastructure does.

![The Loop Closes: a circuit board showing KCP unit status cards (K001:VALID, K002:ACTIVE, K003:RESOLVED, K004:VERIFIED, HASH:OK, TIME:VALID, SIGNATURE:OK) flowing into a central processor labeled ENGINE HONORS DECLARATIONS. An agent asking about 2022 gets a time-correct answer — not because the agent understands temporal validity, but because the infrastructure does. Based on KCP v0.21 | The Organized Truths Pattern | The Compound Developer.](/assets/images/blog/sixteen-versions-metadata/slide-11.png)

---

![Sixteen Versions of Metadata Nobody Read: infographic covering the 16-version gap between KCP v0.21 and Synthesis v0.5 feature level, the two independent no-op bugs (annotate-but-don't-filter; CLI flag never consumed), the getInactiveFilePaths() UNION SQL fix, the EU AI Act phased rollout test cases, and the four KCP health signals K001–K004.](/assets/images/blog/sixteen-versions-metadata-infographic.png)

*Synthesis 1.36.0 and 1.37.0 ship KCP v0.21 support and the temporal filtering fix. The KCP temporal model is described in [Stale Knowledge Is Worse Than No Knowledge](/blog/2026/06/12/kcp-0.19-0.20-temporal/). The corpus design pattern is in [Organized Truths](/blog/2026/06/11/organized-truths/). The compound-developer argument for why this maintenance work is the real work: [The Compound Developer](/blog/2026/06/02/the-compound-developer/).*

There is also a [slide deck version of this post (PDF)](/assets/Closing_the_Circuit.pdf) if you want to walk a team through the two-bug story.
