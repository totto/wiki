---
date: 2026-03-06
categories:
  - Java Development
tags:
  - java
  - synthesis
  - claude-code
  - sdd
  - tooling
  - maven
  - architecture
authors:
  - totto
---

# Claude Code + Synthesis: Five Superpowers for Java Developers

*A practical guide to giving your AI coding assistant an institutional memory*

---

You've tried Claude Code. Maybe you love it. Maybe you've noticed that on your 300K-line, 20-module Maven project it spends the first five minutes figuring out where anything is.

That's not a model limitation. That's a context problem. And it's solvable.

<!-- more -->

This article is about what happens when you pair Claude Code with **Synthesis** -- a CLI tool written in Java that indexes your codebase and builds a persistent knowledge graph of it. Together they give you capabilities that neither provides alone. Five in particular.

---

## The Problem in One Sentence

Claude Code is stateless. Every session, it starts with zero knowledge of your codebase and has to search for context before it can reason about anything. For a side project that's fine. For a 40-repo enterprise system, you burn half your AI budget on archaeology.

Synthesis solves this by doing the archaeology once -- then keeping it current.

```bash
synthesis maintain          # run once (or via cron)
synthesis search "JWT validation flow"   # <1 second, across everything
```

---

## The Missing Concept: Skill-Driven Development

Before we get to the superpowers, there's a concept you need. Without it, Synthesis is just another CLI tool. With it, the five superpowers become compounding.

### What skills are

Claude Code reads `.claude/skills/` directories on startup. A skill is a YAML or Markdown file that encodes domain knowledge -- not a prompt, not a template. Think of it as a machine-readable version of what your most experienced team member knows.

```yaml
# .claude/skills/spring-wiring-conventions.yaml
name: spring-wiring-conventions
version: 1.0.0
description: |
  Our Spring wiring conventions for the payment-service module.

trigger_phrases:
  - "add a new service"
  - "wire a bean"
  - "dependency injection"

instructions: |
  # Spring Conventions (payment-service)

  - @Transactional goes on service methods, never repositories
  - Constructor injection only (no @Autowired on fields)
  - All REST controllers return ProblemDetail for 4xx/5xx
  - The core module has zero Spring dependencies by design
  - Integration tests use @SpringBootTest with TestContainers, never H2
```

That's not a clever prompt. It's institutional knowledge in a file that Claude Code loads every session, for every developer on the team.

### Why this matters for Java shops

Every mature Java codebase has conventions that live in one person's head. The naming pattern for DTOs. Which modules are allowed to depend on which. The reason `DateUtils.java` exists and why you should never call `LocalDate.now()` directly. The architectural decision to use hexagonal ports-and-adapters in the `order` module but not in `notification`.

Today, a new developer takes 3-6 months to absorb this. Claude Code without skills takes even longer -- it rediscovers the conventions by reading code, often getting them wrong.

A skill file makes that knowledge explicit, loadable, and version-controlled. `git blame` tells you who wrote the convention. Pull requests update it when conventions change. Every Claude Code session starts with it.

### Skill routing: where Spring developers feel at home

Skills have a scoping model that will feel familiar:

| Scope | Location | Loads when | Analogy |
|-------|----------|-----------|---------|
| Global | `~/.claude/skills/common/` | Every session | `spring-boot-starter-*` defaults |
| Company | `~/.claude/skills/` | Every session | Shared parent POM conventions |
| Project | `.claude/skills/` | That project only | Module-specific configuration |

You don't want your PCB rendering skills loading when you're writing a REST API. You don't want your REST API conventions loading when you're writing a CLI tool. The scoping prevents cross-contamination, just like Maven module boundaries prevent unwanted transitive dependencies.

### The numbers behind it

Synthesis itself was built with 34 skills. The lib-pcb project -- 197,831 lines of Java in 11 days -- was built with 85. That number is not incidental. Each skill encodes a specific piece of domain knowledge: Gerber format specifications, MIF parser patterns, validation hierarchies, test scaffolding structures. Skills are the missing variable that makes the output mechanistically explainable rather than just impressive.

We benchmarked this across 128 sessions:

- **No skills (baseline):** Claude Code explores from scratch every session
- **Flat skills (15 CLI guides loaded):** 11.2% *worse* than baseline -- too much context, not enough routing
- **Tiered skills (routing + architecture + on-demand):** 23.8% *better* than baseline

Loading everything is worse than loading nothing. Loading the right things at the right time is substantially better than both. The engineering is in the routing, not the volume.

### This is Skill-Driven Development

SDD treats skill creation as a first-class engineering activity. Not "use AI better" -- systematically encode domain expertise into versioned, scoped, benchmarked knowledge assets. The team that does this compounds its AI leverage over time. The team that doesn't restarts from zero every session.

The five superpowers below all depend on this. Synthesis provides the data. Skills tell Claude Code what to do with it.

---

## How the Integration Actually Works

The examples in this article show Synthesis commands as things you type in a terminal. That's accurate -- you can. But it's not how they're usually invoked.

### One command installs the integration

```bash
synthesis export-skills --overwrite
```

This copies 25 skill files -- YAML and Markdown, 2,289 lines of encoded command knowledge -- into `~/.claude/skills/`. From that point forward, Claude Code knows how to use Synthesis. Not "knows it exists." Knows *when* to use `search` vs `relate` vs `code-graph`, *which workspace flag* to pass, and *how to interpret the output*.

### What that looks like in practice

You ask Claude Code:

> "What would break if I refactored the PaymentService interface?"

Without Synthesis skills, Claude Code does what it always does: greps, reads files, builds a mental model from scratch. Maybe it finds the direct callers. Probably misses the ones in other modules.

With Synthesis skills installed, Claude Code does this:

1. The `synthesis-relate-dependencies` skill activates (trigger phrase: "what breaks if I change")
2. Runs `synthesis relate "PaymentService.java" --depth 2` -- instant SQLite lookup across the persisted code graph
3. Gets bidirectional dependencies: every file that imports PaymentService, every module that depends on it transitively
4. Reads the critical ones in parallel
5. Gives you an impact analysis grounded in actual dependency data, not grep heuristics

The developer never typed a Synthesis command. The skill encoded the expertise: for impact analysis, use `relate` with depth 2, on the source workspace.

### The routing layer: not all skills load equally

Synthesis ships a `synthesis-task-routing` skill -- validated across those same 128 benchmark sessions -- that acts as a decision tree:

| What Claude Code is asked to do | What the routing skill triggers |
|---|---|
| "Who calls this method?" (cross-package) | `synthesis search "MethodName"` |
| "How does this specific class work?" (named) | Direct file read -- skip search entirely |
| "Show me the architecture" | Read architecture skill first, verify against source |
| "Find security vulnerabilities in XML parsing" | `synthesis code-graph security --type XXE` |
| "What changed this week?" | `synthesis changelog --since 7d` |

The routing prevents the most common failure mode: using search when you should read directly (wastes time), or reading directly when you should search (misses cross-package references).

### Closing the loop: `synthesis learn`

Synthesis can generate skills from your codebase:

```bash
synthesis org scan       # detect organisational structure
synthesis learn          # generate skills from workspace analysis
```

This reads your workspace -- organisations, clients, modules, file patterns -- and produces YAML skill files that teach Claude Code about *your* domain. Not Synthesis commands. Your conventions. Your organisational structure.

The output: context skills that Claude Code loads on startup. Your new hire's first session starts with the same organisational awareness as your most senior developer.

### For senior Java developers: the composability pattern

The important takeaway is not "install Synthesis." It is this: **any CLI tool your team uses can become a first-class Claude Code capability by writing skills for it.**

Have an internal deployment tool? Write a skill:

```yaml
name: deploy-service
trigger_phrases:
  - "deploy to staging"
  - "release to production"
  - "rollback"
instructions: |
  # Deployment (internal tooling)

  Use `platform-cli deploy` -- never `kubectl apply` directly.

  Staging:    platform-cli deploy --env staging --service <name>
  Production: platform-cli deploy --env prod --service <name> --approval-ticket <JIRA>

  Always verify health check passes before marking complete:
  platform-cli health --service <name> --env <env>
```

That took 30 seconds to write. Claude Code now knows your deployment process. It will use `platform-cli` instead of trying to write raw Kubernetes manifests.

Synthesis is proof that this pattern works at scale: 25 skills, 37 commands covered, benchmarked across 128 sessions with a measured 23-40% efficiency improvement. The pattern is general. The implementation is yours to adapt.

---

## Superpower 1: Instant Orientation on Unfamiliar Code

**The Java-specific pain:** You join a project. The repo has 47 Maven modules, a mix of Spring Boot services and legacy batch jobs, and a README that hasn't been updated since 2019. Where do you start?

Without Synthesis: you spend hours reading pom.xml files, grepping for `@RestController`, trying to build a mental map.

With Synthesis:

```bash
synthesis search "user authentication"
synthesis describe src/main/java/com/example/auth/
```

The first command finds every file related to authentication across all modules -- source, tests, configs -- ranked by relevance, in under a second. The second gives you a structured description of what the `auth` package actually *is*, what it depends on, and what depends on it.

Drop that output into Claude Code and ask: *"Given this, walk me through the authentication flow from HTTP request to database."*

Instead of hedging, it answers. Because it knows where everything is.

> **Under the hood:** The `synthesis-task-routing` skill detects orientation questions and routes them to `synthesis search` (cross-module) or `synthesis describe` (directory-level). Results feed directly into Claude Code's context for the next question.

---

## Superpower 2: Module Dependency X-Ray

**The Java-specific pain:** Your architect says "we should refactor the `core` module." Twenty developers go quiet. Nobody knows what breaks.

Synthesis builds a full package-level dependency graph -- across all your repos, all your modules. Persistent. Query it without re-scanning.

```bash
synthesis code-graph                    # full DAG
synthesis code-graph --instability      # Martin's instability metric per module
synthesis code-graph --cycles           # where are the circular dependencies?
synthesis code-graph --hotspots         # most-depended-on packages
```

The instability metric (Robert C. Martin's *Clean Architecture*) tells you which modules are flexible vs. rigid. A module with instability 0.0 is maximally stable -- many things depend on it, it depends on little. Instability 1.0 is maximally flexible -- you can change it without breaking anything.

When we ran this on our own portfolio (58 repos, 429 cross-repo dependencies) it completed in 31 seconds. The output told us exactly which packages were safe refactoring targets and which were load-bearing walls.

Claude Code gets this graph as context: *"Here's the dependency structure. What should we refactor first?"* It gives you a concrete, reasoned answer.

> **Under the hood:** The `synthesis-code-graph` skill activates on architecture and dependency questions. It selects the appropriate flags (`--instability`, `--cycles`, `--hotspots`) based on what's being asked, then hands the DAG output to Claude Code for reasoning.

---

## Superpower 3: Security Scanning -- With a Java-Specific Story

This is the one that surprised us most.

Synthesis has a built-in static security analyzer -- 21 signal types covering traditional vulnerabilities (SQLi, XXE, hardcoded secrets, insecure deserialization, weak crypto) and agentic AI risks (prompt injection, RAG poisoning).

We pointed it at the **Cantara** open-source Java portfolio -- the Whydah SSO system, 60+ repos, production code used across Norwegian enterprise systems.

```bash
synthesis code-graph security -d /src/cantara --severity HIGH
```

Results: **95 HIGH-severity findings** across the portfolio.

After triaging, the genuine findings included:

**XXE in Whydah-UserIdentityBackend** -- a live `@POST` endpoint accepting XML user credentials with no entity protection:

```java
// Before: vulnerable
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = dbf.newDocumentBuilder();
Document dDoc = builder.parse(input);  // CWE-611: XXE possible
```

```java
// After: fixed
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
dbf.setExpandEntityReferences(false);
DocumentBuilder builder = dbf.newDocumentBuilder();
Document dDoc = builder.parse(input);
```

We fixed it, filed the issue, and pushed the PR. Similar story for `DummyUserAuthenticator` in Whydah-SecurityTokenService.

The workflow: **Synthesis finds it -> Claude Code explains it and writes the fix -> human reviews and merges.**

> **Under the hood:** The `synthesis-security-analysis` skill detects security-related questions and routes them to `synthesis code-graph security` with appropriate severity and type filters. Claude Code chains the findings into explanations and fix suggestions automatically.

---

## Superpower 4: Onboarding in Hours, Not Months

**The Java-specific pain:** "It took me three months to understand how the order processing pipeline actually works."

Every Java shop has this problem. Knowledge lives in senior developers' heads, not in docs.

Synthesis builds persistent models of what each directory *is*, based on its contents. Combined with the code knowledge graph, Claude Code can answer questions like:

- *"What does the `fulfillment` service own, and what does it depend on?"*
- *"Which packages have high test coverage gaps?"*
- *"What changed in the last two weeks across our microservices?"*

```bash
synthesis describe src/
synthesis code-graph health
synthesis changelog
```

The `changelog` command does daily snapshots and produces a structured summary of what changed across all repos -- useful for leads, useful for new team members catching up.

We built this after generating 197,831 lines of Java in 11 days for a PCB design library. Navigating 691 files per day of new output without a knowledge graph was genuinely painful. Synthesis was built to solve our own problem.

> **Under the hood:** The `synthesis-task-routing` skill detects onboarding and change-tracking questions, routing to `synthesis describe` for structural understanding and `synthesis changelog` for temporal context. New team members get the same starting point as the senior developer who's been there five years.

---

## Superpower 5: Refactoring With Actual Confidence

**The Java-specific pain:** You want to extract an interface, move a class, break apart a God object. But you're not sure what you'll break.

The combination of dependency graph + instability metric + bi-directional relationship tracking gives you three things before you touch a single line:

1. **What depends on this** -- not just what it imports, but what imports *it*
2. **The stability score** -- is this a load-bearing module or a leaf?
3. **The health signals** -- over-coupling, circular dependencies, instability threshold violations

```bash
synthesis code-graph --instability
synthesis code-graph health --module com.example.core
```

Claude Code gets this as context. *"I want to extract the pricing logic from OrderService. Here's the dependency graph and health signals. What's your assessment?"*

It tells you: *these three classes depend on `PricingEngine` directly, here's the safe extraction path, here's what you'll need to update.*

That's not AI hallucinating about your codebase. That's AI with actual knowledge of your codebase.

> **Under the hood:** The `synthesis-relate-dependencies` skill activates on refactoring questions. It runs `synthesis relate` with bidirectional depth, surfaces the impact set to Claude Code, and the health signals tell it which changes are high-risk vs. safe.

---

## The Honest Part

Synthesis isn't magic. It's an indexer, a static analyzer, and a relationship graph -- written in Java, observable. The security scanner produces false positives (we're actively tuning them). The dependency graph is as good as your package structure.

What it does do is eliminate the archaeology tax -- the time Claude Code spends re-discovering your codebase every session. For a 50-line toy project, that tax is zero. For a 20-year-old Java enterprise system with 40 modules and tribal knowledge baked into the commit history, it's substantial.

The five superpowers above are real. We use them every day.
