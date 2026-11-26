---
date: 2026-12-06T05:00:00
slug: door-6-the-house-with-one-room-too-many
image: assets/images/night-desk/door-06.webp
description: "A haunted-house story about a heap overflow. CVE-2026-27654."
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

# Door 6: The House With One Room Too Many

![Illustration for Door 6: The House With One Room Too Many](../../assets/images/night-desk/door-06.webp)

*A haunted-house story about a heap overflow. CVE-2026-27654.*

Kaldhavn, 6 December. Eighteen candles left.

At ten to three on Sunday morning something fell over in the boathouse.

<!-- more -->

It fell inside the web server, not among the racks where Tobias Ek sat alone with a cold coffee. One of the server's workers died, and the server, as it is built to, stood another up in its place. Tobias saw the line go by in the log and thought nothing of it.

Four minutes later it happened again.

He had run servers for half his life and maintained other people's software, unpaid, for nine years of it, and he knew the sound of a house settling. This was something else: a thing falling down in the same room, at intervals, and each time being quietly replaced so that nobody would notice.

He did not want to ring Hull. Hull would be right about something. He typed to the Night Desk's terminal instead, where the new thing lived.

*Seen: each fall comes a second or two after the school's nightly backup job sends one very large file. Seen: the worker runs out of memory and is stopped. Inferred: tonight's noise is that, and nothing worse.*

A false alarm, then. Tobias reached for the coffee.

*Seen: your nginx is 1.26. Seen: an advisory from March covers that version, for one rare arrangement of settings. This is a separate matter from the noise. May I read your configuration? Reading only.*

Tobias had spent a year deleting machine-written bug reports that began *I have discovered a critical vulnerability*. This one had begun with what it had not yet established. He let it read.

*Seen: one. The file-sharing module is on, with copying and moving allowed. Seen: two. It sits in a plain prefix location. Seen: three. That location uses an alias. All three conditions in the advisory. Inferred: you are affected.*

He remembered writing it. It was 2013, a shared folder for the school's teachers, and an alias because the disk was somewhere odd. For thirteen years it had sat there, one unusual room in an ordinary house.

The advisory explained the rest. When a file is moved, the server works out the new path and writes it into a space it has measured out beforehand. With that one arrangement of settings, and a destination of a particular kind, the measurement comes out wrong. The space is too small. The path is written anyway, and it runs on past the end, through the wall and into whatever is kept next door. A heap overflow. The record said what might follow: workers falling over, or files given new names in places outside the folder they belonged to. The flaw had been in the server since 2007, waiting for a house built exactly like his.

So the thing that had frightened him tonight was loud and harmless, and the thing in the advisory was neither. It had made no sound in thirteen years. He found he was listening to the racks anyway.

The fix had existed since March. He upgraded to 1.28.3 himself. They were his machines, and no key was needed but his own.

Then he sat for a moment with a feeling that would not settle, until he placed it. He had copied that configuration once. In 2015, for the photography club, onto a machine that was in no inventory, because Tobias was the inventory.

*Seen: I have no record of a second server.*

"No," said Tobias. "You wouldn't."

He patched that one too. Then he looked up who had found the flaw. People, the vendor's note said, working together with a machine. He read the line again, hunting for the catch, and went to bed without one.

*Ledger, 6 December. Co-op web servers, nginx: a path written past the end of its space, under one rare arrangement of settings; in the code since 2007. Both upgraded to 1.28.3 by their owner before I was awake. Not found by us. T. Ek reports that the lodger asked before it answered. I have asked him not to encourage it. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-27654
Affected:         NGINX Open Source 0.5.13 to before 1.28.3, and 1.29.0 to
                  before 1.29.7; NGINX Plus R32 to R36. Only when the
                  configuration uses the DAV module's MOVE or COPY methods in a
                  prefix location with an alias directive.
Bug class:        Heap-based buffer overflow (CWE-122, Heap-based Buffer
                  Overflow)
Severity:         8.2, CVSS 3.1 (8.8, CVSS 4.0), as scored by F5
What it was:      In the WebDAV module, the length of a rewritten destination
                  path could be miscalculated, and the path was written past the
                  end of its buffer. The result may be a crashed worker process,
                  or source or destination file names changed outside the
                  document root. The worker's low privileges limit the damage.
Found by:         Calif.io in collaboration with Claude and Anthropic Research
                  (F5's acknowledgement in the CVE record)
How it was found: AI-assisted: Claude flagged the bug and produced a crash, with
                  Calif researchers directing the work, per Calif's write-up
In the dark for:  about 19 years (since version 0.5.13, February 2007)
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25
Fixed in:         NGINX Open Source 1.28.3 and 1.29.7, both released 2026-03-24;
                  NGINX Plus R36 P3, R35 P2 and R32 P5 (the record lists no fix
                  for R33 or R34; move to a fixed release).
What to do:       Upgrade to a fixed version. If you cannot yet, check whether
                  any location combines DAV MOVE or COPY with an alias; most
                  configurations do not.
Sources:          https://my.f5.com/manage/s/article/K000160382
                  · https://cveawg.mitre.org/api/cve/CVE-2026-27654
                  · https://www.openwall.com/lists/oss-security/2026/03/26/3
                  · https://calif.io/research/nginx
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 5](2026-12-05-door-5-the-guard-who-checked-the-uniform.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
