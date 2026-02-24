---
title: "Neo4Dogs: A Data Quality Platform Approach with SolrCloud and Graphs"
---

# Neo4Dogs: A Data Quality Platform Approach with SolrCloud and Graphs

**Date:** June 2014
**Event:** Graph Cafe, Teknologihuset, Oslo
**Slides:** [slideshare.net/totto](https://www.slideshare.net/slideshow/neo4-dogs-en/35205821)

A real-world data quality platform built for Altran to manage dog breed data across multiple legacy systems with conflicting and incomplete records. Uses SolrCloud and Neo4j to discover, map, score, merge, and verify records continuously — demonstrating a practical graph-based approach to data quality at scale.

## The problem

Dog breed data is spread across legacy systems with errors, deviations, and missing information. Merging records from multiple sources with different identifiers requires a platform that can operate continuously across sources rather than batch-reconciling a golden record.

## The platform components

| Service | Role |
|---------|------|
| **DogSearch** | SolrCloud-based search and lookup using `json_full` format |
| **DogPopulationService** | Pedigree and population structure data |
| **DogIDMapper** | Multi-source identifier mapping across systems |
| **DogCrawler** | Discovers additional data from external sources |
| **DogFixer** | Statistical analysis and automated data correction |
| **DogServiceREST** | Verification and record merging API |

## Performance at scale

| Metric | Value |
|--------|-------|
| Request volume | 10 million requests per 24 hours |
| Latency | 0.2 seconds for 99.7% of requests |
| DogIDMapper throughput | 4,000 dogs per second |

## Technology

SolrCloud for distributed search and lookup, Neo4j graph database for pedigree and relationship traversal, REST APIs for service integration. The graph model is particularly well-suited to pedigree data — the relationships *are* the data.

---

<div class="pdf-viewer">
  <object data="/assets/presentations/neo4dogs.pdf" type="application/pdf">
    <div class="pdf-fallback">
      <p>PDF preview requires a browser with PDF support.</p>
      <p><a href="/assets/presentations/neo4dogs.pdf">⬇ Download slides (PDF)</a> &nbsp;·&nbsp; <a href="https://www.slideshare.net/slideshow/neo4-dogs-en/35205821">View on SlideShare</a></p>
    </div>
  </object>
</div>
