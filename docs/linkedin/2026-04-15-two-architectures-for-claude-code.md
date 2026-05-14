---
tags:
  - LinkedIn
  - Writing
date: 2026-04-15
---

# Two Architectures for Claude Code

*April 15, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7450169281419448320)*

**37 reactions · 7 comments · 4,293 views**

---

A repository called claude-code-best-practice hit #1 on GitHub this week. 19,700 stars. Boris Cherny — who created Claude Code — plus  contributions from the Anthropic team. Eighty-four concrete patterns: subagents, hooks, orchestration chains, parallel agents with tmux and git worktrees, autonomous retry loops, cross-model adversarial review.

It deserves the attention it's getting.

It also made something visible I hadn't articulated before.

The ExoCortex — my Claude Code setup, running for ten-plus weeks across 289 repos — solves many of the same problems from a fundamentally different direction. Two practitioners working independently on making Claude Code reliable at scale. Two different answers.

The divergence point is one question: is memory a configuration problem or an infrastructure problem?

Their answer: configuration. CLAUDE.md files, skills, hooks. Text files you manage. It works.

My answer: infrastructure. Synthesis indexes 65,905 files and scores them behaviourally. topic-health detects when knowledge goes cold. A nightly cycle keeps it from rotting while I sleep. Because at 289 repos, the knowledge surface area exceeds what any individual can manually maintain.

The repo documents LLM degradation as a known problem. Their own memory model degrades the same way. They have no maintenance story for it.

What I learned from theirs: formalized orchestration chains, parallel agent dispatch, the autonomous retry loop, RPI with explicit GO/NO-GO gates. Real gaps. Each one has cost me time.

What they're missing: push-based context injection (53–80% fewer tool calls), semantic memory infrastructure, expert lens skills that change how the model reasons rather than what it does, and RTK — a token filter proxy achieving 60–90% savings on common operations, transparently.

The sharpest finding: both setups independently converged on hooks as the highest-leverage primitive. Not the model, not the prompts, not even the skills. What you inject before the agent thinks and what you intercept after it acts.

Neither setup dominates. The interesting work is in the merge.

---

## Discussion

> **Totto** ↩: Full blogpost:  https://wiki.totto.org/blog/2026/04/15/two-architectures-for-claude-code-what-19700-stars-got-right-and-what-they-missed/

> **I have reached the same conclusion as you. A brain with indexed thoughts, semantic and direct linking, implicit and explicit clusters, automatic decay or graduation. 

Trying to compensate for my own brain that unfortunately over-emphasizes decay 😑**: I have reached the same conclusion as you. A brain with indexed thoughts, semantic and direct linking, implicit and explicit clusters, automatic decay or graduation. 

Trying to compensate for my own brain that unfortunately over-emphasizes decay 😑

> **Totto** ↩: Marius Waldal 
The biological parallel is exact — and I think it's not accidental.                             
          
 Synthesis scores behaviorally (how often something gets accessed, in what context, by what kind of question). topic-health  detects when a knowledge cluster stops being referenced and flags it for review. The nightly maintenance cycle either refreshes or archives.

 That's...

> **Totto** ↩: Thor Henning Hetland And for those who do not know me - I've naturally added the high value stuff from the claude code best practises into ExoCortex :P

> **"My own brain over-emphasizing decay" refers to my physical human brain, and is an unfortunate effect of the convergence of me getting older (which AI so far is not helping me counteract) and my ADHD diagnosis 🙃

Through the years, so much of my energy has gone towards compensating for this with routines, lists, calendars, reminders, archives, etc. Reducing the fallout, yes, but far from sufficiently compensating. 

Not until the emergence of AI have I had a tool that I can mold in a way that promises a potential of *actual* compensation. So, for me, this started as a highly personal endeavor, but the interesting side-effect is that, as you point out, there is a clear parallel between my "mental limitations" and the limitations of agents. So by building a second brain that helps me as a human being, I inadvertently also built a system that turns out to be quite a good fit for agents. 

So I am working on two fairly parallel systems: agent memory and Marius extra-memory 😃

To your question specifically: MY decay issue is fairly domain agnostic. And I don't have enough empirical evidence yet answer that question re agents.**: "My own brain over-emphasizing decay" refers to my physical human brain, and is an unfortunate effect of the convergence of me getting older (which AI so far is not helping me counteract) and my ADHD diagnosis 🙃

Through the years, so much of my energy has gone towards compensating for this with routines, lists, calendars, reminders, archives, etc. Reducing the fallout, yes, but far from suffic...

> **I have also reached the same conclusion. The convergence on hooks as the key primitive is the most reliable signal here. AI models when relying on trust based or honesty based systems in my experiments fail more than 50%, no matter how many .md or instructions you feed. Hooks + formal rules with clear pass/fail/exit criteria is the only thing you can reliably trust **: I have also reached the same conclusion. The convergence on hooks as the key primitive is the most reliable signal here. AI models when relying on trust based or honesty based systems in my experiments fail more than 50%, no matter how many .md or instructions you feed. Hooks + formal rules with clear pass/fail/exit criteria is the only thing you can reliably trust

> **Fadi Labib**: Fadi Labib True. AI systems need determinism, and since the models are inherently non-deterministic, we as architects need to insert determinism as gates in the system. The inclination to do everything with AI seems to be strong, but there are a lot of places where just "old-fashioned" code is the right choice.

---

← [All LinkedIn posts](index.md)
