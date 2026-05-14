---
tags:
  - LinkedIn
  - Writing
date: 2026-02-26
---

# Code Gets Graphs. Knowledge Doesn't.

*February 26, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7432910698608865281)*

**7 reactions · 2 comments · 424 views**

---

Every mature engineering team has dependency graphs for their code.

Import trees. Blast radius analysis. Architecture diagrams. We invested in this tooling because we learned — painfully — what happens when you refactor a core class without knowing what depends on it.

Your Documents workspace has none of this.

Folders tell you where something is. They cannot tell you what it connects to. The business plan that spawned a presentation, the technical proof that validates a sales claim, the architecture decision that explains three years of product choices — those connections exist only in the memory of the people who made them.

Memory decays. People leave. Context gets lost.

We ran a knowledge graph on our main Documents workspace recently. 777 directories, 8,934 files. The result: zero virtual links. A flat directory listing pretending to be a graph.

After fixing the tooling and enriching the workspace: 11,777 edges.

The number that mattered most wasn't 11,777. It was the tightness score per sub-workspace — edges divided by possible edges. Some areas were tight (0.56), meaning coherent, interconnected thinking. Others were sparse (0.10), meaning plans, presentations, and proofs exist but don't point at each other.

Fragmented thinking, made visible.

Code gets graphs because the relationships are deterministic — import statements are edges, the compiler knows. Document relationships require inference. That difficulty is real. It is not an excuse for treating  
 organizational knowledge as a flat pile of files.  
   
Especially now. As AI-augmented workflows generate more output faster, the volume of Documents grows faster than anyone can navigate. Search finds documents. A graph tells your AI tools how your knowledge relates. Without the graph, AI has a library. With it, AI has a map.

I wrote up the full argument — the asymmetry, what the graph adds, tightness as a diagnostic, and what it changes for AI-augmented teams:

→ https://lnkd.in/e2k2ArNN

The engineering session that produced the 11,777 links (including one workflow mistake and its recovery) is here:

→ https://lnkd.in/ea6f5fkW h-claude-code-and-opus/

What does your Documents workspace look like graphed? Has anyone tried this?

#KnowledgeManagement #AIAugmented #DocumentGraph #Synthesis  
 #OrganizationalMemory

---

## Discussion

> **Turning documents into relationship graphs shifts org knowledge from storage to usable context for AI systems.**: Turning documents into relationship graphs shifts org knowledge from storage to usable context for AI systems.

> **Totto** ↩: Mehdi Belkadi *bingo*. :)

---

← [All LinkedIn posts](index.md)
