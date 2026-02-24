# Open Source

I have been involved in open source for most of my career. The work spans three GitHub organizations and ranges from production IAM systems to AI knowledge infrastructure.

---

## eXOReaction

[github.com/exoreaction](https://github.com/exoreaction)

### Synthesis -- Knowledge Infrastructure

**Repository:** [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis)
**Language:** Java | **License:** MIT

Local-first knowledge infrastructure for AI-augmented development teams. Born out of the lib-pcb project, where generating 197,831 lines of code in 11 days created an urgent need for fast, cross-repository search and dependency tracking.

**What it does:**

- Indexes 200--300 files/second across all formats (code, docs, videos, PDFs)
- Sub-second search (< 1 second, validated at 0.4s)
- Cross-repo dependency graphs (58 repos, 429 dependencies in < 31 seconds)
- Bi-directional relationship tracking
- File movement tracking with hash-based detection
- Cross-workspace change reporting with daily snapshots
- Zero cloud dependency -- all processing is local

**Key metrics:**

| Metric | Value |
|--------|-------|
| Files indexed | 8,934 across 3 workspaces |
| Retrieval time reduction | 92--95% (5--15 min down to 10--30 sec) |
| Storage overhead | 2.7% (11.6 MB index for 434 MB content) |

---

### lib-pcb -- PCB Design Library

**Repository:** [github.com/exoreaction/lib-pcb](https://github.com/exoreaction/lib-pcb)
**Language:** Java | **License:** Apache 2.0

A complete PCB design file processing library. 197,831 lines of Java, 7,461 tests, 8 format parsers (Gerber, Excellon, ODB++, KiCad, Eagle, Altium, GenCAM, IPC-2581), 28 validators, 17 auto-fixers. Manufacturing-ready Gerber output. Built in 11 days using Skill-Driven Development.

---

### xorcery-alchemy

**Repository:** [github.com/exoreaction/xorcery-alchemy](https://github.com/exoreaction/xorcery-alchemy)
**Language:** Java | **License:** Apache 2.0

Experimental extensions to the Xorcery framework, exploring temporal analytics and DevSecOps intelligence capabilities.

---

## Cantara

[github.com/Cantara](https://github.com/Cantara)

Cantara builds open-source infrastructure for Java applications: authentication systems, reactive frameworks, messaging abstractions, and microservice tooling. Most projects are Apache 2.0 licensed and production-ready.

---

### Whydah — SSO / IAM Platform

**Repository:** [github.com/Cantara/Whydah](https://github.com/search?q=org%3ACantara+Whydah&type=repositories) (16 repositories)
**Website:** [getwhydah.com](http://getwhydah.com)
**Language:** Java | **License:** Apache 2.0

A complete Single Sign-On and Identity & Access Management solution. Whydah handles user authentication, token management, role-based access control, and user administration. It is production-deployed across multiple Norwegian enterprise clients.

**Core modules:**
- `Whydah-SecurityTokenService` — Application and user token management
- `Whydah-UserIdentityBackend` — Identity storage with LDAP integration
- `Whydah-SSOLoginWebApp` — SSO login interface
- `Whydah-UserAdminService` — User administration backend
- `Whydah-UserAdminWebApp` — Admin UI
- `Whydah-Java-SDK` — Java integration SDK

**Quick start (Docker):**
```bash
docker pull whydah/whydah-all-in-one-image
docker run -it -p 9997:9997 whydah/whydah-all-in-one-image
# http://localhost:9997/sso/welcome  (admin / whydahadmin)
```

---

### Xorcery — Reactive Java Framework

**Repository:** [github.com/Cantara/xorcery](https://github.com/Cantara/xorcery)
**Language:** Java 21+ | **License:** Apache 2.0

A modular Java library framework built around dependency injection (HK2), composable YAML/JSON configuration, and reactive streams. Designed for building highly performing microservices with strong operational characteristics out of the box.

**Key features:**
- Composable configuration (YAML + JSON Schema)
- Reactive streams over WebSockets
- OpenTelemetry integration
- 30+ extensions: AWS, certificates, DNS, EventStore, JAX-RS/Jersey, Jetty, JWT, OpenSearch, and more
- Used as the foundation for the Xorcery AAA (Alchemy + Aurora) analytics platform

---

### Stingray — Microservice Application Framework

**Repository:** [github.com/Cantara/stingray](https://github.com/Cantara/stingray)
**Language:** Java | **License:** Apache 2.0

A Java application framework with strong conventions for building microservices. Provides structure, configuration, and lifecycle management. Used as the base framework in large-scale deployments (34+ services in production).

---

### Messi — Messaging Abstraction

**Repositories:** [MessiSDK](https://github.com/Cantara/MessiSDK) + provider libraries
**Language:** Java | **License:** Apache 2.0

A messaging and streaming abstraction layer with pluggable providers for different backends. Write once, switch providers without code changes.

**Providers:**
- `MessiS3Provider` — AWS S3
- `MessiSQSProvider` — AWS SQS
- `MessiKinesisProvider` — AWS Kinesis

---

### lib-electronic-components

**Repository:** [github.com/Cantara/lib-electronic-components](https://github.com/Cantara/lib-electronic-components)
**Language:** Java | **License:** Apache 2.0

A Java library for working with electronic components in manufacturing contexts. Provides MPN normalization, component similarity analysis, BOM management, and manufacturer data for 135+ manufacturers.

**Capabilities:**
- MPN normalization and type detection
- 17 specialized similarity calculators (resistors, capacitors, MOSFETs, MCUs, sensors, and more)
- BOM (Bill of Materials) creation and validation
- Alternative component finding
- Component categorization with metadata-driven profiles

---

### Nerthus / Visuale — Service Visualization

**Repositories:** [nerthus](https://github.com/Cantara/nerthus) · [nerthus2](https://github.com/Cantara/nerthus2) · [visuale](https://github.com/Cantara/visuale)
**Language:** Go / Java | **License:** Apache 2.0

Real-time dashboards for visualizing microservice environments. Shows service health, deployment status, and version distribution across a fleet of running services.

---

### Infrastructure & Utilities

**[microservice-baseline](https://github.com/Cantara/microservice-baseline)** — Starting point template for building well-structured microservices.

**[HTTPLoadTest-Baseline](https://github.com/Cantara/HTTPLoadTest-Baseline)** — Load testing tool designed for integration into CD/CD pipelines.

**[ConfigService](https://github.com/Cantara/ConfigService)** — Centralized configuration management service with SDK and dashboard.

**[Valuereporter](https://github.com/Cantara/Valuereporter-Java-SDK)** — Metrics and analytics collection: observations, activities, and reporting.

**[property-config](https://github.com/Cantara/property-config-json)** — Lightweight property-based configuration management.

**[realestate-metasys-cloudconnector-agent](https://github.com/Cantara/realestate-metasys-cloudconnector-agent)** — Reads sensor data from Johnson Controls Metasys building automation systems and distributes to cloud.

