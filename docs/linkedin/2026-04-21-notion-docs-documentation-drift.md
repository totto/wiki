---
tags:
  - LinkedIn
  - Writing
date: 2026-04-21
---

# Notion docs — documentation drift

*April 21, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7452448517735919617)*

**12 reactions · 4 comments · 724 views**

---

Your AI agent can read your Notion docs.

That's not always good news.

Documentation drifts. A decision gets revised but the write-up doesn't follow. An architecture page says "microservices" — the repo says monolith. An agent that reads both and trusts both is now navigating contradictions it has no way to resolve.

We built Notion integration for Synthesis. The goal wasn't just "give the agent more context." It was to give it the ability to read the room — to work with organizational knowledge while being aware that Notion and the codebase can be out of sync, and surfacing that when it matters.

Three health signals fell out of the work:  
 - W022: notion-stale — workspace hasn't synced  
 - W023: notion-orphan — page hierarchy has drifted  
 - W024: notion-conflict — naming conventions are inconsistent

These weren't planned. They emerged from a single question: what does it look like when documentation can't be trusted?

The hard part isn't giving an agent more to read. It's teaching it to notice when what's written and what's real have come apart.

---

## Discussion

> **Totto** ↩: Blog post with all the juicy details...   https://wiki.totto.org/blog/2026/04/21/when-your-agent-can-finally-read-the-room/#the-wall

> **Flagging the gap between documentation and reality is such a smart way to handle drift.**: Flagging the gap between documentation and reality is such a smart way to handle drift.

> **That's a funny perspective. Documentation is usually the worst source for information, the code is the truth. As a developer I know everything about that. always said "confluence, were information go to die" 😄.**: That's a funny perspective. Documentation is usually the worst source for information, the code is the truth. As a developer I know everything about that. always said "confluence, were information go to die" 😄.

> **Totto** ↩: Espen Schulstad Haha, true — Confluence is where intentions go to retire. But that's actually the interesting part. Code tells you what is*. Stale docs tell you what was* decided and never followed through on. "We're moving to microservices" sitting in a doc while the monolith grew — that's signal, not noise. The problem isn't that docs drift. It's treating them as current truth instead of read...

---

← [All LinkedIn posts](index.md)
