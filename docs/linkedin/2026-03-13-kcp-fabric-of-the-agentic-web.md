---
tags:
  - LinkedIn
  - Writing
date: 2026-03-13
---

# KCP fabric of the agentic web

*March 13, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7437966354395148288)*

**19 reactions · 1 comments · 537 views**

---

The autonomous agentic web is being built right now.                               
                                                          
 Not in some lab. In production pipelines, CI/CD systems, developer rigs, compliance workflows. Agents that  write code, search knowledge, call APIs, delegate to other agents, escalate to humans when they can't resolve something.

Most of the pieces work. The models are capable. The tooling is solid. The use cases are real.

What's missing is the fabric.

---  
 Think about how the web actually works. It's not that individual web servers are smart. It's that they share protocols. HTTP. HTML. URLs. Because they agreed on how pages connect — not what they contain — anything  
 can link to anything. A browser built in 2026 can navigate a site built in 1996.

That composability isn't magic. It's infrastructure.

The agentic web is at the point the web was before HTTP. Lots of smart individual pieces. No agreed way to connect them.

---  
 Right now, if an agent needs to discover what another agent — or a CLI tool, or a service — can do, the options are roughly:

- Read the documentation and hope it's accurate  
 - Load a vendor SDK that may bring tens of thousands of tokens of overhead  
 - Ask the tool to describe itself and trust the answer

None of these scale. None give the calling agent typed, verifiable, portable information about what's available, what's allowed, and what requires human approval before acting.

That's the gap.

---  
 KCP — Knowledge Context Protocol — is an attempt to fill it.

Typed YAML manifests. Machine-readable. Portable across clients and models. A manifest describes what a tool does, what context it expects, what requires approval, what constraints apply, and how delegation works  
 when agents hand off to other agents.

Agents can discover capabilities without reading documentation. Validate constraints before calling. Understand what they're allowed to do without relying on a system prompt that gets paraphrased across hand-offs.

We started building this for our own rig. Then realised it was more than a local optimisation.

The spec is open. 289 CLI tool manifests are published under Apache 2.0. It's been submitted to AAIF as a companion to MCP. The first independent adopters are building on it.

---  
 The web didn't get composable because individual pages got smarter. It got composable because developers agreed on how pages connect.

We're trying to do the same thing for agents.

https://lnkd.in/e94JbT8e

Would be curious whether others building multi-agent systems are running into the same gap.

---

## Discussion

> **Totto** ↩: More details on my blog:  https://wiki.totto.org/blog/2026/03/13/the-autonomous-agentic-web-needs-a-foundation-layer/

---

← [All LinkedIn posts](index.md)
