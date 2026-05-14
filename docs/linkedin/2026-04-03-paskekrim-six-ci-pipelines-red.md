---
tags:
  - LinkedIn
  - Writing
date: 2026-04-03
---

# Påskekrim — six CI pipelines red

*April 3, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7445859144919801857)*

**13 reactions · 2 comments · 1,150 views**

---

Six CI pipelines. All red. The mug said "It works on my machine."  
                                                       
 It was Easter week in Norway. I was supposed to be reading crime novels.

Instead I spent three days hunting two TypeScript murders that only existed in Docker — invisible to vitest locally, caught only by tsc 2000 km away in a CI container.

TS2783: property specified twice (explicitly + via ...overrides spread). Esbuild strips types at the speed of indifference. No questions about provenance.

TS2322: a value conjured at velocity. "scenario_seed" assigned to a union type it never belonged to. A  string that didn't know it had committed identity fraud.

Then a squash-merge cascade through 6 stacked PRs. 30+ merged by the end of the sprint.

But here's the twist that reframed the whole week:

A student from an SDD workshop went home and built a meal planning app with Norwegian grocery API integration. In two days. 15,500 lines of code. 326 tests. 82% coverage. Live and deployed.

The crimes weren't failures. They were evidence of scale. When AI-augmented output volume reaches a certain threshold, once-a-sprint friction surfaces six times a day. The solution isn't to slow down — it's better forensics at the scene. (tsc --noEmit pre-push hook. Obvious in retrospect.)

Full story on the wiki — written in påskekrim format, with NotebookLM slides that are frankly better than the prose:

https://lnkd.in/e4UJCfTP

#ClaudeCode #TypeScript #DeveloperExperience #AIAugmentedDevelopment #Påskekrim

---

## Discussion

> **Love the twists :d**: Love the twists :d

> **Totto** ↩: Thank you :)

---

← [All LinkedIn posts](index.md)
