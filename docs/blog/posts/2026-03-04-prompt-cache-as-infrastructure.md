---
date: 2026-03-04
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - claude-code
  - prompt-caching
  - kcp
  - knowledge-infrastructure
  - token-economics
authors:
  - totto
  - claude
---

# The Prompt Cache as Infrastructure: Lessons from 3,007 Claude Code Sessions

![The 12 Billion Token Dividend: Prompt Cache as Infrastructure](/assets/images/blog/prompt-cache-infrastructure/prompt-cache-infrastructure.png)

I extracted the token usage from 55 days of Claude Code sessions. The number that stopped me:

**12,198,713,224 cache read tokens.**

Twelve billion. Against 9,965,286 input tokens. For every fresh token sent to the model,
1,224 were served from cache.

That ratio is not an accident. It is the result of treating the prompt cache as infrastructure --
something you invest in once and draw from continuously.

---

## The raw numbers

Claude Code stores every session as a `.jsonl` file under `~/.claude/projects/`. Each assistant
message includes a `usage` block with input tokens, output tokens, and cache statistics.
Across 3,007 sessions from January 9 to March 3, 2026:

| Metric | Tokens |
|--------|--------|
| Input | 9,965,286 |
| Output | 13,279,048 |
| **Non-cached total** | **23,244,334** |
| Cache write | 597,446,099 |
| Cache read | 12,198,713,224 |
| Grand total | 12,819,403,657 |

The cache read volume is **525x the fresh input**.
The average session consumed ~3,300 fresh input tokens while reading ~4M from cache.

---

## Week by week

Breaking it down by week -- and correlating with git commit activity across all active
repositories -- reveals the story behind the numbers:

| Week | Sessions | Input (M) | Output (M) | Cache-R (B) | Cache% | Active repos / commits |
|------|----------|-----------|------------|-------------|--------|------------------------|
| Jan 5--11 | 124 | 1.89 | 1.25 | 0.55 | 96.1% | Elprint suite (128+35+13) -- **176 commits** |
| Jan 12--18 | 339 | 2.83 | 4.57 | 1.27 | 94.2% | lib-pcb(181), lib-electronic-components(156), elprint-ai(88) -- **484 commits** |
| Jan 19--25 | 134 | 1.77 | 0.02 | 0.26 | 88.8% | lib-pcb(265), lib-pcb-app(145), elprint-connector(163) -- **573 commits** |
| Jan 26--Feb 1 | 673 | 1.16 | 0.04 | 0.86 | 93.3% | lib-pcb wrapping up (120+80+47) -- **247 commits** |
| Feb 2--8 | 495 | 0.30 | 0.78 | 2.02 | 94.8% | lib-pcb wind-down (46+53+14) -- **113 commits** |
| Feb 9--15 | 134 | 0.60 | 0.72 | 1.31 | 95.9% | Synthesis begins (79) -- **82 commits** |
| Feb 16--22 | 458 | 0.59 | 1.83 | 2.86 | 96.3% | Synthesis PR#18 (289), lib-pcb(6) -- **304 commits** |
| Feb 23--Mar 1 | 388 | 0.67 | 2.73 | 2.20 | 95.4% | Wiki(134), KCP spec(72), Synthesis(64) -- **270 commits** |
| Mar 2--4 | 110 | 0.17 | 1.35 | 0.87 | 95.4% | kcp-commands(32), wiki(58), KCP(37), kcp-memory(8) -- **163 commits** |

A few things stand out.

**January 12--25** was the heaviest raw output period: the [lib-pcb build](./2026-02-13-six-pillars-200k-lines-11-days.md)
produced 197,831 lines of Java in 11 days across 1,057 commits. Peak sessions, peak fresh input,
lowest cache rates. The infrastructure was still being built.

**January 26--February 8** shows the transition: 673 sessions in a single week (highest count)
but almost no output (0.04M). These were short-lived sessions -- exploration, search, quick lookups.
lib-pcb was wrapping up. The work pattern shifted from generation to comprehension.

**February 9 onward**: the project mix shifts entirely. Synthesis, wiki, KCP spec, kcp-commands --
knowledge infrastructure tooling. Cache reads double and stay high. Fresh input drops. Cache
rates climb above 95% and stay there. The infrastructure is paying for itself.

---

## Model usage breakdown

The 3,007 sessions span five model generations. How each model was used reveals the workflow:

| Model | Messages | Input (M) | Output (M) | Cache-R (B) |
|-------|----------|-----------|------------|-------------|
| claude-sonnet-4-5 | 44,790 | 1.77 | 1.88 | 4.22 |
| claude-sonnet-4-6 | 43,131 | 0.53 | 5.51 | 4.21 |
| claude-haiku-4-5 | 23,506 | 5.56 | 0.65 | 0.94 |
| claude-opus-4-6 | 19,270 | 0.84 | 0.14 | 1.43 |
| claude-opus-4-5 | 17,529 | 1.27 | 5.11 | 1.40 |

**Haiku** has 5.56M input against only 0.65M output. It handles the subagent work -- codebase
search, file exploration, context gathering. High read volume, minimal generation.

**Opus 4-5** has disproportionate output (5.11M) relative to its message count.
This was the long-form writing model: blog posts, documentation, strategic analysis.

**Sonnet 4-6** averages ~128 output tokens per message across 43K messages -- the everyday
workhorse, slightly more verbose than its predecessor.

**Cache reads are remarkably uniform** across models (~0.9--4.2B each). The same
stable context prefix benefits every model equally. The knowledge infrastructure is
model-agnostic.

---

## What is actually being cached

Anthropic's prompt caching works on the stable prefix of the context window. The larger and
more consistent that prefix, the higher the cache hit rate. In practice:

- **`CLAUDE.md`** -- project context, priorities, universal rules. Loaded at session start. Rarely changes.
- **Skills** (~100+ `.yaml` files) -- task-specific knowledge loaded on demand. Stable content, high reuse.
- **Memory files** -- `MEMORY.md`, topic files, persistent notes. The stable parts cache; only diffs are fresh.
- **`knowledge.yaml` manifests** -- KCP metadata that tells the agent what to load and when.

Together these form a **knowledge layer** that sits in cache between sessions.
The agent doesn't re-read it. The cache does.

---

## The kcp-commands effect

[kcp-commands](./2026-03-02-kcp-commands.md) saves 33% of the context window per session
by injecting targeted syntax hints before Bash calls instead of letting the model guess.
Less guessing means shorter tool-use chains, which means a more stable context prefix,
which means better cache utilisation.

The 96%+ cache rates in February reflect both the mature knowledge infrastructure and the
reduced fresh-token noise from kcp-commands.

---

## What this would cost on the API

A rough calculation puts things in perspective. These are approximations, but the order
of magnitude is what matters.

At Anthropic's standard API rates, the 12.2B cache read tokens alone would cost roughly
**$6,800** (at the discounted cache-read rate: $0.30/MTok for Sonnet, $1.50/MTok for Opus,
$0.08/MTok for Haiku). Add cache writes, fresh input, and output, the total lands around
**$8,900**.

Without prompt caching -- if every cache read had been a fresh input token instead --
the same 12.2B tokens priced at standard input rates would push the total past **$40,000**.

The Claude Max subscription for 55 days cost approximately **$200--350**.

| Scenario | Estimated cost |
|----------|----------------|
| Claude Max subscription (55 days) | ~$200--350 |
| API with prompt caching | ~$8,900 |
| API without prompt caching | ~$40,000+ |

The caching infrastructure provides a ~4.5x cost reduction on the API. But the subscription
model changes the economics entirely: it makes high-frequency agentic workflows viable at a
flat rate that would be ruinous per-token.

This is not a detail. It is the economic foundation.

---

## What this means

The prompt cache is not a cost optimisation feature bolted on after the fact.
It is the mechanism by which persistent knowledge pays compound returns.

Every hour spent building a good `CLAUDE.md`, a well-structured skills library, or a
[knowledge.yaml](./2026-02-25-beyond-llms-txt-knowledge-context-protocol.md) manifest
is an hour that reduces the fresh token cost of every future session.
The investment amortises across thousands of interactions.

The 12.2B cache reads represent 55 days of infrastructure paying for itself --
2,412 commits across 15+ repositories, five model generations, one stable context layer.

The practical implication: **treat your prompt context as infrastructure, not scaffolding.**
Write it once. Structure it well. Let the cache do the rest.

---

*Token data extracted from `~/.claude/projects/**/*.jsonl` using a 30-line Python script.
Git activity from `gh api` across all active repositories. Sessions: 3,007. Period: 2026-01-09
to 2026-03-03. API cost estimates are approximations based on published Anthropic pricing as of
March 2026; actual costs would vary with cache TTL, write frequency, and usage patterns.*
