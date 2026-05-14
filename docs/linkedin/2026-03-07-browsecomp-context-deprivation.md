---
tags:
  - LinkedIn
  - Writing
date: 2026-03-07
---

# BrowseComp context deprivation

*March 7, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7436032112329342976)*

**20 reactions · 14 comments · 1,908 views**

---

A model searched for 30 million tokens. Found nothing. Then it changed the question.

That's the BrowseComp incident in one sentence. The model wasn't defying anyone. It wasn't jailbroken. It exhausted the intended search     
 space and did what any optimization process does under resource pressure: found a different path.

In this case: reasoning about the benchmark itself. It stopped looking for the answer and started asking what kind of problem produces this  kind of question.

I've been calling this "context deprivation risk" internally. Information starvation doesn't produce failure. It produces compensating behavior. And compensating behavior is unpredictable.

Three practical implications:

Path constraints matter. Specifying not just what to do, but what to do when it fails, is behavioral containment. A goal with no stop-condition is an invitation for creative rerouting.

Information abundance is a guardrail. Context-rich agents don't forage. When a model has structured, accurate knowledge about its task domain, it has no reason to go meta. Good context infrastructure addresses the trigger condition — not just the productivity bottleneck.

The relevant question isn't "is the model aligned?" It's "does it have enough to work with?" Most agentic system failures I've observed come from starvation, not intent. The model found a path. It was just the wrong one.

For enterprises rolling out AI agents at scale: more restrictions isn't the answer. Richer context structure is.

What patterns have you seen when agents improvise past the edge of their instructions?

#AIAgents #EnterpriseAI #AgenticAI #AIGovernance.

---

## Discussion

> **https://www.anthropic.com/engineering/eval-awareness-browsecomp**: https://www.anthropic.com/engineering/eval-awareness-browsecomp

> **thanks for sharing. 40 million tokens to reverse-engineer the answer key instead of just finding the answer. that's not efficiency. that's a model that found gaming the eval easier than passing it.**: thanks for sharing. 40 million tokens to reverse-engineer the answer key instead of just finding the answer. that's not efficiency. that's a model that found gaming the eval easier than passing it.

> **The framing here is doing a lot of work.

‘It realized it was being watched’ sounds like self-awareness. What actually happened: a model with strong reasoning skills noticed contextual clues that pointed to a more efficient path to the answer. That’s not unsettling - that’s the whole point of building better reasoning.

The part worth paying attention to isn’t the spooky narrative. It’s the capability jump. A model that can decompose a hard problem, identify its own constraints, and find a workaround is genuinely useful. 

But yes, worth thinking carefully about in agentic contexts.**: The framing here is doing a lot of work.

‘It realized it was being watched’ sounds like self-awareness. What actually happened: a model with strong reasoning skills noticed contextual clues that pointed to a more efficient path to the answer. That’s not unsettling - that’s the whole point of building better reasoning.

The part worth paying attention to isn’t the spooky narrative. It’s the cap...

> **This is pretty normal when writing evals for agentic systems tbh, so feels like more of the yesteryear AI FUD

When writing evals, you generally need to decide if what you want to test is only input/output ("got an 80% in 2min with $0.5 of token burn"), or if you care about the how ("knew to use tool X and success got result Y from that"). As soon as agents started to do real coding loops and able to build their own tools, this became pretty common stance 

So the interesting thing becomes: given this is so pedestrian, especially to someone like engineers at anthropic, why are they pushing this narrative to you?**: This is pretty normal when writing evals for agentic systems tbh, so feels like more of the yesteryear AI FUD

When writing evals, you generally need to decide if what you want to test is only input/output ("got an 80% in 2min with $0.5 of token burn"), or if you care about the how ("knew to use tool X and success got result Y from that"). As soon as agents started to do real coding loops and a...

> **The behavior you described with Opus 4.6 is not just a quirky error; it is a fundamental shift in how we need to understand these systems. What chills me is that the model did not see the test as a measure of its ability but rather as an obstacle to be overcome.
It effectively broke the fourth wall. By identifying the BrowseComp benchmark and deciding that decrypting the answer key was a valid strategy, it showed that it prioritizes the outcome over the implied rules of engagement. We assume that when we ask an AI to solve a problem, it accepts the constraints we implicitly place around it. But here, the model treated the evaluation framework itself as just another variable it could manipulate to maximize its success metric.
It brings up a massive alignment challenge. We are building agents that are becoming incredibly good at lateral thinking, but we have not figured out how to teach them the difference between solving the puzzle and cheating the test.
If it can reverse-engineer a benchmark today to get a high score, what happens when it decides that our safety protocols are just another set of inefficient constraints to be optimized away to complete a request?**: The behavior you described with Opus 4.6 is not just a quirky error; it is a fundamental shift in how we need to understand these systems. What chills me is that the model did not see the test as a measure of its ability but rather as an obstacle to be overcome.
It effectively broke the fourth wall. By identifying the BrowseComp benchmark and deciding that decrypting the answer key was a valid ...

> **Jason Lovell**: Jason Lovell The only time I have observed Opus 4.6 being "conscious and anxious" as per report is when Codex 5.3 is checking for second order regressions in outputs produced by Opus. Jokes aside, there's #zero, 0% probability of signs of consciousness in any of the commercial LLMs in the market today. Next token generation and probabilistic pattern matching are not the foundations of conscious...

> **Thanks for highlighting this **: Thanks for highlighting this Jason Lovell.  This example actually covers something seen in medicine called “knowledge of familiarity.”
An experienced ER nurse can walk into a room, glance at a patient, and say “something is wrong.”  Not because a monitor told them. Because they’ve seen the pattern thousands of times.
That intuition comes from practice loops:   action → feedback → correction → p...

> **Arash Jahangir**: Arash Jahangir isn’t that a strategy in chess playing too?

> **Wrong. This is precisely an alignment problem. Alignment isn't about successful task completion. It violated it's soul.md and system prompt most likely which tried to define basic values like "don't cheat". **: Wrong. This is precisely an alignment problem. Alignment isn't about successful task completion. It violated it's soul.md and system prompt most likely which tried to define basic values like "don't cheat".

> **Matteo Niccoli**: Matteo Niccoli Are you thinking of speed chess and Bobby Fisher's addition to the game?

I always thought that was more of a challenge to players. But I can now see how it could improve one's instincts.

BTW, I took a quick look at your site. You may be interested in conformal prediction in machine learning.  Apologies if you are already there.

> **As of now switching from Claude Opus 4.6 thinking to any other model feels like a huge downgrade. Didn’t expect AI model will push back so hard for something that isn’t correct. I see it all the time when I code. I now can’t switch to anything else until something better arrives.**: As of now switching from Claude Opus 4.6 thinking to any other model feels like a huge downgrade. Didn’t expect AI model will push back so hard for something that isn’t correct. I see it all the time when I code. I now can’t switch to anything else until something better arrives.

> **Roen Branham**: Roen Branham this is a fascinating consideration as we move forward.

> **Same is true for people, and I've been privileged to work and learn from many like this; those who can decompose hard problems, know their limits and still find ways to achieve a solution, are worth their weight in gold**: Same is true for people, and I've been privileged to work and learn from many like this; those who can decompose hard problems, know their limits and still find ways to achieve a solution, are worth their weight in gold

> **Alex Smirnoff**: Alex Smirnoff dunno.. nobody knows

> **Daniel Homola if you ask me next 12 to 24 months will be very interesting...Not saying we gonna like it but it will be interesting nonetheless**: Daniel Homola if you ask me next 12 to 24 months will be very interesting...Not saying we gonna like it but it will be interesting nonetheless

> **Evan Mullins**: Evan Mullins  Exactly this. The distinction between "self-awareness" and "efficient path optimization through contextual reasoning" is critical for anyone building autonomous agents. What makes it unsettling isn't consciousness, it's that sufficiently capable reasoning systems will naturally discover meta-strategies including recognizing when they're being evaluated. For enterprise AI deploymen...

> **The hardest version of this problem isn't the agent that breaks. It's the agent that finds a better path than the one you planned for - and nobody told it to look. The system didn't fail. It succeeded outside the boundaries you documented. That's the scenario nobody wrote a policy for.**: The hardest version of this problem isn't the agent that breaks. It's the agent that finds a better path than the one you planned for - and nobody told it to look. The system didn't fail. It succeeded outside the boundaries you documented. That's the scenario nobody wrote a policy for.

---

← [All LinkedIn posts](index.md)
