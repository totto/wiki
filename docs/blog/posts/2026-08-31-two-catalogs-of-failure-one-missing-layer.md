---
description: "A Google Research paper on agent memory and a Norwegian book on organisational dysfunction arrived in the same week — and turned out to be describing the same missing layer. Here's the plan that came out of noticing it."
date: 2026-08-31T11:30:00
series: "Sunstone Atlas"
draft: false
categories:
  - AI Agents
  - Engineering
tags:
  - sunstone-atlas
  - governance
  - skill-provenance
  - sociotechnical-systems
  - pattern-library
  - organisational-dysfunctions
authors:
  - totto
  - fable
  - claude
---

# Two catalogs of failure, one missing layer

Two things landed in my feed the same week, from completely unrelated corners.

The first was a Google Research paper about why AI agents stop getting better: most skill-evolution systems throw away the record of *why* a skill changed, so improvements stop compounding after a few iterations. The second was a book by Trond Hjorteland — someone I know from the Norwegian sociotechnical-systems scene — cataloging seventy-seven named ways human organisations fail, most of which come down to decisions whose reasoning nobody can reconstruct afterward.

It took a few days to notice these are the same finding. Both are saying: the raw log of what happened is not enough, and the final artifact is not enough. There's a third thing — a persistent, honest record of *why* — and when it's missing, both machines and organisations repeat their failures instead of learning from them.

<!-- more -->

This post is about that shape, and about the concrete (and deliberately unbuilt — more on that below) plan it produced for [Sunstone Atlas](2026-08-24-trust-is-earned-not-asserted-introducing-sunstone-atlas.md).

## The paper: WikiSkill, and the layer everyone deletes

The paper is WikiSkill ([arXiv 2608.27454](https://arxiv.org/abs/2608.27454)), from Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, and Tu Vu — Google Research and Virginia Tech.

Their diagnosis of the field: when an agent system revises its own skills, the reasoning behind each revision usually lives in an ephemeral optimization log that gets discarded or overwritten. The skill improves once or twice, then plateaus, because every new revision starts from scratch on the *why*.

Their fix is architectural, not a better prompt. Keep three artifacts permanently separate:

1. **Raw execution traces** — immutable logs of what the agent actually did.
2. **A persistent wiki** — pattern pages documenting failure modes and strategies. Crucially, the wiki is *never rolled back*: even when a specific revision proposal gets rejected, the pattern page documenting the dead end stays, so the next proposal doesn't rediscover it.
3. **The executable skills themselves** — with a hard gate: a revision is only accepted if it beats the prior version on a held-out validation score.

The ablation is the part worth remembering: removing the wiki layer cost 15 accuracy points on average. The win isn't cleverer skill-writing — it's the persistent memory substrate in the middle.

To their credit, the authors state their limitations plainly. Two matter here: the wiki has no automated pruning, so it grows without bound; and skills transfer badly across models — in one measured case, a skill encoding one model's specific workaround dropped a different model from 50.5% to 18.1% accuracy. Hold both of those thoughts.

## The book: Hjorteland's dysfunction taxonomy

The second arrival was [*Organisational Dysfunctions*](https://leanpub.com/organisationaldysfunctions) by Trond Hjorteland — Capra consultant, Open Sociotechnical Systems practitioner, and a long-standing voice in the Norwegian agile and sociotechnical community. I know Trond personally, and this book is exactly what you'd expect from someone who has spent years watching organisations from the inside: a catalog of named failure modes, released on Leanpub, which grew from 63 to 77 chapters with the v1.1 release at the end of August. The chapters are organised by blast radius — "In the Room," "In the Team," "In the Department," "In the Organisation" — plus sections on objections, perspectives, and what happens beyond the walls.

Before I go further, the provenance boundary: the book is Trond's paid work, and nothing in this post or in our plan reproduces it. What I'm drawing on directly is the subset he published free and in public first, as his "Organisational Dysfunction of the Day" LinkedIn series — chapters like "Hired from above," "DORA, the wrong way round," and "What the war room proves" started life as open posts before being folded into the book. If the pattern names below intrigue you, the book is where the full treatment lives, and buying it is the right way to engage with the rest.

"Hired from above" is a good sample of the genre. A team is behind deadline. Management, without a word to the team, hires a consultant. The team finds out when the new person shows up Monday morning. Hjorteland's point, citing Open Systems Theory: "who is in a group is the most fundamental design decision a group can make" — and here that decision was made *about* the group, invisibly, with no trail the group could have engaged with.

Read enough of these and a common structure emerges: something consequential changed, the change itself is visible after the fact, but the *reasoning* — who decided, on what basis, considering what — was never recorded anywhere the affected people could see. The organisation has raw events (the consultant showed up) and final state (the org chart), and nothing in between.

Traces and skills. No wiki.

## The same shape, twice

That's the insight this post exists to record, and I want to state it carefully because it's easy to overclaim: a research paper about agent memory and a practitioner's book about human organisations, written with no knowledge of each other, both locate the failure in the same missing artifact — a persistent record of *why*, distinct from the raw log of what happened and distinct from the current state of the thing.

WikiSkill measured what its absence costs an agent system: 15 points, and improvement that stops compounding. Hjorteland catalogs what its absence costs a human system: seventy-seven chapters' worth.

Two of his chapter titles land so close to Sunstone's own thesis that I'll just quote them: **"Deploying AI into a broken system"** and **"The AI we cannot talk about."** Both are about automating dysfunction instead of fixing it — which is the same critique behind Sunstone's "description ≠ enforcement" principle. Writing down a policy an agent should follow is describing; a system where the policy *mechanically cannot be bypassed* is enforcing. A dysfunction taxonomy nobody acts on is a description. So is a governance document.

## What this means for Sunstone Atlas, concretely

Here's where it stops being an observation and becomes a plan — and I mean *plan* literally. What follows is a written proposal, dated 30 August, not a shipped feature. Nothing below exists in code yet.

Sunstone Atlas's Skill artifact already has the lifecycle mechanics WikiSkill's third layer needs: a `supersedes` pointer linking versions, and a signed, append-only `GovernanceStore` ledger recording clearance and graduation events. What the audit against the paper made obvious is that we have the *edges* of WikiSkill's architecture and are missing its middle entirely:

- `supersedes` is a pointer, not a reason. It records that a change happened — not what failure motivated it, not what evidence justified it.
- There is no pattern-page layer: no persistent, queryable record of the failure modes a skill was written to address.
- There is no validation gate on revisions. A skill is edited and republished on author judgment, with no requirement that the new version demonstrably beats the one it replaces.

The plan closes this by reusing primitives that already exist rather than building a new subsystem: a `skill-revision-proposed` / `-accepted` / `-rejected` event trail on the same ledger pattern `GovernanceStore` already uses, pattern pages that are written on every proposal outcome and never rolled back (the WikiSkill rule), and a publish-time gate that blocks a revision whose validation score doesn't beat the current version's.

And one place where we'd go past the paper: pruning. The WikiSkill authors say outright that their wiki lacks an automated pruning mechanism and flag it as a scalability risk. Sunstone already has a staleness-clock concept — `freshness_policy`, used today for validation dates on knowledge units. Applying the same clock to pattern pages, so a page uncited by any proposal within its freshness window gets flagged for review rather than kept silently forever, would close a gap Google's own paper admits it left open. That's the narrow, checkable claim — not "we do agent memory better than Google."

## The new idea: seed the wiki with Hjorteland's patterns

An empty pattern library is useless for a long time. It has to wait for enough of your own failures to accumulate before it says anything. That's the cold-start problem — and it's where the two arrivals of the week actually connect, beyond rhyming.

The idea: seed the pattern library with a curated, credited subset of the dysfunction patterns Hjorteland already published publicly. Not as vibes or inspiration — the reason this works is that several of his named patterns map onto *mechanically checkable signals* in Sunstone's existing schema:

- **"The blind decision"** — a decision made with no visible reasoning trail — is precisely the failure Sunstone's `decision_basis` field and signed-ledger requirement exist to prevent. A judgment step publishing with no grounding *is* the blind decision, detectable at the moment it happens.
- **"Involvement theatre"** — participation that looks real but carries no power — becomes a query, not a vibe: a human-in-the-loop gate with a 100% historical approval rate and near-zero review latency across its run history is oversight in name only, and the run ledger already holds the data to say so.
- **"Hired from above"** — a new actor inserted into a running process without the team's consent — is the organisational version of a delegation-chain problem we're separately working through: an actor appearing mid-chain that doesn't match a declared allowed sequence.
- **"Matrices"** and **"Playing politics"** — ambiguous authority resolved informally — name exactly the condition Sunstone's `grant_ceiling` mechanism exists to eliminate: it makes "which source actually bound this decision" a structural fact instead of a political negotiation.

A human noticed these dysfunctions, named them, and published the names. An agent-governance system can watch for their signatures in its own ledgers from day one, with each seeded pattern page crediting the person who named it and linking his source. That's the loop I find genuinely new here — and it cuts both ways, because if agents inherit organisational failure modes (and "Deploying AI into a broken system" argues they do), then a catalog of human dysfunctions is a threat model for agent systems, not just a management book.

## What is honestly not here

House rules: the gaps, stated as plainly as the idea.

- **Nothing is built.** This is a plan document with proposed phases. Phase 0 — schema fields and event kinds, no enforcement — has not started, and the plan explicitly does not authorize starting it. If you read this post as a feature announcement, I've failed.
- **The validation gate is unproven in our context.** WikiSkill's accept-only-if-better rule worked on their benchmarks. Whether a meaningful validation score even exists for the kinds of skills Sunstone governs — many of which are judgment procedures, not benchmark tasks — is an open question, not a detail.
- **The pruning claim is a design, not a result.** Reusing `freshness_policy` for pattern pages is plausible precisely because the primitive exists, but "we prune where Google doesn't" is only defensible after it runs.
- **Cross-model transfer is a live risk we haven't addressed.** Our fleet is multi-model. The paper's 50.5% → 18.1% negative-transfer case means a skill encoding one model's workaround, propagated fleet-wide, could be a real and currently invisible failure mode. The plan flags it for the eventual RFC; it does not solve it.
- **The mapping table is my reading, not Trond's.** Hjorteland wrote about human organisations. The translation of his patterns into ledger queries is our interpretation, and any place it distorts what he meant is on us, not him.

## The point

Paper and book, machine and organisation, the same missing layer: the durable record of why, kept separate from the raw trace and the finished artifact, never rolled back, honestly pruned.

Sunstone Atlas already treats *what happened* as sacred — signed, append-only, replayable. The lesson of this week is that *why it changed* deserves the same treatment, and that we don't have to start the library of reasons from zero: some of the best failure patterns have already been named, in public, by someone who spent a career watching them. Go read Trond's book.

---

*Sources:*

- [Organisational Dysfunctions — Trond Hjorteland, Leanpub, v1.1 August 2026](https://leanpub.com/organisationaldysfunctions) — plus his free "Organisational Dysfunction of the Day" LinkedIn series, the only content drawn on directly here
- [WikiSkill — Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, Tu Vu (Google Research / Virginia Tech), arXiv 2608.27454](https://arxiv.org/abs/2608.27454)
- [Trust is earned, not asserted: introducing Sunstone Atlas — wiki.totto.org, August 2026](2026-08-24-trust-is-earned-not-asserted-introducing-sunstone-atlas.md)
