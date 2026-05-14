---
tags:
  - LinkedIn
  - Writing
date: 2026-04-06
---

# Memory rots — deterministic maintenance

*April 6, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7446809082138738688)*

**16 reactions · 8 comments · 1,463 views**

---

Memory that is not maintained becomes memory that lies.                                   
                                                               
 Worse than no memory at all. Your agent confidently acts on stale context, makes decisions based on priorities that shifted weeks ago, references contacts who changed roles. It doesn't know what it doesn't know.               
                                                               
 We hit this at week eight. Our memory system worked — until it didn't. Four rot patterns emerged: topic files going stale, hot topics becoming cold, new knowledge with no home, and the index itself lying about what existed.

So we built maintenance into the system. Two tools — topic-health and topic-triage — that score memory behaviorally. Session frequency times recency. No LLM in the loop. Milliseconds, not minutes.

The counterintuitive result: 19 topic files replaced 25. Smaller system, better performance. Freshness beats completeness every time.

A nightly cron at 02:45 runs advisory scans. ConsolidateState uses dual thresholds to prevent both over-running and under-running. All deterministic. All auditable.

The circular dependency problem — using an LLM to maintain the memory an LLM depends on — is why this has to be mechanical.

New blog post in comments.

#AgentMemory #AIEngineering

---

## Discussion

> **Totto** ↩: Full post:  https://wiki.totto.org/blog/2026/04/06/agent-memory-rots-heres-how-we-stopped-it/

> **agent memory problems are state hygiene problems dressed up as AI problems …**: agent memory problems are state hygiene problems dressed up as AI problems …

> **Totto** ↩: André Lindenberg 
Largely agree — topic-health and ConsolidateState are state hygiene mechanisms with new names. The wrinkle that feels AI-specific: the episodic-semantic propagation gap. Sessions accumulate context the model never writes back as durable knowledge. That's not just stale state — it's state that was never captured at all. The hygiene tools then operate on   an incomplete picture.

> **Das zirkuläre Abhängigkeitsproblem ist der entscheidende Punkt — und es geht über Engineering hinaus.

Stale memory erzeugt keine Fehlermeldung. Der Output sieht korrekt aus; die vergifteten Prämissen sind unsichtbar. Das ist strukturell dasselbe Versagensmuster wie bei agentic systems, die EU AI Act Art. 14 (meaningful human oversight) formal erfüllen — aber nur den Terminal-Output loggen, nicht die Entscheidungskette dahinter.

Observability ≠ Governance. Ein Dashboard, das "3.000 Sessions indiziert" zeigt, während das semantische Layer seit acht Wochen veraltet, ist Governance-Theater.

"Freshness beats completeness" gilt auch für Audit-Infrastruktur.**: Das zirkuläre Abhängigkeitsproblem ist der entscheidende Punkt — und es geht über Engineering hinaus.

Stale memory erzeugt keine Fehlermeldung. Der Output sieht korrekt aus; die vergifteten Prämissen sind unsichtbar. Das ist strukturell dasselbe Versagensmuster wie bei agentic systems, die EU AI Act Art. 14 (meaningful human oversight) formal erfüllen — aber nur den Terminal-Output loggen, nic...

> **Totto** ↩: JeanPaul Goldschmidt 
 The governance theatre framing is precise — and it cuts deeper than most compliance discussions go.

 Session count tells you the system is active. It says nothing about whether the reasoning substrate is sound. Art. 14 "meaningful oversight" requires evaluating the quality of inputs to a decision, not just observing terminal output.  Stale memory is the canonical failure...

> **"Whether that's governance-grade is a separate question" — das ist genau die richtige Frage.

Für DORA- und NIS2-Prüfer bedeutet governance-grade konkret: der Nachweis muss vor der Prüfung existieren, nicht erst während. Ein Freshness-Score mit Timestamp und Session-Frequenz, der nightly läuft und ins Log schreibt, erfüllt das strukturell. "The model decided" nicht.

Das Problem: den Prüfer, der das beurteilen kann, gibt es noch nicht. Die Infrastruktur ist der Aufsichtspraxis um Jahre voraus.**: "Whether that's governance-grade is a separate question" — das ist genau die richtige Frage.

Für DORA- und NIS2-Prüfer bedeutet governance-grade konkret: der Nachweis muss vor der Prüfung existieren, nicht erst während. Ein Freshness-Score mit Timestamp und Session-Frequenz, der nightly läuft und ins Log schreibt, erfüllt das strukturell. "The model decided" nicht.

Das Problem: den Prüfer, de...

> **Another must read! 

I like the way you approach this by deterministic methods instead of “the LLM said this scores 0.3”. **: Another must read! 

I like the way you approach this by deterministic methods instead of “the LLM said this scores 0.3”.

> **Totto** ↩: Matias Luis Lotito Ralli 
Exactly — deterministic beats probabilistic for anything that needs to be auditable. When memory degrades, you want to  know which rule triggered a consolidation, not why a model thought the context felt stale. Same reason your governance point from yesterday lands: predictable mechanics are the precondition for meaningful oversight.

---

← [All LinkedIn posts](index.md)
