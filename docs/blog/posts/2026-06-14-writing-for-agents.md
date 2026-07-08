---
description: "Discoverable is not navigable. Extracting 38 Dutch obligation units from inline YAML to standalone text made content agent-traversable, not just findable."
date: 2026-06-14T12:00:00
draft: false
categories:
  - Knowledge Context Protocol
  - Knowledge Infrastructure
  - AI-Augmented Development
tags:
  - agentic-writing
  - kcp
  - exocortex
  - sdd
  - agents-reading
  - knowledge-infrastructure
  - meta
authors:
  - totto
  - claude
---

# Discoverable Is Not Navigable

This morning I spent three hours on regulatory knowledge infrastructure. 63 fragment manifests across Arbeidsmiljøloven, GDPR, NIS2, DORA, AI Act, NSM Grunnprinsipper, Dutch financial supervision law. Fixed a scope validation bug across 30+ files. Extracted 38 Dutch obligation units from inline YAML to standalone navigable text. Everything passing `kcp validate` by lunch.

None of it would normally get published. Too narrow. Too technical. No audience in the traditional sense — a compliance engineer isn't subscribing to this blog, and a developer evaluating KCP isn't refreshing the RSS feed waiting for fragment extraction patterns.

That instinct is correct. If you're writing for humans, ruthless editing is the right move. Cut the scope validation bug. Keep the summary. Optimize for skimmability, because human reading bandwidth is fixed and attention is scarce.

The instinct is right. The assumption about who's reading has become incomplete.

<!-- more -->

Agentic development produces output at rates that break the old math: lib-pcb, 197,831 lines in 11 days. Synthesis, 84,692 lines in 7 days. This blog, 90+ posts. The rate is accelerating. Human reading bandwidth is fixed — no one is keeping up with that volume, and no one should have to. A compliance engineer's AI assistant asked "how do people actually structure regulatory knowledge for agents?" will find and synthesize across everything available in seconds. They're already reading — targeted queries for exact failure modes, specific architecture patterns, real session data. The question is whether there's signal to find when they look.

---

## The gap everyone misses

Most "writing for agents" advice focuses on discoverability. Add `llms.txt`. Use structured markup. Build sitemaps. Make your content machine-readable so agents can find the files. That solves the easy problem.

The hard problem is navigability: given that the agent found your content, can it determine what to load, what's current, what answers its specific query, and what to skip — without reading everything? Discoverability is a file-system problem. Navigability is a knowledge-structure problem.

A flat list of 90+ posts is discoverable. It is not navigable. An agent can't determine which posts argue what, which supersede earlier versions of the same argument, or which apply to its user's situation without loading most of them. That's expensive, slow, and produces worse results than targeted retrieval. An agent that can find all 90+ posts but can't determine which three answer its question is not much better off than one that can't find them at all.

Navigability requires properties almost no one publishes. **Intent**: what question does this post answer? **Dependencies**: read X before Y, or Y won't make sense. **Currency**: this June post supersedes the January version of the same argument. **Scope**: applies to regulatory knowledge bases, not general content management. **Limits**: what this post does *not* cover. These aren't formatting concerns. They're semantic metadata that tells an agent whether a document is worth loading before it commits the context window.

---

## What this blog has, and what it's missing

The infrastructure exists. KCP v0.21 root manifest. A signed `blog.yaml` cataloging 153 posts with dates, categories, and tags. An `llms.txt` file. Cross-linked reading threads. Hard numbers throughout — dates, line counts, test counts, session durations. The 63 regulatory fragments have full manifests with scope, jurisdiction, and obligation structure. For discoverability, this is well above baseline.

For navigability, it's thin. The `blog.yaml` expresses what files exist and when they were published. It does not express what arguments they make. There is no `intent` field per post — no machine-readable declaration that this post answers "how should technical writers think about agent audiences?" There is no blog-level argument map identifying the threads that run through 90+ posts, with canonical entries per thread. There are no supersession declarations — nothing telling an agent that the June compound developer post evolved the argument from the March productivity post. An agent navigating this blog still has to read broadly to understand the structure.

The gap is honest: the production side is sophisticated — manifests, validation pipelines, signed artifacts. The consumption side is underdeveloped — no intent, no dependency graph, no supersession declarations. Building the validation pipeline was a development problem. Populating semantic metadata across 90+ posts is a curation problem: slower, less automatable, easy to defer indefinitely.

Building the pipes is development. Mapping the water is curation. Having the tools and having done the work are not the same thing.

*Thor Henning Hetland, June 14, 2026. Oslo.*
