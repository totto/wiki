---
date: 2009-02-24
categories:
  - Cloud Computing
tags:
  - cloud
  - architecture
  - enterprise
authors:
  - totto
---

# Clouded Vision

Cloud computing platforms offer many benefits including:

<!-- more -->

1. Cheaper operational costs.
1. Dynamic scaling in response to load spikes.
1. Roll-on, roll-off deployments for e.g. newspaper archive processing.

These platforms exist as the result of the investment of companies such as Amazon, Google and Microsoft in developing cost-effective infrastructure with system to administrator ratios of 2500:1 (whilst the average enterprise manages around 150:1 and inefficient properties manage maybe 10:1).

Key to allowing these infrastructures to be efficient and in turn deliver the benefits above is having applications architected such that:

1. They don't require masses of administrator intervention when they go wrong.
1. They can be installed with minimal administrator effort because there's no need to worry about tweaking URLs, IP addresses, database connections etc.
1. They readily support horizontal scaling e.g. because they contain an abstraction that can support sharding of data-storage.

In essence an application must be **designed for zero administrator intervention** and **fully automated deployment**. It should also have a variable workload component that magnifies the savings of the architectural properties above.

Strange then that many a developer expects to move their existing application, full of **enterprise DNA** (static configuration, vertical clusters, no horizontal scaling, high administration costs) to such an offering with minimal change. They even complain when it proves difficult because all those "enterprise features" aren't present. Why does this happen?

I believe it's because these **developers have fundamentally misunderstood how cloud computing delivers its benefits**. They see the cheap prices but don't stop to consider where the cost saving comes from. Some of it is achieved by cloud platform vendors getting large discounts on huge hardware orders but a significant proportion comes from the fact that they don't need to provide (via human resources or APIs) the sysadmin functions required for conventional hosting solutions.

Quite simply typical applications, their architectures and associated administration practices are not setup for cloud platforms. Some of them may be able to run on these platforms with sufficient hackery, brute force and associated cost. However if the motivation for a move to the cloud is merely to reduce kit costs one might well be better off looking for a cheaper conventional hosting solution.

In summary, making the best of the cloud requires that we take an architectural view, something that we've proven remarkably bad at over and over. Simply deploying an application unchanged to the cloud is unlikely to deliver much benefit.

Reference: [http://www.dancres.org/blitzblog/2009/01/25/cutting-corners/](http://www.dancres.org/blitzblog/2009/01/25/cutting-corners/)
