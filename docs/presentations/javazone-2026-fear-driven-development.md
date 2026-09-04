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

## Watch the recording

<div class="presentation-video">
  <video controls preload="metadata">
    <source src="/assets/videos/javazone-2026-trust-but-verify/recording.mp4" type="video/mp4">
    <track kind="subtitles" srclang="no" label="Norsk" src="/assets/videos/javazone-2026-trust-but-verify/no.vtt" default>
    <track kind="subtitles" srclang="en" label="English" src="/assets/videos/javazone-2026-trust-but-verify/en.vtt">
    <track kind="subtitles" srclang="es" label="Español" src="/assets/videos/javazone-2026-trust-but-verify/es.vtt">
    Your browser doesn't support embedded video — <a href="/assets/videos/javazone-2026-trust-but-verify/recording.mp4">download the recording</a> instead.
  </video>
</div>

Recorded live at JavaZone 2026. Spoken in Norwegian — turn on captions (the CC button in the player) and pick Norsk, English, or Español.

### Prefer to watch fully dubbed?

AI-dubbed full versions, voice-cloned from the original recording — no subtitles needed.

**English**

<div class="presentation-video">
  <video controls preload="metadata">
    <source src="/assets/videos/javazone-2026-trust-but-verify/recording-en.mp4" type="video/mp4">
    Your browser doesn't support embedded video — <a href="/assets/videos/javazone-2026-trust-but-verify/recording-en.mp4">download the English version</a> instead.
  </video>
</div>

**Español**

<div class="presentation-video">
  <video controls preload="metadata">
    <source src="/assets/videos/javazone-2026-trust-but-verify/recording-es.mp4" type="video/mp4">
    Your browser doesn't support embedded video — <a href="/assets/videos/javazone-2026-trust-but-verify/recording-es.mp4">download the Spanish version</a> instead.
  </video>
</div>

**Português**

<div class="presentation-video">
  <video controls preload="metadata">
    <source src="/assets/videos/javazone-2026-trust-but-verify/recording-pt.mp4" type="video/mp4">
    Your browser doesn't support embedded video — <a href="/assets/videos/javazone-2026-trust-but-verify/recording-pt.mp4">download the Portuguese version</a> instead.
  </video>
</div>

## What the talk covers

**Six fears, six systems.** Each fear is a real incident, not a hypothetical: a 500KB file that wanted to allocate 1.1 gigabytes from a single misaligned field, a filter that passed tests but broke production the next day, 23 minutes of a broken `main` branch, a $100,000 cost projection for one 2.5-week project, 47 changed files understood maybe 60%, and green tests reporting the wrong answer. Each one gets paired with the system built in response — round-trip and property-based testing, battle-testing against 191 real-world files, CI as the only arbiter that can override the AI's confidence, disciplined model selection, directed synthesis through independent verification tools, and measurement instead of just pass/fail.

**The proof.** 10,035 tests (99.8% pass rate), 695 commits at ~40/day, zero AI-induced production bugs, delivered in 2.5 weeks.

**Down the rabbit hole.** What happened after lib-pcb shipped — the comprehension problem that generation speed creates, and the tools built to stay oriented inside a codebase growing faster than any one person can read: Synthesis (a knowledge graph over the codebase), and KCP (the Knowledge Context Protocol), now with six projects testing the idea from different angles — kcp-commands, kcp-memory, kcp-agent, kcp-harness, pi-kcp, and Sunstone Atlas.

**The lesson.** The developers who are scared of AI get the most value from it — but only the ones who automate that fear, not the ones who either trust blindly or manually re-verify everything by hand.

**The formula:** Fear → Identify Risk → Design System → Automate Paranoia → Trust Process → 10× Productivity.

---

The deck above is the full interactive version used to give the talk — same navigation, same speaker notes, same optional per-fear deep-dives, opens in a new tab.
