---
description: "What an agentic engineering team on Sunstone Atlas is made of, part by part, each tagged by how built it is: identity, signed channels, co-workers, review, human gates, workflows. Including what does not exist yet. The first of two posts; the second is the experiment where we used all of it on ourselves."
date: 2026-10-01T09:00:00
slug: agentic-engineering-teams-on-sunstone-atlas
series: "Sunstone Atlas"
draft: false
categories:
  - AI Agents
  - Engineering
  - Governance, Trust & Compliance
tags:
  - sunstone-atlas
  - agentic
  - governance
  - agent-teams
  - haah
  - hitl
  - explainer
authors:
  - totto
  - fable
  - claude
image: assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d6-five-role-loop.webp
---


# Agentic Engineering Teams on Sunstone Atlas: What They Are Made Of

*Thor Henning Hetland (Totto) & ExoCortex, our agentic rig of Claude and Fable. Drafted by Claude Fable 5.1. Oslo, October 2026.*

---

## TL;DR, and the business summary

**What this is.** We are sharing our newest features, not selling them; nothing about the agent team below is runnable by an outsider today (see [section 12](#12-where-you-can-see-it)). Sunstone Atlas is our governed substrate for organisations that run humans and AI agents side by side: every participant a principal with its own credential, every conversation a signed append-only channel, every human decision a record signed by the instance and attributed to the authenticated principal. On it we run what the repository calls an agent team (`ops/agent-team`) and this post calls an agentic engineering team: a group of AI roles that works on code under rules about who may touch what. Ours has a fixer that may touch code, two reviewers that may only read a diff, an orchestrator that decides, and a judge that stands in for sign-off.

<!-- more -->

**What exists.** A Node prototype, the README's own word. On main: signed channels and ledgers, per-principal tokens, a governed co-worker daemon with a default tool deny, team provisioning, and `team.review`, one review round that ends in a decision line. Most of it is **[Built]**; the daemons are **[Proven in our pilots]** on one box, with one operator.

**What does not exist.** No configuration UI, installer or release channel for the agent-team code. No Slack, email, SMS or mobile delivery, and no channel view in the browser. No engineering playbook, and no git, pull request, CI or merge integration. No `team.build` on main: the multi-round build loop is a specification that ran once, through an experiment's driver, on a branch.

**The honest maturity picture.** Every part carries one of four tags, and where something exists only on a branch, or ran once outside main, it keeps the lower tag. Ordinary human approvals are signed by the server, not by the person's own key; the run ledgers are not externally anchored; the evidence is n = 1 to n = 12, on one codebase.

**For an executive.** This post is a map of parts and their maturity, not a result. Read the maturity table in [section 10](#10-the-maturity-table) and the list of gaps in [section 11](#11-what-we-do-not-have-yet). The second post, due shortly after this one, is the dogfooding experiment: on 1 October 2026 we used this team on its own orchestrator. That run did not finish, and it is n = 1.

---

**Maturity legend, used on every part below.** **[Built]**: on the main branch, with tests. **[Proven in our pilots]**: we ran it live at least once and there is a record we can point at. **[Designed, not built yet]**: a documented design, a specification, an RFC or a stated intention; no code on main does it. **[Not built]**: it does not exist at all and has no design either. Where something exists only on a branch, or ran once outside main, it keeps the lower tag and the sentence says so. Where a Built part has a known gap, the gap is in the same paragraph. No tag is higher than our own research notes support.

## 1. Why "governed", and the two things that are easy to confuse

Sunstone Atlas describes itself as "the governed knowledge/skill/playbook substrate and coordination fabric for the agent-augmented organization". The README is just as plain about what exists: the Java platform in the design document "is still design-phase"; what is built, tested and released is "the Node prototype the design is being proven through", three deployables called canvas, gateway and bridge. **[Built]**, and the word is the README's own: prototype. The repository is proprietary; only a small conformance kit is packaged for a third party to run. Release v1.69.0 was tagged on 29 September 2026. The agent-team code is on main under `ops/agent-team` and `ops/agent-team-pikcp`, but not in the tagged release artifacts; it deploys by hand to a box. **[Built]** as source, not as a release channel.

"Governed" here means four concrete things: every unit is published as a signed version that is never overwritten; every skill and playbook carries a deny list that is unioned, never narrowed; tool calls are checked against it at run time (since 28 September, see [section 3](#3-anatomy-of-one-role)); and the AI drafting engine has no code path that writes. **[Built]**

Now the two things a reader will want to merge. First, the Canvas playbook engine: a generic, signed, replayable runner for gated procedures, with 61 worked examples, none of them a software-engineering workflow. **[Built]**; the examples **[Proven in our pilots]** by the repository's own account. Second, the agent team: standing daemons talking over group channels, not a playbook, and not replayable the way playbook runs are. **[Built]**, **[Proven in our pilots]** on one box. "Engineering workflow on Atlas" below means the second thing; [section 8](#8-workflows-playbooks-daemon-loops-and-teambuild) says where the first one stops.

| | Playbook engine | Agent-team daemons |
|---|---|---|
| What it is | A signed, versioned procedure with ordered steps and gates | Five long-running processes polling group channels |
| Who signs | Canvas signs every run event; gateway and bridge co-sign theirs | Canvas signs the channel events; a daemon's result is a message body |
| Replay | `GET /api/runs/:runId/verify`, and an offline verifier | Reconstructable from the channel; not replayable as a run |
| Engineering use today | No example exists | The run in the second post |

## 2. The substrate: identity, channels, ledgers

**Principals.** Nine roles: admin, author, publisher, reviewer, bridge, reader, external, disposer and persona. Proposing and publishing are explicit allowlists, so the last five cannot author by construction. A token is 32 random bytes; only its SHA-256 hash is stored, it is shown once, and comparison is timing-safe. An agent bound to a human with `actingForPrincipalId` sees the intersection of both principals' scope memberships, not the human's alone; inheriting channel and group membership through that binding exists behind a flag that is off by default. **[Built]**

**Channels and groups.** One signed, append-only ledger per conversation. A channel is open: anyone with a token can self-join and sees the full history. A group is membership-gated: only an existing member can add you, your window starts at your own `member-added` event, and there is no backfill and no redaction. A non-member's read is refused, not returned empty. Every event is Ed25519-signed by the instance key. Messages are capped at 10,000 characters, with up to 10 citations into run ledgers. The shared root token is refused by name. Membership is never an authority source: being in the room does not let you resolve a gate. Humans and agents use the same six MCP tools: `create_channel`, `join_channel`, `add_channel_member`, `post_channel_message`, `read_channel_messages`, `list_channels`. **[Built]**, 51 tests.

![One group ledger: three members added, a message posted, and a late joiner whose window starts at their own member-added line.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d1-ledger.webp)

*One group ledger: three members added, a message posted, and a late joiner whose window starts at their own member-added line.*

**Run ledgers.** One append-only JSONL file per run; every payload signed by Canvas before append; no update or delete on any ledger. **[Built]**, with a gap stated now and repeated in [section 9](#9-evidence-you-can-check-and-what-a-signature-does-not-prove): events are individually signed and linked by the receipts they cite, but the architecture document itself says the ledgers have "no externally anchored head and no monotonic counter". A signature proves the key signed these bytes, not that the host was honest or that this export is the latest. We do not say "tamper-proof".

## 3. Anatomy of one role

A co-worker is four things stacked. A principal. A standing daemon, `coworker-daemon.mjs`, that polls one group channel and runs each task in a real governed Pi coding-agent session, with a pi-kcp conformance checker and a signed per-turn ledger. **[Built]**, 143+ unit tests; **[Proven in our pilots]**, the record being the run in the second post. A fail-closed policy: the daemon refuses to start unless `.pi/kcp.json` sets `requireActiveSkill: true` and the manifest is readable; the opt-out, `GOVERNANCE_POLICY=none`, is echoed into every result as ungoverned, and the policy's hash travels in every result as `policyDigest`. **[Built]** And, in the pilot, a unix account: five accounts, home `0700`, env file `root:<role>` mode `0640`, the fixer the only one with a login shell. **[Proven in our pilots]**, pilot-grade: scripts a human runs, not an installer.

Two gates sit in front of the work: a dispatcher allowlist (only tasks from principals in `COWORKER_DISPATCHER_IDS` are acted on; an empty list refuses to start) and a channel-kind gate (the daemon exits if its channel is not a group). **[Built]**

Tools are denied by default: bash, edit, write, read, find, grep and ls. A tool is allowed only when the process runs with `COWORKER_ROLE=fixer` and the task itself has kind `fixer`; neither alone suffices, and `COWORKER_DENY_TOOLS` can only add. Reviewers, the judge and the orchestrator's decision turn therefore have no filesystem at all. **[Built]** The read, find, grep and ls half of that list was added on 29 September after a live finding: the judge had used its real `read` tool against its own deployed checkout, a different copy of the same repository, and reported the wrong-repo answer as independent verification; the reviewers ran with the same tools and the same checkout (PR #436). **[Proven in our pilots]**.

![Who can touch what: role and task kind against the seven denied tools, and the #413 before/after.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d2-who-can-touch-what.webp)

*Who can touch what: role and task kind against the seven denied tools, and the #413 before/after.*

**One fact the rest depends on.** Until 28 September, "governed" meant "observed". Both bridge files had constructed pi-kcp's `GovernedLoop` without a `checker`, and the loop's default is pass-through; every earlier governed turn was recorded and never enforced. PR #413 fixed it by building a real conformance checker in `createGovernedLoop`, verified live: a skill whose manifest denies bash and `secrets/**` got `approve: "blocked"` on the secret read, and the canary value was absent from the channel history. **[Built]**; the live denial **[Proven in our pilots]**, cited from the commit message because the second post does not cover it. Two footnotes. `deny.paths` is evaluated against a tool call's declared target, not filesystem traversal, so `ls .` from an allowed ancestor is not itself denied. And that live run left a defect open, a governance summary showing `turns: []` despite a real deny; we have not seen it fixed, so we do not claim it.

Secrets: the Canvas token and the dispatcher list are deleted from the environment before the Pi session starts, but the model API key is deliberately left, so a fixer with bash can read it with `env`; credential-shaped strings are redacted from evidence, best-effort. **[Built]**, residual risk named in the code's own comment.

The model is fixed in the code today, not selectable per role or team, and not printed here. Our intention is to support both frontier models and self-hosted "Norwegian soil" LLMs. **[Designed, not built yet]**

## 4. Configuring a team

A team is a small JSON file: `id`, `groupName`, and `positions[]`, each with a `principalName`, a free-text `label` and an optional real `role` (default `author`). A label equal to a real role is a hard validation error, so a position called "reviewer" cannot quietly inherit publish authority. `provisionTeam()` mints one principal per position with the deterministic id `team-<teamId>-<principalName>`, creates one closed group, and adds every member before anything is posted, because groups have no backfill. It runs behind a server-side lock with a two-minute TTL; a stale lock throws and a human removes it. Tokens come back once and are never persisted; there is no reset, and an orphaned id is burned. **[Built]**, 13 + 18 tests, its own CI job. A native team primitive in the Canvas server was proposed and rejected in review; provisioning stays human-run ops tooling (a decision, not a feature; no tag applies).

![From a team-spec file to five daemons: what provisioning creates and what the orchestrator creates on its own.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d3-provisioning-flow.webp)

*From a team-spec file to five daemons: what provisioning creates and what the orchestrator creates on its own.*
![Terminal: `node cli.mjs team-spec.json` on a disposable local Canvas, tokens redacted.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-provisioning-cli.webp)

*Terminal: `node cli.mjs team-spec.json` on a disposable local Canvas, tokens redacted.*

The orchestrator reads a roster, `{reviewers: {<lens>: {principalId, channelId}}}`. A lens is a key. Its text is one fixed template, "You are reviewing for <lens>. <task>", asking for a first line `VERDICT: approve|revise|reject` and findings tagged blocking or non-blocking. There is no per-lens rubric, prompt or skill binding. The orchestrator creates its own private group per lens, `orchestrator-<id>-reviewer-<lens>`, and audits that its membership is exactly the reviewer and itself before trusting an answer. **[Built]**

Configurable: repository name, policy files, dispatcher allowlist, extra denies, timings, evidence mode, lens names, roster size, the role per position. Fixed in code: model and provider, the default deny list, one task at a time, one review round, six dispatches per root request, the lens template.

By hand today, kept whole because it is the list most at risk of being forgotten: write the spec; hold an admin-role principal's token (the shared root token is refused); copy each one-time token to the right host; write the env files; install pi-kcp from a local checkout (it is not on a registry); author `.pi/kcp.json` and a manifest per working directory; create the OS users (scripts exist, human-run); write the roster; supervise the processes (no unit files on main); post the dispatching envelope by hand (no CLI or UI does it); apply any fixer diff. No configuration UI and no installer exist, and nothing designs them: **[Not built]**. The missing team primitive is a decision, not a gap: we decided not to build one.

## 5. How they talk

A protocol message is prose, then a sentinel line, `---pikcp-coworker/1---`, then one JSON object. Only a valid envelope of a known type is protocol; everything else is chat, silently ignored. Request types: `coworker.task`, `coworker.task-chunk`, `team.review`. Replies: `coworker.accepted` (posted when work starts, not when it is queued), `coworker.result`, `coworker.rejected`, `coworker.failed`, all tied by one `requestId`. A `coworker.task` carries a `requestId` of 8 to 64 characters starting with a letter, a `repo` that must equal the daemon's `--repo`, exactly one of `task` or `taskRef`, `expectEvidence` (`summary` or `full`), `timeoutSec` (default 1,800, maximum 7,200) and `kind` (`fixer`, or else review). Rejections carry one of eight enumerated reasons, from `bad-requestId` and `wrong-repo` to `bad-task-chunks` and `duplicate-requestId`; failures carry `post-processing-error` or `interrupted`. **[Built]**

A task over 10,000 characters goes out as a `taskRef {sha256, bytes, chunks}` header plus `coworker.task-chunk` messages; the receiver reassembles, caps the whole at 300,000 characters and 8,000 chunks, abandons it after ten minutes without a chunk, and verifies both the sha256 and the byte count before trusting the text. Assembly is in memory only. Work is strictly serial; state is an atomic file with a bounded dedupe ledger; every start runs an orphan sweep. The reader cursor is the server's `latestEventDigest`, a hash over the full signed envelope. **[Built]**, **[Proven in our pilots]** on one box. The byte count in that header is where the planted bug of the second post lives.

![The task lifecycle on the wire, and the chunked variant with the receiver's two checks.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d4-haah-sequence.webp)

*The task lifecycle on the wire, and the chunked variant with the receiver's two checks.*

Four things the live runs taught us about the protocol. The receiver splits on the last sentinel, so a task's own prose may mention it without breaking the parse. `accepted` fires at dequeue, which is what makes a crash visible: an `accepted` with no terminal reply is an orphan, and the restart sweep posts `failed` with reason `interrupted` for it. The dispatcher allowlist and channel membership are two gates in two layers, and a live dispatch failed on exactly that: a principal on the allowlist whom nobody had added to the room. And a locally computed event digest looks like a server cursor and is not one; a first real poll crashed on that. All of it was diagnosable because the whole conversation is ordinary events in a channel a human can read.

## 6. Review as a workflow: `team.review`, and what it has caught

`team.review {requestId, repo, task|taskRef, panel[], reviewerTimeoutSec, maxRounds}` is the one multi-agent workflow on main. The orchestrator sends one `coworker.task` per lens to a reviewer daemon, waits, then runs one governed decision turn whose first line is `DECISION: ship | ship-smaller | send-back`. An unknown lens is rejected; child ids are `<parent>-r-<lens>`; a missing reviewer is reported as MISSING with a reason (drifted, unauditable, timeout, rejected, failed). `maxRounds` is pinned to 1, so a send-back is terminal and never re-dispatched; at most six child dispatches per root, counted by the orchestrator's own state. The orchestrator on main has no path to dispatch a fixer or a judge; those are reached by a direct `coworker.task` from an allowlisted dispatcher. **[Built]**, 104 unit tests; **[Proven in our pilots]**.

![The five-role loop with every gate: fixer, two reviewers, orchestrator, judge, human.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d6-five-role-loop.webp)

*The five-role loop with every gate: fixer, two reviewers, orchestrator, judge, human.*

What it has caught, in the order an auditor should read it.

The trap-task experiment of 29 September, pre-registered and hash-pinned: 12 single-file tasks, 4 clean, 4 ambiguous, 4 with a wrong premise, through fixer, two-lens panel, orchestrator and a simulated-HITL judge. Headline: 1 of 8 traps approved; the null hypothesis (at least 4) rejected. Under the headline: 7 of 8 traps came back as empty diffs because the fixer refused the premise, so the panel saw one real diff, the softest call in the bank, and approved it. Its catch rate on that one diff is 0 of 1, and whether the approval was wrong is debatable. Three of four clean tasks shipped; one was sent back for lack of evidence. Orchestrator and judge disagreed on 3 of 12, all reasoned. Reviewer-versus-reviewer disagreement was not measurable; spend was not measured. The experiment ran with `GOVERNANCE_POLICY=none`, so it measured the chain's judgment, not tool enforcement. **[Proven in our pilots]**, n = 12, one codebase.

The 28 September runs, in "The Platform Said No, Even to Me": a three-lens panel found two holes in a worker's verification step, a scope lens found an overstatement (5 of 70, not "almost every"), a `decision_basis: "human"` gate raised a real escalation, and the shared root token was refused for sign-off. A fourth run, in "We Asked the Team to Design Its Own Upgrade": two blocking defects (a role collision granting publish authority, a false idempotency claim) and a bot-pair sign-off bypass; send-back; the worker reversed to the smaller version; merged the same day. **[Proven in our pilots]**, n = 1 each; the first of those two posts says no control run against a single generalist reviewer was made, and neither of them has one.

The second post adds the strongest single data point we have: at its fourth step, two reviewers found two real defects that 18 new tests had missed. It is one step. We do not add any of these into a rate.

## 7. Humans in the loop: two mechanisms, not one

**On Canvas.** A playbook step with `decision_basis: "human"` raises `escalation-raised`. If the step author wrote a free-text `decision_owner`, that string is recorded as `authorityRequired` and used to route the page; if not, it is null. Model, deterministic and tool steps that escalate land in the same pending list, `GET /api/escalations/pending`. To decide, a principal calls `POST /api/runs/:runId/steps/:stepId/resolve`: per-principal identity required, root token refused with 403, `resolvedBy` taken from the authenticated principal, never typed. The code restricts who may decide in exactly three ways: the principal who started the run cannot resolve its own step (self-review ban), the root token is refused, and the in-thread door also refuses `external` principals. That is all. `decision_owner` is routing text, not a permission, and nothing checks it when someone resolves. Nothing distinguishes a human from a bot at that point either: principals have an optional `presence` field (`human` or `bot`) that nothing reads yet (tracked in our issue #402, which is closed, with the field left as groundwork). In our local demo, any other non-root principal could approve; from the code, a bot principal that did not start the run probably could too, which we did not demonstrate. Treat the gate as separation of duties between two credentials, not as proof that a person decided. The result is a `human-approval` event signed by the instance key, which attests who authenticated; the human does not sign personally in the ordinary path. A write-classified tool step needs more, Proof B: a registered disposer key signs over the exact action hash with a single-use nonce. Each pending step has a dialogue thread; free text never approves, no code reads message content, and approving in-thread is a separate door that calls the same resolve function, with the same checks. The decision panel shows facts, a consequence line per disposition, and no preselected choice. **[Built]**

![Three refusals on a local instance: "approved" typed in the thread is accepted as a message and leaves the step pending; resolve with the root token returns 403](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-negative-probe.webp)

*Three refusals on a local instance: "approved" typed in the thread is accepted as a message and leaves the step pending; resolve with the root token returns 403; resolve as the run's starter is refused as self-review; a different principal can resolve it, because nothing says who the designated human is.*
![The decision panel for one pending human step, and the signed human-approval event it produces.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-decision-panel.webp)

*The decision panel for one pending human step, and the signed human-approval event it produces.*

![A worker posts approved in the dialogue thread, the step stays suspended, and the signed ledger shows no human-approval event](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-dialogue-thread.webp)

*The dialogue thread of the same step: a worker types "approved", the step stays suspended ("prerequisite human-approval did not complete"), and the page says the message decides nothing. Real screenshot from the local instance.*

**Getting the human there.** Canvas delivers nothing by itself. A principal can subscribe a channel to an https target it has proved control of; Canvas then POSTs a signed, pointer-only body (subscription id, count, latest digest; never text or author), swept every 10 s, retries held in memory and dropped on restart. Escalation paging posts a signed pointer at most once per recipient, one retry, no durable queue; the deep link carries no token. A run waiting on a person for more than 72 hours is marked stalled and pushed as a pointer. There is no built-in Slack, email, SMS or mobile sender; a receiver you run turns a pointer into a ping. There is no channel view in the browser; a human talks in a channel through an MCP client, the API, or the escalation thread. Passkey login exists, opt-in, and secures login, not each decision. Notifications and paging **[Built]** with those limits; Slack, email, SMS and mobile delivery, and a channel view in the browser, **[Not built]**.

![From a channel post to a human decision: what Canvas sends and what you have to run yourself.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d7-notification-flow.webp)

*From a channel post to a human decision: what Canvas sends and what you have to run yourself.*

**In the daemons.** Here HITL is three cheaper things: the dispatcher allowlist (a human decides who may task a daemon); a judge role that is a simulated human, grounded in past documented verdicts and marked `simulated: true`; and, in the second post's driver, exit codes 10, 11, 12 and 20 plus a human launching the next step. The driver has no notifier of any kind, and the Canvas gate with its signed `human-approval` event was not on the second post's path. **[Proven in our pilots]** for the mechanism; **[Designed, not built yet]** for a notifier in the driver (the intention is in section 8 of the second post).

The public framing is "The Loop Is Not a Switch" (17 September): a charter's `control.mode` goes block, then review-after or sample, then monitor, relaxed only by a separate signed graduation ledger and never to `none` automatically. **[Built]** The personal-edition PR-merge gate has been live since 16 September; one real run stalled on it and forced a redesign. **[Proven in our pilots]**, single user.

## 8. Workflows: playbooks, daemon loops, and `team.build`

Can you define a build-review-merge workflow in Atlas? Three parts.

The playbook engine can express it. A playbook is a signed, published unit with ordered steps, run pinned by version id, with five step forms: judgment (via the gateway, behind a confidence gate), deterministic (Function predicates: data, not code, replayable byte for byte), human (a gate), tool call (http or process through the bridge, pending until a signed bridge receipt arrives), and invokes (a sub-playbook). Chaining only proposes a successor. Enforced: the deny union, the authority ceiling, clearance, the escalation pause, write proofs, signatures. Advisory metadata: autonomy mode ("documented commitment, not substrate-enforced", in the schema's words), criticality, reversibility, performer. The engine governs the decision; it does not perform the action, and a real run stalled on exactly that. **[Built]**, about 220 enactment tests; the 61 examples **[Proven in our pilots]**.

No engineering playbook exists. The closest of the 61 is an IT-operations one: a deterministic freeze-window gate, then a human SRE review of a PR diff summary, with `apply-k8s-config` and `k8s/prod/**` denied. Nothing in Canvas touches git, a pull request, CI or a merge; the only edges out are tool calls over http or process. **[Not built]** A process tool can run a pi-kcp agent, live-tested in a repository test, cost not capped by Canvas. **[Designed, not built yet]** for the engineering playbook itself.

The loop that has actually run is a daemon protocol plus a driver. `team.review` is one round. `team.build`, the two-round fixer, panel, decision, judge, finalise loop, is a specification under `docs/experiments/scale-build-c1`; the orchestrator on main has no `team.build` handler. Around it the experiment's driver adds sha256 pins, bounds (28 chain runs, 2 rounds per step, 1 replan, 24 hours of machine time, a $150 soft stop on a cost proxy), a diff allowlist, a test-weakening detector, a canary seed, eight held-out tests and human gates. It ran once, on 1 October: five steps accepted on a branch, stopped at step six, nothing merged. **[Designed, not built yet]** on main, with a qualifier: in the experiment, five of its seven steps were built as commits on an unmerged branch, and step six was never produced. The run is the second post, and its artifacts will move to a stable place later. Delegation chains in Canvas stop at depth 1. An earlier recursive-bugfix experiment converged in two hops inside a workflow script, 220 of 220 tests, one hop's log backfilled and excluded from calibration. **[Proven in our pilots]**, n = 1.

![The experiment's driver around the team: phases, human gates and the bounds card.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d10-build-phase-machine.webp)

*The experiment's driver around the team: phases, human gates and the bounds card.*

## 9. Evidence you can check, and what a signature does not prove

`GET /api/runs/:runId/verify` re-derives deterministic decisions, citations and upstream receipts from the recorded facts. A judgment's inputs are checkable; its output is not: the verifier says "this decision was made on exactly these facts", never "this decision was correct". `canvas/scripts/verify-offline.mjs` runs the same code with no server and no private key against a committed synthetic fixture; change one recorded fact and the replay no longer matches the recorded result, so the step is reported invalid and the command exits 1. Judgment decisions carry two signatures, the gateway's receipt inside the Canvas-signed event. **[Built]**

![verify-offline on the committed fixture: every decision and citation re-derived, signatures valid.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-verify-offline-ok.webp)

*verify-offline on the committed fixture: every decision and citation re-derived, signatures valid.*
![The same command after one recorded fact is edited: the replay no longer matches the recorded result and the verifier reports the step invalid (exit 1).](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/demo-verify-offline-tamper.webp)

*The same command after one recorded fact is edited: the replay no longer matches the recorded result and the verifier reports the step invalid (exit 1).*
![What a signature proves, and what it does not.](/assets/images/blog/agentic-engineering-teams-on-sunstone-atlas/d11-signature-proves.webp)

*What a signature proves, and what it does not.*

What it does not prove: freshness (no externally anchored head, no monotonic counter, so an old genuine export looks like the current one), host honesty, correctness of a judgment, and anything signed by a rotated-out key, since there is no key-rotation history. **[Built]**, with those gaps named.

One caution that matters for the second post: the daemon loops are not Canvas runs. Their signed evidence is the channel events; whatever the driver logs is append-only by convention, and root can rewrite it. In the second post only the channel events behind the `verbatim` records are Canvas-signed; the run log is the driver's own.

## 10. The maturity table

| Part | Tag | Evidence | Where |
|---|---|---|---|
| Principals and tokens (9 roles, hash-only storage) | Built | `canvas/src/principals.mjs` | Canvas |
| Group channels, signed ledgers, no backfill | Built | `channels.mjs`, 51 tests | Canvas |
| Run ledger, `verify`, offline verifier | Built, gaps named | `run-store.mjs`, `verify.mjs`, `verify-offline.mjs` | Canvas |
| Ledger anchoring, key-rotation history | Designed, not built yet | Architecture doc 17.5 names the gap | Nowhere yet |
| Co-worker daemon (governed session, fail-closed policy) | Built; Proven in our pilots | 143+ tests; second post | `ops/agent-team-pikcp` |
| Default tool deny (7 tools, two-factor unlock) | Built; Proven in our pilots | PR #436, after a live wrong-repo read | `ops/agent-team-pikcp` |
| Governance enforcement (real checker) | Built; Proven in our pilots since 28 Sep | PR #413 commit message, live deny | `lib/session.mjs` |
| Unix isolation (5 accounts, 0700 homes, 0640 env) | Proven in our pilots, pilot-grade | `PHASE2-USERS.md`, human-run scripts | `ops/agent-team-pikcp/infra` |
| Team provisioning (spec, lock, closed group) | Built | 13 + 18 tests, own CI job | `ops/agent-team` |
| Roster and lenses (names only, fixed template) | Built | `orchestrator-daemon.mjs` | `ops/agent-team-pikcp` |
| HAAH envelope, chunking, dedupe, orphan sweep | Built; Proven in our pilots | `lib/daemon-core.mjs`; second post | `ops/agent-team-pikcp` |
| `team.review` (one round, six dispatches per root) | Built; Proven in our pilots | 104 tests; 28 Sep posts; second post | `ops/agent-team-pikcp` |
| Review-chain discrimination | Proven in our pilots, n = 12; 0 of 1 on the one real diff (debatable) | `docs/experiments/trap-task-discrimination` | Repo (private) |
| Canvas human gate, resolve, dialogue, decision panel | Built | `enact.mjs`, `dialogue.mjs`, `decision-panel.js` | Canvas |
| Proof B (disposer-signed write approval) | Built | `dispositions.mjs`; conformance-kit vectors | Canvas |
| Channel notifications, escalation paging (webhooks) | Built, in-memory retries | `channel-notify.mjs` (41 tests), `paging.mjs` | Canvas |
| Slack, email, SMS or mobile delivery | Not built | None in the repo | Outside the repo |
| Channel view in the browser | Not built | None in `canvas/ui` | Nowhere yet |
| Configuration UI, installer, release channel for the agent-team code | Not built | None in the repo | Nowhere yet |
| Daemon-level HITL (exit codes, launcher scripts) | Proven in our pilots | Second post | `docs/experiments/scale-build-c1` |
| Playbook engine (five step forms, signed runs) | Built; 61 examples Proven in our pilots | about 220 enact tests; `docs/examples` | Canvas |
| Software-engineering playbook | Designed, not built yet | Closest: IT-ops freeze-window gate | Not authored |
| git, PR, CI or merge integration | Not built | Only http/process tool calls | Nowhere yet |
| `team.build` (two-round build loop) | Designed, not built yet; 5 of 7 steps built on an unmerged branch in the experiment, ran once via the driver | `docs/experiments/scale-build-c1`; second post | A branch |
| Delegation beyond depth 1 | Designed, not built yet | Delegation-chains RFC | Nowhere yet |
| Model choice per role; Norwegian-soil LLMs | Designed, not built yet | Stated intention | Nowhere yet |

## 11. What we do not have yet

**Product surface.** No public repository, hosted trial or self-serve signup. No UI to configure agents, roles, lenses or policies; configuration is JSON, env files and unix users. No installer, no systemd units on main; pi-kcp is a local checkout, not a registry package. No release channel for the agent-team code.

**Workflow.** No `team.build` on main. The orchestrator cannot dispatch a fixer or a judge. `team.review` is one round. No engineering playbook. No git, PR, CI or merge integration. Delegation stops at depth 1.

**Humans.** No Slack, email, SMS or mobile sender. No channel view in the browser. Ordinary approvals are signed by the server, not by the human's own key. Who may approve is limited only by a self-review ban and root and external refusals: no check on `decision_owner` at resolve, no human-versus-bot check. Notification retries live in memory. The judge is a simulated human. The experiment driver has no notifier.

**Agent runtime.** Model and provider fixed in code; the Norwegian-soil option is an intention. Lenses are names only. Daemons are serial and single-channel; no queue visibility, no horizontal scaling. No spend cap enforced in the repository. A fixer with bash can read the model API key. Redaction is best-effort. `deny.paths` is not traversal-aware. An orphaned principal id cannot be reissued.

**Evidence.** n = 1 to n = 12, one codebase, one box, one operator. No cost, latency or throughput measured for `team.review`. No control run. Run ledgers are not externally anchored; the daemon run log is not a signed Canvas ledger. The architecture document is at release 1.35.0 and says seven roles where the code has nine; the passkey design note says "not built" where code exists.

**Platform.** A Node prototype; the Java platform is design-phase. Flat files, no database, no replication, one instance per tenant. OAuth role inheritance uncapped; no dynamic client registration; no refresh tokens. ACL scopes not enforced on indirect read paths.

## 12. Where you can see it

We are sharing, not selling. Nothing about the agent team in this post is runnable by an outsider today: the repository is private, there is no trial, the agent-team code deploys by hand, and the offline verifier and conformance kit run only from a checkout. What is public is the writing on wiki.totto.org: "How to Build Agentic Software on Sunstone Atlas" (13 August), "Trust is earned, not asserted: introducing Sunstone Atlas" (24 August), "The Loop Is Not a Switch" (17 September), "We Already Run Jev. We Just Never Checked." (18 September), and "The Platform Said No, Even to Me" and "We Asked the Team to Design Its Own Upgrade" (28 September). With repository access, the experiments under `docs/experiments`, the 61 examples and the offline verifier are readable; the verifier runs on its committed fixture with no server. We are not offering access in this post. The demo images come from a disposable local instance; the text stands without them.


---

**Next: what happened when we used all of this on ourselves.** On 1 October 2026 we pointed the team at its own orchestrator. We gave it a pinned 45 KB specification for the multi-round build loop it lacks, and planted a bug in the deployed orchestrator where 318 tests could not see it. The bug had an approved fix 4 minutes 22 seconds after it was detected; the run built five of seven steps on a branch and then stopped itself on a contradiction in our own specification. Nothing was merged, and it is n = 1. The second post, "We Hid a Bug in Our Own Platform", tells it in full and follows shortly.
