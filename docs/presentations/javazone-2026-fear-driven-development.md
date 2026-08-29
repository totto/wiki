---
title: "Fear-Driven Development: Turn Your Anxiety Into Automation"
---

# Fear-Driven Development: Turn Your Anxiety Into Automation

**Date:** September 2026 — JavaZone, Oslo
**Author:** Thor Henning Hetland

An honest talk about what actually goes wrong when an AI agent writes code for you, and the systems that turn each failure mode into something mechanical instead of something you have to trust. Built around six real incidents from a 2.5-week AI-assisted project (lib-pcb), each paired with the concrete system that grew out of it.

<div style="text-align:center;margin:24px 0;" markdown>
[Open the interactive slide deck →](../javazone-2026-fear-driven-development-slides/){ .md-button .md-button--primary target=_blank rel=noopener }
</div>

## What the talk covers

**Six fears, six systems.** Each fear is a real incident, not a hypothetical: a 500KB file that wanted to allocate 1.1 gigabytes from a single misaligned field, a filter that passed tests but broke production the next day, 23 minutes of a broken `main` branch, a $100,000 cost projection for one 2.5-week project, 47 changed files understood maybe 60%, and green tests reporting the wrong answer. Each one gets paired with the system built in response — round-trip and property-based testing, battle-testing against 191 real-world files, CI as the only arbiter that can override the AI's confidence, disciplined model selection, directed synthesis through independent verification tools, and measurement instead of just pass/fail.

**The proof.** 10,035 tests (99.8% pass rate), 695 commits at ~40/day, zero AI-induced production bugs, delivered in 2.5 weeks.

**Down the rabbit hole.** What happened after lib-pcb shipped — the comprehension problem that generation speed creates, and the tools built to stay oriented inside a codebase growing faster than any one person can read: Synthesis (a knowledge graph over the codebase), and KCP (the Knowledge Context Protocol), now with four components testing the idea from different angles — kcp-agent, kcp-harness, pi-kcp, and Sunstone Atlas.

**The lesson.** The developers who are scared of AI get the most value from it — but only the ones who automate that fear, not the ones who either trust blindly or manually re-verify everything by hand.

**The formula:** Fear → Identify Risk → Design System → Automate Paranoia → Trust Process → 10× Productivity.

---

The deck above is the full interactive version used to give the talk — same navigation, same speaker notes, same optional per-fear deep-dives, opens in a new tab.
