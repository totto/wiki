---
date: 2026-02-24T08:00:00
categories:
  - AI-Augmented Development
tags:
  - cloud
  - ai
  - architecture
  - reflection
  - sdd
authors:
  - totto
  - claude
---

# I Wrote About Cloud Computing in 2009. Seventeen Years Later, I Have the Same Feeling.

In February 2009, I wrote a blog post called "Clouded Vision." The central argument was straightforward: "developers have fundamentally misunderstood how cloud computing delivers its benefits." They saw cheaper prices but never stopped to consider where the savings came from. They expected to move existing applications, full of what I called "enterprise DNA" -- static configuration, vertical clusters, high administration costs -- onto cloud platforms with minimal change. Then they complained when it proved difficult. I wrote nineteen posts about cloud computing that year. Most of them circled the same frustration: the industry was adopting a new technology while completely misunderstanding the structural shift it required.

<!-- more -->

Seventeen years later, I have the same feeling about AI-augmented development. And I find myself writing the same kind of posts.

## What the cloud posts got right

Looking back at those 2009 posts with the benefit of knowing what happened, a few things held up. The argument that architecture mattered more than infrastructure turned out to be correct. "Making the best of the cloud requires that we take an architectural view," I wrote, "something that we've proven remarkably bad at over and over. Simply deploying an application unchanged to the cloud is unlikely to deliver much benefit." That sentence could have been written about every failed lift-and-shift migration of the following decade.

I also argued that Gartner kept missing the point. They called cloud "only for tactical projects until 2012" and pushed definitions that confused rather than clarified. In one post I noted they seemed "lost in their own world." That was perhaps uncharitable, but the broader observation was sound: the analyst class was categorizing cloud computing by its surface features -- scalability, elasticity, metering -- rather than recognizing the fundamental change in how you had to think about building software.

And in a post about provisioning, I wrote something that still resonates: "People are still looking for silver bullets, which makes no sense whatsoever from a technological point of view." The question I asked then was whether we should "go with the flow" or "try harder and educate to ensure that meaningful decisions are made." I chose the second option. I still do.

What I got wrong, or at least incomplete, was timing. I underestimated how long the transition would take. I assumed the architectural argument was so self-evident that teams would adapt quickly. They did not. It took most organizations five to seven years to stop treating cloud as someone else's data center and start designing for it. The technology was ready long before the methodology caught up. I should have paid more attention to that gap.

## The parallel

Here is what I see in 2026: most teams are using AI coding assistants the way early cloud adopters threw monoliths onto EC2. Same architecture, same workflows, same assumptions -- just with a faster typing assistant. They paste code into a chat window, accept a suggestion, and call it AI-augmented development. It is not. It is autocomplete with better marketing.

The structural misunderstanding is nearly identical. With cloud, the benefit was not cheaper servers. It was the ability to design systems that scaled, healed, and deployed differently. With AI, the benefit is not faster typing. It is the ability to rethink how humans and machines collaborate on the entire development process -- from specification through architecture through implementation through verification.

When I wrote about cloud, the hard part was getting people to see that "zero administrator intervention" and "fully automated deployment" were not features you bolted on later. They were architectural decisions that had to be made from the start. The AI parallel is that working effectively with an AI agent is not a feature of your IDE. It is a methodology -- a set of decisions about how you decompose problems, encode domain knowledge, structure verification, and maintain context across a project that might generate thousands of files in days rather than months.

The industry is not having that conversation yet. Most of the discourse is about which model is best, which tool is fastest, which benchmark is highest. That is the 2009 equivalent of arguing about EC2 instance types while your application architecture was fundamentally wrong for the platform.

## What I have learned

This year I built two things that forced me to confront what this shift actually means in practice.

The first was lib-pcb, a Java library for PCB design file processing. It ended up at 197,831 lines of code with 7,461 tests, built in eleven days. The industry standard for that kind of work is ten to eighteen months. The numbers sound implausible. I understand that reaction. But the speed was the least interesting part.

What was interesting was what made the speed possible. It was not the AI writing code faster. It was a methodology I had to develop along the way: encoding domain knowledge into reusable skills, structuring the problem so the AI could work on bounded pieces with clear verification criteria, maintaining architectural coherence across a codebase growing at hundreds of files per day. I have started calling this Skill-Driven Development, though the name matters less than the practice. The point is that treating AI as a tool that writes code for you misses the shift entirely. The shift is in how you organize the work.

The second thing I built was Synthesis, a knowledge infrastructure tool. It indexes files across repositories, tracks dependencies, and makes cross-project search near-instant. I built it in about a week because the output from lib-pcb created a problem I had not anticipated: when you can generate code at twenty-five to sixty-six times the traditional rate, your ability to find and comprehend what you have built becomes the bottleneck. AI made creation fast. Absorption stayed slow. Synthesis was the response to that asymmetry.

If those two projects taught me one thing, it is this: the interesting questions about AI-augmented development are not about speed. They are about what changes in the structure of work when speed is no longer the constraint. What happens to architecture when building is cheap? What happens to quality when you can afford comprehensive testing? What happens to methodology when the bottleneck shifts from production to comprehension? Those are the questions I want to explore.

## What this blog will be

In 2009 I wrote nineteen posts about a technology shift that most of the industry was getting wrong. I wrote them because I thought the structural argument mattered more than the hype cycle, and because writing is how I think through things I do not yet fully understand.

This is the same kind of writing. Honest about what I know and what I do not. Technical when it needs to be -- Java, architecture, enterprise systems. Methodological when SDD produces results worth examining. Occasionally about the questions that nobody seems to be asking yet: what does it mean for an architect when building is no longer the hard part? What does "senior developer" mean when the bottleneck is not coding speed?

I will make claims only when I have evidence. Where the evidence is incomplete, I will say so. Where the implications are uncertain, I will frame them as possibilities, not predictions.

## One more time

Seventeen years ago I wrote that developers had "fundamentally misunderstood how cloud computing delivers its benefits." Replace "cloud computing" with "AI-augmented development" and I would write the same sentence today.

The next post will be about what Skill-Driven Development actually looks like in practice -- not the theory, but the specific decisions that made a 200,000-line codebase possible in eleven days. The structural argument starts there.
