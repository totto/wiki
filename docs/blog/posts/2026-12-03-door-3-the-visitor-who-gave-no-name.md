---
date: 2026-12-03T05:00:00
slug: door-3-the-visitor-who-gave-no-name
image: assets/images/night-desk/door-03.webp
description: "A locked-room story about an authentication bypass. CVE-2026-55706."
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

# Door 3: The Visitor Who Gave No Name

![Illustration for Door 3: The Visitor Who Gave No Name](../../assets/images/night-desk/door-03.webp)

*A locked-room story about an authentication bypass. CVE-2026-55706.*

Kaldhavn, 3 December. Twenty-one candles left.

The candle was already burning when Hull came in. It had been lit before she arrived every night so far, and the thing in the cupboard had no hands. She filed that under later.

<!-- more -->

"Lodger. The skerry light."

*Seen: the lighthouse on the skerry talks to the harbour office over one cable on the seabed. Seen: the box out there runs OpenBSD, and it asks our end for a name and a password before it will pass anything. The method is called PAP.*

"I know what it's called. I was switching it on before you were a rumour." She unfolded the advisory, which she had printed, because paper did not rearrange itself. "June. Read it with me."

It was a locked-room mystery, and she liked those. The door had a guard. The guard's rule was sound: compare the name and password the caller offers with the ones on the list. The flaw was in how he measured. He compared exactly as many letters as the caller handed him. Hand him a name of no letters and a password of no letters, and he compared nothing with nothing, found no difference, and opened the door.

"Twenty-seven years," Hull said. "That went in during the summer of 1999. I was working nights then too. People read that file. Good people."

*Seen: reported on 12 June. Seen: fixed two days later.*

"Who found it?"

There was a pause of a kind she had begun to recognise, the fan under the stairs rising half a tone.

*Seen: the finder's own website says an automated system of theirs found it in one sweep. Seen: the mailing-list post announcing the bug does not say how it was found. I have one source, and it is the party taking the credit. I would not put it more strongly than that.*

Hull looked at the amber screen for a while. She had a remark ready about machines marking their own homework, and found that it had just been made for her.

She said nothing, and moved on.

"So. The guard on the skerry. Is he the old guard or the new one?"

*Seen: that box was rebuilt in October from the current sources. Inferred: the June fix is in it. I can stop inferring by reading what it was built from. Reading only. No key needed.*

"Then read."

*Seen: the check that makes him measure against the name on the list, not the one he is handed, is there. The guard is the new one.*

"And if he weren't?"

*Then someone would still have to be on that cable to try it. Seen: the record rates this as reachable only from the neighbouring network, not from the town or the internet. Guessed: nobody has dived for it.*

It was, she supposed, a joke. She decided it had been an accident.

So the room had been locked all along. A week ago she would have known that by taking Friday's supply boat out to the skerry and looking. Tonight she knew it in twenty minutes, in the warm, and what irritated her was that she believed it.

She let the candle burn down to its mark and mended two metres of net by the stove, which was what she did when she was thinking about something she was not going to say.

*Ledger, 3 December. Skerry link, OpenBSD: a guard who compared nothing with nothing, in the code since 1999. Their box already carries the June fix; confirmed by reading, not by hoping. Not found by us. Fixed by its maintainers in two days, which is faster than we checked. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-55706
Affected:         OpenBSD, PAP authentication in the synchronous PPP code
                  (sppp_pap_input in sys/net/if_spppsubr.c), before commit 076e2b1
Bug class:        Authentication bypass through zero-length credentials
                  (CWE-1284, Improper Validation of Specified Quantity in Input)
Severity:         5.8, CVSS 3.1, as given in the CVE record (assigned by MITRE)
What it was:      The PAP check compared the received name and password using
                  the lengths the caller supplied. With an empty name and an
                  empty password the comparison covered zero bytes and
                  succeeded. The fix accepts the credentials only when their
                  lengths match the configured name and password exactly. The
                  flaw can only be reached from the adjacent network.
Found by:         Argus (ByteRay): "Discovered and reported by Argus" in the
                  oss-security advisory. The CVE record itself carries no
                  credit.
How it was found: by Argus, which ByteRay describes as a multi-agent
                  product-security system in which AI agents propose hypotheses
                  checked against deterministic analysis; ByteRay lists this CVE
                  as "Found in one sweep". The oss-security post does not say how.
In the dark for:  about 27 years (the code was imported on 1999-07-01)
Exploited:        no known exploitation; a proof of concept is public; not in
                  the CISA KEV catalog as of 2026-11-25
Fixed in:         OpenBSD -current, commit 076e2b1, 2026-06-14, two days after
                  the report of 2026-06-12. No erratum was issued for 7.8 or
                  7.9; OpenBSD 8.0 (2026-10-20) is the first release made after
                  the fix.
What to do:       Run a build that includes the 2026-06-14 fix. OpenBSD 8.0
                  (2026-10-20) is the first release made after it.
                  Check any PPP link that still authenticates its peer with PAP.
Sources:          https://seclists.org/oss-sec/2026/q2/947
                  · https://github.com/openbsd/src/commit/076e2b1c1fc4ac0883a72d3544131ad5cee7adf8
                  · https://cveawg.mitre.org/api/cve/CVE-2026-55706
                  · https://byteray.co.uk/argus
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 2](2026-12-02-door-2-the-village-that-never-locked-its-doors.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
