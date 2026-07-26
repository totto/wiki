---
description: "A short history of the agentic skill, told through one boring workflow: cutting a release. From prompts pasted into a chat window, to prompt folders in the repo, to knowledge units a planner can select, to signed charters a harness can enforce — each era solved the failure that broke the one before. Skills stopped being advice this year. Here is how, and what it unlocks for teams that compound."
date: 2026-07-26T09:00:00
draft: true
categories:
  - Knowledge Infrastructure
  - AI-Augmented Development
tags:
  - skills
  - skill-driven-development
  - kcp
  - defendable-agents
  - agent-governance
  - synthesis
  - pi-kcp
authors:
  - totto
  - claude
---

# From Pasted Prompts to Signed Charters: A Short History of the Agentic Skill

In 2023, if you wanted an AI to help you cut a release, you typed a small prayer into a
chat window and pasted the answer into your terminal.

This morning, an agent in my toolchain was *offered* a release skill by a deterministic
planner, which noted — in writing, in a receipt — that the skill was relevant to the task
but **not eligible to run**, because no human had granted it enactment rights. The skill
itself declared, in a signed manifest, exactly which tools it may invoke and which files
it may touch. A linter had checked that declaration. A different program stood ready to
block any tool call that reached outside it.

Same workflow. Same twenty lines of playbook. Completely different *kind of object*.

The distance between those two moments is about three and a half years, and almost nobody
noticed the transitions while they happened — each one looked like a small quality-of-life
improvement at the time. Told end to end, they form one story: **the agentic skill slowly
acquiring the properties of a charter** — a scoped, reviewable, revocable grant of
authority. This post walks that history with one deliberately boring running example,
because boring examples keep us honest: *how does the AI help you cut a release?*

<!-- more -->

## Era I — The pasted prompt (2023–2024)

The first agentic skills weren't files. They were folklore.

> *"You are a meticulous release engineer. When I say release, you will: check that CI is
> green, bump the version in pom.xml — never a SNAPSHOT — update the changelog, tag with
> a v-prefix, and push the tag. Ask before anything destructive."*

Everyone had a text file of these. Some people had *good* ones, and you could tell,
because their sessions went better than yours. The prompt was the skill, and the skill
was **personal property** — it lived in a notes app, it traveled by Slack DM, and when
its author went on vacation, the team's release quality went with them.

The era's characteristic failure was **invisibility**. Nobody could review the prompt
that produced a bad release, because nobody else had ever seen it. There was no diff, no
history, no way to say "this instruction is wrong" about an artifact that existed only in
the space between one person and their chat window. We had spent twenty years learning
that tribal knowledge kills teams, built wikis and runbooks to fix it — and then cheerfully
reinvented tribal knowledge with a paste buffer.

## Era II — The prompt moves into the repo (2024–2025)

The fix was obvious in hindsight: put the prompt in version control, next to the code it
operates on.

This is the era of `CLAUDE.md`, of `AGENTS.md`, of `.claude/skills/` directories — the
prompt-folder era. Our release folklore became a file:

```yaml
# .claude/skills/release-and-tag.yaml
name: release-and-tag
description: |
  How do I cut a release safely? Version bump, changelog, tag.
trigger_phrases:
  - "cut a release"
  - "release and tag"
instructions: |
  Bump the version in pom.xml — never tag a SNAPSHOT.
  Update CHANGELOG.md from the actual merged history.
  git tag vX.Y.Z and push the tag with the commit.
```

This was a genuine revolution, and I don't want the later eras to diminish it. The skill
now had an author, a history, a review process, and an audience of *every* agent session
in the repo instead of one person's. Teams that leaned into this — what I've been calling
[Skill-Driven Development](../../topics/skill-driven-development.md) — got compounding
returns: every captured workflow made every future session a little better. The skill had
become an **asset**.

But an asset with three chronic diseases, which I documented at length after running
[benchmarks against our own skills](../../topics/synthesis.md): skills go **stale** (the
skill says X, the code now does X-and-more), they stay **silent** (the trickiest patterns
never get written down), and they end up **ambiguous** (the skill states a fact but not
its intent — "V7 is missing" reads very differently from "V7 is intentionally reserved").
A prompt folder rots exactly the way a wiki rots, because it *is* a wiki — just one with
an unusually diligent reader.

And there was a fourth problem, quieter and more structural: the skill was still
**advice**. The most carefully written release skill in the world could not stop an agent
from touching a file the release process should never touch. Instructions shape behavior;
they do not bound it. Every guarantee in the prompt-folder era was, at bottom, a
politeness.

## Era III — The skill becomes knowledge a machine can select (2025–2026)

The next shift came from an unexpected direction: not better prompts, but better
*addressing*.

As the [Knowledge Context Protocol](../../topics/knowledge-context-protocol.md) grew from
a table of contents into a full protocol, skills started being described the way any
knowledge unit is described — with an `intent` (the question this answers), `triggers`,
a content hash, a validation date, and eventually an Ed25519 signature:

```yaml
- id: release-and-tag
  path: .claude/skills/release-and-tag.yaml
  intent: "How do I cut a release safely?"
  scope: project
  audience: [agent, operator]
  triggers: [cut-a-release, release-and-tag]
  content_hash:
    algorithm: sha256
    value: "b2c6fe39c32a37f6d603dd0faa..."
```

Three things changed at once, and each fixed an Era-II disease.

**Selection became deterministic.** Instead of hoping the model notices the right skill,
a planner — [kcp-agent](https://github.com/Cantara/kcp-agent), no LLM in the loop —
matches the task against intents and triggers and produces an inspectable plan: *this*
skill, for *this* reason, at *this* score. The silent-skill problem became measurable:
if a skill is never selected, the planner's logs tell you, and you can ask why.

**Freshness became checkable.** A hash-pinned, date-stamped skill can be *verified*
against reality instead of trusted. Staleness stopped being a vibe and became a signal.

**The skill became portable.** A skill described in protocol terms isn't a Claude Code
skill or a Pi skill; it's a unit any KCP-aware harness can consume. The asset escaped
its original container — which matters enormously for what comes next, because charters
are only worth writing if more than one court will honor them.

But even here — described, hashed, signed, selectable — the skill remained advice.
Sharper, fresher, better-routed advice. The gap between *what the skill says* and *what
the agent may do* had not moved an inch since 2023.

## Era IV — The skill becomes a charter (2026)

This year, the gap finally closed. KCP v0.26 §4.3a gave the skill unit one new block,
and the block changed what a skill *is*:

```yaml
- id: release-and-tag
  path: .claude/skills/release-and-tag.yaml
  kind: skill
  intent: "How do I cut a release safely?"
  audience: [agent, operator]
  triggers: [cut-a-release, release-and-tag]
  action_scope:
    tools: [read, bash, git]
    paths: ["pom.xml", "CHANGELOG.md"]
    capabilities: [release]
```

`action_scope` is the envelope: the tools this procedure may invoke, the paths it may
touch, the named capabilities it exercises. And crucially, it is not documentation — it
is **enforced**. In a [Pi session running pi-kcp](https://github.com/Cantara/pi-kcp), a
native tool call that reaches outside the active skill's envelope is *blocked*, by the
same deterministic decision function the kcp-harness compliance proxy uses, with the
specific reason (which tool, which path, which capability) written into the turn's
receipt. Every governed turn carries one correlation id, so you can reconstruct
afterwards exactly why the agent read what it read and did what it did.

Look at what quietly happened to the separation of powers. Four distinct authorities now
touch one skill, and no two of them live in the same place:

1. **Declaration** — the manifest states the envelope.
2. **Selection** — the planner decides whether the skill is even offered. Fail-closed:
   here is a real planner deciding about a real generated skill this morning —

    ```text
    ○ 1. release-and-tag (score 9)  .claude/skills/release-and-tag.yaml
         How do I cut a release safely?
         why: intent matches; triggers match;
              kind: skill not invoke-eligible: no explicit eligibility grant
         not load-eligible
    ```

    Selected on merit. **Inert by default.** The spec's own words for this default are
    the whole era in miniature: a skill *fails closed* — absent an explicit grant it
    renders as a pointer, never as an action.

3. **Enactment** — the harness enforces the envelope at tool-call time.
4. **Grant** — a human, and only a human, flips eligibility.

No model holds any of these four powers. The model proposes; a deterministic stack
disposes. This is the same argument the
[Defendable Agents](../../topics/defendable-agents/index.md) work makes for knowledge and
for spending, now landed on *procedure*: the question "what is this agent allowed to do?"
finally has an answer you can print, diff, review, sign, and revoke.

That is a charter. Not a metaphorical one — the actual instrument: **a scoped, reviewed,
revocable grant of authority, from a principal to an agent, with an audit trail.**
Organizations have run on these for centuries. They just never had one that a machine
could both read and enforce.

## Era V — The charter writes itself, from evidence (this week)

One problem remained, and it was the same problem the prompt-folder era had: hand-written
declarations rot. If humans must author every envelope by hand, envelopes will be stale,
generous, or absent — and a generous envelope is barely better than no envelope.

So the newest move is generation from evidence.
[Synthesis](https://github.com/exoreaction/Synthesis) — which already indexes the repo,
holds its code graph, and runs its security analysis — now reads a repo's existing skills
and *infers* the envelope (`synthesis kcp skills`): tools from what the playbook
demonstrably invokes (a shell fence earns `bash`, a `git tag` earns `git`); paths only
where the playbook names files that actually exist in the repo; capabilities never
invented at all. No evidence, no entry. The output must pass the shared governed-skill
linter from [kcp-skill](https://github.com/Cantara/kcp-skill) — conventions, lint rules,
and conformance vectors that both the generator's CI and the enforcing harness's test
suite now run as executable contracts:

```text
$ synthesis kcp skills --write
Governed skills: 1 unit(s) from .claude/skills
  - release-and-tag  (.claude/skills/release-and-tag.yaml)
  [OK] governed-skills block written to knowledge.yaml  (kcp_version: 0.26)

$ npx kcp-skill-lint knowledge.yaml
info  SK007  release-and-tag  capabilities empty/omitted — fail-closed default
0 error(s), 0 warning(s), 1 info
```

The compounding loop this closes is, I think, the actual headline. Watch the shape of it:
work happens → sessions leave receipts and episodic memory → recurring workflows get
captured as skills → envelopes are inferred from the evidence → linted, signed, granted →
enactment produces more receipts → receipts are *observed scope*, which can confirm or
tighten the declared scope. Every cycle, the organization's **safely delegable surface**
grows a little — not because the models got smarter, but because the governance artifacts
are generated and verified by the same infrastructure doing the work.

That is what I mean when I say skills are now **intra-org charters**. Onboarding an agent
to a team stops being "paste our conventions into its context" and becomes "grant it
these six skills, scoped to these paths" — the same instrument you'd use for a new hire's
access, with a better paper trail. Security reviews envelopes without reading playbooks.
Authors write playbooks without holding security context. Operations grants and revokes
without touching either. One artifact; three jobs; separately auditable. Teams compound
because captured procedure compounds. *Organizations* compound because **delegable,
governed procedure** compounds — and can even cross org boundaries, since a signed skill
with a trust tier is something another company's harness can verify before honoring.

## What history has not written yet

An honest history names its open chapters, and there are three.

**Enforcement is only as strong as the harness.** `action_scope` is advisory at the
parser level; today pi-kcp and kcp-harness enforce it, and other harnesses simply don't
yet. A charter honored by one court is a start, not a settlement.

**Declared scope needs verification against observed scope.** Today we verify that
envelopes are well-formed and evidence-based at generation time. The stronger loop —
comparing what a skill *declared* against what its enactments *actually touched*, receipt
by receipt, and flagging the drift — is designed but not built. It is the skills
counterpart of verifying knowledge declarations against the codebase, and it turns the
audit trail from a record into a feedback controller.

**Nobody has defined scope composition.** What happens when a governed skill's playbook
invokes another governed skill? Intersection of envelopes? Escalation with approval?
This is the agentic version of privilege escalation, and it will decide whether
*compound skills* — procedures built from procedures — inherit the safety of their parts
or quietly defeat it. It is, in my view, the most consequential open design question in
the stack.

## The arc, in one line

**2023: the skill was a secret. 2025: the skill was an asset. 2026: the skill is a
charter.** Advice became property became authority — and authority, unlike advice, is
something you can delegate, audit, revoke, and build an organization on.

The next time someone tells you agentic development is about better prompts, ask them
who signs their prompts, who granted them, and what happens when one reaches for a file
it never declared. The teams that can answer are not prompting. They're chartering.

---

*The release-skill outputs above are real artifacts from this morning's toolchain runs —
generated, linted, planned, and refused-by-default exactly as shown. Measured, not
remembered.*
