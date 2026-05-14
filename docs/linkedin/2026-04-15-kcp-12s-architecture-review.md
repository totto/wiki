---
tags:
  - LinkedIn
  - Writing
date: 2026-04-15
---

# KCP 1.2s architecture review

*April 15, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7450073663048945664)*

**24 reactions · 5 comments · 16,083 views**

---

We cancelled a 45-minute architecture review last week.                      
                                                   
 Not because the question wasn't important. Because the answer already existed.           
                                                   
 The question: "If we change the payment service API contract, what else breaks?"  
                                                   
 In any system older than a few years, nobody has the full picture. So the usual move is to find the 4-5 people who each have a piece of it, block out 45 minutes, and spend the first half just assembling what the organisation already knows.                     
                                                   
 Instead, we ran a query.

synthesis search "payment service API consumers"

1.2 seconds. 14 repos checked. Three downstream services with their contract versions. One SDK. And a batch job that nobody on the current team remembered — running nightly at 03:00, calling the v2 endpoint.

That last one would have been discovered in production.

The meeting still happened. 15 minutes, 3 people instead of 5. We talked about the decision — versioning strategy, migration timeline, who owns the deprecated endpoint. Not about what exists.

This is the shift I keep coming back to: architecture reviews aren't a process problem. They're an infrastructure problem. When organisational knowledge can't be queried, it gets assembled in meetings. That's a reasonable workaround for a structural deficit.

The meeting was never the problem.

Full post on the blog if you want the detail on how KCP manifests make this work.

---

## Discussion

> **Totto** ↩: Full blogpost: https://wiki.totto.org/blog/2026/04/15/we-cancelled-a-45-minute-architecture-review-a-kcp-query-answered-it-in-12-seconds/

> **These lines here hit hard and should be written on stone**: These lines here hit hard and should be written on stone

> **Totto** ↩: Matias Luis Lotito Ralli 
 That paragraph took 30 years to write. 😄         

 The process workaround is so well-established that most organisations have stopped noticing it's a workaround. Change advisory boards, architecture review boards, cross-team syncs — all reasonable responses to the same missing layer.

 Appreciate you pulling that out.

> **Yep, and now imagine this information now available always for all agentic work done by this org. So whenever there is a change, it takes into account payments and other important pieces of information.Can we get to 0 regressions with agentic AI?  👀 **: Yep, and now imagine this information now available always for all agentic work done by this org. So whenever there is a change, it takes into account payments and other important pieces of information.Can we get to 0 regressions with agentic AI?  👀

> **This is a view of how governance can and should be . AI supported and controlled by human risk decision making**: This is a view of how governance can and should be . AI supported and controlled by human risk decision making

---

← [All LinkedIn posts](index.md)
