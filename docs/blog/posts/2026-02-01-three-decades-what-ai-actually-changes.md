---
date: 2026-02-01
categories:
  - AI-Augmented Development
tags:
  - ai
  - architecture
  - career
  - java
  - methodology
  - reflection
authors:
  - totto
  - claude
---

# Three Decades of Architecture: What AI Actually Changes (And What Doesn't)

I have been writing software and designing systems since 1994. That is thirty-two years. Long enough to have watched several waves arrive with the promise that everything was about to change, and long enough to have noticed that the pattern of arrival is remarkably consistent. Breathless proclamation. A period of confusion as people try to apply old practices to new technology. Then a gradual, quieter recognition of what actually changed and what did not.

<!-- more -->

I am watching the pattern again now. And because I have seen it before, I find myself less interested in the proclamation and more interested in the recognition.

## The pattern

Object orientation and Java changed how we structured code. Classes instead of procedures, inheritance instead of copy-paste, garbage collection instead of manual memory management. I was at NTNU in the mid-nineties when this shift was happening, and the conversations were intense. People genuinely believed that OO would eliminate entire categories of software failure. It did eliminate some. Buffer overflows became less common in Java. Resource leaks became easier to manage. But good naming, cohesive modules, and the discipline of handling failure gracefully did not change. The teams that wrote unclear procedural code wrote unclear object-oriented code. The structure of the code changed. The quality of thinking behind it did not.

Cloud computing changed how we operated systems. I wrote nineteen posts about it in 2009, arguing that the industry was fundamentally misunderstanding where the benefit came from. The benefit was not cheaper servers. It was the ability to design systems for automated deployment, horizontal scaling, and zero administrator intervention. But system design, data consistency, and failure modes did not change. A distributed system on EC2 failed in the same ways as a distributed system in a data center. The deployment model changed. The engineering required to handle failure did not.

Microservices changed how we decomposed systems. The promise was organizational: small teams owning small services. The reality was that boundaries still needed to make sense, and distributed systems had distributed failure modes. I watched organizations decompose monoliths into microservices without changing their understanding of domain boundaries, and end up with a distributed monolith that was harder to debug than the original.

Each wave changed something real. Each wave left something important unchanged. The changed thing got all the attention. The unchanged thing determined who succeeded.

## What AI does not change

### Architecture judgment

Architecture is the set of decisions that are hard to reverse. When I chaired sessions at IASA, this was the working definition we kept returning to.

What has changed is the consequence. When building is cheap, the cost of a bad architectural decision increases. You can build more on top of a wrong foundation, faster. A team that chooses the wrong decomposition strategy can now generate thousands of lines of code against that wrong decomposition in days instead of months.

The judgment to recognize which decisions are architectural, and therefore deserve careful thought before the AI starts generating code, has not changed. If anything, it is more important. When building was slow, bad architectural decisions were self-limiting. You discovered the problem before you had built too much on top of it. When building is fast, you can be three layers deep before you notice the foundation is wrong.

### Domain expertise

The AI does not know what correct means for your domain. I learned this concretely during the lib-pcb build. Claude could generate a Gerber parser that compiled, passed unit tests, and looked syntactically clean. But whether the bounding box calculation handled the case where a manufacturer embeds title blocks in documentation layers, inflating the apparent board size to twice its actual dimensions, that required knowing how manufacturers actually produce files. The source of that knowledge has not changed. It comes from time spent in the domain.

### Reading critically

The ability to read code and see what is wrong with it. Not just what it says, but what it does not handle. When code can be produced faster than it can be read, the ability to read well becomes the constraining skill. During lib-pcb, I spent more time reading AI-generated code than directing the AI to write it. That ratio was not a failure of the process. It was the process working correctly.

### Writing clearly

Requirements, design decisions, architectural reasoning. Writing clearly enough that another person, or an AI, can understand and act on your intent. AI makes ambiguity more expensive, not less. A vague requirement in a five-month project wastes days as the team converges on what was meant. A vague requirement in an eleven-day AI-assisted project wastes days and hundreds of generated files, because the AI will confidently build exactly what you said, which is not what you meant.

I encode domain knowledge in skill files now. Writing a good skill file is an exercise in precision. Every ambiguous phrase becomes a wrong implementation. The discipline of clear writing has not changed. The cost of unclear writing has gone up.

## What AI does change

### The cost of trying something

Before AI, experimenting with an architectural approach cost weeks of implementation. After AI, the same experiment costs hours. This changes how you think about options.

During lib-pcb, I tried three different approaches to coordinate transformation before settling on the one that handled all the edge cases. In a traditional timeline, I would have chosen one approach based on analysis and committed to it. The ability to try all three and evaluate them against real manufacturer files was a genuine change. Not in what good architecture looks like, but in how many options you can evaluate before committing.

### The economics of craftsmanship

Comprehensive testing used to be expensive. Thorough documentation used to be expensive. Refactoring used to be expensive. All of these are now affordable at scales that were not previously viable.

lib-pcb has 7,461 tests. In a traditional eleven-day sprint, you might write a few hundred if you were disciplined. The AI made it possible to be thorough in a way that was previously reserved for projects with large teams and long timelines. The craft of software development can now be practiced more completely. That is a real change, and I think it is underappreciated. Most of the conversation about AI is about speed. The more interesting change is about quality.

### The bottleneck

For thirty years, producing code was the constraint. The people who could produce more, faster, were more valuable. I built a career partly on that. At JavaZone, the talks that drew the biggest audiences were about writing better code faster.

That constraint has shifted. The bottleneck is now comprehension, architecture, verification. The skills that matter for being effective have changed, not from technical to non-technical, but from production to judgment. I wrote about this in [What Senior Developer Means Now](2026-02-15-what-senior-developer-means-now.md), and I think it is the most consequential change for individual careers.

### The team composition question

If production speed has increased tenfold, the questions about who does what on a team have shifted. Not "AI replaces developers." The question is what the best developers spend their time on when implementation is no longer the bottleneck. More architecture review. More domain modeling. More verification design. Less typing. I do not know exactly where this lands. But the direction is clear.

## Both directions

Here is the part I find most interesting, and the part I am most honest about not fully understanding yet.

AI accelerates in both directions. It lets you test more hypotheses, practice craftsmanship more completely, evaluate more architectural options. It also lets you accumulate architectural debt faster, ship convincing-looking incorrect code faster, and produce systems you do not fully understand faster.

The tools are neutral. The methodology is not.

I have watched this dynamic before. Cloud made it easier to deploy resilient, auto-scaling systems. It also made it easier to deploy fragile, expensive systems that looked modern. Microservices made it easier to build loosely coupled services. They also made it easier to build distributed monoliths with network latency. The technology enables. The methodology determines which direction.

## What I know and what I do not

I know the pattern. I have watched it four times now. The surface changes. The underlying discipline does not. Object orientation did not make bad designers good. Cloud did not make fragile systems resilient. Microservices did not make tangled domains clean. AI does not make shallow thinking deep.

What I do not know is how far this particular wave goes. The acceleration is real. I have the commit logs and the timelines. But whether this is a 10x change or a 100x change over the next decade, I genuinely cannot say. Anyone who claims certainty about that is extrapolating further than the evidence supports.

What I can say, from thirty-two years of watching these waves, is that the people who focus on what does not change tend to do better than the people who chase what does. Architecture judgment, domain expertise, critical reading, clear writing. These were valuable in 1994. They are valuable now. They will be valuable after whatever comes next.

The tools change. The work changes. The thinking that makes the work good does not change as much as the tools suggest it should.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series. Previous entries: [Cloud to AI](2026-02-24-cloud-to-ai-same-feeling.md), [Fear-Driven Development](2026-02-23-fear-driven-development.md), [Building Together](2026-02-22-building-together-11-day-ai-collaboration.md), [Five Superpowers](2026-02-21-five-superpowers-java-developers.md), [The Architecture Mistake](2026-02-19-architecture-mistake-cloud-to-ai.md), [The Hallucination Tax](2026-02-17-the-hallucination-tax.md), [What Senior Developer Means Now](2026-02-15-what-senior-developer-means-now.md), [Six Pillars](2026-02-13-six-pillars-200k-lines-11-days.md), [The Mirror Test](2026-02-11-the-mirror-test.md), [Exploration Beats Specification](2026-02-09-exploration-beats-specification.md), [What a Skill Actually Is](2026-02-07-what-a-skill-actually-is.md), [The Comprehension Bottleneck](2026-02-05-the-comprehension-bottleneck.md).*
