---
tags:
  - LinkedIn
  - Writing
date: 2026-03-03
---

# kcp-commands

*March 3, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7434516403388432384)*

**10 reactions · 0 comments · 2,441 views**

---

Two cohorts this week. Item Consulting, back to back.

We're arriving with something to hand out.

The thing participants kept flagging in the first round: context filling up with output garbage. ps aux dumps 30,000 tokens into the context window when you needed 600. find floods the context before you've asked the real question. The model reads it all. None of it was useful.

Today we released the direct answer: kcp-commands.

It's a Claude Code hook — intercepts Bash calls in two places. Before execution: injects compact flag/syntax guidance so the agent never wastes a round trip on --help. After execution: filters noise from large outputs before they hit the context window.

Measured across a real agentic coding session:

- 67,352 tokens saved  
 - 33% of a 200K context window recovered  
 - 33 additional tool call results fitting in the same space  
 - ps aux: 30,828 tokens → 652 tokens (98% reduction)

283 commands bundled. Git, Docker, kubectl, Maven, npm, AWS, Terraform — covered out of the box.

curl -fsSL https://lnkd.in/efjfmFBy | bash -s -- --java

Full benchmark methodology and design rationale: https://lnkd.in/eWw88EUF

Part of the KCP ecosystem: https://lnkd.in/e3sa5jUD (Apache v2)

#ClaudeCode #AIAgents #DeveloperTools #OpenSource #KnowledgeContextProtocol

---

← [All LinkedIn posts](index.md)
