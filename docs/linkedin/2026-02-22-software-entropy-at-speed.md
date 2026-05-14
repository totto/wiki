---
tags:
  - LinkedIn
  - Writing
date: 2026-02-22
---

# Software Entropy at Speed

*February 22, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7431352219771383809)*

**11 reactions · 1 comments · 559 views**

---

This is what software entropy looks like at speed.

I spent the weekend building more useful functionality into Synthesis. 53,000 lines. 42 features. Five phases of code analysis — from dependency graphs to full security scanning. 3,932 tests passing by Sunday evening.

Then I ran it on Synthesis (doogfooding).

It found and created github issues for some prompt injection vectors in our own AI code. 4 RAG poisoning instances. some more missing prompt boundaries. All written that same weekend, all missed until the tool looked.

And it picked up the issues and fixed them.

This is the part traditional scanners miss entirely — SonarQube, Snyk, Checkmarx have no concept of prompt injection or RAG poisoning. Those risks didn't exist when those tools were designed.

Fast development with AI doesn't just generate features. It generates disorder at the same velocity. We've found two answers to that. Skill-Driven Development keeps entropy from forming — structured skills and context  so the AI builds with understanding, not just speed. Synthesis finds what slips through anyway.

Neither works without the other.

We built the detector. It found entropy in itself. We fixed it. In 4 hours.

That loop — that's the methodology.

---

## Discussion

> **Totto** ↩: In action:

fix(security): S010 scanner now skips XML-commented-out dependencies in pom.xml
DependencyInventoryExtractor.parsePomDependencies() stripped XML comment
blocks before matching dependency tags, preventing false-positive CVE
signals for dependencies that are present in source but excluded from
the build (e.g. Cantara/reactiveservices commons-text 1.9 was flagged as
Text4Shell RCE desp...

---

← [All LinkedIn posts](index.md)
