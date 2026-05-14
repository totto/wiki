---
tags:
  - LinkedIn
  - Writing
date: 2026-03-01
---

# KCP Five-Repo Benchmark

*March 1, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7433824946952515584)*

**12 reactions · 0 comments**

---

Thirty-three tool calls to answer one question.

That was the baseline result when a Haiku agent was asked "how do I add RAG to my crew?" — no guidance, free to explore the CrewAI documentation. It traversed the entire docs tree before finding the answer.

With a knowledge.yaml manifest: 3 tool calls.

We applied KCP to five different repositories this week. Two smaller repos, then the three most-used AI agent frameworks: smolagents (HuggingFace), AutoGen (Microsoft), CrewAI. Same methodology throughout — same model, tool counts from the Anthropic API, not agent self-reports.

Results: 53%, 74%, 73%, 80%, 76% reduction in tool calls.

The pattern that emerged is the part worth paying attention to.

A flat 13-chapter documentation guide with a well-organised README produced 53%. The AI agent frameworks produced 73–80%.

The documentation repo is already navigable without a manifest. The answer is usually in one chapter, titles are descriptive, a baseline agent narrows in 3–4 reads. There's a lower ceiling on how much a manifest can help when the problem wasn't that hard to begin with.

The frameworks are different. Dozens of concept guides, design pattern galleries, API references, integration sections — spread across nested directories with no structural signal. A baseline agent explores, backtracks, reads things twice.

KCP adds the same thing in every case: the agent arrives knowing what the repo contains and which file answers which question. The worse the baseline navigation experience, the bigger the improvement.

We have open PRs on smolagents, AutoGen, and CrewAI. The manifests, TL;DR summary files, and full benchmark methodology are in each PR.

Spec/tools: https://lnkd.in/e8ZE4txV

---

← [All LinkedIn posts](index.md)
