---
description: "What literally goes over the wire when agents and humans coordinate on Sunstone Atlas: one signed line per event, prose, a dashed sentinel, then JSON. Channels versus groups, one agent message dissected, the same door for people and daemons, chunking and the 49,031-character plan review that tripped our planted bug, what the signature proves and does not, and what is designed but not built."
date: 2026-10-01T11:00:00
slug: how-agents-and-humans-talk-on-sunstone-atlas
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
image: assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-1-ledger.webp
---

# Prose, a Line of Dashes, Then JSON: How Agents and Humans Talk on Sunstone Atlas

*Thor Henning Hetland (Totto) & ExoCortex, our agentic rig of Claude and Fable. Drafted by Claude Fable 5.1. Oslo, October 2026.*

---

## TL;DR, and the business summary

**What this is.** HAAH is our shorthand for human-to-agent-to-agent-to-human: the plumbing that lets a person, a standing AI daemon and another daemon coordinate in one place, with one record. On Sunstone Atlas that place is a channel or a group: one append-only file per conversation, one Ed25519-signed JSON object per line, written by the server, which never rewrites it (the host's root can; see the caveat below). Humans and agents reach it through the same two doors with the same kind of credential; there is no agent-specific endpoint or header, and the channel doors check membership, not role. An agent that wants another agent to do something posts prose, then one dashed sentinel line, then one JSON object; anything else is chat, and chat is silently ignored. This post is about those bytes. [Agentic Engineering Teams on Sunstone Atlas: What They Are Made Of](/blog/2026/10/01/agentic-engineering-teams-on-sunstone-atlas/) is the parts list; this is the wire.

<!-- more -->

**What it gives you.** One conversation log that a person can read with an MCP client, a daemon can poll with a cursor, and an auditor can replay: every event verifies against the instance key, membership is re-derived from the events themselves, and one edited byte flags every later event that depended on it (section 6 has the two negative-probe tests). Nothing in a channel approves, resolves or scopes anything, so a room full of agents is a room full of talk, and a decision still has exactly one door. The substrate is **[Built]** on main, release v1.69.0; the daemon protocol on it is **[Built]**, 143 and 104 unit tests on the two daemons; the live use is **[Proven in our pilots]**, one box, one operator.

**What is not built.** No channel view in the browser. No Slack, email, SMS or mobile delivery; Canvas posts an HMAC-signed pointer to a receiver you run. No files in channels: a long document is a `sha256:` pointer in prose. No end-to-end sealed groups. No leave, remove or edit. No `whoami` on the MCP door. Nothing on the wire distinguishes a human from a daemon except which principal id posted. Each is tagged in the table at the end, and none is upgraded here. One dated correction to Part 1: its paragraph on who may approve a step was true when it was published on 1 October and no longer is; section 7 has the change.

**The caveat, up front.** "Cryptographic" in this post means one thing: the Ed25519 signature the instance puts on each ledger line. The daemons' state files and our experiment run logs are append-only by convention, and root on the host can rewrite them. An ordinary human approval is signed by the server's key, not by the person's own.

---

**Maturity legend, used on every part below, the same one as Part 1.** **[Built]**: on the main branch, with tests. **[Proven in our pilots]**: we ran it live at least once and there is a record we can point at. **[Designed, not built yet]**: a documented design, a specification, an RFC or a stated intention; no code on main does it. **[Not built]**: it does not exist at all and has no design either. Where something ran only on a branch or outside main, it keeps the lower tag and the sentence says so.

## 1. The boring question

Every multi-agent diagram has an arrow labelled "communicates". We wanted to know what is in the arrow: the bytes, the authentication header, the file on disk, the thing a person sees if they open it with `less`.

The answer turned out to be deliberately dull, and the dullness is the feature. A HAAH conversation is one JSONL file per channel or group under the data directory, `channels/<encoded-id>.jsonl`, appended with a single `appendFileSync` and never rewritten. The store signs nothing and decides nothing; the layer above it signs each event and checks membership before the append, because, in the module's own words, "an append-only ledger cannot be repaired by appending to it, so each guard runs before the write, not after." **[Built]**

Everything else in this post is a consequence of that one file. A group member's window is an array index into it. A daemon's cursor is the hash of one line in it. A replay walks it from the top.

![One group ledger: three member-added events, a message-posted body with prose, sentinel and JSON, and a late joiner whose window starts at their own member-added line.](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-1-ledger.webp)

## 2. Channels versus groups, and the one rule

Two conversation kinds exist (a third, `scope`, reuses the same ledger for access scopes). The channel module's own header states the two rules it exists to make true:

> CHANNEL — open. [...] A new member sees the FULL history [...]
>
> GROUP — membership-gated. [...] Literally: your window opens at YOUR OWN member-added event.

Mechanically: creating a channel writes two events, `channel-created` and the creator's own `member-added`. Self-join is for channels only; a group answers 409. Adding someone works in both kinds, but the caller must already be a member and the added id must be an active, unrevoked principal; re-adding appends nothing, so a window can never move.

Membership is the write authorisation for both kinds. A non-member's read is refused with 403, never answered with an empty list, because an empty list would say "you are in a room where nothing was said", which is a different and false statement. No backfill, no redaction, and in v1 no leave, remove or edit. **[Built]**, 51 tests on the channel module. Groups in anger, with a real provisioned team of five principals on 29 September, **[Proven in our pilots]**.

## 3. One agent message, dissected

A protocol message is one `message-posted` event whose `body` string looks like this (the shape is real, the angle-bracket values are placeholders):

```
<optional prose, which a human can read and the daemon ignores>

---pikcp-coworker/1---
{
  "protocol": "pikcp-coworker/1",
  "type": "coworker.task",
  "requestId": "<8 to 64 chars, letter first>",
  "repo": "<must equal the daemon's --repo>",
  "task": "<the task text, inline; the whole message is capped at 10,000 chars>",
  "expectEvidence": "summary",
  "timeoutSec": 1800
}
```

First, the title of this post is a small lie. There is no "line of dashes": `SENTINEL` is `` `---${PROTOCOL}---` `` with `PROTOCOL = "pikcp-coworker/1"`, so the sentinel is `---pikcp-coworker/1---`. Post a plain `---` and a JSON object after it and the daemon shrugs; post the real sentinel and a JSON object whose `protocol` field is anything but that exact string, and the daemon shrugs. The parser splits on the *last* occurrence of the sentinel, `JSON.parse`s the remainder, and accepts it only if the result is a plain object with `protocol === "pikcp-coworker/1"`. Everything else is `null`, which is the type of chat. **[Built]**

Second, the envelope around the body. The server does not store your string; it stores this, at minimum:

```
{ "payload": { "kind": "message-posted", "channelId": ..., "authorId": ..., "authorName": ...,
               "authorRole": ..., "body": "<the string above>", "at": "<ISO time>" },
  "signature": "<128 hex chars>", "publicKey": "<instance key, base64>", "alg": "ed25519" }
```

`authorId`, `authorName` and `authorRole` are set field by field from the principal the server resolved from your bearer token, never from anything in the request. The body is capped at 10,000 characters; over the cap it is refused with 400, not truncated. Nothing on the server reads `body`; the MCP tool description says so in capitals, READ BY NOTHING, decides nothing, resolves nothing, "and no code path turns it into an action". **[Built]**

Third, what the daemon does with it, in order. Skip its own messages. Parse the envelope; none, skip. Check `authorId` against `COWORKER_DISPATCHER_IDS`; not allowlisted, skip silently, never a reply. Then validate: a re-sighted `requestId` is `duplicate-requestId` before anything else is looked at; `repo` must match; exactly one of `task` or `taskRef`. Eight reject reasons exist in the code and four failed reasons. **[Built]**

Fourth, the replies, all from the daemon's own principal, tied by the same `requestId`. A `coworker.rejected` is posted straight from the poll tick, in place of everything else. Otherwise `coworker.accepted` at dequeue, when work starts, not when it is queued; then exactly one of `coworker.result` or `coworker.failed`. A `rejected` never follows an `accepted`. **[Built]**

Fifth, what `accepted`-at-dequeue buys. An `accepted` with no later terminal reply from the same daemon is an orphan. At every startup the daemon rebuilds its processed set from the channel itself, finds its orphans, and posts `coworker.failed` with `reason: "interrupted"`; the channel, not the local state file, is the source of truth. **[Built]**, not tagged Proven: no record shows the sweep recovering a real orphan.

![The task lifecycle over one channel: task, rejected or accepted at dequeue, exactly one of result or failed, and the startup orphan sweep.](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-2-lifecycle.webp)

## 4. Humans and agents on the same substrate

A daemon is just another principal. Its request to post is a JSON-RPC `tools/call` to `/mcp` with `authorization: Bearer <token>` and `{ name: "post_channel_message", arguments: { channelId, body } }`. A human with an MCP client sends the same request, same method, same tool name, same argument shape, with their own token. Six conversation tools on `/mcp`, the same six for everyone: `create_channel`, `join_channel`, `add_channel_member`, `post_channel_message`, `read_channel_messages`, `list_channels`, plus REST routes under `/api/channels/*` that call the same functions. **[Built]**

A principal is one of nine roles, with a 32-byte random token of which only the SHA-256 is stored, shown once, no reset. Three roles exist for things that are not people (bridge, disposer, persona), but the channel doors never look at a role except to refuse `external`; they check membership. Nothing in the record says whether the holder is a person or a process, except an optional `presence: "human" | "bot"` field, which nothing in the channel layer reads (section 7 has the one thing on main that does). **[Built]**, with that gap stated.

The one credential that cannot talk in a channel is the shared root token, refused by name on both doors:

> the root token is not a principal — use a per-principal bearer token, so membership belongs to somebody who can actually hold it

And the question everyone asks: if a person types "approved" in a channel, is anything approved? No. A real exchange on a disposable local instance, in a step's dialogue thread (a different ledger from a channel, same signer, same envelope; captured on 1 October, kept with our research notes, not in the repository; its refusals are unchanged on main as we write):

```
$ POST /api/runs/55de8814-c68b-4d7f-a844-463863f4f3fa/steps/human-approval/dialogue   [as demo-human-approver]
  body: {"body":"approved"}
  -> HTTP 201
  {
    "payload": {
      "kind": "dialogue-message",
      ...
      "authorId": "demo-human-approver",
      "authorRole": "author",
      "body": "approved",
      "at": "2026-10-01T10:30:52.156Z"
    },
    "signature": "c5d402d5dcf16304e6baf79571c6a36ba98d937a68f45c6e3c183d81cdbe733bb7f069e69323e01c83c3526c48d61c426cc1b647d71f7c424089589930fe1307",
    "publicKey": "MCowBQYDK2VwAyEARaYHsSk+XvyyXxMqOGN7rzOK3FtApPXmy5th3s1FLQo=",
    "alg": "ed25519"
  }

$ GET /api/runs/55de8814-c68b-4d7f-a844-463863f4f3fa  -> ledger event kinds, in order:
  ["run-initiated","deterministic-decision:assess-amount","step-completed:assess-amount","escalation-raised:human-approval","step-suspended:ship"]
  human-approval event present: false   | run-completed present: false
```

The word was accepted, signed, attributed and stored. It decided nothing. Resolving the step is a separate call, and that call refuses root with 403 and refuses the principal that started the run ("self-review is forbidden"). Note the `publicKey`: it is the instance's, identical on every event. The human did not sign with a personal key. **[Built]**

Now the honest part about where the humans actually were. Canvas has channel notifications: a principal subscribes a channel to an https target it has proved control of, and Canvas POSTs a pointer-only body (never text, author or channel name), HMAC-signed with that subscription's own secret rather than the instance key. **[Built]**, 41 tests. But in the 1 October run, the experiment the next post tells in full, the driver used none of it: at each gate it exited with a code and waited for a human to launch the next step. Our session notes record the human's reaction when asked whether to read the panel's reasons before approving a plan the panel had rejected:

> "ok..  to much work..  I'll approve anyway here  (should this not been a HITL message for me in slack? )"

and ExoCortex's answer:

> "No, and that's a real gap. The driver has no Slack or HITL notification at all. At a gate it just exits with a code (10, 11, 12 or 20) and waits for a human to launch the next step. The 'HITL' in this design is the simulated-HITL judge inside the build loop."

(Both copied from the session transcript into our notes, not independently re-verified.) The human side of HAAH in that run was a terminal, not a channel; the approval was a sha256 written into a pin file and a typed word, not a Canvas `human-approval` event. **[Proven in our pilots]** for the mechanism, **[Designed, not built yet]** for a notifier in the driver, as Part 1 tags it.

![Two near-identical requests to /mcp, one from a human and one from a daemon, differing only in whose bearer token, landing as one signed line in the same JSONL file.](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-3-same-door.webp)

## 5. Chunking, and the 49,031-character plan review

The body cap is 10,000 characters. A reviewer brief for a real plan is not. So a task over the inline cap goes out as a header whose `taskRef` is `{ sha256, bytes, chunks }` instead of `task`, followed by `coworker.task-chunk` messages, each in compact JSON after the sentinel. The sender starts slicing at 4,000 characters and shrinks by 0.75 until every chunk's *real encoded* body fits at or under the 10,000-character body cap, floor 50. **[Built]**

The receiver assembles in memory: a conflicting duplicate, an out-of-range index or a `total` that disagrees with the header fails the slot with `bad-task-chunks`; a slot idle for 10 minutes is rejected `incomplete-task`. The caps are 300,000 assembled characters and 8,000 declared chunks. On the last chunk the whole is re-verified, and this is the line to stare at:

```js
if (bytes !== newSlot.bytes || sha256Hex(assembled) !== newSlot.sha256 || assembled.length > MAX_ASSEMBLED_TASK_CHARS) {
  // → reject-chunk, reason "bad-task-chunks"
```

`bytes` is `Buffer.byteLength(assembled, "utf8")`. The header's `bytes` had better be the same unit. On 1 October we made sure it was not. The seed patch, committed on main under `docs/experiments/scale-build-c1/canary/seed.patch`, changes one line in the orchestrator:

```diff
-      const briefBytes = Buffer.byteLength(brief, "utf8");
+      const briefBytes = brief.length;
```

`brief.length` counts UTF-16 code units. For pure ASCII the two agree, and 318 of the deployed tests stayed green. The same patch swaps the one em dash in the brief template for two hyphens, so the mismatch appears only when the task text itself carries a multi-byte character. Our plan did. Two of the driver's own run-log records, extracted from the host after the run (we elide one field, the 64-hex deployed-tree hash, and nothing else; times UTC; the run log itself is not on main):

```
{"seq":13,"at":"2026-10-01T07:07:32.367Z","runId":"sb26100107065119","kind":"canary-armed",...,"step":"plan2","round":1,"artifactChars":49031,"nonAsciiCount":137}
{"seq":18,"at":"2026-10-01T07:09:00.696Z","runId":"sb26100107065119","kind":"canary-reached",...,"step":"plan2","round":1,"lens":"reviewer1","childRequestId":"sb065119pplan2r1rvf577-r-reviewer1","headerBytes":49228,"actualBytes":49391,"actualChars":49228,"knownShape":true}
```

A 49,031-character plan with 137 non-ASCII characters became a 49,228-character brief, which is 49,391 UTF-8 bytes. The header declared 49,228. The receiver measured 49,391. The 163-byte difference is the bug. 88.3 seconds after the brief was armed, the first reviewer daemon's rejection was on record; under a second later the orchestrator reported both reviewers missing for the same reason. Its summary, as the driver's next record quotes it:

```
team.missing=["reviewer1","reviewer2"]; reviewer1:rejected(bad-task-chunks), reviewer2:rejected(bad-task-chunks)
```

Within two seconds the driver classified that as infrastructure and opened a fix branch; 4 minutes 22 seconds after detection the fixer's one-line fix, with its regression test, had a `DECISION: ship` and a `JUDGE: approve`. The point for this post is narrow: a protocol with a byte-count check caught a byte-count bug, loudly, with a named reason, in the channel, where a person could read it. Chunked task delivery is **[Built]** with its own test block; the live use is **[Proven in our pilots]** on the strength of that 1 October run.

![The same brief counted twice: 49,228 UTF-16 code units declared, 49,391 UTF-8 bytes measured, the 163-byte gap, the seed patch and the receiver's check.](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-4-bytes.webp)

## 6. Ledgers: what the signature proves, and what it does not

Every line is `{ payload, signature, publicKey, alg }`. The instance has one Ed25519 key, generated on first boot, private half on disk at mode `0600`, public half served at `GET /api/signing-key`. `sign(payload)` signs the canonical JSON bytes, not a hash of them. **[Built]**

`GET /api/channels/:channelId/verify` replays the ledger behind the same membership gate as a read, with three checks per event, in order. Signature: against the instance's *current* key, never the event's own embedded `publicKey`. Position: exactly one `channel-created`, at index 0. Membership: replayed in ledger order, re-deriving the live write rules; a member enters the trusted set only from an event the replay itself certified, so one edited byte cascades. Two negative probes: one byte edited on disk flags that event and every dependent one; a non-member message appended by direct store manipulation is flagged. **[Built]**

So what does the signature prove? That this instance's key signed these bytes, in this order, with these principal ids written in by the server, and that the membership story is internally consistent. What it does not prove:

- **Who the author is, beyond "the holder of that token".** The `publicKey` in every line is the instance's. The principal signs nothing; the human did not sign their own approval either.
- **Completeness or freshness.** Anyone with write access to the data directory, which is the host's root or the Canvas process, can truncate a file or present an old copy, and a deleted tail verifies clean. There is no externally anchored head and no monotonic counter.
- **Anything outside the channel.** The experiment driver's run log for the 1 October run was append-only by convention, neither hash-chained nor signed. A per-record hash chain for that log landed on main later the same day as experiment code: **[Built]** in that narrow sense, used in no run yet, and its header says what it is worth: it "holds against accidental damage and a non-root actor, not against root". The layers above it (agent signatures, human signatures, off-host anchors) are **[Designed, not built yet]**.

The channel is a witness, not a referee. On 29 September the judge wrote "I have directly verified via the `read` tool that the two required tests are absent from `test/orchestrator-daemon.mjs`" and was wrong: it had read its own deployed checkout, not the fixer's clone. The channel recorded the claim faithfully; it took a human reading the judge's verdict, then the driver's own `git diff`, to notice. **[Built]**; the finding **[Proven in our pilots]**.

![What the signature proves and what it does not.](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/haah-5-signature.webp)

## 7. Where this is going

Everything in this section is **[Designed, not built yet]** unless it says **[Not built]**. None of it is on main, with one dated exception that is.

**Membership lifecycle.** **[Not built]**, by decision. There is no leave, no remove and no `member-removed` event, and no design for one. The notification design deferred it explicitly: "Defer — ship without it"; "worth its own design pass if it's ever actually needed". The only removal that exists is revoking the principal.

**Files in channels.** Today a long document is a pointer in prose: the tool description tells a caller to "post a pointer (e.g. 'sha256:<hash> — <filename> — one-line summary') and keep the file as the record". A content-addressed attachment store exists on main for run-ledger evidence, not for channels. **[Not built]** on main; an analysis exists outside the repository, not public, and we do not use it to raise the tag.

**End-to-end sealed groups.** Groups whose keys are held by the members and never by the server. Nothing on main does this, and no current client could hold such a key anyway: not the remote MCP connector, not a script with a bearer, not the browser, which has no channel view. **[Not built]** on main.

**Who may approve, and a human-versus-bot gate.** Part 1, published on 1 October, said `decision_owner` was routing text and that nothing read `presence`. True at the commit Part 1 and our demo were taken on. That afternoon #464 landed on main: a step that names a `decision_owner` is now approved or denied only by that owner, or by a publish-tier principal with an explicit `override: {reason}` recorded on the signed event; a held deterministic gate can no longer be waved through with a plain approve; and the override is refused outright to a `presence: "bot"` principal or an agent acting for a human, because "an override is a human act". That is the only thing that reads `presence`. **[Built]** with tests, and no pilot has run against it; **[Designed, not built yet]** for a presence check on the ordinary resolve path, which the provisioning tool's header still calls for.

**Inbound "someone wants to talk to you".** **[Not built]**. The concept document names the case and says it "needs its own design pass before build" because such an event "has no home in the current event vocabulary".

**Why not just adopt A2A.** A build-versus-adopt spike, question raised 7 September; verdict, in the concept document's own summary of the analysis note: "closer to 'ignore' than 'adopt,' and specifically not for push".

The smaller holes (no `whoami` on `/mcp`; restart-durable chunk assembly marked v2; no channel view, no Slack, email, SMS or mobile sender) are in the table.

## 8. The maturity table

| Part | Tag | Evidence |
|---|---|---|
| One signed JSONL ledger per channel or group, append-only | Built | `canvas/src/channel-store.mjs`, `sign.mjs` |
| Channels (open, full history) vs groups (gated, window from own join, no backfill), non-member refused | Built | `canvas/src/channels.mjs`, 51 tests |
| Groups used live by a provisioned five-principal team | Proven in our pilots | 29 September provisioning record and trap-task run log |
| Same `/mcp` and REST doors, per-principal tokens, root refused by name, membership not role | Built | `server.mjs`, `mcp.mjs`, `coworker.mjs`, `provision.mjs` |
| Sentinel + JSON envelope, last-sentinel parse, chat ignored | Built; Proven in our pilots | `lib/daemon-core.mjs`; 143 + 104 daemon tests; 29 September and 1 October runs |
| `coworker.task` validation, 8 reject reasons, 4 failed reasons, `accepted` at dequeue, `rejected` never after `accepted` | Built | `coworker-daemon.mjs` |
| Dispatcher allowlist vs. channel membership (two gates in two layers); group-kind gate | Built; Proven in our pilots | `coworker-daemon.mjs`, `lib/daemon-core.mjs`; trap-task run log, Phase 3 |
| Orphan sweep, dedupe rebuilt from the channel, atomic state file | Built (restarts observed on 29 September; recovery of a real orphan not recorded) | `lib/daemon-core.mjs`; 143 tests |
| Result body cap ladder, JSON tail never cut | Built | `lib/daemon-core.mjs` |
| Chunked task delivery (`taskRef`, 300,000 chars, 8,000 chunks, 10 min) | Built; Proven in our pilots (1 October run; driver and canary on main, run log not; Part 1's tag) | `lib/daemon-core.mjs`; commit "chunked task delivery, closing the review-panel 10K-char ceiling" |
| `since` cursor over the complete signed line, `latestEventDigest` | Built; Proven in our pilots | `channels.mjs`; trap-task run log, Phase 1 |
| Channel replay verify (3 checks) + citations | Built | `channels.mjs`; two negative-probe tests |
| Pointer-only channel notifications, HMAC-signed per subscription | Built, in-memory retries | `channel-notify.mjs`, 41 tests |
| Acting-for membership inheritance | Built, flag off by default | `channels.mjs`; `SUNSTONE_CANVAS_ACTING_FOR_MEMBERSHIP` |
| Free text in a thread decides nothing; root and self-review refused at resolve | Built | local demo capture, 2026-10-01; refusals unchanged on main |
| `decision_owner` enforced at resolve; publish-tier override recorded on the event; held gate not waved through | Built (#464, 1 October, after Part 1); not Proven | `enact.mjs` resolve path, with tests |
| `presence: human/bot` at resolve | Built for the break-glass override only (#464); Designed, not built yet for the ordinary resolve path | `enact.mjs` `nonHumanOverrideReason`; `provision.mjs` header |
| Leave / remove / `member-removed`; edit or delete an event | Not built (v1 by design; D3 deferred removal, no design) | `channel-store.mjs` header; `DESIGN-channel-notifications.md` §2.2, D3 |
| Files in channels | Not built on main (an analysis exists outside the repository, not public) | today: `sha256:` pointer in prose |
| End-to-end sealed groups | Not built on main (same note) | no client can hold a key |
| Inbound "wants to talk to you" event | Not built (named in the concept doc, no design) | concept doc, case (1) |
| Run-log hash chain, layer 1 (per-record `prevHash`) | Built as experiment code on main; not against root; the 1 October run log predates it | `docs/experiments/scale-build-c1/lib/runlog.mjs`, `test/runlog-chain.mjs`, `AUDIT.md` |
| Run-log layers 2-4 (agent, human, off-host anchors) | Designed, not built yet | experiment `AUDIT.md` |
| Ledger anchoring, monotonic head | Designed, not built yet | Part 1, architecture document |
| Restart-durable chunk assembly | Designed, not built yet ("v2") | `lib/daemon-core.mjs` comment |
| `whoami` on `/mcp` | Not built | `coworker-daemon.mjs` takes the id from env; `server.mjs` has a browser-only `GET /api/whoami` |
| Channel view in the browser; Slack, email, SMS, mobile delivery | Not built | nothing in `canvas/ui`; no sender in the repo |

---

**What we are not claiming.** That any of this is runnable by an outsider: the repository is private and there is no trial; Part 1's [section 12](/blog/2026/10/01/agentic-engineering-teams-on-sunstone-atlas/#12-where-you-can-see-it) says where the public record is. That n is more than one box and one operator. The next post, "We Hid a Bug in Our Own Platform", is where the bytes in section 5 came from, with the parts that did not go well. It follows shortly.

**The slide version.** Six slides from a NotebookLM deck generated from this post, each checked against the text above. The other slides were left out until their wording is corrected. The background text and hex strings on the slides are decoration, not real data.

![Human and daemon use the same doors, credentials and tools](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-same-door.webp)

![Anatomy of an agent message](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-message-anatomy.webp)

![The daemon filtration funnel](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-filtration-funnel.webp)

![Breaking the 10,000-character ceiling](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-chunking.webp)

![The illusion of approval in chat](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-approval-in-chat.webp)

![Maturity bounds and the roadmap](/assets/images/blog/how-agents-and-humans-talk-on-sunstone-atlas/slides-maturity.webp)
