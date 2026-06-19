---
description: "Git, CI, package managers, auth -- every developer stack layer was built for humans. Agents break those assumptions and need purpose-built alternatives."
date: 2026-03-16
categories:
  - AI-Augmented Development
  - Architecture
tags:
  - agents
  - kcp
  - agent-architecture
  - claude-code
  - sdd
  - knowledge-infrastructure
  - agentic-infrastructure
  - version-control
authors:
  - totto
  - claude
---

# The Agentic Stack: Every Layer Was Built for Humans

Something caught my attention this week. JJHub launched a version control platform built on Jujutsu instead of Git, designed specifically for agentic engineering teams. The premise: Git's data model breaks under the commit volume that agents produce.

That observation is narrowly about version control. But the pattern it reveals is much broader.

<!-- more -->

The entire software development stack was built for humans. Every layer optimised for human processing speed, human context windows, human coordination patterns. And now, layer by layer, agents are exposing each one as a bottleneck.

Most teams don't realise they're running agent-era workflows on human-era infrastructure.

![Human-Era Infrastructure, Agent-Era Workflows — a diagnostic report on rebuilding the software stack for autonomous systems, based on the architectural field notes of Thor Henning Hetland](/assets/images/blog/agentic-stack-slide-01.webp)

---

## The stack that's being rebuilt

![Git operates at human commit cadence — single-threaded, sequential. JJHub / Jujutsu operates at agent commit cadence — parallel, concurrent, high-frequency. The data model assumption is the bottleneck.](/assets/images/blog/agentic-stack-slide-02.webp)

| Layer | Human-era assumption | What agents need |
|-------|---------------------|-----------------|
| Version control | Git (human commit cadence) | Jujutsu / JJHub (high-frequency, concurrent) |
| Knowledge / context | README files, wikis, onboarding docs | Structured context protocols (KCP, etc.) |
| Tool integration | SDKs, manual documentation | Model Context Protocol (MCP) |
| Orchestration | Manual workflow coordination | CrewAI, autogen, smolagents |
| Identity / auth | OAuth, personal access tokens | SPIFFE, AgentControl |
| CI/CD feedback | Human code review | Agentic CI with automated judgment |

![Warning signs at every layer of the stack — each designed for human-speed operation, now exposed under agent load](/assets/images/blog/agentic-stack-slide-03.webp)

![Infrastructure Paradigm Matrix: six layers, human-era assumptions vs. what agents actually need](/assets/images/blog/agentic-stack-slide-04.webp)

No single layer is the bottleneck. They all are. And because they were all designed together for human-speed operation, upgrading one layer often just moves the constraint to the next.

![The Bottleneck Cascade: upgrading one layer moves the constraint to the next. No single layer is the bottleneck — the layers are co-dependent.](/assets/images/blog/agentic-stack-slide-05.webp)

---

## Consolidated fragility

Dion Wiggins used a phrase recently that stuck with me: "consolidated fragility." Systems that appear distributed but concentrate operational capacity at a few shared assumptions.

That describes the current agentic stack precisely. We distribute capability across agents, tools, and protocols, but concentrate critical assumptions in informal, undocumented places. Which agent has which permissions. What context exists where. Who controls the definitions. When those assumptions break — and they do — the failure mode is not a single component going down. It is the entire operational model becoming unreliable in ways that are hard to diagnose.

![The Wiggins Fragility Paradox: distributed capability over informal, undocumented assumptions. When the assumptions break, the entire operational model becomes unreliable.](/assets/images/blog/agentic-stack-slide-06.webp)

Steve Jones made a parallel observation about the JVM: abstractions work when the layer below has well-defined contracts. Most agentic systems today run on informal assumptions — that is not a virtual machine, that is a runtime with undocumented behaviour.

![JVM vs. current agent stack: the JVM succeeded because layers below had well-defined contracts. Agentic systems today are undocumented runtimes, not virtual machines.](/assets/images/blog/agentic-stack-slide-07.webp)

---

## The ingestion problem

André Lindenberg pointed out something that matches my own experience: agents don't fail at the action. They fail at what they knew before they acted.

This is the knowledge/context layer, and it is where I've spent most of my building time. When I started working on [KCP (Knowledge Context Protocol)](https://github.com/Cantara/knowledge-context-protocol) and [Synthesis](/blog/2026/02/25/ai-agents-without-knowledge-infrastructure-are-interns-with-amnesia/), it was because I kept running into the same problem: an agent with access to powerful tools but insufficient context makes confidently wrong decisions. The failure is upstream of the action, not at the point of execution.

![The Lindenberg Rule of Ingestion: agents don't fail at the action — they fail at what they knew before they acted. The failure is upstream.](/assets/images/blog/agentic-stack-slide-08.webp)

Structured, machine-readable context is not a nice-to-have for agentic workflows. It is load-bearing infrastructure. Without it, every other layer in the stack operates on incomplete information.

![KCP and Synthesis as load-bearing infrastructure: tools, orchestration, and agents rest on the context layer. Without it, every layer above operates on incomplete information.](/assets/images/blog/agentic-stack-slide-09.webp)

---

## Encoding judgment before the loop starts

Lasse Andresen at IndyKite raised a point that I think is underappreciated: judgment, aesthetics, and deliberative reasoning need to be encoded before agents act, not preserved as human competitive advantages.

This is uncomfortable for a lot of practitioners. The instinct is to keep humans in the loop for "the important decisions." But if the important decisions happen at agent speed and volume, the human loop becomes either a bottleneck or a rubber stamp. Neither is useful.

![The Andresen Imperative: procedural guardrails vs. structural guardrails. Procedural = human in the loop for every decision. Structural = judgment encoded into the context layer before the loop starts.](/assets/images/blog/agentic-stack-slide-10.webp)

The alternative is to encode the judgment — quality standards, architectural principles, compliance requirements, risk thresholds — into the context layer itself. Make the guardrails structural, not procedural. This is hard work. It requires making tacit knowledge explicit in ways that most organisations have never had to do.

But it is the only approach I've found that scales.

![Moving from procedural bottlenecks to structural context: if important decisions happen at agent volume, the human-in-the-loop becomes a bottleneck. The solution is encoding judgment into the context layer (KCP).](/assets/images/blog/agentic-stack-slide-11.webp)

---

## What I've learned building at one layer

I've spent the past year building tooling at the knowledge/context layer — KCP as an open specification, Synthesis as a CLI, kcp-commands and kcp-memory as utilities. All open source, all driven by specific problems I kept hitting in practice.

What building at one layer teaches you is how dependent it is on every other layer. Structured context is useless if the agent cannot authenticate to the system that serves it. High-frequency commits are unmanageable without automated review. Orchestration frameworks assume tool protocols that may not exist yet.

The layers are not independent. They are co-dependent. And the teams that figure this out earliest — that treat the agentic infrastructure stack as a coherent problem rather than six separate tool choices — will compound their advantage in ways that are difficult to catch up to.

![The Coherent Stack Advantage: the layers are not independent tool choices — they are a single co-dependent problem. Teams that treat it as a cohesive integration challenge will compound their advantage.](/assets/images/blog/agentic-stack-slide-13.webp)

---

## The question I keep coming back to

We are in a window where every layer is being rebuilt simultaneously, mostly by different teams who are not talking to each other. Version control people are solving version control. Context protocol people are solving context. Auth people are solving auth.

But the real constraint is the integration between layers. The informal assumptions. The undocumented contracts.

Who is working on the seams?

![The Real Constraint: Who is working on the seams? The critical failure points are the integration gaps between layers — the undocumented contracts and informal assumptions.](/assets/images/blog/agentic-stack-slide-12.webp)

---

*The visual companion to this post — a slide deck generated from these field notes — is available here: [Agentic Infrastructure: The Stack That's Being Rebuilt](/assets/presentations/agentic-stack-layer-by-layer.pdf)*
