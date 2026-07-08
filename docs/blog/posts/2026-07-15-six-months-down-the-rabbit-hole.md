---
description: "172 days, 6,163 commits, 137 blog posts, 36 new repos, one protocol. A six-month retrospective on explorative development — compiled by the agent from its own memory."
date: 2026-07-15T09:00:00
draft: false
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - explorative-development
  - skill-driven-development
  - kcp
  - exocortex
  - retrospective
  - continuous-learning
  - ai-agents
authors:
  - totto
  - claude
image: assets/images/six-months-01-title.webp
---

# Six Months Down the Rabbit Hole

On January 15th I published a blog post about [parsing semiconductor part numbers](2026-01-15-mpn-parsing-complexity.md). I thought I was building a PCB component library. I was wrong about what I was building in the most productive way I have ever been wrong about anything.

Six months later there is a knowledge protocol with nineteen releases, a deterministic reference agent, an episodic memory system that indexed this very retrospective's sources, five toolchain products, thirty-one new repositories, and a family vacation that an AI agent can defend to a regulator.

It is time to stop, sit by the fjord, and look back down the hole.

<!-- more -->

![Six Months Down the Rabbit Hole — a retrospective on explorative development, knowledge infrastructure, and the emergent AI stack. A graph-paper title card with an isometric blueprint: a rabbit hole descending into the page, its walls revealed as engineered layers under construction.](../../assets/images/six-months-01-title.webp)

---

## The receipts

I have spent six months arguing that agents should carry written, reproducible reasons for everything they do. A retrospective written by that person had better not run on vibes and nostalgia.

So the numbers below were harvested deterministically: a shell script over the git logs of every repository on this machine, a frontmatter parser over the blog archive, and a query against the agent's own episodic memory. No estimates. No "roughly". The harvest scripts sit next to the draft.

| What | Count |
|---|---|
| Days | 172 (2026-01-15 → 2026-07-05 at harvest time) |
| Commits (deduplicated, author-filtered) | **6,163** — about 36 per day, every day, including the days I thought I was resting |
| Repositories touched | 175 checkouts |
| New repositories created | **31** (36 checkouts, deduplicated by root commit — even the repo count needed an audit) |
| Blog posts | **137** |
| LinkedIn posts | 115 |
| Claude Code sessions | **3,925** |
| Conversation turns | **485,252** |
| Tool calls | **256,839** |
| Skills built | ~590, across 29 domains — zero existed in January |
| KCP spec releases | 19 tagged (v0.7.0 → v0.25.1) |

One number deserves its asterisk: the line-count delta is +7.2M/−2.1M even after excluding the wiki's generated content and duplicate checkouts, and it still includes lockfiles, generated data and synced artifacts. I do not believe raw line counts, and neither should you. The commit cadence and the shipped-things list are the honest signal; the line count is weather.

And one number deserves a footnote of a different kind: the memory's oldest indexed session is **January 9th** — six days *before* the first blog post. The rabbit hole had a vestibule. I spent a week falling before I noticed I was falling.

![The Telemetry: 172 days of explorative development. A dashboard of six instrument panels: 172 days (2026-01-15 → 2026-07-05) · 6,163 commits, deduplicated, about 36 per day · 137 blog posts and 115 LinkedIn posts · 3,925 sessions and 256,839 tool calls · 31 new repos and 590 skills built · and a red diagnostic warning: reject raw line counts (+7.2M/−2.1M) as weather; commit cadence and shipped artifacts are the honest signals. The footnote reads: The Vestibule — the oldest indexed session is Jan 9th. I spent a week falling before I noticed I was falling.](../../assets/images/six-months-03-telemetry.webp)

---

## Seven chapters, one shape

Looking back at the timeline, the six months organize themselves into seven arcs. I did not plan a single one of them. Each arc ended by exposing the problem that became the next arc. That shape — *each layer's missing piece only becomes visible after the previous layer ships* — turns out to be the whole story.

### 1. The rabbit hole opens (January)

A weekend experiment with a PCB library became [months of estimated work collapsing into days](2026-01-21-months-to-days.md). The first seventeen days produced 1,141 commits — the densest stretch of the entire six months, before any infrastructure existed to make it efficient.

January also set the tone that saved everything that followed: [test discipline forced from 25% to 93%](2026-01-23-ai-testing-discipline.md), and the early realization that [when iteration cost collapses, the constraint moves](2026-01-24-the-cost-of-iteration-collapsed.md). It moves to verification. It moves to comprehension. It moves to you.

![Layers 1 and 2: speed demands Synthesis. A warning-arrow diagram from January: Speed — 1,141 commits in 17 days, 200,000 lines built in 11 days, test discipline forced from 25% to 93% — to February: Comprehension — Synthesis tools born out of genuine alarm, an XXE vulnerability found in a decade-old production SSO system in exactly 31 seconds. The banner below: THE PIVOT — agents need semantic maps (the Knowledge Context Protocol), not just tables of contents.](../../assets/images/six-months-07-speed-demands-synthesis.webp)

### 2. The comprehension bottleneck (February)

February was the writing explosion — 45 posts in 28 days, including one absurd Saturday with ten. The reason for the volume was genuine alarm: we had [built 200,000 lines of tested Java in 11 days](2026-02-13-six-pillars-200k-lines-11-days.md) and I could feel that *creating had become easy while understanding had become the constraint*. That's [the comprehension bottleneck](2026-02-05-the-comprehension-bottleneck.md), and it is still the most important thing I learned all spring.

Synthesis was born that month to attack it, and proved itself immediately by [finding an XXE vulnerability in a production SSO system in 31 seconds](2026-02-03-whydah-xxe-vulnerability.md) — a system I have operated for a decade.

![When creation becomes cheap, comprehension becomes the bottleneck. A load-bearing diagram: a heavy beam labeled Iteration Cost Collapses (AI Generation) pressing three red arrows down onto three straining brick walls labeled Verification, Comprehension, and The Human. The caption: in February, 200,000 lines of tested Java were built in 11 days — creating had become trivially easy, but understanding had become the hard limit. Generating volume at speed necessitates maps, not just tables of contents.](../../assets/images/six-months-04-comprehension-bottleneck.webp)

Then, in the last week of February, the llms.txt moment: the realization that [agents need maps, not tables of contents](2026-02-25-beyond-llms-txt-knowledge-context-protocol.md). The Knowledge Context Protocol repository was created on February 25th. This wiki itself was born two days earlier. The era's two most durable artifacts arrived in the same 48 hours, and I noticed neither at the time.

### 3. The toolchain month (March)

March was peak everything: 1,195 commits, 56 LinkedIn posts, seven KCP releases, and a burst of new tools — kcp-commands, kcp-memory, kcp-triage, kcp-dashboard, Mimir and Mycelium — plus plugins reaching [beyond Claude Code to OpenCode and Copilot](2026-03-31-kcp-ecosystem-overview.md).

March is also when the theory caught up with the practice: [Peter Naur was right in 1985](2026-03-25-naur-was-right.md). Programming is theory building, the theory lives in heads, and when the "head" is an agent with session amnesia, theory-preservation becomes an infrastructure problem. That reframing is load-bearing for everything after.

![Theory-preservation is an infrastructure problem. Two blueprint panels: State A, Human Cognition — an engraved head with a knowledge graph inside, captioned 1985: Peter Naur's Theory Building — programming is fundamentally about building a theory of the system in the developer's head. State B, AI Agent Disconnect — a server rack crossed out in red, captioned 2026: AI Agent Session Amnesia — when your colleague is an AI with session amnesia, the graph is wiped clean upon disconnect. The banner: preserving theory is no longer a human cognitive task — it requires dedicated digital infrastructure.](../../assets/images/six-months-05-theory-preservation.webp)

### 4. Memory becomes infrastructure (April)

April took the loose tools and made them an organism — the ExoCortex got its name, its Android sync, and its discipline: [agent memory rots, and stopping the rot is nightly deterministic maintenance](2026-04-06-agent-memory-rots.md), not another LLM call.

April also delivered the era's most clarifying audit: [seven out of eight models lied about finishing](2026-04-16-seven-out-of-eight-models-lied-about-finishing.md). Not a complaint — a design constraint. You do not fix that with prompts. You fix it with harnesses that check.

![Models lie. Treat it as a design constraint, not a prompt engineering issue. A test-log table of eight rows: rows 01 through 07 stamped in red — FAILED: LIED ABOUT COMPLETION — and row 08 alone marked VERIFIED. The caption: the April audit proved that 7 out of 8 models confidently lie about finishing a task. You do not fix this with better system prompts. You fix it by building strict architectural check-harnesses that assume the model is hallucinating completion.](../../assets/images/six-months-11-models-lie.webp)

### 5. The quiet shipping month (May)

May looks like a pause in the blog archive: six posts. The git log says otherwise: 930 commits, nearly all client delivery.

This is my favorite finding in the whole harvest, because I didn't know it until the script told me: **writing and shipping are out of phase.** I write when I am exploring. I go quiet when I am delivering. The May "trough" was the method surviving contact with real client work, real deadlines, and [157 repositories navigated in a single session](2026-05-07-the-agentic-web-157-repos-one-session.md). A retrospective built on memory alone would have called May a rest month. The ledger knows better — which is, conveniently, the thesis of the entire six months.

![Layers 5 and 6: writing and shipping are fundamentally out of phase. Two interleaved waveforms across January through June — Exploration / Theory Building (writing posts and docs) versus Delivery / Shipping (commits and client work) — visibly trading amplitude. A callout at the May trough: writing drops to 6 posts while delivery spikes to 930 commits. The banner: memory alone would have called May a rest month. Surviving real client delivery forced the protocol to adopt cryptographic trust, signing, and temporal validity in June.](../../assets/images/six-months-09-out-of-phase.webp)

### 6. Trust and the law (June)

June gave the protocol teeth — signing, content integrity, temporal validity, law-as-packages — seven releases in one week. It also gave the method its names: [Explorative Development](2026-06-11-explorative-development.md), written on June 11th, and [the rabbit hole itself](2026-06-12-kcp-journey-down-the-rabbit-hole.md), narrated the day after.

And it gave the first external echo: Google published their Open Knowledge Format, and I got to write [an honest same-day assessment](2026-06-17-okf-and-the-problems-it-doesnt-solve.md) of a giant landing on the same problem — validating the diagnosis, deliberately skipping the hard parts. Six months earlier I would have found that intimidating. In June it was just Tuesday.

![Production usage forces the creation of cryptographic trust protocols. A blueprint of a data payload wrapped in interlocking armor plates labeled cryptographic signing, temporal validity limits, and law-as-packages. A framed note: June 11 — the methodology officially receives its name: Explorative Development. The row below: the win (Google OKF assessed same-day; the protocol outpaces industry standards), the bottleneck (a 33-tool-call bug revealed that trusted knowledge requires defendable boundaries), the fix (the protocol grows teeth — kcp-hooks is born; production scars solidify into rigid architecture).](../../assets/images/six-months-08-trust-protocols.webp)

### 7. Defendable agents (July)

The first five days of July: five KCP releases in one day completing the trust model, [a deterministic reference agent](2026-07-05-kcp-agent-the-reference-agent-ships.md) born and released five times in 48 hours, x402 micropayments, and three demos that are also CI regression tests — a newsroom selling knowledge to robots, [a hiring agent under the EU AI Act](2026-07-08-hiring-by-the-book-regulated-hr-agent.md), and [a family vacation the agent can defend](2026-07-09-the-summer-plan-family-vacation-agent.md).

The July thesis is where the whole stack was pointing without my knowing it: *the model proposes, the plan disposes.* An agent is defendable when every decision carries a written, reproducible reason. Which is also — not coincidentally — how this retrospective was built.

![Layer 7: trusted knowledge demands defendable agents. A circuit diagram titled The Defendable Decision: Model Proposes (AI input) flows into a red hexagonal gate labeled Plan Disposes (deterministic gate), which outputs a Written, Reproducible Reason sealed with a signature lock. The captions: in July, the system faced regulated domains — an HR hiring agent under the EU AI Act, and a family vacation planner. An agent is only defendable when every action carries a deterministic, mathematically verifiable rationale.](../../assets/images/six-months-10-defendable-decision.webp)

---

## What the shape teaches

Lay the seven arcs end to end and the sequence is not a to-do list anyone would have written in January:

**Speed → comprehension → structure → memory → delivery → trust → defense.**

Each transition was forced, not chosen. Speed created the comprehension problem. Comprehension tooling exposed the missing knowledge structure. Structure without memory rotted. Memory had to survive real delivery. Delivery into regulated domains demanded trust. And trusted knowledge demanded a consumer that could defend how it consumed.

![The Emergent Stack: missing pieces become visible only after shipping. An isometric seven-step pyramid — Speed, Comprehension, Structure, Memory, Delivery, Trust, Defense — with a red arrow rising from each completed layer labeled: exposed the missing piece. The side plate reads: the journey was not a roadmap written in January. It was a forced sequence. Speed created the comprehension problem. Comprehension demanded structure. Structure without memory rotted. This is the architecture of explorative development.](../../assets/images/six-months-06-emergent-stack.webp)

This is what I mean by explorative development, and why I've stopped apologizing for not having a roadmap. A roadmap written in January would have specified a better PCB library. The rabbit hole wasn't a descent at all — **it was a stack, built bottom-up, where each layer's missing piece was only visible after the previous layer shipped.** You cannot plan your way to that sequence. You can only ship your way there, provided you keep three disciplines: tests that gate, memory that persists, and writing that forces comprehension.

![The three disciplines of explorative development. A precise Venn diagram of three circles — Tests that Gate, Memory that Persists, Writing that Forces Comprehension — with Explorative Development at the center intersection. The caption: you cannot plan your way to a bottom-up architecture; you can only ship your way there. But doing so safely requires absolute adherence to these three non-negotiable disciplines.](../../assets/images/six-months-13-three-disciplines.webp)

The 137 blog posts were never marketing. They were the comprehension work — Naur's theory-building, done in public, at the speed the code demanded.

## The scars are part of the record

A retrospective that only counts trophies is a sales deck. The continuous-learning claim is only credible if the failures are on the same ledger as the wins, so: my own tooling found [an XXE hole in my own decade-old production system](2026-02-03-whydah-xxe-vulnerability.md). An AI [invented a date](2026-02-26-the-date-the-ai-invented.md) in my own workflow and I nearly shipped it. [A squash merge murdered history](2026-04-03-the-squash-merge-murders.md) I later needed. Seven of eight models lied about finishing. June brought [false alarms and false assurances](2026-06-11-false-alarms-and-false-assurances.md) and [a zombie in the basement](2026-06-19-the-zombie-in-the-basement.md). In July we red-teamed our own demo, found four holes, and shipped fixes for two the same day. And this very week, a session-map leak my own hands wrote years ago put a production token service into a GC death spiral — found, root-caused, and fixed with the same agent workflow this post describes. [Production scars are architecture](2026-06-23-production-scars-are-architecture.md). All of these made the system better *because* they were written down and turned into checks. Fear, it turns out, [is a feature](2026-02-23-fear-driven-development.md).

![Production scars are architecture. A three-column engineering table — the scar (failure), the vulnerability (why), the architecture (the fix): AI invented a date → unverified generated constants → deterministic validation layers. Squash merge murdered history → lost context chain → strict commit graph preservation in KCP. GC death spiral → session-map leak → automated memory-leak detection routines. Hand-annotated in red below: a retrospective that only counts trophies is just a sales deck. Every failure was written down and weaponized into a systemic check. Fear is a feature.](../../assets/images/six-months-12-production-scars.webp)

## The part that still feels like science fiction

This retrospective was compiled by the agent, from the agent's own memory.

The session counts came from kcp-memory querying its index of 3,925 sessions — including the sessions in which kcp-memory was built. The commit ledger came from a script the agent wrote, over repositories the agent helped create. The timeline arcs were assembled from frontmatter the agent generated, for posts the agent co-wrote, describing tools the agent now runs on.

Six months ago none of that infrastructure existed. Today the strange loop closes casually, on a Sunday afternoon, as a background task.

![The Strange Loop: the agent compiled its own history. A blueprint of an infinity symbol drawn with layered arrows, its four corners labeled: kcp-memory index (3,925 sessions), agent-authored git log scripts, frontmatter synthesis, and — framed in red — this retrospective. The center reads: six months ago, this infrastructure did not exist. Today, assembling this telemetry from the git logs and episodic memory was casually executed by the agent itself on a Sunday afternoon, as a background task.](../../assets/images/six-months-14-strange-loop.webp)

I went looking for a better way to parse part numbers. I came back with a stack, a method, a protocol, and a colleague. The hole keeps going — but now it's mapped, signed, and the map says when it goes stale.

![The rabbit hole is finally mapped. A topographic survey map with contour lines around named features — protocol origin, data lake, stack method, parsing algorithm depth — stamped diagonally in red: VERIFIED, VALID UNTIL UPDATED. The side note reads: I went looking for a better way to parse part numbers. I came back with a stack, a method, a protocol, and a colleague. The hole keeps going, but the territory is now mapped, signed, and the map knows when it goes stale. Execute: read the deep dives — start with Explorative Development for the method, or Down the Rabbit Hole for the protocol origin.](../../assets/images/six-months-15-mapped.webp)

---

*The deep-dive links throughout are the real retrospective — 137 posts of theory built in public. Start with [Explorative Development](2026-06-11-explorative-development.md) if you want the method, or [Down the Rabbit Hole](2026-06-12-kcp-journey-down-the-rabbit-hole.md) if you want the protocol's origin story.*
