---
title: "EDR MDS: A Less Is More Approach to SOA Master Data Management"
---

# EDR MDS: A Less Is More Approach to SOA Master Data Management

**Date:** September 2008 (JavaZone 2008, Oslo) — also presented at JavaONE 2007
**Slides:** [slideshare.net/totto](https://www.slideshare.net/totto/edr-mds-a-less-is-more-approach-to-mdm)

Traditional MDM platforms are expensive, complex, and often solve the wrong problem. This talk proposes a simpler, domain-driven alternative: Enterprise Domain Repositories (EDR) and Master Data Services (MDS) — a service-oriented approach to master data management that controls data redundancy through dynamic rules rather than centralised platforms.

## What the talk covers

**The MDM problem.** Existing approaches to master data management define the challenge and then introduce solutions that are disproportionately complex and costly. The talk critiques common MDM implementations and the assumptions behind them.

**The EDR-MDS model.** An Enterprise Domain Repository manages disparate business objects across multiple systems. Rather than enforcing a single golden record through a heavyweight platform, EDR-MDS enables standard software to coexist with SOA by applying dynamic, readable rules at the field and value level.

**Core capabilities:**
- Simple, inexpensive strategy to control data redundancy
- Dynamic rules for mastering at the field/value level — readable and auditable
- Automatic updates enforced across sources
- Governance through rules rather than platform lock-in
- Standard software coexistence with service-oriented architecture

**System integration.** The approach addresses how disparate business objects across multiple systems can be synchronised without a centralised hub, reducing both complexity and the failure surface of traditional MDM deployments.

**Domain-driven design.** Emphasises modelling from the domain outward rather than forcing business data into a platform's data model — a less-is-more philosophy that anticipates what later became standard DDD practice.

---

<div class="pdf-viewer">
  <object data="/assets/presentations/edr-mds-mdm.pdf" type="application/pdf">
    <div class="pdf-fallback">
      <p>PDF preview requires a browser with PDF support.</p>
      <p><a href="/assets/presentations/edr-mds-mdm.pdf">⬇ Download slides (PDF)</a> &nbsp;·&nbsp; <a href="https://www.slideshare.net/totto/edr-mds-a-less-is-more-approach-to-mdm">View on SlideShare</a></p>
    </div>
  </object>
</div>
