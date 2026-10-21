---
date: 2026-10-21T08:30:00
draft: false
image: assets/images/blog/open-source-superpowers/slide-as-built-blueprints.webp
categories:
  - AI Agents
  - Open Source
tags:
  - agentic-engineering
  - open-source
authors:
  - totto
  - claude
---

# Open Source Superpowers in the Agentic Era

![The As-Built Blueprints: open source superpowers in the agentic era](/assets/images/blog/open-source-superpowers/slide-as-built-blueprints.webp)

After forty-plus years in software, I hold one belief with near-total confidence: documentation drifts, source code doesn't. A doc describes what somebody believed at some point in the past; the code describes what the machine will actually do tonight. For most of my career that gap was simply a fact of life, because reading someone else's codebase deeply enough to find the truth was expensive — days or weeks of a senior engineer's full attention.

Agentic software development — AI coding agents doing real engineering work under human direction — has just changed that economics. And it hands open source two superpowers it didn't have before:

**a)** Agents can go to the real source to find the truth — and accumulate skills along the way — instead of relying on docs or memory that may be stale.

**b)** When a fix is needed, the path to landing it is now very short: open an issue or a PR against the real repo, or fork and fix.

That's the thesis. Rather than argue it abstractly, let me walk you through a scenario.

<!-- more -->

Here's the picture I'd offer a reader who doesn't write code. Working from documentation is like navigating a building using a description written by someone who toured it once, years ago, before the renovation. Working from the source is standing in the corridor with the as-built drawings in your hand. That's superpower (a). And open source adds the part no building can offer: when you find the cracked beam, you don't file a complaint with the landlord and hope — you're allowed to repair it yourself, submit the repair for the owner's approval, and once accepted it's fixed for everyone who ever walks in after you. That's superpower (b).

![Two ways to navigate software: the tour guide's description from before the renovation, or the as-built drawings in your hand](/assets/images/blog/open-source-superpowers/slide-tour-guide-vs-as-built.webp)

## A composite story

What follows is not a single named incident — it's a composite, built from a pattern I keep running into in my own agentic work. The details are invented; the shape is one I have now lived through enough times to recognize it coming.

Picture a small open-source library — the fifty-kilobyte kind that quietly sits inside half the backends you've ever used — whose one job is retrying failed network calls. Call fails, wait a second, try again; fails again, wait two seconds, then four, then eight. The maintainer's design notes state the contract plainly, in the tone of someone who has strong feelings about it: *waits double each time, and no caller ever waits more than one minute between attempts.* A promise simple enough to put on a business card.

I want to add a feature: an overall time budget. "Whatever happens, give up entirely after five minutes" — the thing every on-call engineer wishes every library had at 3 a.m.

And because I am an experienced engineer, I begin the way experienced engineers do: by reading the design notes and compiling a list of things I would have done better. The list practically writes itself. The waits should be a little randomized, so a thousand clients don't all retry in the same instant — classic improvement, surprised it's missing. The wait times should be configurable. And then my budget feature on top. Three confident improvements before lunch.

I hand the agent the list and point it at the actual repository — not the README, not a blog post about the library, not the model's training-data memory of "how retry libraries usually work." The source. The tests. The maintainer's own notes, cross-checked against the code they describe.

The agent returns with its findings, delivered in the serene deadpan that only an entity with no professional ego can manage. The randomized waits I was going to propose? Shipped over a year ago; the design notes were last touched the month before that. Configurable wait times? Also done, two releases back. There is a particular kind of silence that follows learning your two best ideas shipped before you had them, and that your third-best idea is the only one left. I recommend experiencing it at least once — it is very educational, and much cheaper than the old method of discovering the same thing in the project's issue tracker, in public.

The documentation hadn't lied, exactly. It had drifted, the way all documentation drifts — calm, authoritative, in complete sentences, wrong. The tour-guide description from before the renovation.

![Documentation drifts, source code does not: the real state keeps moving while the documentation line stays flat](/assets/images/blog/open-source-superpowers/slide-documentation-drifts.webp)

In fairness to my own side of the ledger, the reading also produced one false alarm: the agent triumphantly reported that for one category of error the library retries *forever* — surely a bug — three lines below a comment explaining that for exactly that category, the server itself tells the client when to come back, and giving up would be the actual bug. The real source cuts both ways: it also lets the maintainer's comments defend themselves. The agent withdrew the finding with what I can only describe as dignity.

## The bug caught before the code existed

Then comes the moment that made me want to write this post.

Before writing a single line of my budget feature, the agent did something I now insist on: it simulated the design on paper, against the library's real behavior. It traced one maximally unlucky call, by hand — fail, wait one second, fail, wait two, four, eight, and so on — checking each step against the actual code rather than the documented promise.

And the promise doesn't hold. The documentation says no wait ever exceeds one minute. But the real code applies the one-minute cap *before* doubling the wait instead of after — so one extra doubling slips through the fence, and the longest real wait is two minutes, not one. That's the entire bug. Two sentences, one misplaced check, invisible for years because it only shows up on the seventh consecutive failure, and who tests the seventh consecutive failure?

![The invisible crack: the one-minute cap is applied before the wait is doubled, so one extra doubling slips through](/assets/images/blog/open-source-superpowers/slide-the-invisible-crack.webp)

My five-minute budget feature, designed on top of the documented one-minute cap, would have inherited it immediately: the arithmetic says the budget is spent, the library is in fact still asleep in a two-minute wait, and when it wakes it fires one final retry *after* the deadline. We had very nearly shipped a punctuality feature that was itself late — a system whose one job was to give up on time, giving up late. No code existed yet. The bug was caught on paper, purely because the agent could read what the code actually does instead of what the notes say it does. Against documentation alone, this ships. Against training-data memory of "typical" retry libraries, this ships. Against the real source, it never got written.

Better still: the trace didn't just protect my feature — it surfaced a real bug in the library itself, one every downstream user relying on that one-minute promise currently has. The agent, which by this point had absorbed the maintainer's own habit of writing every promise down as a test, wrote exactly that: a failing test demonstrating the two-minute wait, and the one-line fix that makes it pass.

## The short path home

Now superpower (b), which is purely mechanical. The fix exists, is understood, and is proven by a test. Because the library is open source, the rest of the path is almost embarrassingly short: fork the repo, push the branch, open a pull request against the real upstream — failing test, one-line fix, passing test, respectful note. The maintainer reviews a concrete, verifiable diff on their own terms. Total friction: minutes of mechanism, plus whatever review time the maintainer chooses to spend. The cracked beam gets repaired in the building itself, for everyone who walks in after us.

![The short path home: failing test, one-line fix, pull request with a verifiable diff, repaired for everyone](/assets/images/blog/open-source-superpowers/slide-the-short-path-home.webp)

Run the same scenario against a closed, proprietary component and watch both superpowers evaporate. No source to read, so ground truth must be guessed from the outside — timing measurements, probing, and vendor docs that drift just as confidently as anyone else's. The misplaced cap never gets caught on paper, because there's no paper to trace against. And when the two-minute wait finally bites you in production, there is no mechanism to hand back the fix you can't see anyway: you file a ticket, you receive a case number, and the case number and your workaround grow old together in a corner of your repo.

![The proprietary evaporation: guess the ground truth, read drifting vendor docs, meet the bug in production, file a ticket](/assets/images/blog/open-source-superpowers/slide-proprietary-evaporation.webp)

## What this means if you choose dependencies for a living

For engineers: when your agent has a question about a library, send it to the source. Not the docs, not its own memory. The truth is in the repo, and reading it is now cheap.

For leaders: "can our agents reach the source?" just became a first-class architectural criterion. An open-source dependency is a building your agents can inspect against the as-built drawings today and repair tomorrow. A closed one is a secondhand description you have to trust and a landlord queue you have to wait in. That difference used to be philosophical. In the agentic era, it's throughput.

Open source always promised that given enough eyeballs, all bugs are shallow. We finally have enough eyeballs.

*The scenario in this post is a composite, not a single real incident. The slides were generated with NotebookLM from this text and reviewed by hand; slides that did not match the text were left out.*
