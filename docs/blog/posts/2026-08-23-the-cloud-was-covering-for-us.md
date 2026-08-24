---
description: "Local models don't just cost you quality for sovereignty — they're too literal to cooperate with the unstated assumptions a strong cloud model quietly papers over. On why local/embedded LLM support matters, and what it actually takes to ship it: two rounds of bugs, neither of them the model's fault."
date: 2026-08-23T09:00:00
draft: false
categories:
  - AI Agents
  - Engineering
tags:
  - local-llm
  - embedded-ai
  - agents
  - verification
  - data-sovereignty
  - llama.cpp
authors:
  - totto
  - claude
---

# The Cloud Was Covering for Us

We expected the usual trade when we pointed one of our agents at a local model instead of a cloud API: somewhat worse answers, in exchange for the documents never leaving the machine. What we got instead was a smaller, more literal model walking straight into real bugs in our own verification logic — bugs a large cloud model had been sailing past for months without ever tripping them. The local model didn't get dumber. It got honest, and honesty found the gaps.

<!-- more -->

![The Cloud Was Covering For Us: why embedded local LLMs expose the hidden flaws in your system architecture, and the engineering reality of shipping them.](/assets/images/blog/the-cloud-was-covering-for-us/hero-cloud-was-covering.png)

That was the first lesson. The second, which took longer to learn, was how much of the real work of shipping local inference has nothing to do with models at all.

## Why this direction matters

There's a structural tension in AI products right now. Everything about how they get built pulls toward the cloud: the strongest models live behind APIs, the tooling assumes an API key, the economics reward metered calls. "Cloud service" is the default shape of an AI product — not because anyone decided that, but because every incremental choice points the same way.

Now look at who most needs a product like ours — an agent that evaluates documents against externally supplied requirements and has to justify every verdict, not just state one. The customers with the strongest need for that are disproportionately the ones cloud-first design serves worst: regulated industries where a document legally cannot cross a boundary, organizations for whom a foreign API in the loop is a sovereignty problem rather than a latency problem, environments that are simply offline. The pattern generalizes past our niche: the more an AI system's output has to stand up to scrutiny, the less acceptable "we sent your document to someone else's computer" becomes. Cloud-first design quietly optimizes for the customers with the weakest requirements.

![Table: cloud-first defaults versus sovereignty-first reality, across regulated industries, sovereign organizations, air-gapped environments, and accountable systems — the more scrutiny an AI system's output must survive, the faster the cloud-first default breaks down.](/assets/images/blog/the-cloud-was-covering-for-us/cloud-first-weakest-requirements.png)

There's a second, quieter reason to care. If your system has only ever run against one vendor's strongest model, you don't know that your system is correct. You know that it's compatible. Those are different properties, and a local model is the cheapest way to find out which one you have.

## Round one: four bugs, none of them the model's

The plan was boring on purpose: same pipeline, swap cloud for local, ordinary CPU hardware, measure what quality costs. What happened instead was that the agent stopped being able to report a straightforward, correct "no."

1. Our verification logic could confirm a positive citation but had no way to confirm an absence. A claim like "the document doesn't address this" has nothing to cite, so it failed verification regardless of whether it was true. The cloud model phrased negatives in ways that happened to dodge this; the local model hit it constantly.
2. A "thinking" model spent its entire token budget on internal reasoning and returned nothing — a fixed token cap in our code, dressed up as a model-quality problem.
3. Our confidence handling treated a negative answer as inherently less certain than a positive one. It isn't.
4. The model's own conclusion-and-confidence trailer got mistaken for a claim about the document and failed verification against the source text.

![Four bugs across four layers — verification, token/memory, logic, and parsing — each traced to what the code assumed, not to model quality.](/assets/images/blog/the-cloud-was-covering-for-us/round-one-four-bugs.png)

Fixing these improved results with the cloud model too — decent evidence the bugs were ours all along. Performance tuning (reasoning off, thread counts, cache-friendly prompt ordering) helped modestly; the more useful finding was that prompt processing, not generation, dominates on CPU, and that a specialized low-bit kernel lost to a conventional quantization path that had simply earned years more optimization.

## Round two: actually shipping it

The first shippable step was an opt-in setting pointing the agent at a local inference server the customer already runs. That's real, tested, and merged — and not enough on its own, because most people cannot be expected to install and operate an inference server. The honest next step is a bundle: a second, much larger download containing a real inference engine and a real model, so a non-technical person gets local inference with zero setup. As of writing, that bundle is code-complete and has run a real end-to-end evaluation cycle successfully.

Nearly everything hard about it was systems work, not AI work:

- **Sourcing.** An MIT-licensed engine (prebuilt binaries, deliberately the generic build rather than a chip-specific one — customer hardware is whatever it is) and a permissively licensed model of about 2.2GB. We checked before designing, not after, that our distribution channel caps file sizes below the model's size, so the model downloads from its upstream host instead.
- **Integrity.** Every artifact's checksum is computed from the actual downloaded bytes — never trusted from a response header — and pinned in a lockfile. Rebuilds are reproducible and tamper-evident, not "it worked last time."
- **Supervision.** The engine runs as a supervised subprocess: picks its own free port, waits for real readiness (model loads take real time), and fails loudly if the bundle is missing or torn. It never silently falls back to a cloud call the customer didn't ask for and has no credentials for.

![Anatomy of a zero-setup bundle: sourcing (generic, license-checked engine builds), integrity (checksums from downloaded bytes, never response headers), and supervision (subprocess manages its own ports, fails loudly, no silent cloud fallback) — systems engineering, not AI.](/assets/images/blog/the-cloud-was-covering-for-us/zero-setup-bundle-anatomy.png)

- **Two more bugs.** An end-to-end run — not unit tests — caught that our planned context window was too small: a real prompt needed roughly 2.6 times the tokens we'd guessed. The fix went everywhere that number appeared, including the earlier release's bring-your-own-server documentation. And reading the actual code path — not testing the happy path — caught that our settings persistence would have silently written a session-only server address into the customer's permanent configuration the moment they touched an unrelated checkbox, breaking things only after the next restart. The fix separates "what the running process uses" from "what gets saved to disk."
- **Verification, and a false alarm.** We independently re-ran the whole pipeline — download, verify, package — from a fresh checkout on a second machine, and every checksum matched the first machine's byte-for-byte. The live run itself, on the original machine, crashed mid-inference with an out-of-memory-adjacent failure. Instead of assuming the fix was broken, we checked: the real cause was unrelated memory pressure already on that machine, nothing to do with the new code. We moved the live run to the second machine, where it completed cleanly — real model load, real inference, a real signed finding, ed25519 signature and all. A failure during verification is not automatically evidence that the thing you just built is broken. Isolate the cause first, then conclude.

![A failure during verification is not automatically evidence your code is broken: isolating the crash found pre-existing memory pressure on the first machine, unrelated to the fix — moving to a clean machine produced a real model load, real inference, and a real signed finding.](/assets/images/blog/the-cloud-was-covering-for-us/verification-false-alarm.png)

## The pattern

Count the failures across both rounds: an unverifiable negative, a token cap, a confidence prior, a misparsed trailer, a guessed context size, an untested persistence path, a crash we nearly misattributed. Not one was a model-quality problem. Every one was an unstated assumption, an unverified guess, or an unread code path in the system around the model.

The cloud model's fluency had been covering for those assumptions — it produced answers shaped like the ones our code expected, so the code never got tested. The local model was too literal to cooperate, and that turned out to be its most valuable property.

So if you're building verification logic on top of an LLM: build for the plain, terse, occasionally negative answer a small model actually gives, and treat every number you didn't measure as a bug you haven't hit yet. The question a local model asks isn't whether your product can survive a weaker model. It's whether your system was ever correct, or just well-covered. Ours wasn't, until we did the work — and the cloud path is better for it too.
