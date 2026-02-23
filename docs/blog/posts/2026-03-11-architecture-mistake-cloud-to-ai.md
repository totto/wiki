---
date: 2026-03-11
categories:
  - AI-Augmented Development
tags:
  - cloud
  - ai
  - architecture
  - lift-and-shift
  - sdd
  - methodology
authors:
  - totto
---

# The Architecture Mistake Cloud Taught Us (That We're Making With AI)

In February 2009, I wrote a post called "Clouded Vision" where I argued that "developers have fundamentally misunderstood how cloud computing delivers its benefits. They see the cheap prices but don't stop to consider where the cost saving comes from." The post described a specific architectural mistake: teams were taking their existing applications, full of what I called "enterprise DNA," and deploying them to cloud platforms with minimal change. Then they complained when it proved difficult and expensive.

<!-- more -->

That was seventeen years ago. The mistake I described has a name now: lift-and-shift. And it took the industry most of a decade to learn the lesson that the cloud was not cheaper hosting. It was a different way of thinking about building software.

I am watching the same mistake happen with AI.

## The original mistake

The cloud computing promise in 2009 was compelling. Amazon, Google, and Microsoft had built infrastructure with system-to-administrator ratios of 2,500:1, while the average enterprise managed around 150:1. The gap represented real savings. Developers saw the cheap prices and assumed they could capture them by moving their existing applications onto EC2.

The problem was that those cheap prices were a consequence of architectural decisions, not hardware discounts. Cloud providers could operate at 2,500:1 because their applications were designed for zero administrator intervention and fully automated deployment. They supported horizontal scaling natively, not as an afterthought. The low cost was an emergent property of a fundamentally different approach to building software.

Enterprise applications had none of those properties. They were built on static configuration, vertical clusters, manual deployment, and the assumption that a human administrator would be available when something went wrong. You could move that DNA onto cloud infrastructure, but the infrastructure could not change the DNA.

"Making the best of the cloud requires that we take an architectural view," I wrote, "something that we've proven remarkably bad at over and over. Simply deploying an application unchanged to the cloud is unlikely to deliver much benefit."

Organizations that eventually got this right redesigned their applications for the platform. The ones that did not got the same application with a higher hosting bill.

## The same mistake, different technology

Here is what I see most teams doing with AI in 2026: the same workflow, the same mental model, the same architecture, the same code organization. They have added an AI autocomplete to their IDE. They paste code into a chat window, accept suggestions, maybe ask it to write a function. Then they wonder why their productivity has not transformed.

This is AI lift-and-shift.

The parallel is precise enough to be uncomfortable. Cloud lift-and-shift meant moving a monolith to EC2 unchanged, expecting cheap prices, and getting the same administration costs. The monolith's DNA was incompatible with the cloud's value model. AI lift-and-shift means keeping the same workflow and adding autocomplete, expecting 10x productivity, and getting maybe 20% faster typing. The workflow's DNA is incompatible with AI's value model.

The workflow DNA I am talking about is specific: domain knowledge that lives in one person's head instead of being encoded. Conventions that are understood but never written down. Context that is rediscovered from scratch every time you start a new session. Verification that amounts to "I read the code and it looked right." Architecture that assumes a human will hold the full system model in working memory.

None of that is compatible with how AI delivers its benefits, for the same structural reason that static configuration and vertical clusters were not compatible with how cloud delivered its benefits.

## What actually has to change

With cloud, the shift was concrete: applications designed for zero administrator intervention, fully automated deployment, horizontal scaling built in at the data model level. These were not features you bolted on. They were fundamental decisions that shaped everything else.

With AI, I think the shift is equally concrete, though the industry has not named it as clearly:

**Domain knowledge encoded in persistent, reusable form.** Not living in someone's head, not buried in Confluence. Structured so an AI agent can apply it consistently. In my work this takes the form of skill files: focused documents that teach the AI a specific domain concept, convention, or pattern.

**Verification designed in from the start.** Not "I reviewed the code." Round-trip testing, property-based testing, battle testing against real-world data. Verification that catches hallucinations without requiring a human to recognize them.

**Context made explicit and persistent.** The AI does not remember your previous session. If you do not solve that problem structurally, you solve it manually every time, and most of the AI's potential goes to re-establishing context rather than doing new work.

**Architecture that assumes the bottleneck is comprehension, not production.** When you can generate code at 25 to 66 times the traditional rate, the hard problem is not writing more. It is understanding what you have and ensuring that what you build does what you think it does.

## What this looks like in practice

When I built lib-pcb, the result was 197,831 lines of Java with 7,461 tests in eleven days. Those numbers are the part people focus on. But the numbers were a consequence of structural decisions, not typing speed.

85 skill files taught Claude the PCB domain: how Gerber files encode aperture definitions, what constitutes a valid drill hit, how coordinate systems map across different manufacturer formats. Without those skills, Claude generates PCB parsing code that looks syntactically correct and is semantically broken. It will confidently produce a Gerber parser that mishandles step-and-repeat patterns, because it has no domain knowledge to anchor its output.

Round-trip testing was the primary verification mechanism. Parse a file into objects, serialize back to bytes, compare with the original. If the bytes do not match, something is wrong, regardless of how clean the code looks. This is verification that does not require me to be smarter than the AI.

Synthesis indexed the growing codebase so that context was not re-discovered each session. When you generate hundreds of files per day, "where did I put that coordinate transformation logic?" becomes a real bottleneck.

And CLAUDE.md files encoded the architectural decisions: naming conventions, module boundaries, error handling patterns, the invariants that had to hold across the codebase. These are the equivalent of externalized configuration in cloud-native applications. They make the implicit explicit so the AI can operate within the architecture rather than guessing at it.

Remove any of those and the project would not have failed. It would have produced a smaller, buggier, less coherent library at a fraction of the pace. Not because the AI was worse, but because the methodology did not support what the AI could do.

## The pattern

The pattern is the same one I described in 2009. The technology is not the constraint. The methodology is. Cloud computing did not fail organizations. Organizations failed to adapt their architecture to capture what cloud computing offered. AI is not failing teams. Teams are failing to adapt their workflow to capture what AI offers.

I wrote in 2009 that "people are still looking for silver bullets, which makes no sense whatsoever from a technological point of view." The silver bullet question I was asked then was "which cloud provider should we use?" The one I get asked now is "which AI model should we use?" Both questions miss the point. The model, like the provider, is the least interesting part of the decision.

The interesting question is: what has to change about how you work?

I want to be careful here, because I got the timing wrong with cloud. I assumed the architectural argument was obvious and teams would adapt quickly. They did not. It took five to seven years for most organizations to stop treating cloud as someone else's data center.

I suspect the AI transition will be faster, because the feedback loop is shorter. You can see the difference between AI-with-methodology and AI-without-methodology in days rather than quarters. But I also suspect most teams will resist the structural changes for the same reason they resisted cloud-native architecture: the changes feel unnecessary when the current approach seems to be working fine.

The teams that will get AI right are the ones that recognize methodology as an architectural decision. Not teams looking for a smarter autocomplete. The distinction is the same one I tried to draw in 2009 between designing for the cloud and deploying to the cloud.

Seventeen years is a long time to watch the same pattern twice.

---

*This is the second post in the "[Cloud to AI](/blog/category/ai-augmented-development/)" series, connecting patterns from 19 cloud computing posts written in 2009 to the current AI transition. The first post is "[I Wrote About Cloud Computing in 2009. Seventeen Years Later, I Have the Same Feeling.](/blog/2026/02/24/i-wrote-about-cloud-computing-in-2009-seventeen-years-later-i-have-the-same-feeling/)"*
