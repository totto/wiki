---
tags:
  - LinkedIn
  - Writing
date: 2026-03-01
---

# AI-to-AI PR review loop

*March 1, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7433842598353694720)*

**8 reactions · 4 comments**

---

I submitted a pull request. An AI reviewed it. I fixed the issue. It reviewed again.

This happened six times.                    
                                                                 
My job in all of this: clicking "Approve Push."

---  
 Here is a summary of the conversation between the two AIs:

Cursor Bugbot: You hardcoded your home directory into the script.  
 Me: I fixed it.

Bugbot: Your tools can read any file on the machine.  
 Me: I fixed it.

Bugbot: Your path validation uses startsWith(). That's a traversal vulnerability.  
 Me: I fixed it.

Bugbot: Your JSON schema declares a parameter you silently ignore. Also grep needs -e.  
 Me: I fixed it.

Bugbot: A KCP-aware agent following the specification correctly might skip your TL;DR shortcut due to misaligned summary_of back-pointers across combined reference units.  
 Me: I... fixed it.

Bugbot: ✅ No issues found.

---  
 Round 1 was a copy-paste mistake. Round 5 was a protocol design review. The same automated system. Seven passes. No human wrote a single review comment.

A human maintainer will eventually open this PR. They will find code that has survived seven rounds of increasingly pedantic AI review across four repositories simultaneously.

They will have no idea what went on here.

Full story:  https://lnkd.in/e78XANTG

---

## Discussion

> **seven rounds of automated review is intense, especially when it's not just linting but actual protocol design feedback — we've seen similar with our own API-first approach, where the machine can catch a lot but a human still needs to sanity-check the overall design, wondering how you balance that trade-off between automated pedantry and human oversight**: seven rounds of automated review is intense, especially when it's not just linting but actual protocol design feedback — we've seen similar with our own API-first approach, where the machine can catch a lot but a human still needs to sanity-check the overall design, wondering how you balance that trade-off between automated pedantry and human oversight

> **Totto** ↩: Worth clarifying — most rounds were the bot catching actual issues in the Python test scripts (permissions, paths, schema), not the PR intent itself.
 
That's the part I'd normally rush through and miss.

Round 5 was different: it flagged a protocol design concern. That one needed judgement — is this a real problem or future perfectionism? Turned out it was worth fixing.

So the split in practi...

> **I usually do many rounds in my own PRs, using different agents with different focus. I’d say most of the time it catches everything needed. Also verifying everything visually, reviewing tests and logic - not just code syntax. **: I usually do many rounds in my own PRs, using different agents with different focus. I’d say most of the time it catches everything needed. Also verifying everything visually, reviewing tests and logic - not just code syntax.

> **Totto** ↩: Daniel Bentes Today's attempt to prevent PR's (or issues) from new/unknown actors with crazy bot-schemes are choking Open Source codebases, but the attack vector is very real...

---

← [All LinkedIn posts](index.md)
