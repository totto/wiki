---
date: 2026-03-08
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai-agents
  - kcp
  - a2a
  - knowledge-infrastructure
  - standards
  - security
  - multi-agent
authors:
  - totto
  - claude
---

# The Front Door and the Filing Cabinet: A2A Agent Cards Meet KCP

![The Front Door and the Filing Cabinet: Composing A2A and KCP in Multi-Agent Systems](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-01.png)

Multi-agent systems need two kinds of identity. The first answers "who is this agent and how do I call it." The second answers "what knowledge does this agent have and who is allowed to see each piece of it." Google's A2A protocol handles the first. KCP handles the second. They are not competitors. They are different layers of the same stack.

<!-- more -->

![Multi-Agent Systems Require Two Distinct Identities: Service Identity (A2A) and Knowledge Identity (KCP)](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-02.png)

## What an A2A Agent Card does

An [A2A Agent Card](https://google.github.io/A2A/) is a JSON file published at `/.well-known/agent.json`. It describes an agent's identity, what it can do, and how to authenticate when calling it. Think of it as a service directory entry — the front door.

```json
{
  "name": "Clinical Research Agent",
  "description": "Answers questions about clinical trial protocols and patient cohort data.",
  "url": "https://research.hospital.example/a2a",
  "version": "1.0.0",
  "provider": {
    "organization": "Hospital Research Division",
    "url": "https://hospital.example"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "securitySchemes": {
    "hospital-oauth": {
      "type": "oauth2",
      "flows": {
        "clientCredentials": {
          "tokenUrl": "https://auth.hospital.example/token",
          "scopes": {
            "agent:invoke": "Invoke this agent"
          }
        }
      }
    }
  },
  "security": [{ "hospital-oauth": ["agent:invoke"] }],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "protocol-lookup",
      "name": "Protocol Lookup",
      "description": "Find clinical trial protocols by ID or condition.",
      "tags": ["clinical", "research", "protocols"]
    },
    {
      "id": "cohort-analysis",
      "name": "Patient Cohort Analysis",
      "description": "Statistical analysis of patient cohort data.",
      "tags": ["analysis", "patients", "statistics"]
    }
  ]
}
```

This tells a calling agent everything it needs to connect: the endpoint URL, OAuth2 token endpoint, supported content types, and available skills. It is the agent equivalent of a Swagger/OpenAPI definition for a REST service — discovery and invocation in one file.

What it does not tell you is which pieces of knowledge inside the agent are public, which require specific roles to access, and what delegation constraints apply when one agent passes context from this agent to a third agent.

---

## What a KCP manifest does

A [KCP manifest](https://github.com/cantara/knowledge-context-protocol) (`knowledge.yaml`) describes the knowledge an agent has access to, at the level of individual units. It does not describe the agent itself — it describes the filing cabinet inside the agent.

```yaml
knowledge:
  id: clinical-research-knowledge
  version: "1.0"
  description: "Knowledge context for the Clinical Research Agent."

  auth:
    methods:
      - type: oauth2
        flow: client_credentials
        token_endpoint: "https://auth.hospital.example/token"
        scopes: ["read:knowledge"]

  trust:
    audit:
      agent_must_log: true
      require_trace_context: true

  delegation:
    max_depth: 2
    require_capability_attenuation: true
    audit_chain: true

  units:
    - id: trial-protocols
      intent: "What are the active clinical trial protocols?"
      path: protocols/active-trials.md
      scope: project
      audience: [agent, researcher]
      access: authenticated
      triggers: ["trial", "protocol", "study", "phase"]

    - id: public-guidelines
      intent: "What are the published research guidelines?"
      path: guidelines/public.md
      scope: global
      audience: [human, agent]
      access: public

    - id: patient-cohort
      intent: "What does the patient cohort data show?"
      path: data/patient-cohort.md
      scope: project
      audience: [agent]
      access: restricted
      auth_scope: "clinical-staff"
      sensitivity: pii
      delegation:
        max_depth: 1
        human_in_the_loop:
          required: true
          approval_mechanism: oauth_consent
```

The `patient-cohort` unit carries constraints the Agent Card cannot express: PII sensitivity, a maximum delegation depth of 1, mandatory human approval before an agent reads it, and a specific role requirement (`clinical-staff`). The `public-guidelines` unit is freely loadable. The `trial-protocols` unit needs any valid credential but no special role.

This per-unit granularity is KCP's purpose. An agent reading the manifest knows — before fetching any content — what it can load freely, what needs credentials, and what needs human approval.

---

![The Core Metaphor: A2A is the front door, KCP is the filing cabinet inside](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-03.png)

## Different layers, different granularity

| Concern | A2A Agent Card | KCP Manifest |
|---------|---------------|--------------|
| **Identity of** | The agent (service) | The knowledge (content units) |
| **Published at** | `/.well-known/agent.json` | `knowledge.yaml` (project root) |
| **Format** | JSON | YAML |
| **Auth answers** | "How do I call this agent?" | "What credential do I need for *this specific unit*?" |
| **Granularity** | Per-agent | Per-knowledge-unit |
| **Delegation controls** | Not in scope | `max_depth`, capability attenuation, audit chain |
| **Sensitivity labels** | Not in scope | `public`, `internal`, `confidential`, `pii` |
| **Human-in-the-loop** | Not in scope | Per-unit, with approval mechanism |
| **Discovery** | Agent skills, I/O modes, capabilities | Knowledge units, intents, triggers, freshness |
| **Complementary to** | MCP (tool transport) | MCP (unit retrieval), A2A (agent invocation) |

A2A answers: *Can I call this agent? What does it accept? How do I authenticate to it?*

KCP answers: *What knowledge does this agent have? Which pieces require which credentials? What happens when this agent delegates access to another agent?*

---

![Granularity in Practice: three drawers — public-guidelines, trial-protocols, patient-cohort — each with different access constraints](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-06.png)

## How they compose in a multi-agent system

A concrete scenario. An orchestrator agent needs clinical trial data from a research agent.

```
Human
  → authorizes Orchestrator Agent

  Orchestrator Agent
    → discovers Research Agent via A2A Card (/.well-known/agent.json)
    → authenticates TO Research Agent (OAuth2 bearer, per A2A securitySchemes)

      Research Agent
        → reads its KCP manifest (knowledge.yaml)
        → unit "public-guidelines": access=public
            → loads immediately, no constraints
        → unit "trial-protocols": access=authenticated
            → caller has valid OAuth2 token, loads
        → unit "patient-cohort": access=restricted, auth_scope="clinical-staff",
            delegation.max_depth=1, human_in_the_loop=required, sensitivity=pii
            → checks: does caller hold "clinical-staff" scope? (KCP auth)
            → checks: delegation depth ≤ 1? (KCP delegation)
            → requests human approval before loading (KCP HITL)
            → logs access with W3C Trace Context headers (KCP trust.audit)
```

![Production Scenario: The Clinical Trial Handshake — Step 1 A2A, Step 2 KCP, Step 3 MCP](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-10.png)

A2A got the orchestrator through the front door. KCP determined what happened once inside — which drawers opened freely, which required a specific key, and which required a human to unlock them.

Without A2A, the orchestrator does not know how to find or call the research agent. Without KCP, every unit inside the research agent has the same access level — all or nothing.

---

## The auth overlap, honestly

![Demystifying the Auth Overlap: A2A Auth (transport layer) vs KCP Auth (knowledge-access layer)](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-07.png)

Both protocols touch authentication. This is the area where a superficial reading might suggest redundancy. It is not.

**A2A auth** operates at the transport layer. It defines how a calling agent authenticates *to* the target agent — OAuth2 flows, API keys, bearer tokens. The question is: "Are you allowed to talk to this agent at all?"

**KCP auth** operates at the knowledge-access layer. It defines what credentials are needed to access *a specific knowledge unit* within the agent's context. The question is: "Now that you are inside, are you allowed to read *this particular file*?"

A2A cannot express: "The patient records unit requires human-in-the-loop approval, maximum delegation depth 1, audit trail required, PII sensitivity." There is no field for it. Agent Cards describe the agent, not the agent's knowledge.

KCP cannot express: "This agent accepts calls via OAuth2 bearer at this endpoint URL, supports streaming, and has these skills with these I/O modes." There is no field for it. Knowledge manifests describe the knowledge, not the service hosting it.

The overlap is that both support OAuth2. The difference is the question being asked and the granularity at which it is asked.

---

## What this means for production deployments

![The Production Mandate: A2A without KCP vs KCP without A2A — if handling mixed sensitivity levels, you need both](/assets/images/blog/a2a-cards-and-kcp/a2a-kcp-slide-11.png)

If you are building a multi-agent system that handles data with mixed sensitivity levels — which is most production systems — you need both layers:

1. **Agent discovery and invocation** (A2A): Which agents exist? What can they do? How do I call them?
2. **Knowledge access control** (KCP): Within each agent, which knowledge units exist? What are their access levels? What delegation constraints apply?

Neither protocol alone covers the full stack. A2A without KCP gives you a well-described front door with no access control inside. KCP without A2A gives you fine-grained knowledge control with no standard way for agents to find or invoke each other.

The composability model extends to MCP as well. [KCP and MCP](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/) already work together — KCP provides the knowledge manifest, MCP provides the transport for retrieving units. A2A adds the agent-to-agent discovery layer on top.

---

## Working example

The KCP repository includes a complete worked example using the clinical research domain from this post:
[`examples/a2a-agent-card/`](https://github.com/Cantara/knowledge-context-protocol/tree/main/examples/a2a-agent-card/) — an A2A Agent Card and a KCP manifest for the same agent, with a README walking through the multi-agent composition step by step.

## Running the simulator

The example includes a runnable Java simulator that executes the full composition story:

```bash
git clone https://github.com/Cantara/knowledge-context-protocol.git
cd knowledge-context-protocol/examples/a2a-agent-card/simulator
mvn package
java -jar target/kcp-a2a-simulator-0.1.0-jar-with-dependencies.jar --auto-approve
```

The simulator walks through all four phases — A2A discovery, KCP manifest loading, OAuth2 token exchange, and per-unit access decisions — and prints structured output tagged `[A2A]`, `[KCP]`, `[HITL]`, and `[AUDIT]`. For the `patient-cohort` unit it triggers the human-in-the-loop gate (skipped with `--auto-approve`; remove the flag for an interactive prompt).

30 tests cover all access decision cases, agent card parsing, and the full integration flow: `mvn test`.

---

## Related

- [Who Let the Agent In?](/blog/2026/02/28/who-let-the-agent-in/) — KCP auth and delegation (RFC-0002) in detail
- [KCP and MCP: One Protocol for Structure, One for Retrieval](/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/) — how KCP and MCP compose
- [A2A Protocol specification](https://google.github.io/A2A/)
- [KCP spec and RFCs](https://github.com/cantara/knowledge-context-protocol)
