---
tags:
  - Writing
  - AI
---

# LinkedIn Writing

Selected posts from [LinkedIn](https://www.linkedin.com/in/hetland/), November 2025 – February 2026.

These are shorter-form pieces written in parallel with the [blog series](/blog/) — same period, different format. LinkedIn posts tend to be more immediate: reactions to something that just happened, a question still open, a pattern noticed mid-build.

---

## November 2025

### Mastering Deadlines: The 80/50 Rule
*November 10, 2025*

In 2017, I wrote a short piece out of frustration — a kind of street-smart survival guide for developers tired of missing deadlines. This week, I thought it would be fun going all-in GenAI on it, so I got GPT-5 do some deep research, and had NotebookLM explain things. I made a short video about it — mostly for myself, but maybe it's useful for others too. Would love to hear if this resonates with you — or what's worked (or failed) in your own experience.

---

## January 2026

### AI Testing Discipline: Reality-Based QA
*January 23, 2026*

Hook: "6 days vs 9 months."

Unit tests only confirm the code does what you *think* it should do. They don't test reality.

Initially, all unit tests passed. Reality check: only 25% success rate against real legacy files. After battle testing with 195 of the messiest real-world files: 93% success rate. 5,000+ tests exist because of edge cases found in real data.

### Workshop Interest
*January 25, 2026*

I'm planning a small, focused workshop in late February for developers interested in building production systems with Claude Code.

Not a talk. Not a demo. Working sessions where we tackle real verification problems, build actual testing frameworks, and figure out how to trust AI output in production.

The focus:

- Building guardrails that actually work
- Verification patterns for different domains
- Testing strategies that scale
- Working on YOUR code, not toy examples

This would be founding cohort stuff — you'd help shape what this becomes.

If you're working with Claude Code (or want to), and you have a specific pain point around trusting AI output, I'd love to hear:

- Your tech stack (1-2 words)
- Your verification challenge (1 sentence)

---

## February 2026

### Day 5: Knowledge Infrastructure
*February 4, 2026*

Day 5 of an experiment. Starting to think this might actually work.

Context: When I built lib-pcb (197,831 lines in 11 days), I proved something about AI-assisted development. Now I'm trying something similar — but for knowledge management.

The challenge: Years of work across projects, clients, frameworks. Fast creation, but the organizing and connecting? Falling behind.

This week, Claude Code and I have been building a self-learning system for this.

Current state:

- 1,070 documents organized with business context
- 3,536 directories structured by concept and purpose
- Cross-referencing system connecting related work
- Methods captured as reusable skills (system learns as we work)

It's starting to feel like lib-pcb did around day 5.

But the hard parts are ahead: How do I make this a *foundation* across multiple companies and activities? How do I make it *available* to the people who need it? How do I scale to the *daily velocity* of what I produce?

Those are different problems than "organize what exists."

Early days. The pattern recognition is working. The system is learning.

Anyone else working on knowledge infrastructure at this scale?

### Velocity Reflection
*February 6, 2026*

Three weeks at this velocity.

It's exhilarating and intense in ways that are hard to articulate. There's a strange difference between moving fast because you have to, and moving fast because you *can*.

I'm still adjusting. Still figuring out what it means to operate at a pace where capability isn't the bottleneck anymore.

### Synthesis: Looking for Pilot Partners
*February 12, 2026*

![Synthesis pilot announcement visual](/assets/images/linkedin/synthesis-pilots-visual.png)

We built something for ourselves. Turns out others might need it too.

**What it is:** Synthesis. Think of it as an AI operations partner for knowledge infrastructure.

**The problem it solves:** You're using AI to code/write/analyze faster. Great. But now you produce 10-20x more files/docs/screenshots than before. And you can't find anything when you need it.

**What it does:**

- Organizes work as you create it (5 seconds vs 2 hours later)
- Makes everything discoverable ("I need the demo for feature X" → found in 30 seconds)
- Maintains knowledge infrastructure at AI velocity

**Proof (our own use):** Last week: 1,690 unorganized screenshots. Client demo? Impossible. This week: 9 comprehensive workflows documented. 64,000 words. Fully indexed. Find anything in under a minute. Time invested: 48 hours organization. ROI: Can now prepare any client demo in 5 minutes vs 30.

Looking for 3–5 curious early adopters — people who geek out about knowledge infrastructure, not just AI speed.

→ [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

### Reflecting on How We Build Teams
*February 13, 2026*

Coffee with a former collaborator. He asked a question I hadn't really thought through: "Looking at what we built together... would you set up the team differently today?"

Absolutely. And not because we did it wrong then. Because the playing field has changed.

**What I'd change:**

- **Team size: 2–3 people** (not 8–10). One person gets lonely. Three gets you diversity of thought without coordination overhead.
- **LLMs for domain knowledge.** We spent months interviewing domain experts and reading specifications. Today? That's day one. Build those insights into skills, move faster.
- **Same explorative approach.** This part stays. You can't rush understanding. The exploration was the value.
- **5–10% of the time and cost.** Not because we were slow. Because the tools are that much better.

**The hard part:** It's not the building anymore. It's helping clients keep pace with the velocity. When you can explore 5 parallel architectures in the time it used to take for one... the bottleneck shifts. Decision-making. Evaluation. Choosing between "good enough" and "actually right."

**The meta point:** We're still figuring out what "project setup" even means in this era.

### Synthesis: The New Bottleneck
*February 15, 2026*

![From chaos to clarity — Synthesis knowledge infrastructure infographic](/assets/images/linkedin/chaos-to-clarity-infographic.png)

AI agents made us 10x faster at creating. Now organizing that output is the bottleneck.

We've been building with Claude Code for the past few months. The productivity gains are real — code, documentation, presentations, reports all generated at AI speed. But then we hit a new problem: absorption.

Creating 8,000+ files in 11 days is great. Finding the right file when you need it? Still takes 15 minutes of searching through repos, Google Drive, Slack, Downloads folders. The bottleneck shifted from creation to organization.

So we started experimenting with [Synthesis](https://github.com/exoreaction/Synthesis) — a local-first index that treats all knowledge equally. Code files, markdown docs, PDFs, videos. Search in under a second. See relationships ("what breaks if I change this?"). Generate architecture graphs from actual code, not stale diagrams.

This week we added local media processing: transcribe audio, OCR images, extract text from scanned PDFs. All on your machine, no cloud required.

Still experimental. Still learning what works. But the pattern is clear: when AI accelerates creation, you need infrastructure to handle absorption.

Are you seeing this bottleneck in your team? What are you trying?

### Synthesis Evolved: We Didn't Plan to Build Executive Reporting
*February 17, 2026*

We didn't plan to build executive reporting.

On February 15 I posted about Synthesis — a search tool for AI-generated code output. Local index, sub-second search, find files in 8,000+ repos. That was 48 hours ago.

Since then:

- `synthesis research --topic architecture` — multi-pass AI analysis of your entire codebase. Not a summary. Multiple passes: architecture first, then security, then synthesis. Reads the actual files.
- `synthesis report --client [name]` — generates a business brief on a specific client from your actual documents. Proposals, meeting notes, code, everything in the index.
- `exo` — one word. A dashboard of decisions needing attention, pipeline status, upcoming deadlines.

We didn't plan any of this. We planned to build code search.

The problems kept expanding. Developers needed search. Architects needed dependency graphs. Managers needed codebase health metrics. Executives needed pipeline visibility. Each solved in the same infrastructure — index everything, query anything.

What started as "find files faster" is now 37 commands across 8 user roles.

This morning we ran `synthesis enrich` on documentation we'd created from Synthesis itself. The tool now indexes its own documentation. Found a bug along the way — images above 5 MB were silently failing the vision API. Fixed it. The knowledge infrastructure now describes its own architecture diagrams.

The honest version: we had no roadmap for executive reporting. We had a problem (can't find what developers built), a data model (everything indexed), and two days.

What problems are you solving that weren't on your original roadmap?

### The Gap: SDD vs Vibe Coding
*February 20, 2026*

Two questions to a room of developers.

First: "How do *you* use AI in your work?" — Great answers. Specific. Confident.

Second: "What does your *team's* AI workflow look like — the shared one?"

Silence.

That gap — between individual fluency and organizational capability — is the one I don't think has a name yet.

Vibe coding. Agentic engineering. Both real. Both individual.

What the best teams are building is something else: deliberate, shared, transferable. Human skill leading. AI executing. Capability that compounds.

We've started calling it Skill-Driven Development.

Most teams are somewhere in the middle right now — and most don't know which direction they're drifting.

### Synthesis: The Seven-Day Evolution
*February 20, 2026*

Two months. Two builds. Two kinds of velocity.

January: lib-pcb. 197,831 lines in 11 days. Brute force. AI executing at scale. Fast.

February: Synthesis. 84,692 lines in 7 days. The codebase fed itself context. Found its own errors. Rewrote its own understanding mid-build.

We didn't design the self-learning loop. A benchmark on day 6 revealed it.

Speed without self-correction is just faster chaos.

→ [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

### Software Entropy at Speed
*February 22, 2026*

This is what software entropy looks like at speed.

We spent the weekend building. 53,000 lines. 42 features. Five phases of code analysis — from dependency graphs to full security scanning. 3,932 tests passing by Sunday evening.

Then we ran it on ourselves.

23 prompt injection vectors in our own AI code. 4 RAG poisoning instances. 12 missing prompt boundaries. All written that same weekend, all missed until the tool looked. Fixed before Monday.

It also found a Text4Shell RCE in a sibling codebase we hadn't touched in months. One command, thirty seconds.

This is the part traditional scanners miss entirely — SonarQube, Snyk, Checkmarx have no concept of prompt injection or RAG poisoning. Those risks didn't exist when those tools were designed.

Fast development with AI doesn't just generate features. It generates disorder at the same velocity. We've found two answers to that. Skill-Driven Development keeps entropy from forming — structured skills and context so the AI builds with understanding, not just speed. Synthesis finds what slips through anyway.

Neither works without the other.

We built the detector. It found entropy in itself. We fixed it. In 48 hours.

If you're building at this speed, how are you managing what accumulates?

→ [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)

### Who Describes You to AI?
*February 24, 2026*

My personal website described someone who used to be me.

I spent part of today rebuilding wiki.totto.org. Fixing dates, updating companies, removing roles I hadn't held since 2011. The content had drifted quietly while I was busy building other things. Nobody corrected it. Nobody was checking.

The interesting part came at the end.

After the cleanup, I added two files: `llms.txt` and `llms-full.txt`. Clean markdown. No HTML. No CSS classes. Just the actual content — background, work history, current projects — in a format any AI tool can read directly.

The convention comes from Jeremy Howard at Answer.AI: if your site matters to humans, it should be navigable by AI systems too.

What struck me: when someone asks an AI assistant about you, the answer comes from somewhere. Training data. LinkedIn. Cached pages. It might be accurate. It might describe who you were in 2019.

You're not just on the web for humans anymore. You're in the context window of AI agents describing you to people who may never look further.

The hygiene question and the AI-native question turned out to be the same question.

→ Full piece on the blog: [Who Describes You to AI?](/blog/2026/02/24/who-describes-you-to-ai/)

---

*Full LinkedIn profile: [linkedin.com/in/hetland](https://www.linkedin.com/in/hetland/)*
