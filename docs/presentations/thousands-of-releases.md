---
title: "Thousands of Releases per Year, 24/7 with No Downtime, with a Team of 5"
---

# Thousands of Releases per Year, 24/7 with No Downtime, with a Team of 5

**Date:** ~2022
**Conference:** Rebel Share

*Let's talk about productivity in software development.*

The original version of this talk. 11,008 GitHub contributions in one year from a team of 5 — the opening slide makes the claim concrete before a word is spoken. What follows is an honest, opinionated account of how eXOReaction works: full active lifecycle management, 24/7, across all time zones.

## What the talk covers

**Context and scope.** eXOReaction is a custom-built, actively optimised company pushing what is really possible in bespoke software development and lifecycle management. "Last mile" mentality — we do not stop at good enough. The technology word cloud says it all: AWS, x3 Java champions, NoOps, XORcery, Whydah, Visuale, Nerthus, Stingray.

**What they do differently.** 24×7 distributed organisation, cloud-native and microservice by default, willingness to invest in homegrown libraries and tooling, and a clear-eyed view of where common industry practices fall short.

**A small rant on "Best Practice".** If best practice were a real thing, it would be defined by someone, scoped to specific problems, and agreed upon slowly — making it a good practice for some problems, from years ago. In practice it is a vendor-driven technique to persuade customers to do things the vendor's way.

**The controversial details.** The part most conference talks skip:

- *Natively distributed* — async communication by default, text over voice, developer-time not manager-time, experts at work almost 24×7 across time zones
- *Social Coding* — trunk-based development, micro-commits, no long-lived branches, branches and PRs are mostly waste, Apache ASL v2 by default
- *Microservices* — 300–500 active codebases, high-availability in the many nines, XORcery (event-sourced monolith to microservices), Stingray/Messi for traditional microservice stacks
- *NoOps* — no Kubernetes, no Istio, no Docker unless needed; semantic version-controlled pull-based environments; continuous OS and dependency patching; 7-day oil-lamp alerts; side-by-side production verification
- *Homegrown libs, frameworks and tooling* — investment in productivity that pays back across customers
- *No meetings. No timesheets.*

---

<div class="pdf-viewer">
  <object data="/assets/presentations/thousands-of-releases.pdf" type="application/pdf">
    <div class="pdf-fallback">
      <p>PDF preview requires a browser with PDF support.</p>
      <p><a href="/assets/presentations/thousands-of-releases.pdf">⬇ Download slides (PDF)</a></p>
    </div>
  </object>
</div>
