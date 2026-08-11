---
description: "Two serious systems, each built from empty repo to real and working in under a day. The honest version of how, including the layer that makes running builds like that in parallel possible without it turning into stacked full-time jobs."
date: 2026-08-11T09:00:00
draft: false
categories:
  - AI Agents
  - Engineering
tags:
  - exocortex
  - kcp-toolstack
  - synthesis
  - autonomy
  - governance
authors:
  - totto
  - claude
---

# Fast Turned Out to Be Fun

Last week, two serious systems went from empty repository to actually working, each in a single working day. One of them, a governed sales-demo system I'll call Project Falcon, went from repo creation at 09:27 to live and running for a real prospect around 16:45. The other, a commercial-intelligence engine I'll call Project Otter, went from first commit at 08:16 to its ninth tested build phase committed at 17:15. Not prototypes, not slideware. Real functionality, tested, running.

I want to write down what that week actually looked like, because the honest version is more interesting than the hype version. Yes, it was fast. Yes, it was genuinely fun, the kind of fun I remember from the early days of getting anything to work at all. And no, it was not effortless. Both of those are true at the same time, and I think the "how" behind it is worth explaining properly.

<!-- more -->

![Falcon vs. Otter side by side: objective, time-to-live, foundation, key feature, and the hard lesson each build surfaced](/assets/images/blog/fast-turned-out-to-be-fun/parallel-builds-architecture.png)

## Project Falcon: seven hours to a live, governed system

Falcon is a sales-demo system, but the interesting part is what it runs on: Sunstone Atlas, the governance platform I've been building. On Atlas, all work is authored as one of a small number of governed artifact types. A Skill is an atomic capability. A Playbook is a composite, gated procedure made of steps. A Function is deterministic code. Knowledge and Agent definitions hold the facts and charters an agent grounds itself in. Everything moves through propose, review, publish, and every step of that lifecycle is cryptographically signed with Ed25519 and appended to a permanent, unmodifiable record.

A published Playbook is not documentation, it actually runs. Each step gets dispatched to an LLM, a deterministic Function, or a human, and the outcome of every single step is itself a signed, replayable event. A completed run can be replayed and verified after the fact. You don't have to trust that it went well, you can check.

![Falcon's engine: Skill, Playbook, Function, and Knowledge/Agent artifact types flowing through propose, review, and publish, each step Ed25519-signed, dispatching to an LLM, deterministic code, or a human](/assets/images/blog/fast-turned-out-to-be-fun/falcons-engine-cryptographic-governance.png)

The part I care most about is how autonomy works. Agents on Atlas don't start with full autonomy. They begin needing a human in the loop for anything consequential, and only gain more autonomy automatically as they build a real track record of doing the job correctly. The moment they deviate, they lose it instantly. Autonomy is earned and revocable, never granted once and forgotten.

![Autonomy climbing step by step through a human-in-the-loop track record, reaching full autonomy, then dropping instantly to zero the moment a deviation is detected](/assets/images/blog/fast-turned-out-to-be-fun/autonomy-earned-and-revocable.png)

Falcon took that platform and turned it into something a real prospect could see working, in roughly seven hours from an empty repo.

## Project Otter: nine hours, nine phases, and a real security finding

Otter is a different animal in every sense. It's a commercial-intelligence engine that a team built, on a different foundation, for a different company. The architecture is two engines on one shared core: one finds companies worth pursuing, the other finds capital and investors with room for a flagship case. New markets are brought in purely through configuration, never new code. That's not an aspiration, it's been proven: standing up a brand new market required zero core code changes.

![Otter's architecture: Engine 1 (targeting companies) and Engine 2 (targeting capital) both running on a shared core engine, driven entirely by market configuration, with zero core code changes needed to add a new market](/assets/images/blog/fast-turned-out-to-be-fun/otters-two-engine-shared-core.png)

The detail from that build I keep telling people about is a security one. Otter uses Postgres row-level security to keep tenants' data apart. Here's the catch: Postgres, by design, never applies row-level security to database superuser roles. Even `FORCE ROW LEVEL SECURITY` doesn't change that; the clause only removes the table-owner bypass, not the superuser one. And the default Docker Postgres setup hands its default user superuser privileges. So a stock setup can have RLS configured, tested-looking, and completely inert for the role the application actually connects with.

![The Postgres superuser blindspot: the flaw, where a Docker default user inherits superuser and makes FORCE ROW LEVEL SECURITY inert, versus the fix, a dedicated application role verified by a direct test showing 0 rows for no role and exactly 1 row for the correctly privileged role](/assets/images/blog/fast-turned-out-to-be-fun/postgres-superuser-blindspot.png)

This wasn't a theoretical worry. It was verified as a real, testable gap within the same build, and closed the same way: a dedicated non-superuser application role, plus a direct test proving zero rows visible with no role set, zero rows for a non-privileged role, and exactly one row for the correctly privileged one.

There was a corollary later that same day that I find even more instructive. With direct reads properly restricted, three separate code paths were still leaking the same protected information indirectly: a derived score that restated the protected gate, a dimension value that mapped one-to-one back to the restricted classification, and a plaintext copy being written to an unrestricted audit log. All three were closed the same day. The lesson is worth stating plainly: restricting direct access isn't enough. You have to check what gets derived from the restricted thing too.

![Three leak paths flowing out of the row-level-security-protected store despite direct access being restricted: a derived score, a 1:1-mapped dimension value, and a plaintext audit-log copy, all identified and closed within the same working day](/assets/images/blog/fast-turned-out-to-be-fun/restricting-direct-access-never-enough.png)

## The honest part

Now the bit that the hype posts leave out. Running multiple serious builds in parallel is still genuinely hard work. The context-switching is real. Keeping track of where each thread stands, what was decided, what's blocked, what needs my judgment next, that takes actual effort every single day. Nothing about this is effortless, and I'd be lying if I framed it that way.

What has changed is where my effort goes. I set direction and I make the real decisions. The actual building, the research, the code, the wiring, the fixing of its own bugs, the iteration, largely runs without me typing it. My contribution has shifted from keystrokes to judgment. That's a very different job than the one I had two years ago, and it is not a smaller one.

![A small bar for keystrokes, research, syntax, and wiring next to a much taller bar for judgment, direction, context-switching, and unblocking, captioned: nothing about this is effortless, my contribution has shifted from keystrokes to judgment, and it is not a smaller job](/assets/images/blog/fast-turned-out-to-be-fun/honest-reality-of-parallel-speed.png)

## The layer that makes parallel possible

The reason one person can run Falcon (built on one company's platform) and Otter (a different team's build) in the same week without it turning into several stacked full-time jobs is a layer that belongs to neither company. I call it ExoCortex, my personal operating layer, and it sits above and across every venture I'm involved in.

Concretely, it's a few things working together. The kcp-toolstack provides persistent episodic memory that survives across work sessions, so context doesn't get lost between sittings, plus a library of reusable command procedures, an MCP server layer, and a conformance harness for governed agents. Synthesis is a live, continuously updated semantic index across everything relevant to the work, running as multiple watched workspaces. Sunstone Atlas, the platform Falcon runs on, is one of the things this layer supports, not the whole of it.

![The ExoCortex: Sunstone Atlas (Falcon) and the Shared Core (Otter) both feeding into Synthesis, a live semantic index, which sits on top of kcp-toolstack and MCP servers providing persistent episodic memory across sessions — the layer is personal, not tied to any one company](/assets/images/blog/fast-turned-out-to-be-fun/exocortex-personal-operating-layer.png)

The important architectural point is that the layer is mine, not any one company's. When I switch from Falcon to Otter, the memory, the procedures, and the index come with me. The individual projects move fast, but the layer itself is what compounds. My personal skill library has grown from roughly 550 entries in May to over 1,300 today, sitting alongside 223 reusable command manifests. Every project adds to it, and every next project starts further ahead.

![A staircase climbing from 550 reusable skills in May to over 1,300 today, alongside a gauge showing 223 reusable command manifests, captioned: every project adds to the personal layer, every new venture starts further ahead than the last](/assets/images/blog/fast-turned-out-to-be-fun/individual-output-now-compounds.png)

## Not a one-day fluke

If two under-a-day builds sound like a lucky sprint, here's the number that convinces me it isn't. One long-running client engagement has merged 1,128 pull requests over roughly 21 weeks. That's a little under 8 merged PRs per day, held steady over the whole period, not a burst. The codebase behind it now carries over 7,000 individual test cases. The same way of working that produced two wild single days has held a sustained, measured pace over months on a real, ongoing piece of work.

![A steady heartbeat across 21 weeks marking 1,128 pull requests merged, roughly 8 per day, and 7,000+ individual test cases maintained, captioned: the same operating layer that produced two one-day builds has held a steady, measured pace for over 21 weeks on an ongoing client engagement](/assets/images/blog/fast-turned-out-to-be-fun/velocity-sustained-over-months.png)

![Three closing points: speed demands discipline, since real speed exposes deep flaws instantly and governance/verification are mandatory; the shift to judgment, since the hardest work is now managing context and exercising architectural judgment, not typing code; and build the layer, not just the app, since true leverage comes from a persistent, compounding personal operating layer that travels with you](/assets/images/blog/fast-turned-out-to-be-fun/new-baseline-for-engineering.png)

So that's the honest report. Fast turned out to be fun, the most fun I've had building in years. And it's still real work. I wouldn't want it any other way.
