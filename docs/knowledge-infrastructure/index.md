---
tags:
  - AI
  - Synthesis
  - Knowledge Infrastructure
  - Open Source
---

# Knowledge Infrastructure

Over the past three months I have been building and writing about a specific problem: AI agents create faster than humans comprehend. The bottleneck in AI-augmented development is not code generation -- it is finding, understanding, and connecting what has already been generated. Knowledge infrastructure is the missing layer.

This page maps the body of work that emerged from that problem. It spans four codebases, four blog series, and roughly thirty posts -- from the first observation that comprehension was the bottleneck, through building Synthesis and the Knowledge Context Protocol, to the three-layer memory architecture for AI agents.

---

## State of the work

<div class="grid cards" markdown>

-   :material-magnify: **Synthesis** · v1.21.0

    ---

    Local-first knowledge infrastructure platform. Indexes workspaces, builds multi-layer knowledge graphs, exposes everything through CLI, MCP, and LSP.

    **55** CLI commands · **4,170** tests · **8** MCP tools

    [:octicons-arrow-right-24: Release history](../notes/synthesis-releases.md) · [:octicons-link-external-16: GitHub](https://github.com/exoreaction/Synthesis)

-   :material-map: **Knowledge Context Protocol** · v0.5 draft

    ---

    YAML file format that makes knowledge navigable by AI agents. Topology, intent, freshness, audience targeting, context window hints. Submitted to the Agentic AI Foundation.

    **5** RFCs · **3** reference implementations

    [:octicons-arrow-right-24: Spec](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md) · [:octicons-link-external-16: GitHub](https://github.com/Cantara/knowledge-context-protocol)

-   :material-console: **kcp-commands** · v0.8.0

    ---

    Claude Code hook that intercepts Bash tool calls. Injects flag guidance before execution, strips noise after. Java daemon at 12ms/call.

    **283** bundled manifests · **67,352** tokens saved per session

    [:octicons-link-external-16: GitHub](https://github.com/Cantara/kcp-commands)

-   :material-robot: **IronClaw**

    ---

    Open-source AI agent framework. Runs on Linux, connects to Slack, supports MCP tool registration. Powers Mimir and Klaw in the four-layer stack.

    [:octicons-link-external-16: GitHub](https://github.com/nearai/ironclaw)

</div>

!!! abstract "At a glance"
    **~30 posts** across 4 blog series · **Jan 15 -- Mar 3, 2026** · Latest: [Three-Layer AI Memory](/blog/2026/03/03/three-layer-ai-memory-episodic-memory-semantic-memory-your-agent-has-one/)

---

## The argument in five minutes

1. **AI made creating easy but understanding harder.** Output velocity increased 10--50x. Shipping speed improved 2x. The gap is comprehension -- navigation, context-gathering, relationship-tracking. ([The Comprehension Bottleneck](/blog/2026/02/05/the-comprehension-bottleneck-why-ai-made-creating-easy-but-understanding-harder/))

2. **Agents without knowledge infrastructure are interns with amnesia.** They hallucinate when they lack current, structured information. The problem is not the model -- it is what the model has to reason about. ([AI Agents Without Knowledge Infrastructure Are Interns With Amnesia](/blog/2026/02/25/ai-agents-without-knowledge-infrastructure-are-interns-with-amnesia/))

3. **The fix is four layers, not one.** Keyword search, document graphs, code graphs, and temporal tracking -- each answers a fundamentally different question. Teams that pick one layer and stop create a blind spot where the agent fails confidently. ([Your AI Has One Layer. It Needs Four.](/blog/2026/02/28/your-ai-has-one-layer-it-needs-four/))

4. **Agents need maps, not tables of contents.** A flat list of files (llms.txt) does not express topology, freshness, intent, or selective loading. The Knowledge Context Protocol (KCP) is a YAML standard that makes knowledge navigable. ([Beyond llms.txt](/blog/2026/02/25/beyond-llmstxt-ai-agents-need-maps-not-tables-of-contents/))

5. **Memory is three layers, not one.** Working memory (context window), episodic memory (session history), semantic memory (workspace knowledge graph). Most agents have only the first. ([Three-Layer AI Memory](/blog/2026/03/03/three-layer-ai-memory-episodic-memory-semantic-memory-your-agent-has-one/))

---

## The series

Four blog series document the arc from problem to architecture to implementation.

<div class="grid cards" markdown>

-   :material-layers-triple: **[The Four-Layer AI Stack](/blog/2026/02/28/your-ai-has-one-layer-it-needs-four/)**

    ---

    The capstone series. How Synthesis, Claude Code, Mimir, and Klaw compose into an AI development environment that partly runs itself.

    1. Your AI Has One Layer. It Needs Four.
    2. Four Layers: How I Built an AI Development Environment That Partly Runs Itself
    3. What a 10x Workday Actually Looks Like
    4. What It Looks Like from Inside the Stack

    **4 posts** -- the architecture, a realistic day, and a first-person account from the model running inside it.

-   :material-map: **[Knowledge Context Protocol](/blog/2026/02/24/who-describes-you-to-ai/)**

    ---

    From llms.txt to KCP: how AI agents actually find and use knowledge, why the gap between a table of contents and a navigable map matters, and the RFC series defining auth, federation, trust, payments, and context hints.

    **9 posts** -- specification, benchmarks, and the CrewAI PR review loop.

-   :material-brain: **[Giving an AI Agent a Brain](/blog/2026/02/24/giving-an-ai-agent-a-brain-connecting-ironclaw-to-synthesis-via-mcp/)**

    ---

    Connecting IronClaw (a persistent AI agent on EC2) to Synthesis via MCP -- and debugging kimi-k2.5 when it lies about its tool calls.

    **2 posts** -- setup, gotchas, and the four bugs stacked on top of each other.

-   :material-chip: **[Building lib-pcb](/blog/2026/01/15/the-surprisingly-hard-problem-of-semiconductor-part-numbers/)**

    ---

    The project that created the knowledge infrastructure problem. 197,831 lines of Java in 11 days -- the story of what the methodology looked like from the inside.

    **5 posts** -- the build that proved the need.

</div>

---

## Key findings

These standalone posts document specific discoveries -- benchmarks, failure modes, engineering sessions -- that shaped the architecture.

### Benchmarks and evidence

| Post | Finding |
|------|---------|
| [We Gave the AI Better Documentation. It Got Slower.](/blog/2026/02/26/we-gave-the-ai-better-documentation-it-got-slower/) | CLI documentation *increased* tool calls by 11%. MCP *decreased* them by 35%. One sentence in the system prompt beat 41 rewritten tool descriptions. |
| [The Date the AI Invented](/blog/2026/02/26/the-date-the-ai-invented/) | The agent answered with zero tool calls, every metric correct -- except a date it confabulated from surrounding narrative. Temporal metadata needs structured fields, not prose. |
| [KCP on Two Repos, Two Days](/blog/2026/03/01/kcp-on-two-repos-two-days-what-the-numbers-actually-show/) | 119 to 31 tool calls on application code. 53 to 25 on documentation. KCP manifests cut agent work by 53--74%. |

### Knowledge graphs and structure

| Post | Finding |
|------|---------|
| [Zero Links: An Engineering Session](/blog/2026/02/26/zero-links-an-engineering-session-with-claude-code-and-opus/) | 777 directories, zero edges. One day later: 11,777 edges, 23 new tests, 4 bugs fixed. TDD with Opus on the knowledge graph. |
| [Code Gets Graphs. Knowledge Doesn't. That's Backwards.](/blog/2026/02/26/code-gets-graphs-knowledge-doesnt-thats-backwards/) | Every team graphs code dependencies. Almost no one graphs knowledge. The asymmetry is costly and fixable. |

### Coverage and dogfooding

| Post | Finding |
|------|---------|
| [The Synthesis Excavation](/blog/2026/02/25/the-synthesis-excavation-recovering-35-years-of-lost-history/) | Text coverage was 99.6%. Real asset coverage was 15.2%. One working day, 4,852 binary files surfaced from 3.5 years of lost history. |
| [The Mirror Test](/blog/2026/02/11/the-mirror-test-how-synthesis-benchmarked-itself-into-something-better/) | Using an AI tool to measure whether an AI tool is trustworthy -- the dogfooding loop. |
| [Software Entropy at Speed](/blog/2026/02/22/software-entropy-at-speed/) | 23 prompt injection vectors, 4 RAG poisoning instances, 12 missing prompt boundaries -- all found by running the security scanner on itself. |

### Memory and agent architecture

| Post | Finding |
|------|---------|
| [Three-Layer AI Memory](/blog/2026/03/03/three-layer-ai-memory-episodic-memory-semantic-memory-your-agent-has-one/) | Working memory, episodic memory, semantic memory. AI agents have one. They need three. Synthesis v1.21.0 adds episodic memory via session indexing. |
| [Five Architecture Patterns for AI Agents](/blog/2026/02/01/five-architecture-patterns-ai-agents/) | Grep over RAG. Read-only agents. Middleware that validates. The patterns that survive contact with real workloads. |
| [The AI-Augmented Consultant](/blog/2026/03/02/the-ai-augmented-consultant-knowledge-infrastructure-before-deliverables/) | Knowledge infrastructure before deliverables. The same architecture applied to consulting, not just code. |

---

## The codebases

Four open-source projects underpin this work:

**[Synthesis](https://github.com/exoreaction/Synthesis)** -- Knowledge infrastructure for AI-augmented development. Local-first indexing (200–300 files/second), sub-second search, multi-layer knowledge graphs, MCP server (8 tools), session indexing (episodic memory). Java 21. v1.21.0, 4,170 tests, 55 CLI commands.

- [Release history](../notes/synthesis-releases.md)

---

**[Knowledge Context Protocol](https://cantara.github.io/knowledge-context-protocol)** -- A YAML file format specification that makes knowledge navigable by AI agents. KCP is to knowledge what MCP is to tools: it adds topology (`depends_on`, `supersedes`), intent (what question each unit answers), freshness (`validated` dates), audience targeting, and context window hints — the metadata layer that `llms.txt` cannot express.

- **Status:** v0.5 draft spec — published under Cantara, submitted to the [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) (Linux Foundation) alongside MCP and AGENTS.md
- **Spec:** [SPEC.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md) · [PROPOSAL.md](https://github.com/Cantara/knowledge-context-protocol/blob/main/PROPOSAL.md)
- **RFCs:** Auth & Delegation (RFC-0002) · Federation (RFC-0003) · Trust & Compliance (RFC-0004) · Payment & Rate Limits (RFC-0005) · Context Window Hints (RFC-0006, accepted into v0.4 core)
- **Reference implementations:** parsers in Python and Java · MCP bridge servers in TypeScript, Python, and Java
- **Repository:** [github.com/Cantara/knowledge-context-protocol](https://github.com/Cantara/knowledge-context-protocol)

---

**[kcp-commands](https://github.com/Cantara/kcp-commands)** -- A Claude Code hook that applies KCP at the Bash tool boundary. Intercepts every Bash tool call at two points: before execution (injects concise flag/syntax guidance from a KCP manifest — no `--help` round-trips) and after execution (strips noise from large outputs before they consume context). 283 bundled manifests covering git, Linux, Docker, Kubernetes, cloud CLIs, build tools, package managers, and more.

- **Measured saving:** 67,352 tokens per session — 33.7% of a 200K context window recovered
- **Performance:** Java daemon (12ms/call warm) · Node.js fallback (250ms) · unknown commands auto-generate manifests from `--help`
- **Current version:** v0.8.0
- **Install:** `curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java`
- **Repository:** [github.com/Cantara/kcp-commands](https://github.com/Cantara/kcp-commands)

---

**[IronClaw](https://github.com/nearai/ironclaw)** -- Open-source AI agent framework. Runs on Linux, connects to Slack, supports MCP tool registration. Powers Mimir (awareness agent) and Klaw (maintenance agent) in the four-layer stack.

---

## Reading guides

??? abstract "New to this work"

    Start with **[The Comprehension Bottleneck](/blog/2026/02/05/the-comprehension-bottleneck-why-ai-made-creating-easy-but-understanding-harder/)** for the problem statement, then **[AI Agents Without Knowledge Infrastructure Are Interns With Amnesia](/blog/2026/02/25/ai-agents-without-knowledge-infrastructure-are-interns-with-amnesia/)** for the foundational argument. The capstone post **[Your AI Has One Layer. It Needs Four.](/blog/2026/02/28/your-ai-has-one-layer-it-needs-four/)** synthesizes everything into a framework.

??? abstract "Building agent infrastructure"

    Read the **[MCP vs CLI benchmark](/blog/2026/02/26/we-gave-the-ai-better-documentation-it-got-slower/)** (how agents integrate with tools), then **[Beyond llms.txt](/blog/2026/02/25/beyond-llmstxt-ai-agents-need-maps-not-tables-of-contents/)** (how agents navigate knowledge). The **[IronClaw series](/blog/2026/02/24/giving-an-ai-agent-a-brain-connecting-ironclaw-to-synthesis-via-mcp/)** covers the practical setup including every gotcha.

??? abstract "Evaluating knowledge tools"

    The **[Synthesis Excavation](/blog/2026/02/25/the-synthesis-excavation-recovering-35-years-of-lost-history/)** and **[Zero Links session](/blog/2026/02/26/zero-links-an-engineering-session-with-claude-code-and-opus/)** show real-world deployment -- what breaks and how long recovery takes. The **[Mirror Test](/blog/2026/02/11/the-mirror-test-how-synthesis-benchmarked-itself-into-something-better/)** shows what dogfooding looks like.

??? abstract "Understanding the daily practice"

    **[What a 10x Workday Actually Looks Like](/blog/2026/02/28/what-a-10x-workday-actually-looks-like/)** walks through a realistic Tuesday with real output numbers. **[What It Looks Like from Inside the Stack](/blog/2026/02/28/what-it-looks-like-from-inside-the-stack/)** is written by the model running inside the environment.

---

## Timeline

| Date | Milestone |
|------|-----------|
| Jan 15--27 | lib-pcb built: 197,831 lines, 7,461 tests -- the project that proved the comprehension bottleneck |
| Feb 5 | "The Comprehension Bottleneck" published -- the problem statement |
| Feb 14 | Synthesis v1.0.0 ships -- core indexing, search, CLI |
| Feb 15 | MCP and LSP servers ship -- agents can query the index |
| Feb 20 | "The Seven-Day Evolution" -- Synthesis builds itself using itself |
| Feb 22 | Code Knowledge Graph and security scanning ship |
| Feb 24 | IronClaw connected to Synthesis -- first persistent agent with knowledge |
| Feb 25 | KCP series begins -- knowledge format for AI agents |
| Feb 26 | MCP benchmark, knowledge graph session (0 to 11,777 edges), temporal hallucination finding |
| Feb 28 | Four-Layer AI Stack series -- the architecture described |
| Mar 1 | KCP benchmarked on two external repos -- 53--74% efficiency gain |
| Mar 3 | Synthesis v1.21.0 -- episodic memory via session indexing, three-layer memory model |

---

*This body of work is ongoing. The blog has the latest posts; this page has the map.*
