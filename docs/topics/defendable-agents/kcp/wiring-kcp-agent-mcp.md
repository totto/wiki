---
title: "Wiring kcp-agent as MCP"
description: "Expose the deterministic planner to any MCP-speaking agent through kcp_plan, kcp_load and kcp_validate — selection stays governed, and navigation costs zero model tokens."
image: assets/images/summer-plan-00-defendable-agent-workflow.webp
---

# Wiring kcp-agent as MCP

The point of the deterministic planner is that a machine, not a language model, decides which knowledge units a task needs. But the planner is useless if it lives in a corner your agent cannot reach. So you expose it over the Model Context Protocol as a small tool server called `kcp-agent`. Any MCP-speaking client — a coding agent, a chat runtime, a batch worker — can then call three tools and get exactly the governed context it is entitled to, without ever seeing the parts it is not.

This page shows the wiring. It is short by design: the mechanism is deliberately boring, and boring is the property we want.

## The three tools

`kcp-agent` exposes precisely three MCP tools. That is the whole surface.

| Tool | What it does | Determinism |
| --- | --- | --- |
| `kcp_plan` | Given a task description and a [manifest](/topics/defendable-agents/kcp/manifest-basics/), returns the ordered set of units to load — resolving `depends_on` edges | Pure function of `(task, manifest)` |
| `kcp_load` | Returns the content of a named unit (and only that unit) | Deterministic read |
| `kcp_validate` | Checks a manifest for missing paths, cycles, or dangling dependencies | Pure function of the manifest |

The division of labour is the important part. `kcp_plan` **selects**; your model **synthesises**. The planner walks the manifest graph and answers "which units, in what order" using nothing but the declared metadata and dependency edges. The model never sees that navigation happen — it receives a resolved plan and, via `kcp_load`, the unit contents. It spends its tokens on the actual work: reading a scoring model, composing an answer, drafting a plan. It spends nothing on figuring out where things live.

This matters more than it sounds. In a naive retrieval-augmented setup, the model burns context and API spend rummaging through an index, guessing at filenames, re-reading things it already had. Here the guessing is gone. Selection is a graph walk over a [declared set of governed units](/topics/defendable-agents/kcp/declaring-governed-units/), so the same task against the same manifest yields the same plan every time — the same reproducibility guarantee the scoring engine gives you, applied to context assembly.

## Adding the server

For a Claude Code client, registration is one command:

```bash
claude mcp add kcp-agent \
  --scope project \
  -- npx -y @kcp/agent serve \
     --manifest ./knowledge/knowledge.yaml \
     --root ./knowledge
```

That writes an entry into the project MCP config. The equivalent raw JSON, for clients that take a config file directly:

```json
{
  "mcpServers": {
    "kcp-agent": {
      "command": "npx",
      "args": [
        "-y", "@kcp/agent", "serve",
        "--manifest", "./knowledge/knowledge.yaml",
        "--root", "./knowledge"
      ]
    }
  }
}
```

Notice what is *not* here: no API key, no bearer token, no auth block. `kcp-agent` is a local process that reads local manifests and local files. Navigation — planning and loading — is a filesystem operation, not a network call to a metered service. The only tokens you spend are the ones your model spends reasoning over the content the planner hands back.

## A worked call

Once registered, the tools are callable like any MCP tool. From a shell, driving the server directly to show the shape of the exchange:

```bash
# 1. Validate the manifest before anything trusts it
kcp-agent call kcp_validate \
  --manifest ./knowledge/knowledge.yaml
# => { "ok": true, "units": 12, "cycles": [], "missing": [] }

# 2. Plan the units needed to score a buyer
kcp-agent call kcp_plan \
  --manifest ./knowledge/knowledge.yaml \
  --task "score a buyer for priority banding"
# => {
#      "plan": [
#        "scoring/buyer-model",
#        "scoring/need-layer",
#        "scoring/attractiveness-layer",
#        "scoring/winnability-layer"
#      ]
#    }

# 3. Load exactly one selected unit
kcp-agent call kcp_load \
  --unit scoring/buyer-model
# => { "id": "scoring/buyer-model", "content": "...model manifest..." }
```

Step 2 is where the discipline lives. The plan is the four units the buyer model actually depends on — the [three-layer composite](/topics/defendable-agents/decisions/layers-weights-bands/) and nothing adjacent. The planner did not "decide" to include the match-scoring units or a tenant's confidential plans; they were not on the dependency path, so they never entered the model's context. In a governed session this same `kcp_plan`/`kcp_load` pair runs behind the [governance harness](/topics/defendable-agents/architecture/governance-harness/), whose `governance.domains[].tools` list is literally `[kcp_plan, kcp_load]` — the only two the agent is permitted to invoke inside a domain.

## Why selection stays governed

Because the scoring models are themselves [declared as KCP units](/topics/defendable-agents/decisions/scoring-model-manifest/), the planner selects the *versioned* model, not whatever a prompt happened to name. There is no path by which the model silently swaps to a different scoring definition mid-session: the unit id resolves through the manifest, the manifest is pinned, and the resulting choice is recorded. Pair that with the [append-only audit trail](/topics/defendable-agents/primitives/audit-trail/) and you can reconstruct, months later, exactly which units were planned and loaded for a given decision.

## Honest limits

`kcp_plan` guarantees that selection is *deterministic and governed*, not that it is *correct*. If a manifest declares a wrong `depends_on` edge — omits a layer the model actually needs, or pulls in one it should not — the planner will apply that mistake faithfully and identically on every call. That is a feature only in the sense that a consistent, visible error is one you can find and fix; an inconsistent one hides. So run `kcp_validate` in CI, review dependency edges the way you review code, and treat the manifest as governed source, not configuration you set once and forget.

And the obvious caveat: the planner removes the model from *navigation*, not from *reasoning*. Whatever the model does with the loaded units is still the model at the edge — probabilistic, fallible, and outside the deterministic boundary. The wiring here is what keeps that boundary crisp. For where it sits in the larger picture, see the [architecture overview](/topics/defendable-agents/architecture/overview/) and [federation and dogfooding](/topics/defendable-agents/kcp/federation-and-dogfood/).
