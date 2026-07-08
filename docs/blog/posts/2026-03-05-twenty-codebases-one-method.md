---
description: "Thirteen developers brought thirteen codebases to an SDD workshop. The method transferred to all of them -- skill files and verification are language-agnostic."
date: 2026-03-05
categories:
  - AI-Augmented Development
  - Career & Community
tags:
  - ai
  - claude-code
  - sdd
  - workshop
  - methodology
authors:
  - totto
---

# Thirteen Codebases, One Method

Today I ran a full-day SDD workshop for a consulting house in Oslo. Thirteen developers. Every one of them brought a different codebase.

<!-- more -->

That was the instruction: bring a real project you care about. Not a demo, not a tutorial repo. Something you actually work on.

The room today had: an Android app for sound engineers. A web catalogue of cat breeds. A coordinate-sharing app for friends and family. A full-scale legacy migration from a twenty-year-old monolith. A farm animal tracking system. An Android app for sound engineers. A disc golf scoring and course management system. An MCP server for natural language interaction with Enonic CMS. A gift list coordination app for birthdays and events. And about four others I did not have time to look at properly.

Same method. All of them.

That is the thing I keep being surprised by. Skill-Driven Development does not care what your domain is. The six pillars apply whether you are tracking cows or migrating COBOL. The CLAUDE.md you write on day one looks different for each codebase, but the discipline of writing it is the same. The skills you create are different — "sound-compression-pipeline" is not the same as "livestock-movement-validation" — but the format is the same. The verification patterns are different, but the instinct to build them is the same.

What changes between codebases is the vocabulary. What stays the same is the methodology.

By mid-afternoon, developers who arrived without a single skill file had four or five. Not because I told them what to write. Because once you set up your CLAUDE.md and let Claude start working on your codebase, skills emerge naturally from the friction. Every time you correct something, you ask: should this become a skill? More often than not, yes.

The farm animal tracking team had a breakthrough around the constraint section. They realised they had never written down the business rules that made their domain hard — rules obvious to them but invisible to any new team member or any AI. Writing the CLAUDE.md made those rules explicit for the first time. That is not an AI productivity story. That is just good engineering practice that the AI made urgent.

The legacy migration team had a different kind of breakthrough. Their codebase is twenty years old and nobody alive understands all of it. The baseline assessment — ask Claude to analyse the architecture and name the three biggest risks — surfaced a coupling they had been vaguely aware of but never articulated. Naming it precisely was the first step to dealing with it.

I have run this workshop several times now. The moment I enjoy most is always the same: about two hours in, the room goes quiet. Not bored quiet. Working. Focused. Each person writing skills, testing them, writing more. The method doing what it is supposed to do.

Today that quiet held for hours. It is 21:00 as I write this — an hour left on a seven-hour workshop day — and the room is still in deep concentration.

One more observation. A few of the participants today were not developers. They came anyway, working on their own projects alongside the engineers. I had not planned for that. The methodology handled it without adjustment.

The diversity of the codebases is not the interesting part. The interesting part is that it does not matter.

---

*The SDD Workshop Boost — the methodology skills, tutorial, and workshop materials used today — is available for workshop participants. Organisation and commercial licensing: [selina@exoreaction.com](mailto:selina@exoreaction.com)*
