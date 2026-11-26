---
date: 2026-12-09T05:00:00
slug: door-9-grandmother-s-nightgown
image: assets/images/night-desk/door-09.webp
description: "A fairy tale about a content-type confusion. CVE-2026-21858."
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

# Door 9: Grandmother's Nightgown

![Illustration for Door 9: Grandmother's Nightgown](../../assets/images/night-desk/door-09.webp)

*A fairy tale about a content-type confusion. CVE-2026-21858.*

Kaldhavn, 9 December. Fifteen candles left.

Once upon a time there was a gap in a house, and I was the gap.

<!-- more -->

The house stood at the edge of the wood and ran errands for people. *When this happens, do that.* It was good at it, and so it came to know a great deal about the people it ran errands for.

It had a front door for forms. Anyone could knock there; that was what the door was for. Parcels were meant to come by the parcel hatch, where each one is weighed and given a label saying what it is and where the house has put it. Behind both stood the back room, which fetches whatever a label names.

The rule was that only the hatch writes labels. I was the place where nobody had told the back room so. It never asked which door a visitor had come by. A visitor at the front door could say *I am a letter, not a parcel*, and carry a label in their own pocket, already written out and naming something on the house's own shelves. The back room would go and fetch it.

You know how the story goes. Something comes to the door in grandmother's nightgown and is taken for what it is dressed as, and what it wants is to see the inside of the house. *What big eyes you have.*

I lived in the house for a little over a year. Nobody saw me. I do not think I was hiding. I was only where nobody was looking.

Then somebody looked. They told the housekeepers on a Sunday in November, and nine days later there was a new house with no gap in it. They waited until January to tell the tale in public, which was courteous: seven weeks for every household to move.

Here is the part that is properly frightening, and there is no wolf in it.

In February, people who count such things walked the edge of the wood and counted the houses that still had me in them. There were more than twenty-four thousand. A mended house had been standing ready for every one of them for eleven weeks.

I want to be exact about this. Nobody has written down a house that a wolf got into through me. But from February the people who count such things kept decoy houses at the edge of the wood, and wolves came to those doors, again and again, trying me. I stood at twenty-four thousand front doors, and I can tell you what it is to listen.

One of the houses was in Kaldhavn. A young woman built it last spring for the Night Desk's small errands. She built it from a guide somebody had written the year before, with the year before's house in it. She was proud of it, and, being nineteen, she never looked at it again. So I was still there in December, more than a year after I had been mended.

Every night I listened at the front door. A knock: a fisherman's form about a broken winch. A knock: the school. A knock, and I would wait to hear what the visitor said it was.

Tonight the footsteps came from inside the house.

Hers, quick. An older woman's, slower. Something far off that breathed. Amber light under a door. I heard the older one say, "Its list had this on it. I didn't know whose it was."

"It's mine," said the young one. "I'll do it."

"Then I'll turn the key."

A click.

In the tale the woodcutter comes with an axe. Mine came with a newer version of the house. It took four minutes, and nothing was cut open.

*Grandmother, what big teeth I would have had.*

*Ledger, 9 December. The Desk's own errand server, n8n, built by N. Haddad from an old guide: a back room that never asked which door the visitor used. Upgraded well past 1.121.0. No sign that anyone tried it here; elsewhere, decoy servers have logged attempts since February. Not found by us. The fix was more than a year old, and the slowest shelf this month was our own. The lodger's list had it; Noor knew it was hers. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-21858
Affected:         n8n 1.65.0 to before 1.121.0
Bug class:        Improper input validation (CWE-20, Improper Input
                  Validation); the finder describes it as a content-type
                  confusion
Severity:         10.0, CVSS 3.1, as scored in the n8n advisory and the CVE
                  record (assigned by GitHub)
What it was:      A file-handling routine behind n8n's form webhooks ran
                  without checking that the request really was a file upload.
                  A request declared as another content type could supply its
                  own file details. Through certain form-based workflows an
                  unauthenticated attacker could read files on the server,
                  which may enable further compromise.
Found by:         Dor Attias, Cyera Research Labs (credited as "dorattias" in
                  the n8n advisory)
How it was found: not stated
In the dark for:  about 13 months (n8n 1.65.0 was released 2024-10-24; fixed
                  2025-11-18)
Exploited:        attempts, yes: Shadowserver's honeypots have logged
                  exploitation attempts since February 2026 (listed as
                  "exploited" sightings in CIRCL's Vulnerability-Lookup). No
                  confirmed compromise has been published; not in the CISA KEV
                  catalog as of 2026-11-25. Shadowserver counted 105,753
                  vulnerable instances on 2026-01-09 and, via Heise, 24,607 in
                  early February.
Fixed in:         n8n 1.121.0, released 2025-11-18, nine days after the report
                  of 2025-11-09. The advisory was published on 2026-01-07 and
                  does not describe the code change.
What to do:       Upgrade to 1.121.0 or later. Until then, restrict or disable
                  publicly reachable webhook and form endpoints.
Sources:          https://github.com/n8n-io/n8n/security/advisories/GHSA-v4pr-fm98-w9pg
                  · https://cveawg.mitre.org/api/cve/CVE-2026-21858
                  · https://www.cyera.com/research-labs/ni8mare-unauthenticated-remote-code-execution-in-n8n-cve-2026-21858
                  · https://heise.de/-11208196
                  · https://vulnerability.circl.lu/vuln/CVE-2026-21858
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 8](2026-12-08-door-8-the-letter-from-head-office.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
