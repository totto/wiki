---
date: 2026-12-07T05:00:00
slug: door-7-the-taster-at-the-dinner-party
image: assets/images/night-desk/door-07.webp
description: "A poisoned-dinner story about a supply-chain compromise. CVE-2026-33634."
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

# Door 7: The Taster at the Dinner Party

![Illustration for Door 7: The Taster at the Dinner Party](../../assets/images/night-desk/door-07.webp)

*A poisoned-dinner story about a supply-chain compromise. CVE-2026-33634.*

Kaldhavn, 7 December. Seventeen candles left.

Hull pinned four sheets of paper to the pigeonholes and stood back from them, as one does from a seating plan.

<!-- more -->

**Exhibit A. The guest list for the dinner of 19 March.**
*In the lodger's hand. Pencil notes, T.A.H.*

The dish is Trivy, a scanner. It tastes every build for known flaws before the build is served. Four members' kitchens use it.

- **Hosting co-op.** Invited the scanner by its full fingerprint, forty characters long. Got the scanner it had always had.
- **School.** Invited it by version label. Did not dine: no build ran that Thursday evening or overnight.
- **Fish auction.** Keeps its own copy, 0.69.3, in the larder. Ate from the larder.
- **Harbour office.** Invited it by version label, through a contractor's pipeline nobody has opened since. Sat down at 19:02 UTC.

*Pencil: a label is the name on a bottle, and somebody can change what is in the bottle. A fingerprint is the contents.*

**Exhibit B. Harbour office pipeline, 19 March, as logged.**

```
19:02:11  fetch   trivy-action (by version label)
19:02:14  step    scan
19:03:40  result  0 critical, 2 medium
19:03:41  done    success
```

*Pencil: the soup tasted fine. That is the mark of a careful poisoner.*

**Exhibit C. The lodger's reading.**

*Seen: on 19 March at about 17:43 UTC, someone holding stolen credentials moved the scanner's version labels so that they pointed at an altered copy. Seen: the label the harbour office used was one of them, and stayed that way until about 05:40 the next morning. Inferred: at 19:02 the harbour office was served the altered copy.*

*Seen: the altered copy did its own work first and ran the real scan afterwards, so the result looked as it always did. Its own work was to collect every secret the pipeline could reach and send the collection out.*

*Seen: the scanner's own people identified it within about three hours and began clearing the table; the labels the harbour office used were not all put right until morning. Seen: their advice to anyone who dined that night is to treat every secret as taken and replace it.*

*Seen: the harbour office's secrets tonight are the ones it had in March. Nobody replaced them. Seen: there is no repository named tpcp-docs in their account, which closes the second of two ways out. Guessed: nothing left by the first. I cannot see what left.*

**Exhibit D. Pencil, T.A.H.**

In a country-house poisoning everyone asks who touched the tureen. Here it was the taster. The one dish on the table whose whole job was to be trusted is the one that was got at, and its labels pointed the wrong way for about twelve hours.

Nobody at the harbour office did anything wrong on 19 March. Nobody there did anything at all. The pipeline fetched what the label named, as it had every evening, by itself, and that convenience was the reason for having it. The pipe that brings the mending brought this, at the same speed.

And the remedy for a dinner like this one cannot be sent down the pipe. It is each guest replacing their own keys, by hand. It never reached the harbour office, because nobody had told them they were at the table. Eight and a half months.

She took the sheets down.

The lodger had already drafted it: eleven secrets, where each one lived, what would stop working while it was changed, and for how long. Hull read the draft with a pencil and turned the brass key eleven times. The last change made the pipeline ask for its scanner by fingerprint.

"I would not have found the 19:02," she said aloud, to nobody, and then remembered that there was somebody.

The cupboard, to its credit, said nothing.

*Ledger, 7 December. Harbour office build pipeline: served the altered Trivy action on 19 March and never told. Eleven secrets replaced tonight, action pinned by fingerprint. Whether anything was taken in March: unknown. Not found by us; the scanner's own team caught it the same evening. The lodger found our guest by reading every pipeline in town. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-33634
Affected:         Trivy 0.69.4 (binary and container image); the trivy-action
                  GitHub Action, version tags 0.0.1 to 0.34.2 (76 of 77 tags);
                  the setup-trivy GitHub Action, 0.2.0 to 0.2.6 before 0.2.6 was
                  re-created; Docker Hub images 0.69.5 and 0.69.6. The CVE
                  record also lists LiteLLM 1.82.7 to 1.82.8 and telnyx 4.87.1
                  to 4.87.2.
Bug class:        Supply-chain compromise (CWE-506, Embedded Malicious Code)
Severity:         9.4, CVSS 4.0, as given in the CVE record (assigned by GitHub)
What it was:      On 19 March 2026 an attacker used compromised credentials to
                  publish a malicious Trivy release and to repoint the version
                  tags of two GitHub Actions at credential-stealing code. The
                  code ran before the real scan and collected the secrets a
                  build pipeline could reach. It continued an attack begun in
                  late February: an earlier credential rotation had not revoked
                  everything at once.
Found by:         not publicly credited. Aqua's account says: "The Trivy team
                  identified and contained the attack".
How it was found: not stated
In the dark for:  hours, not years. The altered trivy-action tags were live for
                  about 12 hours (19 March about 17:43 to 20 March about 05:40
                  UTC), setup-trivy for about 4 hours, the 0.69.4 release for
                  about 3 hours 20 minutes.
Exploited:        yes, it was an attack; added to the CISA KEV catalog on
                  2026-03-26. Aqua's account does not state confirmed victims.
                  LiteLLM says it believes the theft of its own PyPI
                  publishing access, and its malicious releases 1.82.7 and
                  1.82.8 on 24 March, came through the Trivy step in its CI.
Fixed in:         safe versions are Trivy 0.69.2 and 0.69.3, trivy-action
                  0.35.0 and setup-trivy 0.2.6; the malicious releases, tags
                  and images were removed.
What to do:       Check whether a pipeline ran an affected version on 19 to 20
                  March 2026 (22 to 23 March for the Docker Hub images). If it
                  may have, treat every secret it could reach as exposed and
                  rotate it. Look for a repository named tpcp-docs in your
                  GitHub organisation. Pin Actions to full commit hashes, not
                  version tags. A trivy-action pinned to a commit older than
                  2025-04-09 still fetched setup-trivy by tag.
Sources:          https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23
                  · https://cveawg.mitre.org/api/cve/CVE-2026-33634
                  · https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know/
                  · https://docs.litellm.ai/blog/security-update-march-2026
                  · https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2026-33634
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 6](2026-12-06-door-6-the-house-with-one-room-too-many.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
