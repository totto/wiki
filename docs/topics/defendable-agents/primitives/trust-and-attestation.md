---
title: "Trust & Attestation"
description: "Signing and provenance for governed knowledge units: ed25519 signatures over exact bytes, the four honest verification statuses, and require-signature gating in the harness."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Trust & Attestation

A governed agent spends most of its effort worrying about what it *does* — the budget it burns, the scores it emits, the audit line it leaves behind. But before any of that, it reads. It loads scoring models, layer weights, band thresholds, and reference data as declared knowledge units. Those units are passive files on disk. Nothing about being passive makes them trustworthy.

This is the quiet gap. I have watched teams build a beautiful [deterministic engine](/topics/defendable-agents/architecture/deterministic-planner/), pin every score temporally, and log every variable — and then load the model definition from a file that anyone with commit access could have edited last Tuesday. Determinism only guarantees that the same inputs give the same outputs. It says nothing about whether the inputs were the ones you meant to ship. Reproducibility without provenance reproduces the tampering just as faithfully as the intent.

So the Lodestar stack treats every governed knowledge unit as something that must be *attested*, not merely *present*.

## Signing the exact bytes

The mechanism is deliberately boring: an ed25519 signature computed over the exact bytes of the unit file. Not over a normalised form, not over a parsed AST, not over "the meaningful fields". The bytes. If a single character of whitespace changes, the signature is invalid, and that is the correct outcome — you asked for byte-exact reproducibility, so byte-exact is what gets attested.

```bash
# Sign a governed unit with the publisher's private key
openssl pkeyutl -sign \
  -inkey publisher_ed25519.pem \
  -rawin -in models/buyer-scoring.yaml \
  -out models/buyer-scoring.yaml.sig

# Verify against the published public key
openssl pkeyutl -verify \
  -pubin -inkey publisher_pub.pem \
  -rawin -in models/buyer-scoring.yaml \
  -sigfile models/buyer-scoring.yaml.sig
```

ed25519 is the right primitive here: small keys, small signatures, fast verification, no parameter choices to get wrong. The signature travels beside the unit and is recorded in the manifest alongside the unit's content hash. That hash is the same one the [temporal pin](/topics/defendable-agents/primitives/temporal-pinning/) captures as `modelHash`, so a signed model and a pinned score reference the same identity.

## The four honest statuses

The temptation is to reduce trust to a boolean — signed or not, load or block. That throws away information the operator needs. The verifier returns one of four statuses, and each means something distinct:

| Status | Meaning | Default action |
|---|---|---|
| `verified` | A signature exists, matches a trusted key, and covers the exact bytes on disk. | Load. |
| `unsigned` | No signature is present at all. | Load only if `require_signature` is off; otherwise fail closed. |
| `unverifiable` | A signature exists but is signed by a key not in the trust set, or the key is unavailable. | Fail closed. |
| `invalid` | A signature exists, the key is trusted, but the bytes do not match. | Fail closed, loudly. |

The distinction between `unsigned` and `invalid` matters more than any other. `unsigned` is an *absence* — a unit nobody ever attested, which may simply be old. `invalid` is a *contradiction* — someone attested these bytes and the bytes on disk are not those bytes. That is either corruption or tampering, and it should never be silently downgraded to "well, load it anyway". Collapsing these two into one "not verified" bucket is how you end up loading a modified model and never knowing.

`unverifiable` is the honest admission that you *cannot decide*. A signature is present but you have no trusted key to check it against. This is not the same as trusting it, and the [fail-closed policy](/topics/defendable-agents/primitives/fail-closed-policy/) treats it exactly as it treats a hard failure: absence of a positive answer is a negative answer.

## Wiring it into the harness

Attestation is enforced at load time, inside the [governance harness](/topics/defendable-agents/architecture/governance-harness/), before a unit ever reaches the engine. The policy is a single flag:

```yaml
# harness.yaml (excerpt)
policy:
  fail_closed: true
  require_signature: true      # unsigned/unverifiable/invalid all block
  trust_anchors:
    - key_id: lodestar-models-2026
      algorithm: ed25519
      public_key: MCowBQYDK2VwAyEA...   # base64 raw public key
```

When `require_signature` is true, only `verified` units load. Everything else raises at load time and emits an audit event, so a blocked load is as visible in the [audit trail](/topics/defendable-agents/primitives/audit-trail/) as a budget overrun. The verifier's finding is recorded as structured provenance:

```json
{
  "unit": "buyer-scoring.yaml",
  "attestation": {
    "status": "verified",
    "algorithm": "ed25519",
    "key_id": "lodestar-models-2026",
    "content_hash": "sha256:9f2c...e1",
    "signed_at": "2026-06-30T09:12:00Z"
  }
}
```

In the [KCP manifest](/topics/defendable-agents/kcp/manifest-basics/), each governed unit carries this attestation block so provenance is declared, not inferred. Because the scoring models are [declared as governed units](/topics/defendable-agents/kcp/declaring-governed-units/) rather than hard-coded, the signature is what stops one from being silently swapped for another — the swap changes the bytes, the bytes fail the signature, the load fails closed.

Trust also has to cross boundaries. When one Lodestar tenant consumes a model published by another, or dogfoods a shared unit, the same signature is what carries trust across the gap without a shared filesystem. That is the whole point of [federation](/topics/defendable-agents/kcp/federation-and-dogfood/): the consumer verifies the publisher's signature against a known key, so provenance survives the hop between systems.

## Honest limits

A signature attests *who* produced these bytes and that they are unchanged. It says nothing about whether the model inside is any good. A publisher can sign a scoring model with a wrong weight, and the verifier will happily return `verified` — the tampering guarantee holds, the correctness guarantee was never offered. Attestation moves the question from "did anyone change this?" to "do we trust the signer's judgement?", which is a governance decision, not a cryptographic one.

Two more caveats worth stating plainly. Key management is now your problem: a leaked private key means an attacker can produce `verified` units, so trust anchors and rotation belong in your operating procedures, not an afterthought. And `require_signature: true` is a fail-closed control like any other — over-tune it and you block legitimate, freshly authored units that simply have not been signed yet. As with every part of a [defendable agent](/topics/defendable-agents/architecture/overview/), this is maintenance, not a one-time setup.
