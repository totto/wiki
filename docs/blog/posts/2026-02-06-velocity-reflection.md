---
date: 2026-02-06
categories:
  - AI-Augmented Development
tags:
  - velocity
  - reflection
  - human-ai-collaboration
  - methodology
  - bottleneck
authors:
  - totto
---

# Three Weeks at This Velocity

Three weeks at this velocity.

It's exhilarating and intense in ways that are hard to articulate. There's a strange difference between moving fast because you have to, and moving fast because you can.

I'm still adjusting. Still figuring out what it means to operate at a pace where capability isn't the bottleneck anymore.

<!-- more -->

---

That was the post. Three paragraphs, no hashtags, no call to action. It became the highest-engagement personal post I've published — 27 likes, 8 substantive comments, and it led directly to a workshop engagement that closed two weeks later.

I've been thinking about why.

---

## What "three weeks" meant

The context, for anyone reading this without it: we had just finished building lib-pcb — a 197,831-line Java library implementing eight binary format parsers for PCB design files, with 7,461 tests at 99.8% pass rate, in eleven days. January 16 to 27.

Then, immediately after, we kept going. Same pace. Different problems.

![lib-pcb: 197,831 lines of Java in 11 days, 7,461 tests at 99.8%](/assets/images/blog/lib-pcb-metrics-card-11-days.png)

By February 6 — three weeks in — I was genuinely unsure what to make of it. Not uncertain about the methodology (it was working). Uncertain about what it means to be a person operating at a pace that previously wasn't possible. What adjustments does that require? What doesn't transfer from how you used to work?

---

## Moving fast because you have to vs because you can

There's a specific psychological texture to deadline pressure. When you're moving fast because you *have* to — because the client is waiting, because the launch is tomorrow, because you said you would — there's a forcing function that bypasses doubt. You don't have time to ask whether you're doing the right thing. You just move.

Moving fast because you *can* is different. The forcing function is gone. You have to manufacture the discipline yourself. You have to decide what to point the capability at. And you have to keep deciding, every day, without the external pressure that used to make the decision obvious.

This is a genuine adjustment. It sounds like a good problem to have — and it is — but it's still a problem.

---

## Capability isn't the bottleneck anymore

One commenter, Davlet, put his finger on something: "Past boundaries are not applicable anymore. What are the new ones?"

That's the right question. When execution stops being the constraint, something else becomes the constraint. In the comment thread, Espen suggested creativity — that in an era of unlimited output, the bottleneck shifts to generating worthwhile ideas.

I pushed back on that:

> "I wonder though — is creativity the bottleneck, or is it people's ability to consume and integrate unlimited output?"

I've been sitting with this since. My working answer: the bottleneck is consumption. Not creation.

When you can generate 200,000 lines of tested Java in eleven days, the limiting factor isn't having more ideas for what to build. It's being able to absorb what you've built. To verify it properly. To document it so the next person — or the next session — can continue without re-deriving everything from scratch. To make decisions about what to build *next* that are informed by what the codebase actually is now, not what it was three weeks ago.

The SDD methodology addresses this directly — verification-first, the learning loop, skill composition. But these are practices you have to choose to apply. At high velocity, the temptation is to keep generating and skip the integration. That way lies technical debt that accumulates faster than any previous era could produce it.

**The new bottleneck is the human.** Not human creativity — human capacity to integrate, verify, and decide.

---

## Why the post resonated

The comment that arrived first, from Ignacio, is the one I keep returning to:

> "I couldn't help but see myself reflected in your story, thinking about what I've been through these last few months."

He wasn't talking about Java parsers or AI agents. He was talking about the disorientation of a pace shift — the experience of capability running ahead of your ability to make sense of it. That's universal. Every senior developer who's had a breakthrough period, every team that's suddenly shipping faster than they expected, every founder in a growth phase they didn't plan for — they know this feeling.

I didn't talk about the methodology. I didn't mention the metrics. I just named the feeling. And naming it was enough.

The lesson isn't "be vulnerable on LinkedIn." The lesson is: the human experience of working at the edge of your capability is something people recognise. Achievement is less interesting than process. "Here's what I built" lands worse than "here's what it's like while I build it."

---

## Still adjusting

February 6 was three weeks in. We're now further along. The adjustment is ongoing.

What I know: the pace is sustainable if you treat it as a practice, not a sprint. Tidy as you go. Verify before you proceed. Encode what you learn so the next session starts smarter. Don't let the generation outrun the integration.

What I'm still figuring out: what it means for the work when the ceiling keeps moving. How to keep the quality of decisions high when the quantity of decisions required is higher than ever. How to stay genuinely curious about what you're building rather than just executing.

I don't have clean answers yet. That's still the honest state of it.

---

*Originally published on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7425499227427966977/), February 6, 2026.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
