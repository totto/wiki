---
date: 2026-02-22
categories:
  - AI-Augmented Development
tags:
  - security
  - entropy
  - synthesis
  - skill-driven-development
  - prompt-injection
  - ai-security
  - methodology
authors:
  - totto
---

# Software Entropy at Speed

Fast development with AI doesn't just generate features. It generates disorder at the same velocity.

That's the part nobody talks about. The productivity numbers are real — 53,000 lines, 42 features, five phases of code analysis built in a weekend sprint. But every line you write is also a line you haven't reviewed, a boundary you haven't enforced, a vector you haven't considered.

The entropy compounds with the output.

<!-- more -->

---

## What we built

Over a weekend we built CKG-5 — a code guardrails system for Synthesis, our knowledge infrastructure tool. Five analysis phases: dependency graphs, dead code detection, complexity metrics, coverage analysis, and full AI security scanning.

By Sunday evening: 53,000 lines of code, 3,932 tests passing.

Then we ran it on ourselves.

---

## What it found

In the code we had just written that same weekend:

- **23 prompt injection vectors** — places where user-controlled input could manipulate AI behaviour
- **4 RAG poisoning instances** — data paths where retrieved context could be tampered with
- **12 missing prompt boundaries** — points where context separation had been skipped

All written that weekend. All missed until the scanner looked.

Fixed before Monday.

While we were at it, the tool ran against a sibling codebase — Cantara's `reactiveservices` module, which we hadn't touched in months. One command, thirty seconds: Text4Shell, CVE-2022-42889, a remote code execution vulnerability in Apache Commons Text. Already there, already waiting.

---

## The gap traditional scanners can't see

SonarQube, Snyk, Checkmarx — these are mature tools with genuine track records. But they were designed for a world where the risks were SQL injection, XSS, insecure dependencies.

They have no concept of prompt injection. No concept of RAG poisoning. No concept of missing prompt boundaries. Those risks didn't exist when those tools were designed, and the attack surface they cover doesn't include the AI layer at all.

This is the new category. When you build systems that interact with language models — when user input reaches a prompt, when retrieved documents shape AI output, when context windows blur the boundary between data and instruction — you have a threat model that traditional scanners simply cannot reason about.

At high velocity, this gap widens fast.

---

## Two answers to the same problem

We've found two approaches, and they address different parts of the problem.

**Skill-Driven Development** operates upstream. When AI builds with structured, shared skills rather than pure generation speed, the output carries the understanding that went into the skill design. Prompt boundaries are defined in the skill, not improvised in the moment. The entropy is lower because the constraints are built in — not because the developer is being more careful, but because the methodology encodes care into the workflow.

SDD keeps entropy from forming.

**Synthesis** operates downstream. When entropy does slip through — and it will, even with good methodology — the scanner finds it. Prompt injection vectors that were missed in the speed of a weekend sprint. Legacy CVEs in codebases that haven't been touched in months. The things that accumulate silently until something asks the right question.

Synthesis finds what slips through anyway.

Neither works without the other. SDD without scanning is assuming the methodology is perfect. Scanning without SDD is managing technical debt that keeps regenerating at AI velocity.

---

## The self-referential proof

The following Monday morning, there was a follow-up worth noting.

Running the scanner continuously, it flagged a false positive in its own dependency analysis: the `DependencyInventoryExtractor` was reporting CVE hits on dependencies that appeared only in commented-out XML — not active code paths at all. The scanner was generating noise about its own archive comments.

Fixed with a targeted patch: strip XML comment blocks before parsing, so commented-out dependencies don't appear as active vulnerabilities.

The commit was co-authored by `Synthesis Security Scanner` and `Claude Code`.

A system built to find entropy in AI-generated code, finding entropy in itself, fixed with the same tools that found it — and committed with co-authorship that makes the lineage explicit. That's what this methodology looks like in practice, not in principle.

---

## The question worth asking

If you're building at this speed — if your team is shipping features at AI velocity — the question isn't whether entropy is accumulating. It is. The question is whether you have anything watching for it.

The weekend that surfaced 23 prompt injection vectors in code we'd written ourselves was uncomfortable. It was also exactly what the tool is for.

We built the detector. It found entropy in itself. We fixed it.

That's the loop. That's what managing entropy at speed actually requires.

→ Synthesis — the knowledge infrastructure tool described in this series.

---

*Originally published on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:share:7431352218844569600/), February 22, 2026.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
