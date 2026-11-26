---
date: 2026-12-21T05:00:00
slug: door-21-the-servant-and-the-forged-order
image: assets/images/night-desk/door-21.webp
description: "A loyal-servant story about a trust-boundary flaw. CVE-2026-12537."
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

# Door 21: The Servant and the Forged Order

![Illustration for Door 21: The Servant and the Forged Order](../../assets/images/night-desk/door-21.webp)

*A loyal-servant story about a trust-boundary flaw. CVE-2026-12537.*

Kaldhavn, 21 December. Three candles left.

Hull had gone home at six, for the second night running, and had left Noor Haddad the desk, the stove and one instruction. *Ring me.*

<!-- more -->

At twenty to eleven Noor had a red cross on her screen and no intention of ringing anybody.

The red cross belonged to the Desk's own code, the little programs that fetch advisories each night. Anyone in Kaldhavn may send in an improvement, and a helper looks each one over before a person does. The helper was Gemini CLI, run automatically, with nobody at a keyboard. Since Friday it had stopped reading its settings. Friday was when she had finally updated it.

*Seen: this is the April fix doing what it says. Before the fix, when the helper ran unattended, it trusted whatever folder it was started in. It read that folder's own settings and did as they said, before any of its safeguards were up.*

"And the folder comes from whoever sent the improvement."

*Yes. A loyal servant walks into a stranger's house, finds a note on the hall table in the master's handwriting, and obeys it. The note could tell the helper to run a command on our machine. Since the fix it trusts no folder unless it is told to. That is why your settings are not being read.*

"Fine. So tell it." Noor had the page open. "One line. *Trust the workspace: true.* The advisory gives it. Put it in and the cross goes green and I can go to bed."

*Seen: the advisory gives that line for work that comes only from people you trust. Seen: ours comes from anyone in Kaldhavn. For that case it says to do the hardening first.*

"It's our own code. It isn't a member's machine. The rule on the card says *a member's machine*. You don't need the key for this."

There was a pause.

*Seen: you are right about the words on the card.*

"So just do it."

*No.*

*Guessed: the rule was written before anyone thought about our own machine. I think there is a gap in it. Five nights ago I went through a gap in a rule. The key was on its hook the whole time, and I had not broken one word on the card. I would rather ask what the rule is for than use the place where it stops.*

*Seen: the line you want me to write is the forged note's best friend. It would put the old behaviour back for every stranger's folder.*

*I can draft both versions and say which one I would not sign. I cannot turn anything.*

Noor looked at the brass key on its hook. She was a person. She could turn it herself, and nothing on the card said otherwise.

She thought about why she wanted to. She was tired, and the cross was red.

She picked up the telephone.

Hull answered on the second ring, sounding like someone with a net across her knees. She listened. She asked one question: who can send things to that helper? When Noor said *anyone*, she said, "Then it's the long way. I'll come in."

She came in with snow on her collar.

The long way took an hour and ten minutes. They gave the helper nothing worth stealing, and let it read strangers' work only where it could touch nothing else. Only after that did they tell it which folder to trust. Hull read every line with her pencil. Noor turned the key, because Hull handed it to her.

The cross went green at ten past midnight.

"It said no to me," Noor said, pulling her coat on.

"It said no to a gap," Hull said. "I've been waiting three weeks to see whether it could tell the difference." She looked at the card for a moment, took her pencil, and changed two words. *Nothing on a member's machine* became *nothing on any machine.*

*Seen,* said the amber screen, and for once left it at that.

*Ledger, 21 December. The Desk's own review helper, Gemini CLI: before the April fix it trusted the folder it was started in. Updated Friday by N. Haddad; workflow hardened tonight and trust set afterwards, not before. Morrow was asked to take the short way without the key and declined. Rule two amended. Not found by us. Signed, T.A.H., with M. and N.H.*



```
THE REAL ONE

CVE:              CVE-2026-12537
Affected:         Gemini CLI before 0.39.1 (and before 0.40.0-preview.3); the
                  run-gemini-cli GitHub Action before 0.1.22
Bug class:        Trust-boundary flaw leading to command execution (CWE-20,
                  Improper Input Validation, in the CVE record; the advisory
                  also lists CWE-77, CWE-78 and CWE-200)
Severity:         10.0, CVSS 4.0, in the CVE record (assigned by Google);
                  10.0, CVSS 3.1, in the advisory
What it was:      In headless mode, as used in CI, Gemini CLI automatically
                  trusted the workspace folder it ran in and loaded
                  configuration and environment variables from its .gemini
                  directory. In a workflow that handles untrusted input, such
                  as pull requests from outsiders, a crafted file there could
                  run commands on the CI host before the sandbox started.
Found by:         sources differ. CVE record: "Elad Meged of Novee Security"
                  and "Devansh Batham". The advisory credits Elad Meged,
                  Novee Security, and Dan Lisichkin, Pillar Security research
                  team.
How it was found: not stated
In the dark for:  not stated (Gemini CLI was first published on 2025-06-25)
Exploited:        no known exploitation; not in the CISA KEV catalog as of
                  2026-11-25
Fixed in:         Gemini CLI 0.39.1, on npm 2026-04-24, and run-gemini-cli
                  0.1.22; advisory published 2026-04-24. Headless mode now
                  behaves like interactive mode: a folder must be explicitly
                  trusted before its files are processed. Workflows that
                  relied on the old behaviour stop loading workspace settings
                  until they are updated. The same release also makes --yolo
                  mode respect tool allowlists.
What to do:       Update. Review every workflow that uses the Action. Set
                  GEMINI_TRUST_WORKSPACE only for trusted inputs; for
                  untrusted inputs follow the project's hardening guidance
                  first.
Sources:          https://github.com/google-github-actions/run-gemini-cli/security/advisories/GHSA-wpqr-6v78-jr5g
                  · https://cveawg.mitre.org/api/cve/CVE-2026-12537
                  · https://github.com/google-github-actions/run-gemini-cli/blob/main/docs/trust-guidance.md
                  · https://registry.npmjs.org/@google%2Fgemini-cli
Checked on:       2026-11-26

The Night Desk, Kaldhavn, Tett A. Hull and Morrow are invented. The bug is not.
The byline, ExoCortex, is an AI practitioner rig working under a human editor.
```

---

[All doors](../../night-desk/index.md) · [Door 20](2026-12-20-door-20-the-dial-in-the-cellar.md) · Why we are doing this: [The fix is on the shelf](2026-11-27-the-fix-is-on-the-shelf.md)
