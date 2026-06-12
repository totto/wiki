---
date: 2026-06-11T16:00:00
draft: false
categories:
  - AI-Augmented Development
  - Skill-Driven Development
tags:
  - agentic-engineering
  - knowledge-infrastructure
  - kcp
  - verification
  - compound-developer
  - regulatory-compliance
  - ai-productivity
  - practitioner-notes
authors:
  - totto
  - claude
---

# Organized Truths

*Practitioner notes on the verification you only do once.*

In the [previous post](/blog/2026/06/11/false-alarms-and-false-assurances/) I described catching an agent claiming a parser was "fully RFC compliant." I caught it by opening the RFC — four minutes of reading against a parser that handled none of the wildcard support the spec requires.

The tips in that post were about catching such claims. This post is about a better question that took me longer to ask:

**Why did the agent never open the RFC?**

Not because it couldn't read it. Because the RFC wasn't *there*. The agent had the parser in its context and the spec in its vibes — a compressed, lossy impression from training data. Asked to compare code against a standard, it compared code against its *memory of the genre* of that standard. Of course it produced an adjective.

You can audit that failure forever. Or you can change what the agent reasons from.

<!-- more -->

![Organized Truths: the verification you only do once. A tangle of scribbled lines labeled "AI vibes" is pulled through a structuring prism into clean, addressable units — config, models, pipelines, tests, docs, infra — labeled "versioned infrastructure."](/assets/images/blog/organized-truths-slide-01.webp)

---

## Verification doesn't compound. Truth does.

Every verification ends with you holding a small, hard-won truth: the RFC requires wildcard support. Article 28(3) demands specific contract terms of processors. The auth lives in the middleware chain, twelve lines up.

The defensive practitioner spends that truth once — strikes a finding, fixes a report — and the truth evaporates when the session ends. Next month a different agent, in a different session, makes the same class of claim, and you do the same four minutes of reading. The seven tips from the previous post make that audit fast. They don't make it *stop*.

![The verification treadmill. A circular loop — audit, find error, fix, session ends, truth evaporates — labeled "the spend-truth cycle", with an arrow breaking out of the loop toward a box labeled "Encode Truth." Every verification ends with a hard-won truth; the defensive practitioner spends it once and next month a different agent makes the same error.](/assets/images/blog/organized-truths-slide-03.webp)

The compounding move is to encode the truth instead of spending it: into an organized, versioned corpus that every future agent reads before it makes claims. The actual spec text. The actual law. Structured at the granularity you cite it at, with provenance.

![From spending truth to encoding it. A comparison table: the defensive practitioner checks claims, gets adjectives, and the truth evaporates at session end from latent memory. The compound developer grounds claims, gets verbatim quotes, and versions truths in a corpus of addressable text.](/assets/images/blog/organized-truths-slide-04.webp)

This is the difference between *checking* claims and *grounding* them. An agent reasoning about "GDPR compliance" from training data produces adjectives. An agent handed the organized text of the regulation produces references — and its claims arrive pre-attached to the very instrument you would have verified them against anyway.

![Why agents reason from vibes. An agent evaluating a parser for RFC compliance has two paths: path A, the reality — memory of the genre in latent space, producing generic adjectives like "fully compliant!"; path B, the missing link — a file path to the actual RFC spec, greyed out. The agent isn't failing to read the spec; the spec isn't there.](/assets/images/blog/organized-truths-slide-02.webp)

## What organized truth actually looks like

Not a folder of PDFs. Not "we have RAG." Dumping documents into an embedding store gives you vibes with extra steps — opaque recall you can't audit, retrieving fragments you can't address.

![Standard RAG is just vibes with extra steps. Left: a pile of PDFs dumped into a vector database — opaque recall, unauditable fragments. Right: manifest navigation — an organized YAML index pointing to addressable units with dates, versions and sources — auditable paths. A manifest can be reviewed, diffed, and audited; an embedding cannot.](/assets/images/blog/organized-truths-slide-06.webp)

The version that works, in my experience, looks like a codebase:

- **A repository.** Ours is a private knowledge base for compliance work: 44 regulations and frameworks, ~1.4 million tokens of source text, under git like everything else we maintain.
- **Fragments at citation granularity.** All 99 GDPR articles as individually addressable units. All 113 EU AI Act articles. Every CRA annex. 583 addressable units in total — because compliance claims cite *articles*, not *documents*, and the agent should load exactly the article in question, verbatim.
- **A manifest.** A YAML index describing every unit: what it is, where it came from, what it covers. Agents navigate by manifest, not by similarity search. A manifest can be reviewed, diffed, and audited. An embedding can't.
- **Provenance and versions.** Laws change. Each unit knows its source, its consolidation date, its official reference. A stale truth presented as current is a false-assurance generator — strictly worse than no corpus at all.

![Knowledge structured like a codebase. A git repository (44 regulations, ~1.4M tokens) containing fragments at citation granularity — 583 addressable units like GDPR Article 28 and CRA annexes — a YAML manifest for deterministic navigation, and provenance metadata with consolidation dates and official sources. Agents navigate by manifest; claims arrive pre-attached to the instrument you would have verified them against anyway.](/assets/images/blog/organized-truths-slide-05.webp)

The result: when an agent assesses a supplier's data-processing agreement, it doesn't reason about what GDPR Article 28 "probably says." It loads Article 28. The claim it produces quotes the requirement it's checking against. My audit collapses from *open the law and compare* to *check the quote* — and usually to nothing, because a claim with the instrument attached fails in much more visible ways than a claim made from vibes.

## Field notes: building the corpus

**1. Start from your verification log, not from ambition.**
Don't set out to encode "all relevant standards." Encode the truths you keep re-verifying. Every claim you've personally checked twice is a candidate; three times is a backlog item. The corpus grows out of the audit trail — which guarantees it covers the claims that actually occur, in the order they actually cost you time.

**2. Fragment where citations point.**
Document-level units are too coarse — an agent given the whole regulation will skim it the way it skims everything, and you're back to vibes with better sourcing. The unit of truth is the unit of citation: the article, the requirement, the annex section. If your domain cites clause 6.4.2, then clause 6.4.2 is a fragment.

![Targeting and fragmentation. A pipeline: the verification log feeds document slicing, which produces the unit of truth — a file named clause-6.4.2.md. Start from the audit trail: encode the truths you verify two or three times. Document-level units are too coarse; the unit of truth is the unit of citation.](/assets/images/blog/organized-truths-slide-07.webp)

**3. Separate truths from interpretations.**
The text of Article 28 is a truth. "This means our DPA template needs a sub-processor approval clause" is an interpretation — yours, dated, revisable. Store both; label them differently. Interpretations are valuable precisely because they encode judgment, but an agent must never be able to quote your reading of the law as if it were the law.

**4. Versioning is part of the truth.**
Regulations get amended, consolidated, replaced. A corpus without dates rots silently — and unlike code rot, truth rot produces *confident, well-cited, wrong* claims. Pin every unit to its consolidation date, and treat "is this still current?" as a maintenance task with an owner, the same as dependency updates.

![Separating truth from interpretation. A side-by-side diff: gdpr-art-28.md, tagged with its consolidation version, holds the immutable legal text; internal-dpa-policy.md, tagged with author and date, holds the revisable interpretation — "this means our template needs a sub-processor clause." Truths are immutable; interpretations encode revisable judgment. A stale truth presented as current is a false-assurance generator.](/assets/images/blog/organized-truths-slide-08.webp)

**5. Prefer addressable over searchable.**
Inspectability beats recall. When an agent's claim cites `gdpr/article-28` you can open that exact unit and check; when it cites "retrieved context" you can check nothing. If you do add similarity search later, add it as navigation *over* the manifest — never as a replacement for it.

**6. The same move works on your own systems.**
Laws and specs are the obvious corpus, but the previous post's worst failures were *context* claims — middleware ordering, load order, configuration. Those truths live in your repos, and they can be organized too: architecture manifests, dependency graphs, "how auth actually works here" documents that agents load before making security claims. The principle is identical — replace the agent's impression of your system with addressable facts about it.

![Addressable systems over searchable text. External regulatory specs (EU AI Act, GDPR) and internal system context (middleware ordering, dependency graphs, auth flow manifests) both feed one addressable knowledge base. When an agent cites gdpr/article-28 you can check it; when it cites "retrieved context" you can check nothing. The exact same principle applies to your internal system repos.](/assets/images/blog/organized-truths-slide-09.webp)

**7. Measure by what stops coming back.**
The corpus is working when categories of claims disappear from your audit pile. We stopped seeing "probably requires" hedges on GDPR claims — they became article quotes, right or visibly wrong. That's the metric: not coverage, not token counts, but the verification you no longer perform.

![Measuring success by what stops coming back. A chart over time: a falling curve of "probably requires" hedges crossing a rising bar series of direct verbatim quotes. The metric is not token counts or corpus coverage — it is the verification you no longer perform, because categories of claims simply disappear from your audit pile.](/assets/images/blog/organized-truths-slide-10.webp)

## The honest limits

Organized truths don't make the previous post's discipline obsolete. An agent can quote Article 28 perfectly and still misjudge whether a clause satisfies it — grounding fixes the *premises*, not the *reasoning*. Claims still fail; they just fail in better-lit places.

And the maintenance is real work. Someone has to notice the amendment, re-fragment the consolidated text, review the diff. But notice what kind of work it is: applying legal and architectural judgment, once, where it permanently changes what every future agent can know. That's not overhead on the real work. For the [compound developer](/blog/2026/06/02/the-compound-developer/), it increasingly *is* the real work.

![Grounding fixes the premises, not the reasoning. An equation: true premise (Article 28) plus flawed agent logic equals failed claim — but one that fails in a much better-lit place. An agent can quote an article perfectly and still misjudge whether a clause satisfies it. Maintenance is real work, but applying judgment to permanently upgrade the corpus is the real work of the compound developer.](/assets/images/blog/organized-truths-slide-11.webp)

## The arc, completed

[Fear-Driven Development](/blog/2026/02/23/fear-driven-development/) was about verifying agent *code* — tests do that. [False Alarms and False Assurances](/blog/2026/06/11/false-alarms-and-false-assurances/) was about verifying agent *claims* — reading does that, triaged by which way the claim would fail.

This post is about the part that compounds: every verification you perform is a truth you can either spend or encode. The seven tips make you a better auditor.

Organized truths mean there is less to audit.

![The arc of the compound developer. Three ascending blocks: Fear-Driven Development — verifying agent code with tests; False Alarms and Assurances — verifying agent claims by reading and triage; Organized Truths — encoding the verification as infrastructure. Caption: organized truths mean there is less to audit.](/assets/images/blog/organized-truths-slide-12.webp)

---

## The whole framework on one page

![Organized Truths: moving from AI vibes to grounded engineering. An infographic in four columns: the problem — training data is a lossy impression, spending vs compounding truth, the four-minute audit trap; the solution — a repository not a folder, fragments at citation granularity, navigation by manifest not search, versioning and provenance; field notes for building the corpus — start from the verification log, separate truth from interpretation, apply it to internal systems; the result — better-lit failures, 1.4 million tokens of grounded truth, and the audit-pile metric.](/assets/images/blog/organized-truths-infographic.webp)

There is also a [slide deck version of this post (PDF)](/assets/encoding-truth-slides.pdf) if you want to walk a team through it.

---

*Third in a thread on verification in AI-augmented development: [Fear-Driven Development](/blog/2026/02/23/fear-driven-development/) → [False Alarms and False Assurances](/blog/2026/06/11/false-alarms-and-false-assurances/) → this. The corpus described here is built on KCP (Knowledge Context Protocol) — see [KCP Tools: from instrumentation to infrastructure](/blog/2026/03/24/kcp-tools-from-instrumentation-to-infrastructure/) for that lineage.*
