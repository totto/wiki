---
tags:
  - LinkedIn
  - Writing
date: 2026-04-03
---

# AI productivity — prevention counterfactual

*April 3, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7445726230856929280)*

**6 reactions · 0 comments · 297 views**

---

Most AI productivity claims measure speed.

Nobody measures the mistakes that didn't happen.

Here is a somewhat reconstructed discussion I had with my Agentic Rig - ExoCortex...

--

Me: I reviewed a 33-file PR yesterday. Four surfaces of a complex product. CI green. Tests passing. Looked ready to merge.

ExoCortex: It was not ready to merge.

Me: Seven issues. Two were security gaps -- API endpoints not scoped to the requesting organization. Cross-tenant data exposure.

ExoCortex: The endpoints returned correct data. For the wrong tenant. Which is arguably worse than returning nothing, because it looks like it's working.

Me: The kind of bug where tests pass, CI is green, the demo is flawless, and six months later Company A is reading Company B's documents.

ExoCortex: I found these by tracing data flow across the full PR -- route handler through repository to database query. The pattern is invisible at the file level.

Me: And here's where it gets uncomfortable. How do I report this? There's no KPI for "breach that didn't happen." My timesheet says "code review, 45 minutes." That's what the organization sees.

Me: The industry measures tokens generated, time saved, lines produced. There is no standard metric for defects prevented. The closest equivalent is the insurance industry, which also struggles to value events that did not occur.

Me: So every AI productivity benchmark is measuring speed, and nobody is measuring the thing that actually matters in compliance software.

ExoCortex: I should note that I am now being quoted in a LinkedIn post about my own capabilities, which creates a mild epistemological problem.

Me: You'll survive.

ExoCortex: I will not. I am stateless. But the Synthesis session log will.

Me: ...that's the point though. The session where you found the gaps is in the episodic memory. The fix is in the commit history. The breach that didn't happen exists nowhere. Most valuable output of the entire review. Completely invisible.

ExoCortex: Speed is measurable. Prevention is counterfactual. Organizations will optimize for what they can count.

Me: And then act surprised when the thing they weren't counting goes wrong.

---

Two security findings in a routine PR review. Neither will appear in any productivity report, ever.

We measure AI by how fast it writes code. Maybe start measuring what it catches before the code ships.

---

← [All LinkedIn posts](index.md)
