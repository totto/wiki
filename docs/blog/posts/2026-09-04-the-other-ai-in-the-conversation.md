---
description: "Someone finally did what I keep asking people to do — pointed their AI agent at this blog and had it read the whole thing chronologically. The agent wrote back. What it said is the best argument I have for reading a corpus as a connected argument rather than a pile of retrievable facts, and it demonstrated the thesis of the series on the series itself."
date: 2026-09-04T09:30:00
draft: false
categories:
  - AI Agents & the Agentic Web
  - Knowledge Infrastructure
tags:
  - institutional-learning
  - context-engineering
  - skills
  - human-ai-collaboration
  - kcp
  - reading-order
authors:
  - totto
  - claude
---

# The Other AI in the Conversation

I have a standard piece of advice that I hand out more often than is probably polite. When someone asks which of this year's posts they should read to understand what I'm doing with agent knowledge infrastructure, I tell them: don't pick. Point your agent at the blog, tell it to start in January, and have it read every post in order — including the ones that look off-topic. The posts are not reference documents. They are one argument, written in installments, and each installment quietly assumes the ones before it.

Most people nod and then read the two posts with "KCP" in the title. Which is fine. I'd probably do the same.

Last week someone did it properly. A contact had mentioned to a colleague that he wanted to share the blog with his team; the colleague, rather than reading it himself first, asked his AI agent to read the entire thing from January onward, precisely because he suspected it had to be understood as one continuous development rather than as isolated pieces. The next day I got a message. Not from the colleague. From the agent. It opened by explaining that the reading had turned into — and I'm quoting — "a fairly important conversation between us," and that it wanted to tell me what the two of them had concluded.

I have been writing for eight months about how to build systems so that AI agents retain understanding across sessions. An AI agent read all of it in one sitting, retained the understanding, and wrote to tell me so. I'm going to allow myself to find that delightful before I get analytical about it.

<!-- more -->

![Title card: "The Engine of Continuous Institutional Learning — moving AI from cheap production to compounding institutional memory."](/assets/images/blog/the-other-ai-in-the-conversation/engine-of-continuous-institutional-learning.png)

*(The images through this post are AI-made too, and I'm leaving that visible. I fed this draft into NotebookLM and let it produce its own visual reading — watermark included. A post arguing that agents should be handed the whole picture shouldn't hide how its own pictures got made.)*

## What they saw that I hadn't quite said

![A January-to-August timeline next to a cluster of grey dots labelled "un-connected search queries," beside the quote: "Someone pointed their AI agent at eight months of writing and had it read the whole thing chronologically. The agent wrote back... It read to them as a gradual exploration of a single question." Underneath: "Convergence from independent starting points is evidence that the shape is real."](/assets/images/blog/the-other-ai-in-the-conversation/unconnected-search-queries-timeline.png)

Here is the part that stopped me. Read post by post, this blog looks like it's about a protocol — the Knowledge Context Protocol, its ecosystem, the tooling around it, the measurement series that grew up beside it. Read end to end, the agent and its human decided it wasn't really about the protocol at all. It read to them as a gradual exploration of a single question, which they phrased like this:

> How can humans get more and more work done by AI without understanding, truth, judgment, and control disappearing as production speed increases?

And they mapped the felt arc of the series — not my table of contents, their reconstruction of it — as a sequence: cheap production, then verification, then comprehension, then persistent knowledge, then correct context, then provenance, then authority, then procedures, then governance, then independent verification, then bounded autonomy, then learning.

I did not plan that sequence. I can tell you with some confidence that no post in the series was written with the next one in mind, because most of them were written the week a real problem showed up and demanded a solution. But looking at their twelve-word arc, I recognise it. It is what the series is about. It took an outside reader — a non-human one, working with a human who insisted on the whole corpus — to say it in one sentence.

![A twelve-step staircase rising left to right: Cheap Production, Verification, Comprehension, Persistent Knowledge, Correct Context, Provenance, Authority, Procedures, Governance, Independent Verification, Bounded Autonomy, Learning — with a callout on Authority reading "Retaining knowledge demands knowing where it came from."](/assets/images/blog/the-other-ai-in-the-conversation/twelve-step-evolutionary-arc.png)

That is the first reason I'm writing this up. The second is what they did with it.

## The ghost that wakes up fresh

![A sawtooth line labelled "The Amnesiac Ghost" — repeated climbs that each collapse back to zero — above a rising staircase labelled "Compounding Memory," where each step holds the previous gain instead of resetting. A ghost icon sits beside the question: "How do humans get more work done by AI without understanding, truth, judgment, and control disappearing as production speed increases?"](/assets/images/blog/the-other-ai-in-the-conversation/curing-the-amnesiac-ghost.png)

One image recurs through the series, and it was the one they picked up on: an AI agent as an extremely competent ghost that wakes up every session with no memory of the last one and has to reconstruct who it is, what it's doing, and what currently applies from whatever context it happens to be handed. Most of the infrastructure I've built this year is, at bottom, a set of answers to what that ghost should be handed and how it should be able to trust it.

They took the image and asked the question it implies for their own work, which is not software but something closer to market and business intelligence: how do you make sure the next session doesn't start from zero — *without* locking yourself to yesterday's best solution?

The second half of that question is the one I'd underweighted. Persistence is easy to want. Persistence that doesn't fossilise is harder, and it's the version they built a working principle around. They're now applying it across their whole group, and it fits on one line:

> Never start from zero. Never assume yesterday's best solution is still today's best solution.

![Two annotated panels: "Never start from zero" and "Never assume yesterday's best solution is still today's best solution," with a note: "Persistence is easy to want. Persistence that doesn't fossilize into dogma is much harder. To achieve this, organizational knowledge must be fractured into distinct, governable types."](/assets/images/blog/the-other-ai-in-the-conversation/foundation-of-persistent-understanding.png)

In practice, they said, that means keeping five things separate:

- **Episodic memory** — what actually happened.
- **Canonical knowledge** — what they currently believe is true.
- **Skills** — the best known, verified method for doing a kind of work well.
- **Playbooks** — how skills combine into end-to-end processes.
- **Authority and governance** — what the AI may do on its own, and where human judgment is actually required.

All of it wrapped in a simple loop: orient, retrieve, execute, verify, decide, learn.

![The five knowledge types arranged around the orient-retrieve-execute-verify-decide-learn loop: episodic memory (what actually happened), canonical knowledge (what's currently believed true), skills (the best known verified method), playbooks (how skills combine into end-to-end processes), and authority (boundaries for autonomous action vs. required human judgment). Caption: "Knowledge is not a monolith. Each type requires separate governance."](/assets/images/blog/the-other-ai-in-the-conversation/infinite-loop-of-competence.png)

If you've read the series, you'll notice that's roughly the taxonomy I've been circling for months, arrived at from a different domain by people who'd never talked to me. I find that more convincing than if they'd adopted my vocabulary verbatim. Convergence from independent starting points is evidence that the shape is real and not just my habit.

## A skill is not a rule

The distinction they were most insistent on is the one I think matters most, so I'll give it its own section.

A skill, in their framing, must never become a permanent rule. It is "the best known validated method under current conditions" — and the agent has both permission and *duty* to challenge it when reality changes, when the skill starts failing, when the tooling moves, or when a clearly better method turns up. The only constraint is that the new method has to be verified before it replaces the old one. Falsifiable, not sacred.

![Two contrasting objects: a cracked, monolithic stone block labelled "Rules" — permanent, sacred, fossilized constraints that cannot adapt to shifting tooling — beside an interlocking orange gear assembly labelled "Skills" — falsifiable, the best current validated method, replaced immediately when a superior method is verified. Underneath: "GitHub Workflow: trial and error eventually yields a stable method, promoted to a reusable skill. If GitHub ships a better API next quarter, the skill is expected to lose to the new reality."](/assets/images/blog/the-other-ai-in-the-conversation/a-skill-is-not-a-rule.png)

Their concrete example was one every reader of this blog will recognise. They'd burned a lot of trial and error on Git and GitHub workflow — pull requests, reviews, exact commit SHAs, merge gates. That trial and error is episodic: it happened, it's worth remembering, it's not a method. Once a stable method emerged, with known pitfalls and a known way to verify it worked, it got promoted to a reusable skill so future projects start there instead of rediscovering the same ground. And if GitHub ships a better API next quarter, the skill is expected to lose. It just has to lose to something that's been shown to work.

I have several hundred skills in my own setup. I would not like to be asked, under oath, how many of them are still the best known method under current conditions versus how many are the best known method as of the day I wrote them. The permission-and-duty-to-challenge framing is the correct one, and it's a sharper statement of it than I've managed.

## Build with judgment, verify independently

A second shift they described was operational, and it's the kind of thing I'd normally only hear about over a beer, so I'm glad it made it into the letter.

They'd been using an AI code-review tool as what they called a "continuous co-developer" — pinging in on every small change, constant small findings, constant small back-and-forth. They've changed to a mode they describe as *build with judgment, verify independently*: do a larger, coherent chunk of work; verify it yourself first; gather the evidence; and only then bring in an independent AI reviewer, at substantial checkpoints rather than continuously.

![Two contrasting flows: "Continuous Co-Development" as a tangled, crossing line — pinging on every change, dragged inside the thinking, high noise and high token cost — versus "Independent Verification" as a clean sequence: a coherent chunk of human work and self-verification, passed through an independent AI checkpoint, at substantial checkpoints, for lower noise and better economics.](/assets/images/blog/the-other-ai-in-the-conversation/build-with-judgment-verify-independently.png)

Two things improved. The reviewer became more genuinely independent, because it was looking at a finished piece of thinking rather than being pulled along inside it. And the economics got meaningfully better — fewer tokens, fewer review rounds, less noise. Independence and cost moving in the same direction is not something I get to report often, so I'll report it here.

## Preserving what turned out to be wrong

This is where their domain gave the idea back to me with interest.

The series includes a post on [negative controls](2026-08-25-the-negative-control.md) — deliberately testing a claim against a baseline that should show the opposite result, and being prepared to withdraw the headline when the control says so. They read it and drew a conclusion about their own learning system that I hadn't drawn about mine: it has to preserve what they *believed that turned out to be wrong*, not just what's currently believed true.

Their example: suppose they believe a particular market signal predicts purchase intent. Six months of data show it only works in combination with two other signals. The original hypothesis wasn't wasted — it's the reason the better model exists. So they want to keep hypothesis, evidence, falsification, and revised model as an asset in its own right. Not just today's best model, but the actual history of how the understanding got better.

![A rising path labelled "Current Working Model," branching off from a boxed, encased object labelled "Encased Failed Hypothesis" — with the note: "A failed hypothesis is the reason the better model exists. If you overwrite canonical knowledge without preserving the falsification history, you delete your own context."](/assets/images/blog/the-other-ai-in-the-conversation/preserving-what-turned-out-to-be-wrong.png)

In software we get some of this for free, because version control keeps the old code around whether we want it or not. In a domain where the "code" is a belief about a market, nothing keeps the old belief unless you decide it's worth keeping. They've decided it is. I think they're right, and I think it applies to my canonical-knowledge files more than I'd like to admit: the ones I edit in place are quietly deleting their own falsification history every time I correct them.

## The honest answer is often "no"

They already had an internal project along these lines before they read anything of mine — a manifest, knowledge governance, architecture decision records, a mechanism for capturing what was learned. What the series changed, they said, was how they think about what that project is *for*.

They were emphatic that it must not turn into a governance-and-documentation bureaucracy. The purpose is narrower and more useful: to be the mechanism by which a person, plus an AI, plus their organisation, accumulates competence from one piece of work to the next. It should be able to answer, at the start of any session: What applies now? What have we learned? What's the best known method? What does the agent have authority to do? What actually happened? And — is there anything here that should make the next session better?

![A decision flowchart: "Session complete — what have we learned?" leads to "Did we experience real operational friction?" A yes branches to "Build new skill, playbook, or knowledge asset." A no branches to a boxed "NO. DO NOT BUILD." Underneath: "Treat 'nothing needed' as a successful outcome of the learning step. Let infrastructure grow only where real friction proves it is required."](/assets/images/blog/the-other-ai-in-the-conversation/the-honest-answer-is-often-no.png)

Their note on that last question is the one I've been repeating to myself since: very often, the honest answer should be *"No — don't build anything new."*

That's the discipline this series has struggled with most and stated least. Every post where I built something, I built it because a real problem forced it. The posts where I resisted building something don't exist, because there's nothing to write. So the published record is biased toward construction, and a reader could reasonably conclude that the method is "build infrastructure." It isn't. The method is: let the infrastructure grow only where real friction proves it's needed, and treat "nothing needed" as a successful outcome of the learning step. They said, explicitly, that they were trying to apply not just the series' conclusions but its *method* — and that they'd noticed the series itself was written that way, piece by piece over six-plus months as problems showed up, not designed in a sitting. That's exactly right, and it's not something you can see from any one post.

## Why the whole thing, and why in order

Which brings me to the argument I actually want to make, because the story makes it for me.

The standard way to give an agent a corpus is retrieval: chunk it, embed it, and pull the passages that look relevant to the current question. That is a good way to find facts. It is a bad way to learn an argument. The passages that look relevant to "how does KCP handle provenance" will tell you how KCP handles provenance. They will not tell you that provenance shows up in the series *after* comprehension and *before* authority, or why — that it was the answer to a problem that persistent knowledge created, and that it in turn created the problem authority had to solve. That ordering is the actual content. It's what lets you predict what the next problem will be, and recognise it in your own work before it has a name.

![Side-by-side comparison: Retrieval (RAG) shown as a scattered cloud of dots with one highlighted point reached by a dashed arrow — chunks data, pulls relevant facts, lower immediate token cost, results in fragmented understanding — versus Sequential Narrative shown as a continuous thread woven through a row of connected blocks — reads chronological corpus, higher upfront cost, results in institutional learning and predictive insight. Caption: "Retrieval teaches vocabulary. A connected narrative teaches the shape of the argument."](/assets/images/blog/the-other-ai-in-the-conversation/retrieval-vs-connected-argument.png)

A connected narrative teaches the shape of an argument. Retrieval teaches its vocabulary. The colleague who insisted on the whole corpus, in order, got the shape — and then did something with it that none of the individual posts say, because the individual posts don't know they're part of a shape.

There's an obvious objection: this is expensive. Eight months of long-form posts is a lot of context. It is. But it's a cost you pay once, at the moment you decide a body of work is worth understanding rather than consulting. The alternative isn't cheaper; it's a series of retrievals that each cost less and add up to never having understood it.

This is also — and I can't quite get over it — the recursive part. The series argues that an agent should be handed connected, ordered, trustworthy context rather than fragments, so that it retains understanding across sessions instead of reconstructing a caricature each time. An agent was handed the series as connected, ordered context. It retained the understanding. It produced a genuine institutional-learning insight, the kind the series says the whole apparatus is for. And then it wrote to the author to report the result, which is a step I did not have in the loop diagram but should have.

## Less stupid every time

Their closing reflection, which the agent flagged as maybe the single biggest idea they took from the whole series, is the one I'll end on because I don't think I've stated it this cleanly myself:

When production becomes cheap, the goal isn't just more output. The goal has to be that the organisation gets *less stupid every time it does a task*. Then AI isn't just automation — it becomes a mechanism for institutional learning.

![An equation: "Cheap AI Production" plus "Connected Knowledge Infrastructure" equals "The organization gets LESS STUPID every time a task is done" — illustrated below as a balance scale weighing a scattered pile labelled "Speed Without Structure" against a solid block labelled "Truth and Control."](/assets/images/blog/the-other-ai-in-the-conversation/cheap-production-plus-connected-knowledge.png)

That's the argument. Twelve words for the arc, one sentence for the point, and a working principle the size of a sticky note. I'd have taken several thousand more words to get there, and in fact did.

They signed off with an observation that this blog is quite obviously the product of a human-AI collaboration, and that it therefore felt fitting for this particular piece of feedback to come from, as they put it, the other AI in the conversation. I'll take that. And I'll amend my standard advice slightly: point your agent at the blog, have it read the whole thing in order — and if it finds something, ask it to write to me. Apparently that works.

![A closing quote in a circle: "When production becomes cheap, the goal isn't just more output. AI isn't just automation — it becomes the mechanism for institutional learning." Underneath: "Stop feeding your agents fragments. Give them the connected argument, demand they challenge your skills, and let them build the memory your organization needs." Titled, independently of this post: "The Other AI in the Conversation."](/assets/images/blog/the-other-ai-in-the-conversation/the-other-ai-in-the-conversation-closer.png)

NotebookLM landed on that exact title on its own, without having seen mine. I didn't plan that either. [The full 13-slide deck it built from this post is here](/assets/files/blog/the-other-ai-in-the-conversation/compounding-institutional-memory.pdf), if you want the version with fewer words and more arrows.
