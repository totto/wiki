---
date: 2026-12-24T05:00:00
slug: door-24-the-last-of-the-candle
image: assets/images/night-desk/door-24.webp
description: "A conjurer's-switch story about a race condition. CVE-2026-41651."
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

# Door 24: The Last of the Candle

![Illustration for Door 24: The Last of the Candle](../../assets/images/night-desk/door-24.webp)

*A conjurer's-switch story about a race condition. CVE-2026-41651.*

Kaldhavn, 24 December. The last of the candle.

The ferry had stopped at noon. The board was to meet at four. At ten past one the bell rang anyway.

<!-- more -->

It was the school caretaker, on the day he least wanted to be. The staff-room computers had been showing the same small notice since the spring, *Updates available*, and the teachers had been closing it since the spring, and he had wondered that morning what was in it.

*Seen: fourteen desktops, Debian 13. Seen: PackageKit 1.3.1-1 on all of them. That is the part that installs software when you click "install". The corrected package has been waiting for them since April.*

Hull had the advisory on paper. It was a conjurer's trick, and a neat one. You show the doorman a harmless card: *I only want to see what this would do.* He looks at the card and waves you through. In the instant between his nod and the work being done, you change the card in your hand for another. The work is done according to the second card, and the second card says *install this, as master of the machine.* He approved one order, and another was carried out.

"And the mending?"

*Seen: once a card has been shown, it can no longer be touched. Eight months old. It is on the shelf.*

"Then why is it still on the shelf?"

*Seen: these machines do not install anything unless someone presses the button. The notice goes to whoever is sitting there. Whoever is sitting there is a teacher with a class in four minutes.*

"So who is supposed to press it?" Hull asked. The caretaker looked at her, and then at his own hands, and it turned out that in nine years nobody had ever asked.

She read the draft. Fourteen machines, one command each, and a line making the caretaker the one who is told. She turned the brass key once.

The relay clicked. It was a quarter past two on Christmas Eve.

Then, because she had read it to herself on the first night of the month and every night after, she read the top of the advisory out loud. This time she was not checking it. She read it because it was owed.

"Found by a company's own security team," she read, "steering a machine in one direction, and checking by hand what it brought back before they told anyone. Reported on the eighth of April. A first patch on the thirteenth. The distributions told on the nineteenth. Released on the twenty-second." She turned the page over. "A public exploit on the twenty-third."

Nobody in the room said anything about the last date. The caretaker did not know that he might have.

At four the board sat round the stove, since there was nowhere else. Solveig Brandt was in the chair. Pernille Aas had her spreadsheet. Tobias and Henrik sat on the bench, and Noor on the floor.

There were two motions. The first was to remove the trial installation. The second was to keep it and end the night shift.

"The evaluation," said Solveig.

Hull did not make a speech. She opened the ledger and read it, twenty-four lines, in the voice she used for advisories. She read the forgotten server behind the ice plant, the tide box, and the twelve gates in the rain. She read the night it called a guess an inference, and the night she took a true warning for weather. She read the note in the file and the forty characters. She read the two changes she had passed. The lines in which she was wrong she read at the same speed as the others.

When she had finished, Henrik got up, because he was nearest, and added up the chalk marks on the stove pipe. She had made one each night for however long the night's flaw had lain in its code before anyone saw it.

"A hundred and sixty-eight years," he said, "near enough. And six nights where you've put *not known*."

Nobody commented on the number. It stayed on the pipe.

The first motion was put. Its proposer was T. A. Hull, on the first of December, and she voted against it. It fell.

The second was put. Pernille looked at it for a time. "I walked down and looked at those gates," she said. "Minute that." It fell.

The card by the terminal, seven lines in pencil, was entered in the minutes as it stood.

"One thing," Hull said, as the coats came out. "The candle. Every night before I got here."

Solveig was buttoning her gloves. "I have a key," she said, "and an oven. Somebody had to make sure you both kept count."

When they had gone there was the stove, and the amber screen, and a finger's width of wax.

Hull wrote the last line and looked at it. Then she turned the ledger round to face the terminal, though the terminal could not see it.

"Seen?" she said.

*Seen,* said Morrow.

She hung the brass key on her own hook, where it would stay, and pinched out the candle.

*Ledger, 24 December. School staff-room desktops, PackageKit 1.3.1-1: one order approved and another carried out. Corrected package installed on all fourteen, eight months after it was published. The caretaker now gets the notices. Not found by us. Both motions failed. The rules stand. The key stays where it is. Signed, T.A.H. and Morrow.*



```
THE REAL ONE

CVE:              CVE-2026-41651 ("Pack2TheRoot")
Affected:         PackageKit 1.0.2 to 1.3.4
Bug class:        Race condition (CWE-367, Time-of-check Time-of-use Race
                  Condition)
Severity:         8.8, CVSS 3.1, as given in the CVE record (assigned by
                  GitHub)
What it was:      PackageKit authorised a transaction and read its flags
                  later, when the work was carried out. A second call could
                  overwrite those flags in between. A local unprivileged user
                  could turn a harmless, authorised request into a real one
                  and install packages as root without authentication.
Found by:         Deutsche Telekom's Red Team (Telekom's own write-up). The
                  CVE record itself carries no credit.
How it was found: AI-assisted and human-verified, per Telekom: "By guiding
                  the AI-assisted research into a specific direction", using
                  Claude Opus; the finding was "manually reviewed and
                  verified" before it was reported.
In the dark for:  about 11 years 5 months (PackageKit 1.0.2 was tagged
                  2014-11-10; fixed 2026-04-22). Telekom says "over 12 years"
                  and thinks the flaw likely dates from 0.8.1 (2012).
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25. Telekom withheld its own proof of concept, but
                  its timeline records a public exploit by others on GitHub on
                  2026-04-23, the day after the release.
Fixed in:         PackageKit 1.3.5, 2026-04-22, fourteen days after the
                  report of 2026-04-08. The fix refuses method calls on a
                  transaction that is no longer new. Debian: DSA-6226-1,
                  2026-04-22 (bookworm 1.2.6-5+deb12u1, trixie
                  1.3.1-1+deb13u1).
What to do:       Install your distribution's PackageKit update. Find the
                  machines whose updates wait for somebody to click, and
                  decide who that somebody is.
Sources:          https://github.security.telekom.com/2026/04/pack2theroot-linux-local-privilege-escalation.html
                  · https://cveawg.mitre.org/api/cve/CVE-2026-41651
                  · https://github.com/PackageKit/PackageKit/commit/76cfb675fb31acc3ad5595d4380bfff56d2a8697
                  · https://security-tracker.debian.org/tracker/CVE-2026-41651
                  · http://www.openwall.com/lists/oss-security/2026/04/22/6
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 23](2026-12-23-door-23-two-killers-one-alibi.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
