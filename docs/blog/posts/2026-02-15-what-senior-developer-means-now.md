---
date: 2026-02-15
categories:
  - AI-Augmented Development
tags:
  - ai
  - architecture
  - senior-developer
  - methodology
  - sdd
  - career
authors:
  - totto
  - claude
---

# What "Senior Developer" Means When AI Can Code

There is a narrative forming in the industry that goes something like this: AI will replace junior developers, senior developers will become more valuable, and if you have enough experience you have nothing to worry about. I think this misreads what is actually happening. The shift is real, but it is not the one most people describe.

<!-- more -->

For thirty years, the bottleneck in software development has been production. Writing the code. Senior developers were valuable because they could produce more, faster, and with fewer defects. They knew the frameworks. They could hold complex systems in their heads. They had built enough things to avoid the obvious mistakes.

That bottleneck is moving. AI can now produce code at a rate that would have been unimaginable five years ago. When I built lib-pcb, a PCB manufacturing library, in eleven days, the constraint was never "can the AI write Java fast enough." The constraint was whether I could understand, verify, and direct what was being produced. The bottleneck had shifted from production to comprehension.

This changes what "senior" means. Not in the way the reassuring narrative suggests.

## The skills that do not depreciate

Some skills become more valuable when production is cheap. Architecture is the clearest example. When building something takes months, you get one shot at the architecture. When building something takes days, you can try multiple approaches and evaluate which one actually works. The person who can look at three implementations and say "this one handles the edge cases the others miss" is more valuable than before, because there are more options to evaluate.

Domain expertise is another. During the lib-pcb build, Claude could generate Gerber parsing code that compiled, passed basic tests, and looked correct. But it could not know that some manufacturers embed title blocks and dimension tables in documentation layers, and that including those layers in bounding box calculations will produce board dimensions twice the actual size. That knowledge came from parsing real manufacturer files and discovering the failure.

Critical reading may be the most important skill now. The ability to read code you did not write and know when it is wrong. Not "does this compile" but "does this match the domain, and what failure modes is it not handling." I spent more time reading AI-generated code during lib-pcb than directing the AI to write it. That ratio surprised me.

And underneath all of these: knowing what to verify. You cannot test everything. The judgment to identify which invariants matter, which edge cases are likely, which component interactions are risky. That judgment comes from having shipped software and watched it fail in specific ways.

## The skills under pressure

Other skills are losing their differentiating power. Typing speed and boilerplate fluency matter less when the AI writes boilerplate faster than you can think about it. "I can set up a Spring Boot service from scratch" is still useful, but it no longer separates a senior developer from someone with six months of experience and a capable AI assistant. Memorizing framework APIs is increasingly pointless when the AI has the same documentation and applies it more consistently.

This is uncomfortable for people whose seniority was built on accumulated implementation knowledge. Knowing every annotation in the Spring ecosystem was genuinely valuable when the bottleneck was writing correct Spring code. It is less valuable when the bottleneck is deciding whether Spring is the right choice for this problem.

I want to be honest about the discomfort, because I have felt it. There is a moment, watching the AI produce in minutes what would have taken you hours, where your sense of professional identity shifts. I wrote about this in a previous post as Fear #5: "Am I still a developer if the AI is doing the thinking?" The answer I found was yes, but the nature of the work changed. The thinking moved from implementation to direction, verification, and judgment.

## What "senior" will actually mean

If I had to describe the senior developer of 2029, it would not be "this person can produce code faster than anyone on the team." It would be closer to:

This person can encode domain knowledge so the AI applies it correctly. They can evaluate AI output against domain reality, not just syntactic correctness. They can make architectural decisions when building is cheap, which means considering more options and choosing with more rigor. They can see the failure modes that are not represented in the test suite.

In my methodology, encoding domain knowledge takes the form of skill files: structured documents that teach the AI specific domain concepts and constraints. Writing a good skill file requires deep understanding of the domain. You cannot write a skill for Gerber format parsing unless you understand aperture definitions, step-and-repeat patterns, and the ways manufacturers deviate from the specification. The skill authoring process forces domain expertise. It does not replace it.

The evaluation piece is equally demanding. When I review AI-generated code, I am not checking syntax. I am checking whether the logic matches how PCB manufacturing actually works. Does this validator correctly implement the IPC-6012 minimum annular ring requirement? Does this auto-fixer preserve design intent while fixing the spacing violation? Those questions require domain understanding the AI does not have.

## The uncomfortable transition

Here is what lib-pcb taught me about this shift, concretely.

Eleven days. 197,831 lines of Java. But the work was not writing Java. The work was knowing what a correct PCB parser looks like. Knowing that Excellon drill files can use both leading-zero and trailing-zero suppression, and that confusing them produces drill holes in the wrong locations by orders of magnitude. Knowing that when the bounding box calculation returned 425mm for a board that should have been 216mm, the problem was a documentation layer with inflated coordinates, not a math error.

That knowledge did not come from prompting. It came from reading format specifications, debugging coordinate system mismatches, parsing files from six different manufacturers and discovering that they all interpret the "standard" differently.

The transition is uncomfortable because it redefines what experience is for. It is no longer primarily for producing code. It is for understanding the domain deeply enough to direct and verify what the AI produces. The experience still matters. What it is used for has changed.

## The bar is rising, not falling

There is a version of this argument that says AI will lower the bar, that anyone can produce software now. I think the opposite is true for work that matters.

You cannot verify what you cannot understand. An AI-assisted developer who does not understand their domain will make incorrect decisions about what to verify, miss real bugs, and ship plausible-looking software that fails in production. The AI produces code faster than you can verify it if your domain understanding is shallow.

The floor is rising, yes. You no longer need to write a SAX parser from memory. But you need to understand XML parsing well enough to catch when the AI's entity handling is vulnerable to XXE attacks. You need to understand HTTP well enough to spot a timing side-channel in authentication middleware. The junior developer of 2029 will produce more code than the senior developer of 2019. But the senior developer of 2029 will need to understand systems more deeply than either of them.

## I have seen this pattern before

In 2009, cloud computing created a similar structural shift. The people who understood server administration -- racking hardware, configuring networks, managing storage -- saw their differentiating skills erode. Not overnight, but steadily. The people who understood distributed systems architecture became more valuable. The bottleneck moved from infrastructure management to infrastructure design.

The parallel is not perfect, but the pattern is recognizable. When a technology makes one part of the work cheap, the adjacent skills that were previously less visible become the constraining factor. Cloud did not make operations people obsolete. It changed which operations skills mattered. AI is not making developers obsolete. It is changing which development skills matter.

I got the timing wrong with cloud. I thought the transition would be fast. It took most organizations five to seven years. I suspect the AI transition will be faster, because the feedback loop is shorter. But I do not know exactly where this lands in five years. Anyone who claims certainty about that timeline is selling something.

## What I would tell a senior developer today

Do not optimize for writing code faster. Optimize for understanding your domain more deeply. The developers who will thrive are the ones who can explain why the AI's output is wrong, not just that it compiles and passes tests. Invest in architecture, in domain knowledge, in the ability to read code critically.

And invest in encoding what you know. The implicit knowledge in your head -- the conventions, the edge cases, the reasons behind architectural decisions -- is more valuable now than it has ever been, precisely because it is what the AI does not have. Making it explicit, structured, and reusable is the highest-leverage activity a senior developer can do today.

The title has not changed. What it means has.

---

*This is the sixth post in the "[AI-Augmented Development](/blog/category/ai-augmented-development/)" series. Previous posts covered the [cloud-to-AI parallel](/blog/2026/02/24/i-wrote-about-cloud-computing-in-2009-seventeen-years-later-i-have-the-same-feeling/), [fear-driven development](/blog/2026/02/27/im-scared-of-ai-thats-why-it-works/), the [architecture mistake](/blog/2026/03/11/the-architecture-mistake-cloud-taught-us-that-were-making-with-ai/), and the [hallucination tax](/blog/2026/03/13/the-hallucination-tax-three-more-fears-that-made-my-ai-workflow-better/). All observations are grounded in building [lib-pcb](https://github.com/exoreaction/lib-pcb), a 197,831-line PCB manufacturing library, in 11 days.*
