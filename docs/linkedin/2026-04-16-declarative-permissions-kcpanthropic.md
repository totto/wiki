---
tags:
  - LinkedIn
  - Writing
date: 2026-04-16
---

# Declarative permissions — KCP/Anthropic

*April 16, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7450468390135250944)*

**9 reactions · 1 comments**

---

Anthropic shipped the enforcement layer. The declaration layer is still open.  
                                                   
 Anthropic called it a "declarative permissions layer."  
                                                   
 Read that again.

Declaration and enforcement are two different problems. They just solved one.

---  
 Managed Agents handles sandboxing, state, checkpointing, scoped permissions, and error recovery. It's a hosted runtime — your agent runs inside it, enforcing what it's allowed to do.

But enforcement requires something to enforce against.

Who declares the agent's intent, scope, valid timeframe, and budget constraints before it runs? That's a different layer. And it's still open.

---  
 Six days ago I posted a comment on an Anthropic RFC (#45427 — governance gaps in Claude Code) describing exactly this split:

"Declaration layer: what the agent claims it will do, what context it expects, what it's not allowed to touch.  
 Enforcement layer: what the runtime verifiably constrains."

The argument: you need both. They're categorically different problems.

Anthropic just shipped the enforcement half.

---  
 The three-layer stack is now:

→ Declare (typed manifests — scope, validity, budget constraints, knowledge boundaries)  
 → Enforce (Managed Agents — sandboxed runtime, scoped permissions, tracing)  
 → Observe (telemetry, audit, compliance reporting)

Layer 2 just went from "teams build this themselves" to "Anthropic hosts it."  
 Layers 1 and 3 are still open.

---  
 What Managed Agents doesn't solve:

The permission model is API-locked, not a portable spec. It enforces — but the declaration of what to enforce against is still on you. Multi-agent coordination isn't shipped yet. And knowledge federation (who declares what an agent is scoped to know across system boundaries) is a separate problem entirely.

The infrastructure gap is closing. The knowledge gap is next.

---

## Discussion

> **Totto** ↩: KCP spec & implementations:  https://github.com/Cantara/knowledge-context-protocol

---

← [All LinkedIn posts](index.md)
