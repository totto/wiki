---
title: "Federation & Dogfooding"
description: "Federating governed manifests across teams with parent includes and signed sub-manifests, then publishing this very field guide as navigable KCP units an agent can discover."
image: assets/images/kcp-agent-020-00-end-of-vibes-overview.webp
---

# Federation & Dogfooding

A single manifest is easy. One team, one `knowledge.yaml`, a handful of governed
units — you can hold the whole thing in your head. The problem starts when a
second team wants to reuse your scoring models, and a third wants to layer their
own domain knowledge on top without forking yours. At that point you either
copy-paste manifests (and watch them drift apart within a fortnight) or you
federate. This page covers both halves of the discipline: composing manifests
across teams with parent includes and signed sub-manifests, and the harder,
more honest test — publishing this guide itself as KCP units so an agent can
navigate it the same way it navigates Lodestar's scoring models.

If you have not read [Manifest Basics](/topics/defendable-agents/kcp/manifest-basics/)
and [Declaring Governed Units](/topics/defendable-agents/kcp/declaring-governed-units/),
start there. Federation assumes you already know what a governed unit is.

## Parent includes

Federation in KCP is a parent manifest that `include`s child manifests. The
root manifest owns nothing but coordination: it names the children, records the
hash each child was pinned at, and re-exports the union of their units under one
namespace. A child manifest is an ordinary manifest — it does not know it is
being federated, which is what lets a team publish once and be consumed many
times.

```yaml
kind: manifest
metadata:
  name: lodestar-root
  version: 3.2.0
  domain: regulated-professional-services
  description: Federated root for Lodestar scoring, GTM, and this field guide
  temporal:
    valid_from: 2026-01-15
    refresh_interval: 30d
includes:
  - manifest: scoring/knowledge.yaml
    pin: sha256:9f2c…a1        # the child hash this root was built against
    signature: scoring.sig
  - manifest: gtm/knowledge.yaml
    pin: sha256:41be…7d
    signature: gtm.sig
  - manifest: fieldguide/knowledge.yaml
    pin: sha256:c07a…e9
    signature: fieldguide.sig
units: []                       # the root re-exports children; it declares none of its own
```

`kcp_validate` walks the include tree, resolves every child, and checks that the
`pin` in the parent matches the child's actual content hash. A drifted child —
someone edited `scoring/knowledge.yaml` without re-pinning the root — fails
validation loudly. This is the same fail-closed instinct the whole stack runs
on; see [Fail-Closed Policy](/topics/defendable-agents/primitives/fail-closed-policy/).
The root does not silently accept the newer child. It stops.

## Signing sub-manifests

A pin proves the child has not changed since the root was built. A signature
proves *who* built the child. These answer different questions and you want
both. The pin is integrity; the signature is provenance. When team A consumes
team B's scoring manifest, the signature is how A's harness attests that the
units it loaded came from B and not from an attacker who slipped a manifest into
the search path.

```bash
# child team signs its manifest hash with its own key
kcp-agent sign scoring/knowledge.yaml \
  --key ~/.kcp/keys/scoring-team.ed25519 \
  --out scoring.sig

# consuming harness verifies before any unit is loadable
kcp-agent kcp_validate --manifest lodestar-root/knowledge.yaml --verify-signatures
```

The harness maps each `governance.domains[].manifest` to a signature it will
accept. If a sub-manifest's signature does not verify against a trusted key, the
domain is not mounted and `kcp_plan`/`kcp_load` return nothing for it — the
governed operation then fails closed rather than scoring against unattested
knowledge. This is the manifest-level counterpart to
[Trust & Attestation](/topics/defendable-agents/primitives/trust-and-attestation/);
the wiring into the agent runtime is covered in
[Wiring KCP, Agent & MCP](/topics/defendable-agents/kcp/wiring-kcp-agent-mcp/).

### Honest limit

A signature attests authorship, not correctness. A perfectly signed, perfectly
pinned scoring model can still weight `signal-freshness` wrong. Federation makes
the supply chain reproducible and attributable; it does not make the units
right. That remains the job of [reproducibility](/topics/defendable-agents/decisions/reproducibility/)
and the review discipline around [variable design](/topics/defendable-agents/decisions/variable-design/).
Determinism guarantees process, not truth — the whole stack rests on that line.

## Dogfooding: this guide as KCP units

Here is the part that keeps us honest. This field guide is not just prose about
governed knowledge — it *is* governed knowledge. Every page you are reading is
declared as a KCP unit in its own child manifest, federated under the same root
as Lodestar's scoring models. If we could not model our own documentation as
navigable units, we would have no business telling you to model yours.

```yaml
kind: manifest
metadata:
  name: defendable-agents-fieldguide
  version: 1.4.0
  domain: documentation
  description: The Defendable Agents field guide, published as governed units
  temporal:
    valid_from: 2026-06-01
    refresh_interval: 90d
units:
  - id: kcp.federation-and-dogfood
    path: topics/defendable-agents/kcp/federation-and-dogfood.md
    tags: [kcp, federation, signing, dogfood]
    description: Federating manifests across teams and publishing this guide as units
    depends_on:
      - kcp.manifest-basics
      - kcp.declaring-governed-units
  - id: kcp.manifest-basics
    path: topics/defendable-agents/kcp/manifest-basics/index.md
    tags: [kcp, manifest]
    description: The shape of a KCP manifest and its temporal block
```

The `depends_on` edges are not decoration. They are the same dependency graph an
agent uses to plan a load. When `kcp_plan` is asked for `kcp.federation-and-dogfood`,
it resolves the two dependencies first, so an agent answering a question about
federation arrives with manifest basics already in context — bounded by the
session's `context_budget`, the same 200000-token ceiling that governs a scoring
run.

## How an agent discovers it

Discovery is the payoff. An agent never hard-codes a path to this page. It asks
the root manifest.

1. The harness mounts the federated root and verifies every sub-manifest
   signature.
2. `kcp_plan` receives a query — say, "how do I sign a sub-manifest?" — and
   ranks units by tag and description across *all* federated children, guide and
   scoring alike.
3. The winning unit's `depends_on` closure is resolved into a load order.
4. `kcp_load` returns the units' content within the context budget, and the
   agent answers with the guide's own text as grounding.

The same machinery that lets an agent select the correct scoring model
deterministically — never silently swapping `buyer-scoring` for a stale
version — lets it select the correct page of this guide. Documentation and
domain knowledge sit in one graph, discovered by one mechanism, governed by one
harness. That is what "practising what you preach" reduces to in code: no
special case for the docs.

## Where this fits

Federation is where KCP stops being a per-team convenience and becomes shared
infrastructure. Read it alongside the [architecture overview](/topics/defendable-agents/architecture/overview/)
for how the harness mounts domains, and the
[Lodestar case study](/topics/defendable-agents/reference/case-study-lodestar/)
for how a real federated root behaved in production. The broader protocol lives
at [Knowledge Context Protocol](/topics/knowledge-context-protocol/).

One caution before you federate everything in sight: a federated root is
maintenance, not a monument. Every child that re-pins forces the root to
re-pin and re-sign, and a root with forty children and stale pins is worse than
no federation at all — it looks governed and is not. Federate what is genuinely
shared. Leave the rest local.
