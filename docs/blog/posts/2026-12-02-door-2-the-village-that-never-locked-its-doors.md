---
date: 2026-12-02T05:00:00
slug: door-2-the-village-that-never-locked-its-doors
image: assets/images/night-desk/door-02.webp
description: "An unlocked-door story about an argument injection. CVE-2026-24061."
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

# Door 2: The Village That Never Locked Its Doors

![Illustration for Door 2: The Village That Never Locked Its Doors](../../assets/images/night-desk/door-02.webp)

*An unlocked-door story about an argument injection. CVE-2026-24061.*

Kaldhavn, 2 December. Twenty-two candles left.

Henrik Moe had been harbourmaster for thirty-one years and had never locked the office. Nobody in Kaldhavn locked anything that faced the water. So when Hull came up the outside stair at ten to eight, grey from the night shift, carrying two coffees and a toolbag, he took the coffee and resented the toolbag.

<!-- more -->

"Your tide box," she said.

The tide box sat on the windowsill where it had sat since 2011: a grey computer the size of a loaf, wired to the gauge on the pier. From his kitchen, on bad mornings, Henrik could ask it the water level without putting his boots on. It answered over telnet, which was how machines had talked when he was young. It had worked every day. He said so.

"I know," Hull said. "That's the trouble with it."

She explained it the way she explained everything, as if to a jury. When you call on the tide box, a doorman asks your name and carries it inside on a slip of paper to the clerk who checks passwords. That is the rule. But the clerk also takes instructions on slips, and the doorman never looked at what he was carrying. Write the right thing where your name should go and the clerk reads it as an order from the house: *this one has already been checked.* He lets you in as master of the place and never asks for a password.

"A name that is really an order," Henrik said.

"It was in there for eleven years. It came to light in January, and the fix came with it." She put her cup down. "Within a day, other people were out trying doors."

Henrik looked at the pier, where nothing was happening, slowly.

Hull had a small screen with her. Amber words came up on it. He had heard about the thing in her cupboard.

*Seen: this box runs the affected telnet service. Seen: its log holds seven days. In those seven days, 212 callers from outside Kaldhavn. Seen: none of them got in by this route.*

"And before this week?"

*Guessed: no. I cannot see what the box did not keep.*

Nobody said anything. Henrik was working out that for ten months his door had stood open onto a street much longer than the one he could see.

"It isn't in the Mutual's inventory," Hull said. "The cupboard would never have found it. I remembered you boasting."

"I wasn't boasting."

"You were a bit."

The fix had been on the shelf since January. This morning it took her nine minutes, by hand: the telnet service switched off for good, a newer way in that asked for a proper key, the gauge still answering. Henrik watched her do it and could not have said afterwards what she had done. That, he thought, was probably how it had got this way.

He tried it from the kitchen that evening. It asked him for more than his name. He supposed he could live with that.

He still did not lock the office. But he noticed, now, that he didn't.

*Ledger, 2 December. Harbour office tide box: a telnet service that took an order for a name. Service switched off, access replaced. No sign of entry in the seven days of log that exist. Before that, unknown, and it will stay unknown. Not found by us. The fix was ten months old. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-24061
Affected:         telnetd in GNU Inetutils, versions 1.9.3 to 2.7
Bug class:        Argument injection leading to authentication bypass (CWE-88,
                  Improper Neutralization of Argument Delimiters in a Command)
Severity:         9.8, CVSS 3.1, as given in the CVE record (assigned by MITRE)
What it was:      telnetd passed the user name offered by the client on to the
                  system's login program without checking it. A value shaped like
                  a command-line option was read by login as a statement that the
                  user was already authenticated. A remote caller could become
                  root without a password.
Found by:         Kyu Neushwaistein (Carlos Cortes Alvarez). The CVE record
                  itself carries no credit.
How it was found: not stated
In the dark for:  about 11 years (introduced March 2015, shipped in 1.9.3 in
                  May 2015; patched 2026-01-20)
Exploited:        yes; added to the CISA KEV catalog on 2026-01-26. Probing began
                  within a day of the fix. About 800,000 telnet services of all
                  kinds were still reachable on 2026-01-26 (Shadowserver, via
                  press); that figure counts telnet, not this flaw.
Fixed in:         patches published 2026-01-20; GNU Inetutils 2.8, released
                  2026-04-29 (per the project's NEWS file)
What to do:       Switch telnetd off and use SSH. If it must stay, install a
                  fixed Inetutils or your distribution's patched package, and
                  keep port 23 off the internet.
Sources:          https://www.openwall.com/lists/oss-security/2026/01/20/2
                  · https://cveawg.mitre.org/api/cve/CVE-2026-24061
                  · https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2026-24061
                  · https://codeberg.org/inetutils/inetutils/raw/branch/master/NEWS.md
                  · https://www.theregister.com/2026/01/22/root_telnet_bug/
                  · https://www.bleepingcomputer.com/news/security/nearly-800-000-telnet-servers-exposed-to-remote-attacks
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 1](2026-12-01-door-1-the-lodger.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
