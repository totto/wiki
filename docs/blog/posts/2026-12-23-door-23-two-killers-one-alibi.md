---
date: 2026-12-23T05:00:00
slug: door-23-two-killers-one-alibi
image: assets/images/night-desk/door-23.webp
description: "A two-killers story about a race condition. CVE-2026-86805."
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

# Door 23: Two Killers, One Alibi

![Illustration for Door 23: Two Killers, One Alibi](../../assets/images/night-desk/door-23.webp)

*A two-killers story about a race condition. CVE-2026-86805.*

Kaldhavn, 23 December. One candle left.

The temp in the fish auction's accounts office had been in Kaldhavn for nine weeks and had run out of things to do in it by the third.

<!-- more -->

It was eleven at night. The year's last invoices were entered. On the shared server where the accounts lived, the temp had a login, a folder, and exactly the rights of someone who types in herring prices. And the temp had been reading.

The reading was about the oldest and most trusted program on the machine, the one that starts all the others. It is called the loader, and it comes with a library named glibc. When a privileged program starts, the loader goes to fetch the parts it needs, and it will fetch them only from trusted places. That is the rule. Somebody had noticed, this summer, how it kept the rule. It worked out the tidy form of an address and asked: *is this a trusted place?* Then it went and opened the untidy form.

Two addresses. On an honest day they are the same place. The loader asked the sensible twin for an alibi and then walked off with the other one.

So the plan, as the temp understood it, had three steps. Put a link to a privileged program in a folder of your own. Get the loader to check the address while it pointed somewhere respectable. Then, in the instant between the asking and the opening, swing the signpost round. It had been possible for fifteen years.

Step one: the link.

*Operation not permitted.*

The temp tried twice more, and then looked it up. The machine would not let an ordinary user make that kind of link to a program they did not own. It was a setting. It was switched on by default on every large distribution, and the advisory itself said so, in its last sentence, which the temp had not read as far as.

All right. Suppose it could be got round. The temp went looking for the second thing the plan needed, which was a privileged program built in one particular and rather unusual way.

There was not one on the machine. The temp looked properly. It took forty minutes.

All right. Suppose there were. The temp checked the library's version, and found it had been updated the Tuesday before. Somebody called N. Haddad had signed the change. The note read, in full: *glibc to 2.41-12+deb13u5. The loader now opens the same address it checked. Before the holiday, not after.*

Three doors. One was bolted by default. One opened onto a room that was not there. The third had been mended six days ago by somebody who, to judge by the note, had not thought it worth more than two lines.

Nobody had even been waiting for them. That was the insulting part.

The temp sat back. Somewhere across it a light was on in the old telegraph station, and the temp wondered, without much interest, what anyone found to do in there at this hour.

In the telegraph station the amber screen had been showing a line for some time, and Hull had read it and gone on mending her net.

*Seen: four refused link attempts on the auction's accounts server between 23:12 and 23:19, from one ordinary account. Seen: a search of the whole disk for one kind of program, forty minutes. Seen: nothing after that. Inferred: somebody read the advisory and then met the machine.*

"Do we need the key?"

*No. Nothing is open.*

"Then log it, and put it on Noor's desk for the morning. She did that one. She ought to see what it looks like from the other side."

*And the account?*

"The auction's manager can have a quiet word after the holiday." She bit off the twine. "It's the night before Christmas Eve, Morrow. Let them go home."

The temp logged off at seven minutes past midnight, and went.

*Ledger, 23 December. Fish auction accounts server, glibc: the loader checked one form of an address and opened another. Updated to 2.41-12+deb13u5 last Tuesday by N. Haddad. Tonight someone tried it and failed three times over. No key turned; nothing to mend. Not found by us. Found by a person, and it was in the code for fifteen years. Signed, T.A.H., with M.*



```
THE REAL ONE

CVE:              CVE-2026-86805
Affected:         GNU C Library (glibc) 2.14 to 2.44, in the dynamic loader
                  (ld.so)
Bug class:        Race condition (CWE-367, Time-of-check Time-of-use Race
                  Condition)
Severity:         6.3, CVSS 3.1, as scored by the glibc project
What it was:      For setuid and setgid programs whose library search path
                  uses $ORIGIN, the loader validated the normalised form of
                  the path against the trusted directories but then opened
                  the raw form. A local attacker who could hard-link such a
                  program into a directory of their own and win a race could
                  make it load their code with the program's privileges. It
                  needs a program built in that particular way. The advisory
                  notes: "Major Linux-based OS distributions ship with
                  fs.protected_hardlinks enabled by default and mitigate the
                  vulnerability."
Found by:         Jann Horn (credit in the CVE record and the glibc advisory)
How it was found: not stated
In the dark for:  about 15 years (glibc 2.14 was released 2011-06-01; fix
                  committed 2026-09-01)
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25
Fixed in:         fix committed on 2026-09-01 for glibc 2.45 and backported
                  to the 2.41 to 2.44 branches (advisory GLIBC-SA-2026-0022;
                  CVE published 2026-09-22). The loader now normalises the
                  path and opens exactly the path it validated. Debian 13
                  (trixie): 2.41-12+deb13u5 (accepted for the stable point
                  update on 2026-11-14); Debian 12 still listed as vulnerable.
What to do:       Install your distribution's glibc update. Check that
                  fs.protected_hardlinks is enabled.
Sources:          https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=advisories/GLIBC-SA-2026-0022
                  · https://cveawg.mitre.org/api/cve/CVE-2026-86805
                  · https://sourceware.org/git/?p=glibc.git;a=commit;h=ed0c137b97eb940b4b64981e84ed806d3276edd9
                  · https://security-tracker.debian.org/tracker/CVE-2026-86805
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 22](2026-12-22-door-22-the-guest-who-was-shown-out-twice.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
