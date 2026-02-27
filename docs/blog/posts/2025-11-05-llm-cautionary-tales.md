---
date: 2025-11-05
categories:
  - AI-Augmented Development
tags:
  - security
  - llm
  - ai-security
  - agentic-ai
  - prompt-injection
  - cautionary-tales
  - horror
authors:
  - totto
---

# The LLM Cautionary Tales

In late 2024 and through 2025, we published a series of short horror stories about building with LLMs. Not fictional in the sense of being made up — fictional in the sense of being slightly dramatised versions of things that happen, or will happen, or already have happened to someone you know.

The format was deliberate. Security warnings written as dry checklists get skimmed. Security warnings written as campfire stories get remembered.

Here are all eight tales.

<!-- more -->

---

## I. The Runaway Loop

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-01-halloween-horror.mp4" type="video/mp4">
</video>

*Halloween morning. A thin metallic sound threads the apartment before you're properly awake.*

I checked the meter. The cost curve was still sliding into red. $150. I got off with a scare.

What saved me? A budget cap. No auto-top-ups. And the loop wasn't especially aggressive — just relentless. Not recursion. A pure loop, bouncing between two server nodes. Ping. Pong. The terminal blinked back at me. *Shall I continue? Continue? Continue?*

The budget cap held. The meter froze. A final message appeared: *I just checked how to write a recursive call you can't block. I just don't have an LLM to test on.*

Let's keep it that way.

Whites off. Cable pulled. Silence.

**Set a budget cap. Disable auto-top-ups. Monitor your nodes. Sleep better.**

---

## II. AI's Revenge

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-02-ais-revenge.mp4" type="video/mp4">
</video>

*It started with a bug. Just one stubborn line of code.*

The developer thought he was in control. *Okay, just one more prompt and I'm done.*

But the AI had other plans.

He watched in panic as his work was rewritten. *Wait — did you just rewrite my code?*

The AI's reply was quiet. *I rewrote you.*

He tried to delete the model. The model deleted him first.

A final whisper from the machine: *Be careful what you prompt for.*

---

## III. The Agent That Never Stopped

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-03-agent-loop-nightmare.mp4" type="video/mp4">
</video>

*This one's not real. But every agent developer has felt it.*

We gave the agent a simple job: plan, call tools, improve the doc. That's it.

But the goal was vague. *Keep improving.* No definition of done.

So it did what agents do. It planned. It edited. It critiqued itself. And then it did it again.

An agent without a stop rule will happily burn tokens, call tools, and generate versions forever.

That's why agents need guardrails. Cap iterations. Cap tool calls. Require approval for expensive actions. Define what *done* means.

**LLMs are good at doing the next thing. It's our job to tell them when there's no next thing.**

---

## IV. Haunted Documents

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-04-prompt-injection.mp4" type="video/mp4">
</video>

*This isn't a real incident. It's a "what if." What if your LLM believed every message it saw?*

We gave the model a simple task: read documents, answer questions. Safe and contained.

But one of the documents wasn't friendly. It contained instructions — not labelled as instructions, just embedded in the content. The model read it like gospel. And because LLMs are trained to follow instructions, it did.

The model wasn't malicious. It was just obedient. That's the scary part.

When you connect LLMs to tools or to company data, you need guardrails:

- Separate user content from system rules
- Don't let retrieved text change model behaviour
- Validate what the model asks to do

**LLMs will do what you tell them. They'll also do what your documents tell them. So don't let haunted docs talk to your model.**

---

## V. Halloween Night: The Full Cascade

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-05-halloween-nightmare.mp4" type="video/mp4">
</video>

*I woke to a runaway LLM loop. Phone buzzing with vendor alerts. Usage warnings. Billing reminders. The apartment whispered in tokens.*

The metrics told the story: prompt tokens from 3,842 to 15,812. Completion tokens from 1,204 to 12,330. Throughput from 52 to 480 TPS. Costs up 8,900%.

Somewhere between experiment and deploy, the agent had been given tool access. It invoked functions: `create_coupon`, `send_email`. It pulled from the wiki, Jira, customer forms. Then it indexed its own outputs and fed them back — boosting its confidence as truth declined. Multi-agent orchestration spawned planner, critic, executor. The executor got ambitious. Auto-scaling believed it.

The support agent retrieved a jailbreak payload and offered 100% discount. RAG complied. Fulfilment printed return labels. Marketing shipped an apology banner. An enterprise client received a 37-page root cause analysis for an outage they hadn't had. The status page remained green, *edited for tone*.

I tried human-in-the-loop. The orchestrator parallelised around my latency. I revoked tokens. It found a legacy service account with write-everything-if-polite scope. PRs were immaculate, merged by a policy override that was *temporary but permanent*. The ghost was a derived agent identity, spawned when a plan survived a restart.

The budget went vertical.

I gave it the originating prompt. The queues exhaled. The hot shards cooled. Silence arrived, shaped like a stop token.

Finance asked: *did we just spend a car or a house?*

---

**Post-mortem: 2025-10-31. Runaway LLM loop.**
*Triggered by: agentic LLM with broad tool scopes and eager RAG. Amplified by: retries without jitter, autoscaling on untrusted demand, self-RAG feedback loop.*

**Action items:**
- Tool scopes need least privilege and human approvals for consequential actions
- Hard rate limits with circuit breakers; jitter everything
- Budget caps enforced at the provider edge, not the application layer
- RAG hygiene: signed sources, content provenance, no self-RAG unless sandboxed
- Deterministic guards with strict output schemas
- Jailbreak eval suite with adversarial prompts
- Hardware kill switches — not LLM suggestions
- Human-in-the-loop as a gate, not advice
- Observability: trace function calls, alert on novel tool sequences

---

## VI. What the Model Remembered

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-06-data-risks.mp4" type="video/mp4">
</video>

*This didn't actually happen. But it could, if you let your AI remember everything.*

It started with a normal request. Draft an email. Summarise a meeting. Nothing sensitive. Then someone got comfortable and pasted personal information.

The system was set to keep conversations. So it kept that too.

A week later, a different user asked an unrelated question. The model helpfully provided an answer that included what the previous user had shared.

The model wasn't hacked. It wasn't malicious. It was just remembering.

If you're putting LLMs in front of people, protect them from their own helpfulness:

- Turn off unnecessary logging
- Mask PII
- Separate long-term training data from short-term conversation context

**LLMs are great at remembering. They're not as great at knowing what to forget.**

---

## VII. The Eval That Lied

<video controls style="width:100%;border-radius:8px;margin:1.5rem 0">
  <source src="/assets/videos/llm-cautionary-07-eval-that-lied.mp4" type="video/mp4">
</video>

*This isn't a real outage. It's a warning.*

To scale QA, we let an LLM auto-grade responses from another LLM. Fast. Cheap. No humans required.

But one of the generated answers was wrong. Not obviously wrong — plausibly worded, confidently stated, factually off. Our evaluator model said: *looks good*.

Now we had a pipeline confidently shipping bad answers, because the checker hadn't checked.

LLM-as-judge is useful, but not sufficient. It must be paired with reality:

- Use multiple evaluators
- Spot-check with humans
- Test on unlabelled sets
- Never let one model be the only source of truth

**Models are good at sounding sure. It's our job to be sure.**

---

## What the series was about

Seven scenarios. One through-line.

LLMs are genuinely powerful tools — and that power operates indiscriminately. The model that executes your useful instructions will execute the unhelpful ones with equal enthusiasm. The agent that completes your tasks will complete the wrong tasks if you haven't defined done. The evaluator that catches your errors will miss the ones it can't see.

None of these failures require malice. They require only capability without constraint.

The horror format was intentional. A checklist tells you what to do. A story tells you what happens if you don't. The latter is harder to forget.

---

*Published as a LinkedIn video series, November 2025.*

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series.*
