---
date: 2026-12-13T05:00:00
slug: door-13-the-crime-where-every-check-passed
image: assets/images/night-desk/door-13.webp
description: "A perfectly-legal-crime story about an authentication bypass. CVE-2026-8932."
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

# Door 13: The Crime Where Every Check Passed

![Illustration for Door 13: The Crime Where Every Check Passed](../../assets/images/night-desk/door-13.webp)

*A perfectly-legal-crime story about an authentication bypass. CVE-2026-8932.*

Kaldhavn, 13 December. Eleven candles left.

On St Lucia's night the schoolchildren walk the quay in white with candles in their hair, and for ten minutes Kaldhavn is the brightest thing on the coast. Hull watched them pass the telegraph station window. When she turned round there were saffron buns on her desk, still warm, and the calendar candle was lit.

<!-- more -->

"You didn't see who," she said.

*Seen: nothing. I have no eyes on the room. Inferred: someone with a key and an oven.*

She ate a bun and opened the night's advisory. It was about curl, the small tool that fetches things over the network for half the programs ever written.

It was a crime she rather admired. Think of the ferry gangway. To save time, the crew leave it down between passengers if the next ticket matches the last one: same boat, same destination, same class. The rule is sound, and every check on the list was carried out every time. But one line was missing from the list. Nobody had written *same passenger*. So when a program fetched something first as one identity and then as another, the second request could walk aboard on the first one's papers. Every check passed, and the wrong person was on the boat.

"Since when?"

*Seen: since version 7.7, March 2001. Fixed in 8.21.0, June this year.*

"Twenty-five years. In a tool that half the world reads." She shook her head. There was no scorn in it. "Who has it here?"

*Seen: curl is on nearly every machine in the Mutual. Seen: the flaw only matters to a program that changes its own identity between two requests to the same place. I cannot tell from an inventory which programs do that.*

"No. But I can." She was already reaching for her coat and then, remembering it was Sunday, for the telephone instead. "The fish auction files catch reports to the directorate for every boat in one go, each boat with its own certificate. A cousin of Henrik's wrote it as one loop in 2016. I told him at the time it was too clever."

*Seen: the auction's server has libcurl 8.14.1. Affected.*

"Check the directorate's receipts against the landing slips, Morrow. Every boat, back to the summer."

The fan under the stairs rose. Hull finished the bun.

*Seen: 2,310 receipts. 2,309 agree with the slips. On 14 October, four hundred kilos of cod landed by Havørn were credited to Terna.*

"There it is." It was a small wrong, quite harmless, and it could be put right with one embarrassed telephone call on Monday. Both skippers would dine out on it until Easter. She turned the brass key and the auction's server went to 8.21.0.

"Who found it?"

*Seen: one person is credited as the finder. Seen: the same person is credited with the fix, and the change itself carries their name as author. Seen: their employer is a firm that builds AI tools for this kind of work. Not seen: any statement that such a tool was used here. The advisory does not mention it.*

"Then we don't either." Hull took down the card by the terminal and wrote a new rule under the others. *Credit goes where the work was done.* "Found it and mended it. Twenty-five years of people walking past, and one of them stops, and then stays to fix the gangway.

She chalked *25* on the stove pipe under the other twelve marks. Two of them said only *not known*."

She pinned the card back up. Outside, the last of the candles was going round the end of the fish hall.

It was some minutes before she noticed what she had called it. She looked at the amber screen. Nothing on it had changed. If it had noticed too, it had the manners not to say so.

She left the second bun by the cupboard door on her way out, which was absurd, and she knew it.

*Ledger, 13 December. Fish auction reporting script, libcurl 8.14.1: a connection reused for the wrong identity because one line was missing from the comparison. One receipt out of 2,310 misfiled; skippers to be told Monday. Upgraded to 8.21.0. Not found by us. Found and fixed by the same hand, after twenty-five years. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-8932
Affected:         libcurl 7.7 to 8.20.0 (the curl command-line tool itself
                  is not affected, per the advisory)
Bug class:        Authentication bypass (CWE-305, Authentication Bypass by
                  Primary Weakness)
Severity:         Low, as rated by the curl project, which gives no CVSS score;
                  CISA's enrichment of the record scores it 7.5, CVSS 3.1
What it was:      libcurl keeps used connections in a pool and reuses one when
                  a new transfer's setup matches. Some TLS client-certificate
                  settings, in particular those for the private key, were left
                  out of that comparison. A transfer could reuse a connection
                  that had been authenticated with a different client
                  identity.
Found by:         "Reported-by: Joshua Rogers (Aisle Research)" and
                  "Patched-by: Joshua Rogers (Aisle Research)" in the curl
                  advisory; the fix commit names the same author
How it was found: not stated. The advisory does not mention AI.
In the dark for:  about 25 years 3 months (since curl 7.7, released
                  2001-03-22; fixed 2026-06-24)
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25. CISA's assessment notes a proof of concept; none
                  is confirmed here.
Fixed in:         curl 8.21.0, released 2026-06-24, six weeks after the report
                  of 2026-05-13. The fix adds the client key and certificate
                  type settings to the configuration that connection reuse and
                  the TLS session cache compare.
What to do:       Upgrade curl and libcurl to 8.21.0 or later. If you cannot,
                  the project advises not reusing handles when client
                  certificate details change.
Sources:          https://curl.se/docs/CVE-2026-8932.html
                  · https://cveawg.mitre.org/api/cve/CVE-2026-8932
                  · https://github.com/curl/curl/commit/7541ae569d82fb308a5e2d94916027da4fa3ba3e
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 12](2026-12-12-door-12-the-porter-who-vouched-for-everyone.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
