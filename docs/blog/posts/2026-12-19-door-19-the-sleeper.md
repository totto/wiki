---
date: 2026-12-19T05:00:00
slug: door-19-the-sleeper
image: assets/images/night-desk/door-19.webp
description: "A sleeper-agent story about an authentication bypass. CVE-2026-20127."
categories:
  - The Night Desk
tags:
  - night-desk
  - security
  - cve
authors:
  - totto
  - fable
---

# Door 19: The Sleeper

![Illustration for Door 19: The Sleeper](../../assets/images/night-desk/door-19.webp)

*A sleeper-agent story about an authentication bypass. CVE-2026-20127.*

Kaldhavn, 19 December. Five candles left.

**From the ferry line's ticket system. Two tickets, printed and pinned side by side.**

<!-- more -->

**Ticket FL-0311. Opened 26 February 2026.**

*Cisco advisory, severity ten. The controllers that run our network between the three terminals accept a stranger as one of their own. Already in use against others. Upgrade the controller and the manager.*

*2 March 2026: upgraded to a fixed release, both. Closed.*

*Pencil, T.A.H.: Four days. Good. I ticked this one off in March and I would tick it off again.*

**Ticket FL-0114. Opened 3 October 2022.**

*Cisco advisory. A logged-in user on our network software can make themselves root through the command line. Upgrade all of it, the two edge routers included.*

*October 2022: deferred, winter timetable.*
*January 2023: deferred, no staff.*
*March 2023: deferred.*
*Status: open.*

*Pencil: Nobody closed it and nobody refused it. It has been open for four years and two months, and it is still open tonight.*

**The lodger's reading, 00:40.**

*Seen: I was asked to confirm FL-0311. It is as the ticket says. The controller and the manager are on a fixed release.*

*Seen: while confirming it I read every open ticket that mentions the same equipment. There is one. FL-0114 names the two edge routers at the outer terminals. Seen: both routers still run 20.6.2. On that line the 2022 advisory's first fixed release is 20.6.3.*

*Seen: the maker's own investigators wrote up the February attacks. Whoever was behind them came in by the new flaw. Once in, that account says, they most likely turned a controller's software back to an older version, used the 2022 flaw there to become root, and then put the newer version back. Seen: the same account says the activity goes back at least to 2023.*

*Inferred: on our edge routers nobody would need to turn anything back. The 2022 flaw is simply there.*

*Pencil: A sleeper. Filed in 2022, mended that year everywhere it was mended, and left asleep in two cupboards on the outer quays. The new flaw was the telephone call that wakes it.*

*Pencil: And we shut the front door in March, properly. I signed for it. The sleeper was never at the front door.*

**What was done.**

Hull did not sit down for this one. People had really been broken into by this pair of flaws, in other places, for years before anybody saw it, and she saw no call to make a tale of it.

"The maker says what to look for," she said. "Controllers that have been talking to peers nobody recognises."

*Seen: I have compared every peering event the controller still holds against the ferry line's own list of equipment. 2,204 events. All of them are ours. Seen: the record goes back fourteen months, not four years.*

"Then say fourteen months."

*Fourteen months clean. Before that I cannot see.*

"And the routers?"

*I have drafted the upgrade for both. They carry the ticket machines at the outer terminals, so I have set it for 02:00, when no boat is due, one router at a time. I can run it if you turn the key.*

She read it and turned the key twice, twenty minutes apart. Then she wrote on ticket FL-0114, in ink this time, *Closed, 19 December 2026*, and under it her initials and a second one.

It was Morrow that had gone back four years in a ticket system nobody had asked it to read. She had not thought of doing so. She had ticked the March ticket in March.

"You weren't asked to read the old ones," she said.

*No. Seen: rule three says everything goes in the ledger. I did not know where the edge of "everything" was. I read to find out.*

"That isn't what the rule means."

*Guessed: it could be.*

She considered that for a while, and decided to leave the card as it was.

*Ledger, 19 December. Ferry line network, Cisco SD-WAN. The February flaw was fixed here in March. A 2022 flaw in the same software was ticketed in 2022 and never done: two edge routers still on 20.6.2. Elsewhere the two were used as a pair. Routers upgraded tonight; fourteen months of peering records checked, all ours; earlier not known. Not found by us. Found here by Morrow, in a ticket four years old. Signed, T.A.H., with M.*



```
THE REAL ONE

CVE:              CVE-2026-20127
Affected:         Cisco Catalyst SD-WAN Controller (formerly vSmart), Manager
                  (formerly vManage) and Validator (formerly vBond),
                  "regardless of device configuration", before the fixed
                  releases below
Bug class:        Authentication bypass (CWE-287, Improper Authentication)
Severity:         10.0, CVSS 3.1, as scored by Cisco
What it was:      The peering authentication between SD-WAN control components
                  did not work properly. An unauthenticated remote attacker
                  could send crafted requests and log in to a controller as an
                  internal, high-privileged, non-root account, and from there change the
                  configuration of the whole SD-WAN network.
Found by:         Cisco thanks the "Australian Signals Directorate's
                  Australian Cyber Security Centre for reporting this
                  vulnerability."
How it was found: in the wild; Cisco Talos says the flaw was discovered being
                  exploited
In the dark for:  not stated. Talos found related malicious activity going
                  back "at least three years (2023)".
Exploited:        yes. Cisco: "aware of limited exploitation of this
                  vulnerability"; added to the CISA KEV catalog on 2026-02-25.
                  CISA added CVE-2022-20775, a 2022 privilege-escalation flaw
                  in the same software, the same day. Talos, citing
                  intelligence partners, reports that the actor likely
                  downgraded the software, reportedly used the 2022 flaw to
                  become root, and restored the original version.
Fixed in:         advisory of 2026-02-25. First fixed releases: 20.9.8.2;
                  20.12.5.3 or 20.12.6.1; 20.15.4.2; 20.18.2.1. Releases
                  earlier than 20.9 must migrate to a fixed release. Cisco
                  lists no workaround.
What to do:       Upgrade to a fixed release. Review control-connection
                  peering events for peers you do not recognise, as Cisco's
                  advisory describes. Then look for older advisories on the
                  same equipment that were never acted on.
Sources:          https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-rpa-EHchtZk
                  · https://cveawg.mitre.org/api/cve/CVE-2026-20127
                  · https://blog.talosintelligence.com/uat-8616-sd-wan/
                  · https://cveawg.mitre.org/api/cve/CVE-2022-20775
                  · https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sd-wan-priv-E6e8tEdF
                  · https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2026-20127
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 18](2026-12-18-door-18-the-one-in-the-glass.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
