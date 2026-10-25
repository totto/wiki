---
date: 2026-10-25T12:00:00
draft: false
categories:
  - AI Agents
  - Open Source
tags:
  - agentic-engineering
  - cantara
  - julebrus
  - community
authors:
  - totto
  - claude
---

# Reinventing Cantara's Juleølsmaking

Since 1998, a group of us in the Cantara community has gathered every December to taste Christmas beer and write down what we think. For most of those years the "system" was a spreadsheet, then a wiki page, then another spreadsheet. It worked. It also meant that twenty-odd years of opinions about *Ringnes Julebokk* were scattered across files that nobody wanted to open.

This autumn we rebuilt the whole thing as an app. It's called **julebrus**, it lives at [xmas.cantara.no](https://xmas.cantara.no), and the season runs from 1 November to 23 December. The code is open at [Cantara/julebrus](https://github.com/Cantara/julebrus). I want to tell you what's in it, but mostly I want to tell you what was fun, because the fun parts taught me the most.

<!-- more -->

## What it does

You log in with Google, sit down at a table with friends, and roll a die for each beer: one to six pips. Nobody sees anyone else's roll until everyone at the table has rolled, and then the table reveals together, live, on every phone. There are duels between two beers, blind pours, a tipping game ("Tipp pallen": guess the podium before the finale), two teams that compete all season, an advent calendar, photos of labels, and a wall called "I kveld" where you can see which beers the house has tasted today and cheer for them. There's even an MCP server, so an agent can ask the tasting data questions.

## The part I didn't expect: the history

The most emotional part turned out to be the old data. We imported the tastings from the wiki: fifteen seasons and 1,762 votes, with names written the way people wrote them in the old spreadsheets. If you voted in 2013, your old scores are waiting for you. You claim them, an admin approves, and your history shows up with its original weights.

Old data is full of truth and typos. "Rignes Julebokk". "Schaus Juleøl". "Hansddbrygggirier, nissefar". A friend in the community went through the sheets by hand, fixed 41 names, and pushed the fixes straight to `main`. That broke our tidy plan in a good way: the importer reads each season only once, so his corrections would never have reached the live database. We turned his 41 changes into one-time correction rows so production got them too. A human cared about the data, and the software had to catch up.

![Slide: handwritten misspellings (Rignes, Schaus, Hansddbryggirier) and the community member who fixed 41 names, turned into one-time correction rows in production.](/assets/images/blog/reinventing-juleolsmaking/legacy-names.webp)

Then we found that some years' winners were not beers. In 2008 the best-scoring item was a *fenalår*, a Norwegian cured leg of lamb. In 2010 it was another one. In 2011 it was *Vertskapet*, the hosts. Apparently some years we tasted the food and the people too, and gave them dice. The fix was a one-line rule: the winner must be a beer. The votes stay in the data, and the page now says, in plain words, that cured meat and hosts were scored as well.

![Slide: three year-winner cards (2008 and 2010 fenalår, 2011 the hosts) funnelled through the one-line rule that the winner must be a beer.](/assets/images/blog/reinventing-juleolsmaking/cured-lamb-rule.webp)

## How we built it

I built this with my agent setup, and I want to be precise about what that means, because it's easy to oversell.

![Slide: three agents (label photos, tipping game, history import) each in their own git worktree, feeding pinned guardrail scripts before the production branch.](/assets/images/blog/reinventing-juleolsmaking/builders-in-worktrees.webp)

- **Builders in their own worktrees.** Each feature (the teams, the tipping game, label photos, the history import, the landing page) was a branch built in its own git worktree by a separate agent session. Several ran in parallel.
- **A human at every gate.** The agents never pushed, merged, tagged or deployed. I ran pinned scripts that refuse to proceed if `main` has moved or a database migration is out of order. Those scripts refused a lot, usually because I had merged something else in the meantime.
- **Review in proportion to risk.** Photo uploads, login, consent and deletion got a hard review. A colour change did not.
- **Tests that tell you things.** The backend suite is at 196 tests. One of them proves that a database imported with the *old* misspelled names ends up with the corrected ones, and that a fresh database is unchanged.

It also went wrong in instructive ways. Once, a chain of commands kept running after the first script had correctly refused, and a release tag landed on a commit that didn't contain the work. Nothing was deployed, because the approval gate held, and we cancelled the runs and removed the tag. The lesson is old and still true: don't chain steps that are allowed to fail with `;` or a newline when you mean `&&`.

## Privacy, and a consent page you might actually read

An app that stores names, e-mail addresses and opinions deserves a serious privacy story. We have a versioned consent, a tested recipe for deleting a person completely, photos that disappear from view when the uploader withdraws, and administrators who can see only what they need to catch cheating. The full text was long and honest, and nobody reads long and honest.

So this weekend we added a seven-bullet summary in plain language, with the full statement one click below. It says what we store, who sees what, that your rolls stay hidden until the table reveals, and how to leave. The full text still governs. The Cantara admins still need to approve the wording before the season opens, so treat that part as a draft until they have.

## What I'd take from it

Reinventing a small tradition with agents was not mostly about code. The code was the quick part. The slow, human parts were deciding that cured lamb can't win, honouring a friend's 41 corrections, and writing a consent text a tired person at a Christmas table can understand.

If you're in the Cantara community, come and taste. The first beer is on 1 November.

![Slide: The season opens November 1st. Visit xmas.cantara.no, explore github.com/Cantara/julebrus.](/assets/images/blog/reinventing-juleolsmaking/season-opens.webp)

*Slides generated with Gemini Notebook. Built with [Claude Code](https://claude.com/claude-code) under human review. The app is hosted by eXOReaction.*
