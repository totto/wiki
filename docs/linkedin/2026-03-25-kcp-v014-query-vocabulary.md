---
tags:
  - LinkedIn
  - Writing
date: 2026-03-25
---

# KCP v0.14 query vocabulary

*March 25, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7442648447595241472)*

**11 reactions · 2 comments · 489 views**

---

Every agent that queries a knowledge manifest reinvents filtering.

One tool checks token budgets. Another filters by audience. A third ignores stale content. None of them agree on the format. You cannot swap one for another without rewriting the glue.

KCP v0.14 standardises this.

The query vocabulary (§15) gives agents a shared way to ask: which units match my task, fit my budget, andrequire capabilities I actually have? Scored results. Budget-constrained selection. Stale content filtered. Federation across sub-manifests in one hop.

We also published RFC-0014 — a composition model so teams stop forking manifests and start inheriting them. Open for discussion.

Full writeup + examples in the article linked in comment.

#KCP #AIAgents #OpenSource #KnowledgeContextProtocol

---

## Discussion

> **Full post:  https://wiki.totto.org/blog/2026/03/25/every-agent-that-queries-a-knowledge-manifest-reinvents-filtering/**: Full post:  https://wiki.totto.org/blog/2026/03/25/every-agent-that-queries-a-knowledge-manifest-reinvents-filtering/

> **This is a classic problem when agents grow beyond a single domain - inconsistent filtering logic across tools makes it nearly impossible to debug which agent is actually causing issues downstream. One approach that helps is centralizing the filtering rules as a schema layer that all tools validate against before execution, then logging what each tool rejected and why. If you're deploying this to production, you might also want real-time visibility into which filters are actually being triggered per agent run - something like AgentShield provides cost and safety scoring that can catch when filtering rules are silently dropping critical queries.**: This is a classic problem when agents grow beyond a single domain - inconsistent filtering logic across tools makes it nearly impossible to debug which agent is actually causing issues downstream. One approach that helps is centralizing the filtering rules as a schema layer that all tools validate against before execution, then logging what each tool rejected and why. If you're deploying this t...

---

← [All LinkedIn posts](index.md)
