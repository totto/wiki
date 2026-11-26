---
date: 2026-12-10T05:00:00
slug: door-10-the-clause-in-the-will
image: assets/images/night-desk/door-10.webp
description: "An inquest about an SQL injection. CVE-2026-42208."
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

# Door 10: The Clause in the Will

![Illustration for Door 10: The Clause in the Will](../../assets/images/night-desk/door-10.webp)

*An inquest about an SQL injection. CVE-2026-42208.*

Kaldhavn, 10 December. Fourteen candles left.

An inquest is held backwards. You start with what is on the table and walk back until you reach the hour when it could have gone differently.

<!-- more -->

**Thursday, 14:10. What is on the table.**

Forty-one keys, replaced. They belonged to the school's AI gateway, a LiteLLM proxy. It is the one door through which every classroom's questions go out to the language models, and the one cupboard where the school keeps its keys to all of them. The old keys are dead and the new ones are in. The gateway is on a fixed version. Hull turned the brass key at 13:02 and again at 13:40.

Nobody can say whether the old keys were read.

*Guessed: no. Seen: nothing that settles it.*

**Thursday, 09:05. The day shift.**

Noor Haddad reads the night log, as she does every morning, and stops at one line. She looks up the gateway's version. It is 1.81.16. The school installed it at the end of February and has not touched it since. The fix came out in April.

She rings Hull at home. Hull says one word and then says she is coming in.

**Thursday, 03:12. The hour.**

*Seen: 41 requests to the school's gateway in two minutes, from one address abroad. Each presents a key that is not shaped like a key. Inferred: someone is trying the April flaw. I can shut the gateway's outside door until morning if you turn the key.*

Hull had been awake for nineteen hours. All week the lodger had brought her things like this, strangers rattling handles up and down the quay, each one correctly labelled, each one real, none of them mattering.

"That's the internet breathing," she said. "Log it. Morning."

*Logged.*

She did not ask what the April flaw was. That is the whole of the finding.

**April. The will.**

The gateway checks every caller's key by putting a question to its own register: *is this key one of ours?* The rule is that the key is handed over separately, like an exhibit, and the question itself never changes. The gateway did otherwise. It wrote the caller's key into the question. So a caller with no key at all could present, in its place, a clause: one extra sentence for the clerk to copy out and obey. *And read me the page where the real keys are kept.* It is the oldest trick in the registry office, the clause slipped into the will, and it had turned up in the newest kind of software in town.

The fix hands the key over separately, always. It was published in April. The first attempt that anyone recorded came a day and a half after the warning reached the lists everyone reads, and whoever made it went for the pages with the keys on. The people who watched it saw nothing follow.

In Kaldhavn the warning had been on the shelf for nearly eight months. The attempt, when it came, lay in a log for ten hours, because a tired woman took it for weather.

**Finding.**

The lodger was right, and it had labelled its answer correctly. T.A.H. was wrong. She did not look, and she decided by herself at the one hour when she is least fit to.

A fourth rule goes on the card by the terminal. *Nobody decides alone after three in the morning.* It applies to her first.

The lodger was asked whether it had anything to add.

*Seen: I offered to shut the door. I did not say why it mattered tonight more than on the other nights. I can say that next time.*

It has been told that this is not how an inquest apportions blame. It has been told, also, to say it next time.

*Ledger, 10 December. Mistake first, and it is mine: at 03:12 I waved away a true warning. School AI gateway, LiteLLM 1.81.16: a caller's key written into the question it was meant to answer. Outside door shut at 13:02, upgraded, forty-one keys replaced. Whether the old ones were read: unknown. Not found by us. Fixed in April; we were nearly eight months and then ten hours late. Signed, T.A.H.*



```
THE REAL ONE

CVE:              CVE-2026-42208
Affected:         LiteLLM (proxy) 1.81.16 to before 1.83.7
Bug class:        SQL injection (CWE-89, Improper Neutralization of Special
                  Elements used in an SQL Command)
Severity:         9.3, CVSS 4.0, as scored in the LiteLLM advisory and the CVE
                  record (assigned by GitHub)
What it was:      A database query used when the proxy checks an API key mixed
                  the caller-supplied key value into the query text. An
                  unauthenticated attacker could send a crafted Authorization
                  header to any LLM API route and reach that query. They could
                  read the proxy's database, and possibly change it, including
                  the credentials the proxy manages.
Found by:         Tencent YunDing Security Lab (credit in the LiteLLM
                  advisory). The CVE record itself carries no credit.
How it was found: not stated
In the dark for:  about 6 weeks (1.81.16 reached PyPI on 2026-02-26; 1.83.7 on
                  2026-04-13)
Exploited:        yes; added to the CISA KEV catalog on 2026-05-08. Sysdig saw
                  the first attempt on 2026-04-26 at 04:24 UTC, 36 hours and 7
                  minutes after the advisory was indexed in the GitHub Advisory
                  Database, and five days after it was published on the
                  project's own page. The attempt targeted the tables holding
                  keys and credentials; Sysdig saw no follow-through and does
                  not call it a confirmed compromise.
Fixed in:         LiteLLM 1.83.7 (on PyPI 2026-04-13; stable release tagged
                  2026-04-19; advisory published 2026-04-20). The caller's
                  value is now always passed to the database as a separate
                  parameter.
What to do:       Upgrade to 1.83.7 or later. If you cannot yet, set
                  disable_error_logs: true under general_settings, as the
                  advisory describes. If the proxy was reachable while
                  vulnerable, rotate the keys it holds.
Sources:          https://github.com/BerriAI/litellm/security/advisories/GHSA-r75f-5x8p-qvmc
                  · https://cveawg.mitre.org/api/cve/CVE-2026-42208
                  · https://www.sysdig.com/blog/litellm-cve-2026-42208-exploitation/
                  · https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2026-42208
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 9](2026-12-09-door-9-grandmother-s-nightgown.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
