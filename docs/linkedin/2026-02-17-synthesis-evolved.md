---
tags:
  - LinkedIn
  - Writing
date: 2026-02-17
---

# Synthesis Evolved

*February 17, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7429582224452313088)*

**19 reactions · 0 comments**

---

On February 15 I posted about Synthesis — a search tool for AI-generated code output. Local index, sub-second search, find files in 8,000+  repos.  
That was 48 hours ago.

Since then:

synthesis research --topic architecture — multi-pass AI analysis of your entire codebase. Not a summary. Multiple passes: architecture first, then security, then synthesis. Reads the actual files.

synthesis report --client Company X — generates a business brief on a specific client from your actual documents. Proposals, meeting notes, code, everything in the index.

exo — one word. An executive gets a dashboard of decisions needing attention, pipeline status, upcoming deadlines. No Git knowledge required.

We didn't plan all of this. We planned to build something to help organizations handle the AI Agent 2026 level of output.

The problems kept expanding. Developers needed search. Architects needed dependency graphs. Managers needed codebase health metrics.

Product managers needed content audit. Executives needed pipeline visibility. Each solved in the same infrastructure — index everything, query anything.

What started as "find files faster" is now:  
 - 37 commands across 8 user roles  
 - Research reports (multi-pass AI, not summaries)  
 - Business intelligence (client reports, pipeline, decisions)  
 - Credential store, staging areas, file movement tracking  
 - MCP server (AI agents use it natively)  
 - 8 perspective-specific documentation guides

This morning we ran synthesis enrich on NotebookLM presentations we'd created from the Synthesis documentation itself. The tool now indexes its own documentation. Found a bug along the way — images above 5 MB were silently failing the vision API. Fixed it. The knowledge infrastructure now describes its own architecture diagrams.

Synthesis was built to solve eXOReaction's problem. 691 files/day from lib-pcb, and other codebases, no easy way to find anything. It solved that. Then kept solving the problems we hadn't named yet.

The honest version: we had no real roadmap for executive reporting. But we had a problem (CEO can't find/keep up with what developers built), a data model (everything indexed), and built it in two days.

---

← [All LinkedIn posts](index.md)
