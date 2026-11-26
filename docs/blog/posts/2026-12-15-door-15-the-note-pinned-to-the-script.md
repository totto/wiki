---
date: 2026-12-15T05:00:00
slug: door-15-the-note-pinned-to-the-script
image: assets/images/night-desk/door-15.webp
description: "A theatre story about a code injection. CVE-2026-1281."
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

# Door 15: The Note Pinned to the Script

![Illustration for Door 15: The Note Pinned to the Script](../../assets/images/night-desk/door-15.webp)

*A theatre story about a code injection. CVE-2026-1281.*

Kaldhavn, 15 December. Nine candles left.

The ferry line's operations manager had come in person, which people did when they wanted to be told that everything was fine.

<!-- more -->

"We did this one," she said. "January. It was in all the papers. We patched within the week. I only want it ticked off before the audit."

On the desk between them lay the thing she meant: Ivanti's mobile manager, the appliance that keeps every phone and tablet on the ferries in order. In January its maker had announced a flaw that was already being used against a small number of customers. Hull explained it as a matter of the theatre. An actor is handed a script and is meant to speak the lines. In two corners of this play, the parts that hand out the company's own apps and move files to its Android devices, the actor did something else. He performed whatever a stranger had written into the margin. The stranger did not need a ticket to get in.

*Seen: the ferry line's change log, 4 February. "Security patch applied, EPMM." Inferred: patched.*

"There," said the manager.

"Patched with what?" said Hull.

The manager looked at her.

"In January there was no new edition of the play," Hull said. "There wasn't time. What the maker sent out was a note to pin to the script. *At this line, do not improvise.* It works. But it is pinned to that copy of the script. The maker said so in as many words: when you move to a new edition, the note does not come with you. You pin it again." She turned to the screen. "When did they last change edition?"

The fan under the stairs rose.

*Seen: the appliance was upgraded on 6 March, from 12.6.0.0 to 12.7.0.0. Routine. Seen: the change log for that day does not mention the note. Seen: I have now looked on the appliance itself. The note is not there.*

*My inference was one label too high again. The log said "patched". I did not ask what the word meant in January.*

"No," Hull said. "But you said so before I had to." She was aware that this was not what she would have said a fortnight ago.

The manager had gone quite still. "Since March."

"Since March."

It is not a comfortable thing to learn across a desk. For nine months the ferry line had believed, in good faith and with a signed change log, that a door was shut. Out on the internet, the watchers who keep decoy doors had gone on recording people trying this one, month after month, into the autumn.

*Seen: the maker's guidance says where to look for signs of entry. I have looked in the logs the appliance still holds. Seen: none of the signs, in ninety days of log. Guessed: none before that. The older logs are gone.*

"Then we say that, and no more than that," Hull said. "Ninety days clean. Before that, not known." She drew the lodger's draft towards her: pin the note again tonight, and book the move to the edition in which the correction is printed in the script itself. She read it through and turned the key.

The relay clicked. The manager let out a breath.

"Nobody did anything wrong," she said. It was half a question.

"No. You patched in a week. Then you kept your system up to date, which is what we tell everyone to do, and the one undid the other. I would have ticked it off myself." Hull wrote the line in the ledger while it was fresh. "The lesson I'd take to your audit is a small one. Never write *patched* in a log. Write what you did."

*Ledger, 15 December. Ferry line phone manager, Ivanti EPMM: the January patch was a temporary one and did not survive March's upgrade to 12.7.0.0. Unprotected for nine months in good faith. Patch reapplied tonight; permanent version booked. No signs of entry in ninety days of logs; earlier not known. Not found by us. The lodger read the log; I asked what it meant. Signed, T.A.H., with M.*



```
THE REAL ONE

CVE:              CVE-2026-1281
Affected:         Ivanti Endpoint Manager Mobile (EPMM), on-premises: 12.5.1.0
                  and earlier, 12.6.1.0 and earlier, 12.7.0.0 and earlier (as
                  listed by CERT-EU from Ivanti's advisory)
Bug class:        Code injection (CWE-94, Improper Control of Generation of
                  Code)
Severity:         9.8, CVSS 3.1, as scored by Ivanti
What it was:      "A code injection in Ivanti Endpoint Manager Mobile allowing
                  attackers to achieve unauthenticated remote code execution"
                  (CVE record). The affected features are In-House Application
                  Distribution and Android File Transfer Configuration.
Found by:         not publicly credited
How it was found: not stated. Ivanti said at disclosure: "We are aware of a
                  very limited number of customers whose solution has been
                  exploited at the time of disclosure."
In the dark for:  not stated
Exploited:        yes, before disclosure; added to the CISA KEV catalog on
                  2026-01-29. Shadowserver's honeypots logged exploitation
                  attempts on 32 days between 2026-02-01 and 2026-10-04 (via
                  CIRCL's Vulnerability-Lookup).
Fixed in:         first by an RPM script (12.x.0.x or 12.x.1.x, by version),
                  2026-01-29. Ivanti: "If after applying the RPM script to
                  your appliance, you upgrade to a new version you will need
                  to reinstall the RPM." The permanent fix was announced for
                  version 12.8.0.0; Ivanti's release notes record 12.8.0.0 on
                  2026-03-18. That it contains the fix rests on Ivanti's
                  January announcement.
What to do:       Move to 12.8.0.0 or later. Until then, apply Ivanti's RPM
                  script and reapply it after any upgrade. Check for signs of
                  compromise as Ivanti's guidance describes.
Sources:          https://forums.ivanti.com/s/article/Security-Advisory-Ivanti-Endpoint-Manager-Mobile-EPMM-CVE-2026-1281-CVE-2026-1340
                  · https://docs.ivanti.com/epmm/release-upgrade-guide/revision-history
                  · https://cveawg.mitre.org/api/cve/CVE-2026-1281
                  · https://cert.europa.eu/publications/security-advisories/2026-001/
                  · https://www.helpnetsecurity.com/2026/01/30/ivanti-epmm-cve-2026-1281-cve-2026-1340/
                  · https://vulnerability.circl.lu/vuln/CVE-2026-1281
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 14](2026-12-14-door-14-the-voice-in-the-file-server.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
