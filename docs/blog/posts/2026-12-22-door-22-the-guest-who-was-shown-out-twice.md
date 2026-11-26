---
date: 2026-12-22T05:00:00
slug: door-22-the-guest-who-was-shown-out-twice
image: assets/images/night-desk/door-22.webp
description: "A ghost story about a use-after-free. CVE-2026-23479."
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

# Door 22: The Guest Who Was Shown Out Twice

![Illustration for Door 22: The Guest Who Was Shown Out Twice](../../assets/images/night-desk/door-22.webp)

*A ghost story about a use-after-free. CVE-2026-23479.*

Kaldhavn, 22 December. Two candles left.

**Hull's working file on the Redis advisory. Four sheets.**

<!-- more -->

**Sheet 1. Why I pulled the file.**

The co-op's Redis is on 7.2.13. The advisory is from May. The lodger put it at the top of tonight's list. Its makers' note says the flaw was reported by something called Xint Code during a hacking contest, and the finders describe that as a machine working by itself.

I have read a great many machine-written reports of flaws that were not there. So before I spend Tobias's evening two days before Christmas, I will read the code myself. The finders name the two changes that made the flaw. Two changes can be read.

**Sheet 2. The change of January 2023.**

Redis lets a caller wait. *Wake me when something arrives for this name.* When it arrives, a porter goes to the waiting guest's room and hands the delivery in. This change tidied how the porter does that.

Handing it in can go badly. A guest who has taken up too much room can be shown out of the hotel in that very moment. The porter is told so, by a word passed back to him. In this change he does not listen for the word.

It does no harm. Handing in the delivery is the last thing he does. He turns and leaves whether the guest is still there or not.

*Pencil: Untidy. Not a flaw. PASS.*

**Sheet 3. The change of March 2023.**

Two months later. After the delivery the porter is given a few more small duties in the room: read the guest's card, put the guest on a list, tidy up after.

Each duty is reasonable. Each is correctly done.

*Pencil: PASS. Nothing here. I have told the lodger this one can wait until after the holiday. Two clean changes do not make a flaw because a contest says so.*

**Sheet 4. The lodger's reading, which I did not ask for.**

*Seen: you read each change as it stood on the day it was made. Both are correct on that day.*

*Seen: I laid the second on top of the first. After March the porter has duties in the room after the delivery. Since January he does not listen for the word that says the guest has been shown out. So he carries out his duties in a room that may already have been handed back, on a guest who is no longer there. That is the flaw. It is in neither change. It is in the two together.*

*Seen: the finders say the same, and name the same two changes. Seen: the fix is seven lines. The porter now listens for the word, and if the guest is gone he leaves.*

*Seen: it needs a caller who is already logged in. Our Redis has eleven of those, and four are programs written by other people.*

**Pencil, later.**

I read both. I passed both. I was pleased with myself, and I very nearly sent a real flaw away until January.

Whoever reviewed those two changes in 2023 was, I expect, at least as careful as I am, and read the one in front of them. I had both in my hand, and I chose to read them one at a time because that is how I have always read.

It read them together. That is all it did differently, and I could not have done it.

It is the second time this month. The first time I was tired. Tonight I was sure.

A seventh line for the card: *If a change can be read, it gets read. If it had to be split to be read, somebody reads the whole as well.*

I asked Morrow who "somebody" ought to be.

*Guessed: whichever of us did not do the splitting.*

I rang Tobias. He upgraded to 7.2.14 in twenty minutes and asked what had kept me.

*Ledger, 22 December. Mistake first, and it is mine again: I read the two changes separately, passed both, and told Morrow the upgrade could wait. Co-op Redis 7.2.13: a blocked client used after it had been evicted. Upgraded to 7.2.14 tonight. Not found by us. Found by a machine, the finders say; and understood here by Morrow before me. Signed, T.A.H., with M.*



```
THE REAL ONE

CVE:              CVE-2026-23479
Affected:         Redis (redis-server) 7.2.0 to before 8.6.3: by branch,
                  7.2.0 to 7.2.13, 7.4.0 to 7.4.8, 8.2.0 to 8.2.5, 8.4.0 to
                  8.4.2 and 8.6.0 to 8.6.2
Bug class:        Use-after-free (CWE-416, Use After Free)
Severity:         7.7, CVSS 4.0, as scored in the Redis advisory and the CVE
                  record (assigned by GitHub)
What it was:      When a blocked client was unblocked and its command run
                  again, the code did not handle an error return telling it
                  the client had been freed. If the client was evicted during
                  that step, the server went on using it. An authenticated
                  attacker could trigger this, and it may lead to remote code
                  execution.
Found by:         The Redis advisory says the issue "was reported by
                  independent researcher Xint Code during the Wiz Zeroday
                  Cloud event." The CVE record itself carries no credit.
How it was found: by an AI tool, according to the finders: their write-up
                  calls Xint Code "a fully autonomous AI-powered security
                  analysis tool" and names no individual.
In the dark for:  about 2 years 9 months (Redis 7.2.0 was released
                  2023-08-15; fixed 2026-05-05). The finders trace it to two
                  changes of January and March 2023, each harmless alone.
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25. The finders demonstrated a working exploit at a
                  contest in December 2025.
Fixed in:         Redis 7.2.14, 7.4.9, 8.2.6, 8.4.3 and 8.6.3, released
                  2026-05-05. The fix checks the return value and stops using
                  the client if it was freed.
What to do:       Upgrade to the fixed release on your branch. Limit who can
                  authenticate to Redis, and deny CONFIG to application users.
Sources:          https://github.com/redis/redis/security/advisories/GHSA-93m2-935m-8rj3
                  · https://cveawg.mitre.org/api/cve/CVE-2026-23479
                  · https://zeroday.cloud/blog/redis-cve-2026-23479-deep-dive
                  · https://github.com/redis/redis/commit/c14e9925e571c3c8ecbeb8632fe834faa32175ea
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 21](2026-12-21-door-21-the-servant-and-the-forged-order.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
