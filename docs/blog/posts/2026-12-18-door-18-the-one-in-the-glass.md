---
date: 2026-12-18T05:00:00
slug: door-18-the-one-in-the-glass
image: assets/images/night-desk/door-18.webp
description: "A doppelgänger story about a page-cache write. CVE-2026-31431."
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

# Door 18: The One in the Glass

![Illustration for Door 18: The One in the Glass](../../assets/images/night-desk/door-18.webp)

*A doppelgänger story about a page-cache write. CVE-2026-31431.*

Kaldhavn, 18 December. Six candles left.

The school's computing teacher did not want his server restarted, and said so twice before he had sat down.

<!-- more -->

"It's the end of term. Two hundred pupils have work on it. There are jobs on it that have been running since Monday. And it is patched. It patches itself. I checked this afternoon."

"You checked the disk," Hull said.

"Where else would I check?"

Hull pushed the advisory across the desk. It had a name, Copy Fail.

"A Linux machine does not run a program off the disk each time," she said. "It keeps a copy in its memory, and runs the copy, because that is quicker. Two of everything: the one on the shelf, and the one in the glass. The rule is that an ordinary user may look at the copy and never write on it. This flaw let any user who could log in change four bytes of the copy. Any file they could read. The one on the shelf stays exactly as it was. Every check you own compares the one on the shelf."

"So the pupil runs the usual program for becoming administrator, the one that asks for a password," Hull said. "The machine runs its copy. The copy has been altered to stop asking."

*Seen: the school server is Ubuntu 24.04. Seen: it has two hundred and six accounts that can log in. Seen: the corrected kernel was installed on the disk in May, by the automatic updates. You are right about that.*

"Then."

*Seen: the machine has not restarted since 2 February. The kernel it is running was loaded into memory that day. The corrected one is on the shelf. The old one is in the glass. No live patch is installed.*

*Seen: in April the same automatic updates switched the affected part off as a stopgap. When the corrected kernel arrived, the stopgap was withdrawn, on the assumption that the machine would be restarted. It was not.*

"That's the same thing. That's the bug again."

"It is," Hull said. "A machine and its double. Your disk has been correct for seven months, and it has been the wrong place to look for all of them."

*Seen: I compared every system program on the disk against its published fingerprint. All match. Seen: that tells us nothing about the copies in memory. I have no way to read those copies that does not go through the kernel I am doubting.*

*Guessed: nobody has done this here. I have nothing to see it with.*

That was the cold part: two hundred and six children, a public demonstration that had been on the internet since April, and a door that had stood open again since the stopgap was withdrawn. Nobody could look.

"What makes it true again?" the teacher asked.

*A restart. The memory is emptied. Every copy is made fresh from the disk, and the kernel that wakes up is the corrected one. Ten minutes. I have drafted it: warn the pupils now, pause the long jobs at 01:50, restart at 02:00, resume. Nothing else. I can run it if you turn the key.*

"Friday's deadline moves to Monday," he said, after a while. "I'll tell them myself."

At two o'clock Hull turned the key. On the amber screen the school's server went away, and for four minutes there was only the candle. Then it came back and said its new number, and Morrow read the number out, and it was the right one.

"The people who found this," the teacher said. "Did they have something like yours?"

*Seen: their own account says it began with one researcher's idea about where to look, and that a machine then searched the rest. Seen: the mainline correction was written within nine days of their report. Seen: it was made public four weeks later, and two days after that several of the large distributions had still not shipped it.*

"So everyone was quick," he said, "and it still took until tonight."

"Yes," said Hull. "It did."

*Ledger, 18 December. School server, Linux, Copy Fail: any user could alter the in-memory copy of a file while the disk stayed clean. Corrected kernel on disk since May; machine not restarted since February, so never running it. Restarted 02:00. Whether anyone used it: unknown and now unknowable. Not found by us. Found by a person with an idea and a machine that followed it up. Signed, T.A.H., with M.*



```
THE REAL ONE

CVE:              CVE-2026-31431 ("Copy Fail")
Affected:         Linux kernel from 4.14; fixed in the stable kernels
                  released from April 2026 (see the record)
Bug class:        Local privilege escalation through a write to the page
                  cache (the CVE record names no CWE)
Severity:         7.8, CVSS 3.1, as given in the CVE record (assigned by the
                  Linux kernel CNA)
What it was:      In the kernel's userspace crypto interface (algif_aead), an
                  optimisation from 2017 let an unprivileged local user make a
                  controlled 4-byte write into the page cache, the in-memory
                  copy, of any file they could read. The file on disk is
                  unchanged, so checks against the disk miss it. Altering the
                  cached copy of a privileged program gives root; the finders
                  also describe container escapes.
Found by:         Taeyang Lee (Theori) with Theori's Xint Code, according to
                  Theori. The CVE record itself carries no credit.
How it was found: Theori: the finding "was AI-assisted, but began with an
                  insight from Theori researcher Taeyang Lee", who used the
                  tool to search the crypto subsystem.
In the dark for:  about 8½ years (introduced by a 2017 commit; mainline fix
                  2026-04-01)
Exploited:        yes, according to CISA, which added it to the KEV catalog on
                  2026-05-01, two days after public disclosure. The finders
                  published exploit code. No victims are named.
Fixed in:         mainline on 2026-04-01 (reported 2026-03-23; public
                  2026-04-29), then the stable versions above. The fix
                  reverts the interface to out-of-place operation, so cached
                  file pages are never in the writable destination. Distributions followed over the next weeks: Debian's
                  stable release (trixie) on 2026-04-30 and bookworm on
                  2026-05-01; Ubuntu disabled the affected module through an
                  update on the disclosure date and shipped fixed kernels in
                  May.
What to do:       Install your distribution's fixed kernel and restart into
                  it (Ubuntu: "a reboot is required"). Until then, the finders suggest disabling the
                  algif_aead module.
Sources:          https://xint.io/blog/copy-fail-linux-distributions
                  · https://cveawg.mitre.org/api/cve/CVE-2026-31431
                  · https://ubuntu.com/blog/copy-fail-vulnerability-fixes-available
                  · https://lists.debian.org/debian-security-announce/2026/msg00148.html
                  · https://wiz.io/blog/copyfail-cve-2026-31431-linux-privilege-escalation-vulnerability
                  · https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2026-31431
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 17](2026-12-17-door-17-the-body-was-already-cold.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
