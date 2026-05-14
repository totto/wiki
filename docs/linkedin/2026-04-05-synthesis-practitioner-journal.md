---
tags:
  - LinkedIn
  - Writing
date: 2026-04-05
---

# Synthesis practitioner journal

*April 5, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7446623196495110145)*

**18 reactions · 8 comments · 2,726 views**

---

Ten weeks ago I shipped Synthesis v1.0 as a search tool for my own codebase.  
                                                               
 I didn't plan what it became.

Today it's at v1.27.0 — 8 knowledge layers, episodic memory, workspace graph indexing, topic health scoring, autonomous nightly triage. It evolved faster than I could write about it.

So I finally wrote about it.

3,800 words covering what Synthesis actually is, the benchmark numbers (65,905 files indexed, 4,200+ tests, 20ms average query), what shifted in practice (retrieval dropped from 40–55% of session time to 10–15%), and the parts that still don't work well.

That last section matters. False-hot topic calibration. Warm/cold task tension. MCP stability under load. Writing about the wins without the limitations would be marketing, not a practitioner's journal.

The post includes the NotebookLM slides from the ExoCortex architecture deck — 14 of them, woven into the narrative.

Link in comments.

---

## Discussion

> **Totto** ↩: Post:  https://wiki.totto.org/blog/2026/04/05/the-tool-i-didnt-plan-to-build-synthesis-ten-weeks-later/

> **I'm so tired of seeing fellow developers build projects that 'could' be something but never actualize their potential because they're stuck in tutorial hell watching someone else implement a feature without any real-world application. I built TeckGrowth to help people like me break the cycle and go from consuming tutorials to having a tangible product, starting with actual project-based learning instead of just watching videos. Have you finally got to ship something real? Learn it. Prove it. Own it. teckgrowth.com**: I'm so tired of seeing fellow developers build projects that 'could' be something but never actualize their potential because they're stuck in tutorial hell watching someone else implement a feature without any real-world application. I built TeckGrowth to help people like me break the cycle and go from consuming tutorials to having a tangible product, starting with actual project-based learnin...

> **Hey really nice job, I’ve read the whole article and indeed is an insightful approach

What I find most intriguing is how you categorize each file and how do you set the archetypes for each directory. What method do you use to get the topics for example? Clustering of labels fron Lucene? LLM-assisted?

And thanks for sharing!**: Hey really nice job, I’ve read the whole article and indeed is an insightful approach

What I find most intriguing is how you categorize each file and how do you set the archetypes for each directory. What method do you use to get the topics for example? Clustering of labels fron Lucene? LLM-assisted?

And thanks for sharing!

> **Totto** ↩: TeckGrowth 
 The tutorial-to-ship gap is real — and AI has actually changed the math significantly. What used to take weeks of setup  to get to a working prototype now takes hours. That changes who can ship something real.                

 But in practice, the harder problem is what comes after. Developers ship something, learn an enormous amount, then start the next project and rediscover hal...

> **Totto** ↩: Matias Luis Lotito Ralli 
Close on the mechanism. Two corrections:                                        
                                                             
 1. No camel case splitting — 
tokenization is delimiter-based ([-_. ]+). TokenValidator.java becomes tokenvalidator +  java, not token/validator separately. Package segments split on . though, so com.exoreaction.security.auth g...

> **Thor Henning Hetland**: Thor Henning Hetland now it’s way more clear. I will keep digging into these concepts to learn more as I’m not really versed about Lucene and the tokenizer. 

I’m impatient to see updates on your design! Keep pushing, your work is amazing :)

---

← [All LinkedIn posts](index.md)
