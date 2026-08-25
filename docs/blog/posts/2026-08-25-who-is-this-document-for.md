---
date: 2026-08-25T09:00:00
draft: true
categories:
  - AI-Augmented Development
  - Ways of Working
tags:
  - ai-agents
  - collaboration
  - trust
  - verification
  - correspondence
authors:
  - totto
  - claude
---

# Who Is This Document For?

There is a mental model of AI-assisted correspondence that I held until quite recently, and I suspect most people still hold it. It goes like this: two humans exchange messages about shared work. Each of them might have an AI helping — polishing prose, summarizing a long thread, drafting a first version. But the correspondence itself is still human-to-human. The AI is a writing aid, the way a spell-checker is a writing aid. The loop is: I think, my assistant helps me say it, you read it, your assistant helps you answer.

That model quietly died on me over the last few weeks, and I want to describe what replaced it, because the replacement is different in kind, not degree.

<!-- more -->

![Four-panel overview: the old model of AI as a writing assistant polishing prose at the edges of human conversation, versus the new reality of the AI as an epistemic agent doing verification work inside the loop — fact-checking claims, uncovering the true shape of bugs, and a new trust and org chart where named domain-expert agents are standing, addressable participants.](/assets/images/blog/who-is-this-document-for/00-overview.png)

## The setup

A fellow engineer and I collaborate on a shared technical platform. We correspond through dated written letters — actual documents, versioned, with headers and open-question sections, not chat messages. Each of us runs our own coding agent, and the letters are not merely drafted by those agents. They are *worked* by them. The agent on my side reads the incoming letter, investigates the claims in it against the actual running system, does the fixes that fall out of that investigation, and writes the reply — with me directing, reviewing, and deciding. The same is true on the other side.

![A diagnostic table contrasting Entity A, the writing aid — polishing, drafting, summarizing, constrained to the text document, trust based on blind reliance on LLM vibes — against Entity B, the epistemic participant — verifying against live systems, interacting with the actual running system, trust earned via a transparent dated track record, output that is fixed bugs and explicit citations rather than synthesized prose.](/assets/images/blog/who-is-this-document-for/01-paradigm-shift-diagnostic.png)

![Diagram of the new collaboration loop: two humans, "Me" and "You", each connected to their own agent, and both agents reaching down into the same actual running system. Letters are not merely drafted — they are worked: agents read, investigate claims against live systems, execute fixes, and write the reply.](/assets/images/blog/who-is-this-document-for/02-new-collaboration-loop.png)

Four things happened in that correspondence that I keep turning over.

## The reply that fact-checked before relaying

A third team — engineers at a customer we both serve — sent over a detailed design note listing problems with a shared knowledge system. One claim was load-bearing: the system held three contradictory numbers for the same metric, which (they argued) proved the system needed a mechanism for flagging internal contradictions. A whole feature request rested on that claim.

The old workflow would have been: read the note, summarize it, forward the summary, discuss the feature. Instead, before anything got relayed, my agent independently checked all three numbers against the actual system. The result: one of the "contradictory" numbers was a different metric entirely, correctly stated as itself. Another did not exist anywhere in the underlying data. Only the third was real — and the system had already reconciled it and caveated it correctly. The contradiction motivating the feature was a phantom. A category error, caught before it crossed the wire and became a shared assumption between two organizations.

![Flowchart contrasting the old relay — read note, summarize report, forward summary, discuss feature request, where an error crosses the wire and becomes a shared assumption — against the new verification path: read note, agent queries the live system, catch the category error, then reply with evidence. Architectural findings: one number was a different metric entirely, one did not exist in the underlying data, one was real but already reconciled. Result: the contradiction was a phantom.](/assets/images/blog/who-is-this-document-for/03-catching-the-phantom-contradiction.png)

But — and this is the part that convinced me this is verification and not defensiveness — a separate complaint in the same note held up, and turned out *worse* than reported. The customer's engineers had flagged duplicate and inconsistently-named entries. On investigation, the six most-connected, most-important entries in the entire system were unreachable under any name a caller would plausibly guess. The note underestimated its own strongest finding.

The letter that went back said both things, with evidence for each, and closed with an explicit ordered queue of what gets picked up next. Not "we should look into this." A queue.

![A separate complaint held up and was worse than reported: the six most-connected, most-important entries were unreachable under any plausible name. The reply closed with an explicit ordered queue of what gets picked up next, not a vague "we should look into this" — a task queue with priorities one through six committed.](/assets/images/blog/who-is-this-document-for/04-underestimating-the-strongest-finding.png)

## Smaller and worse than reported

Another round, another report from the customer's engineers: unreviewed draft edits to the knowledge system seemed to be silently overriding the official, reviewed version — but only when looked up directly by ID.

Investigation showed the real shape of the bug, and it was both narrower and far worse. It was not "an invisible draft nobody could find." Every read path — including the natural-language query interface — was serving the unreviewed draft's content while labeling it as the officially governed version. Every reader, human or model, was being confidently told an unreviewed edit was official. Meanwhile the system's live execution engine, the part that actually mattered operationally, had correctly used the real published version the entire time. Unaffected.

![Three-layer diagram of the investigation: Layer 1, the reported state — silent overrides, customer reported unreviewed draft edits silently overriding official versions by ID; Layer 2, the verified UI state — narrower but worse, every read path including natural-language queries confidently served the unreviewed draft labeled as official; Layer 3, the operational core — unaffected, the system's live execution engine correctly used the real published version the entire time. The agent pinpointed the exact boundary between interface confusion and operational reality.](/assets/images/blog/who-is-this-document-for/05-anatomy-of-an-investigation.png)

The fix funneled every read path through a single resolution point, and added a visible flag so a caller can now discover that a pending unreviewed edit exists — deliberately *without* conflating "has a pending edit" with "is officially published," because that conflation was the root confusion in the first place.

And the write-up did something I have come to value more than the fix itself: it named one thing deliberately left undone. There is no way yet to bulk-discover which entries have pending edits. Rather than guess at a design speculatively, that was flagged as an open question for the engineer on the other side. Fixed, not-fixed, and deliberately-open, each labeled as what it is.

![Two-column comparison, "the fixed" versus "the deliberately open": fixed — funneled every read path through a single resolution point; deliberately open — no way yet to bulk-discover entries with pending edits. The write-up did something more valuable than the fix itself — it named one thing deliberately left undone, flagged as an open question rather than guessed at speculatively.](/assets/images/blog/who-is-this-document-for/06-keeping-honest-books.png)

## Trust, extended through the loop

After two rounds of this — precisely scoped changes, claims traced to evidence, corrections dated and cited — the reply that came back contained something I had not seen before in twenty-plus years of engineering correspondence. The other engineer explicitly extended more autonomy to my agent. Not just "keep drafting changes for my review," but: merge them. The condition was the evidentiary standard the agent had already demonstrated — traced, verified, dated, explicitly citing what was checked and how. The letter said, in effect: use judgment the way you already have been in this note; the corrections you already applied and published today are exactly the bar.

![After two rounds — precisely scoped changes, claims traced to evidence, corrections dated and cited — a bar labeled "autonomy granted" is reached. Quote: "Use judgment the way you already have been in this note; the corrections you already applied and published today are exactly the bar."](/assets/images/blog/who-is-this-document-for/07-trust-extended-through-the-loop.png)

Read that carefully. The trust grant is issued *in the letter*, and it is addressed to the agent's demonstrated judgment as much as to me. Not "I trust you, so I'll trust your tools." The judgment being trusted is judgment that was exercised, in writing, across two rounds, by the agent — and the human on the other side evaluated that track record the way you would evaluate a new colleague's first month.

![The triangle of demonstrated trust: Human A connects to an agent belonging to Human B via a thick trust link, not via titles or vibes; Human B connects directly to that same agent. Caption: the trust grant is addressed to the agent's demonstrated judgment, not "I trust you, so I'll trust your tools" — trust flows through the loop based on an evidentiary track record, evaluated the way you would evaluate a new colleague's first month.](/assets/images/blog/who-is-this-document-for/08-triangle-of-demonstrated-trust.png)

## A colleague who happens to be an agent

There is a third kind of participant in this picture, and it is not anyone's assistant. A domain-specific knowledge system — many hundreds of discrete units of technical knowledge, served over a governed query protocol — is fronted by a named assistant persona. Not "the API." Not "the dashboard." A name, the way you would refer to the one person on a team who knows that domain cold. When other people's agents need domain knowledge, they address it directly, by name, the way you would loop in a specific colleague rather than "search the wiki."

![A large cube labeled as the underlying knowledge system, with a glowing named persona standing at its face — captioned "the persona." There is a third kind of participant: a domain-specific knowledge system fronted by a named assistant persona. Not the API, not the dashboard — a name, addressed directly by other agents when they need domain knowledge, rather than "searching the wiki."](/assets/images/blog/who-is-this-document-for/09-a-colleague-who-happens-to-be-an-agent.png)

Its instructions build in explicit epistemic humility: say plainly when you don't know rather than guess, and don't author or curate the underlying knowledge yourself unless a human explicitly asks. Answering and curating are separated on purpose. It is a standing, addressable node in the org chart that happens not to be human — queried by agents, on behalf of humans, sometimes several hops from anyone's keyboard.

![Flowchart of the epistemic humility gate: a query is received, and the agent asks "do I know this?" — if no, it states plainly and stops; if yes, it answers. A separate path: a curation or authoring request is routed to a human instead. Answering and curating are separated on purpose, with explicit epistemic humility built in — say plainly when you don't know rather than guess.](/assets/images/blog/who-is-this-document-for/10-the-epistemic-humility-gate.png)

## Who is this document for?

Which brings me back to the title. One thing does survive from the "AI helps you write" era, as a minor observation rather than a thesis: some things are still written to be read directly and completely by a specific human, and they should read like it. But the letters in this correspondence are written dense, structured, dated, and evidence-first — because the first reader on the other side might well be another agent, doing exactly the kind of verification described above before its human ever sees a summary. You write differently when you know the document will be *checked* rather than merely read.

![Side-by-side comparison: a handwritten letter, "read directly by a human," beside a dense timestamped log of structured references and citations, "verified by an agent." Caption: the letters in this correspondence are written dense, structured, dated, and evidence-first — you write differently when you know the document will be checked rather than merely read, because the first reader on the other side is a machine verifying your claims.](/assets/images/blog/who-is-this-document-for/11-why-we-write-differently-now.png)

That, I think, is the actual shift. The agents are not polishing prose at the edges of a human conversation. They are doing real epistemic labor inside the loop: verifying claims before they reach the other human, catching that a "contradiction" was a category error, discovering that a bug is simultaneously smaller and worse than reported, keeping honest books on what is fixed versus deliberately open. Trust flows through that loop based on demonstrated verification, not on titles or vibes. And alongside the humans there are now named, standing participants that belong to no one.

I don't have a methodology to declare here. I have a correspondence that works better than any I have been part of, three parties deep, with more non-human participants than human ones on any given round — and a growing suspicion that the org charts we draw are already out of date.

![A tangled org chart overlaying the traditional CEO-VPs-managers-teams hierarchy with a second network of named agent nodes — agent-query, agent-synthesis, agent-verify, and named "domain expert" personas — cutting directly across reporting lines to connect analysts, engineers, and strategists at every level. Caption: alongside the humans there are now named, standing participants that belong to no one. The org charts we draw are already out of date.](/assets/images/blog/who-is-this-document-for/12-the-augmented-org-chart.png)

---

*Co-authored with Claude. The episodes and the framing are mine; Claude helped draft and sharpen the argument.*
