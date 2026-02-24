---
date: 2026-02-24T10:00:00
categories:
  - AI-Augmented Development
tags:
  - ai
  - personal-site
  - llms-txt
  - identity
  - web
authors:
  - totto
---

# Who Describes You to AI?

I spent part of today rebuilding this wiki. Not because it was broken. Because when I read it carefully, it was wrong.

Not dramatically wrong. Wrong in the way things get wrong when you stop paying attention. I was listed as Chairman of IASA Norway. I stepped down from that role in 2011 -- fifteen years ago. One of my companies had the wrong founding year. The framing throughout was from a different era: SOA, distributed systems, the vocabulary of a decade ago. The site looked like me. It described someone who used to be me.

<!-- more -->

That is a specific kind of problem. Your public record drifts without you. You update your LinkedIn occasionally, give a conference talk, publish something. But the connective tissue -- the site that's supposed to say *this is who I am right now* -- calcifies quietly while you are busy building things.

Fixing it was straightforward. Reading the actual content carefully, correcting what was wrong, updating what had changed. An hour of work that should have happened incrementally over years. The process was unremarkable.

What happened at the end of it was not.

## The file nobody asked for

When the content was clean and current, I added two files to the site. `llms.txt` and `llms-full.txt`. They live at the root, alongside everything else, and they contain the same information as the rest of the wiki -- my background, employment history, the projects I'm working on, the talks I've given -- written in clean, plain markdown. No HTML. No CSS classes. No theme wrappers. Just text.

The `llms.txt` convention comes from Jeremy Howard and the team at Answer.AI. The idea is simple: if your site matters to humans, it should be navigable by AI tools too. A compact index at the root, pointing to clean versions of your content. The same information you provide to a browser, provided in a form that an AI assistant can read without having to parse rendered HTML, strip navigation elements, and guess at structure.

I added it to this site in about twenty minutes. And then I sat with what I had just done for longer than that.

## Who is answering the question?

When someone asks an AI assistant about me -- who is Thor Henning Hetland, what does he work on, what is his background -- the answer comes from somewhere. Training data. LinkedIn. GitHub. Cached versions of old pages. Whatever the model has access to, assembled into something that resembles a description.

That description might be accurate. It might be from 2019. It might describe someone who was Chairman of IASA Norway and focused on SOA governance. It might be missing Synthesis entirely, because Synthesis did not exist when the model was trained.

The `llms.txt` does not fix this for the models that have already been trained. But it changes the trajectory. As AI agents increasingly browse the web in real time -- fetching context before answering questions, checking current information rather than relying on training data alone -- a clean, canonical, up-to-date description of who you are becomes meaningful.

I had been thinking about my website as something humans read. That stopped being the whole picture somewhere in the last year. Increasingly, my website is something AI systems encounter on behalf of humans. The agent reads it, extracts what's relevant, and summarises it into a response that the human never scrutinises too carefully. The HTML I've been optimising for browsers is only half the interface now.

## What changes when you think about it this way

Not much, practically. You add two files. You keep them updated when your circumstances change -- the same discipline you should already have but probably do not.

But the framing shift is real. Your professional identity now has multiple audiences that each need different things from the same content. Humans want design, narrative, context. Search engines want structure and keywords. AI tools want clean text and clear organisation.

The interesting thing is that clean text for AI and good writing for humans are almost identical. The HTML wrappers, the CSS classes, the theme machinery -- those are for the browser renderer, not the reader. Strip them away and what's left is just well-organised prose. Serving AI readers well turns out to mean writing clearly and keeping your facts current. Neither of those is a new requirement.

What is new is that you can no longer assume your primary reader is a human being sitting in a browser. Increasingly, the first reader is a system assembling context on someone's behalf. That system will describe you to the human. What it says depends on what you give it.

I would rather give it something accurate.

## The stale record problem

The thing I keep returning to is the fifteen years. IASA chairman, still listed on a personal site, long after it stopped being true. Nobody corrected it because nobody was checking. I was not checking. The site existed in a quiet corner of the web, accurate enough, visited occasionally, never quite worth the effort of a full review.

Adding `llms.txt` required the full review. The file is only useful if it is accurate, and making it accurate meant reading everything carefully. The AI-native format turned out to be the forcing function for basic hygiene I should have applied years ago.

That seems about right for where we are. The pressure to make content machine-readable is creating a secondary benefit: content that is actually correct. Which is what it should have been for the human readers all along.

---

*This site now publishes `llms.txt` at [wiki.totto.org/llms.txt](https://wiki.totto.org/llms.txt) and a full clean version at [wiki.totto.org/llms-full.txt](https://wiki.totto.org/llms-full.txt).*
