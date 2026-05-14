---
tags:
  - LinkedIn
  - Writing
date: 2026-02-25
---

# Beyond llms.txt: KCP

*February 25, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7432372973228949504)*

**10 reactions · 0 comments**

---

llms.txt is a table of contents. AI agents need a map.

A table of contents tells you what exists. A map tells you what's relevant,    
 how things connect, and whether the information is still current. Those are different problems.

I've been running production AI agents against a codebase of ~9,000 files. The agents were confident. Sometimes they were confidently wrong — and there was no way for them to know they were reading stale documentation.

I've been calling this the Mirror Test. If an agent can't tell whether its  
 knowledge is outdated, it will answer as if it isn't.

After observing six structural gaps in llms.txt at this scale, I drafted a  
proposal: the Knowledge Context Protocol (KCP). A knowledge.yaml manifest that adds topology, freshness signals, intent metadata, and selective loading.

The positioning that keeps clarifying it for me: KCP is to knowledge what MCP is to tools.

The spec, a blog post, and reference parsers (Python + Java) are at  
 https://lnkd.in/e8ZE4txV.

Full write-up at wiki.totto.org/blog — "Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents."

Have you hit this problem? What did you do about it?

---

← [All LinkedIn posts](index.md)
