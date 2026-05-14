---
tags:
  - LinkedIn
  - Writing
date: 2026-03-20
---

# KCP v0.12 governance

*March 20, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7440685012007612416)*

**18 reactions · 2 comments · 960 views**

---

KCP v0.12 is out. We shipped three new governance blocks this week.

I've been thinking about the gap between "an agent that can do things" and "an agent I trust in production."                       
                                 
 The first is a capability problem. The second is a governance problem.

We've spent months on the first -- KCP v0.10 gave agents a query vocabulary so they stop loading entire codebases blindly. v0.11 added a cold discovery chain so agents can find the manifest from just a domain name.

v0.12 is different. It answers a harder question: what is the agent allowed to do, and how much should it trust what it found?

Three new blocks:  
 - discovery -- provenance tracking. Was this unit human-verified, crawled at 85% confidence, or inferred from marketing copy (MUST declare confidence < 0.5)?  kcp-triage by Stig Lau is exactly the tool this block was designed for.  
 - authority -- fine-grained permissions. initiative, requires_approval, or denied per action. Missing authority block = safe, not permissive.  
 - visibility -- environment and role-aware access. Same doc is internal in dev and confidential in prod. First-match-wins, fallback to default.

The Nova Corp payments API example in the post shows all three together: an agent that says "I need approval, I lack the finance role, and my source was a web crawl at 63% confidence" instead of just trying.

110+ repos carrying knowledge.yaml manifests. 284 live manifests in kcp-commands. First community tooling appearing.

Full writeup with 15 slides on my wiki:

---

## Discussion

> **Totto** ↩: Full post:  https://wiki.totto.org/blog/2026/03/20/from-capable-to-trustworthy-how-kcp-evolved-from-discovery-to-governance/

> **🔥**: 🔥

---

← [All LinkedIn posts](index.md)
