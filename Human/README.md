# Germán Küber

<div align="center">
  <img src="germankuber_2.jpg" width="150" style="border-radius:50%" alt="Germán Küber"/>

  ### Staff Engineer — Systems, AI & Blockchain | Microsoft MVP

  [![LinkedIn](https://img.shields.io/badge/LinkedIn-germankuber-blue?style=flat&logo=linkedin)](https://linkedin.com/in/germankuber)
  [![GitHub](https://img.shields.io/badge/GitHub-GermanKuber-black?style=flat&logo=github)](https://github.com/GermanKuber)
  [![YouTube](https://img.shields.io/badge/YouTube-germankuber-red?style=flat&logo=youtube)](https://youtube.com/@germankuber)
  [![Website](https://img.shields.io/badge/Web-germankuber.com-teal?style=flat&logo=google-chrome)](https://germankuber.com)

  📄 **[View HTML](https://germankuber.github.io/resume/resume.html)** | **[Download PDF](https://github.com/germankuber/resume/raw/main/Germ%C3%A1n%20K%C3%BCber.pdf)**
</div>

---

## 👋 About

Microsoft MVP for 8 consecutive years. Founder of Net-Baires, Argentina's largest dev community (100K+ members). 15+ years building systems that move money, ship products, and scale—from low-latency MEV trading in Rust ($50M+ daily on-chain flow, $100K+ annual P&L, sub-10ms execution) to real-time AI platforms (multi-provider LLM orchestration, sub-200ms voice TTFT, RAG, MCP) to enterprise architectures. Currently AI Architect at Nera, owning the knowledge and code-intelligence layer the whole company queries in natural language, and the agentic tooling that takes product and engineering from problem to spec. Player-coach who builds teams (up to 8 engineers), drives architectural decisions, and stays deep in production code across Rust, Python, .NET, and Node.js. 80+ international talks at .NET Conf, DevFest, NetCoreConf, vOpen and more across LATAM & Europe. EU citizen (Spanish nationality), remote-first, open to EU/Americas.

---

## 🏆 Key Achievements

- Microsoft MVP — 8 consecutive years
- Net-Baires Founder — 100K+ developer community
- 80+ Technical Talks — .NET Conf, DevFest, vOpen
- $100K+ MEV Profit — Rust pipelines at Borderless
- Kliver Co-Founder — AI training platform, 500+ users
- $50M+ Daily Volume — On-chain monitoring systems

---

## 💼 Work Experience

### AI Architect
**Nera (Full-time)** | 02/2026 - Present

- Own Nera's AI architecture: the knowledge and code-intelligence layer that lets the whole company query the business in natural language, and the agentic tooling product and engineering use to go from problem to spec.
- Designed and built a company-wide ontology (28 classes, 26 invariants) that ingests Notion, Jira and GitHub into a Neo4j knowledge graph plus a pgvector semantic index—so every area gets end-to-end traceability from problem to PR, and natural-language Q&A over MCP.
- Built a code graph of the entire microservice fleet (66 repos, 77k nodes, 210k relationships across Java, TypeScript and Go), enriched with runtime calls from OpenTelemetry and served through a 32-tool MCP server that engineers use to design features and product uses to write PRDs.
- Built an AI product-engineering platform where multi-agent LangGraph flows take a problem through PAD, PRD, epic and tech spec, grounded in the code graph and business knowledge.
- Made evals a release gate: record-and-replay harnesses, a 100-question benchmark for the knowledge graph, fidelity audits for the code graph and LLM-as-judge for generated PRDs.
- Automated user-research capture with a pipeline that transcribes interviews and extracts verifiable quotes and insights into Notion with human approval, replacing a manual tracker.
- Built AI tooling for product and design: a Claude plugin for research, interview guides and synthesis, and a Figma plugin that audits screens against the design system.
- Drove Spec-Driven Development (SDD) across engineering with a shared framework (specs, TDD, review gates) that standardized how features are built and raised quality team-wide.
- Organized Nera's internal training space and gave talks on engineering cognition, LLM architecture beyond the prompt, Vertical Slice Architecture and HTTP internals.

### Independent AI Consultant — Agent Engineering & Enterprise AI Delivery
**Self-employed (client under NDA)** | 03/2026 - 07/2026

- Work forward-deployed alongside an enterprise engineering organization—working directly with the customer, running discovery with business and technical stakeholders, architecting the agent solution, and owning delivery from pilot through production and continuous iteration.
- Design and ship production agentic workflows on LangChain, LangGraph, and Microsoft Agent Framework—testing each graph, running eval frameworks and eval suites against it, and monitoring it live in production to tune behavior from real traces.
- Built multi-agent architectures on Google's A2A (Agent2Agent) protocol, exposing agent capabilities as Agent Cards and designing a central capability registry so functionality is discoverable and reusable across agents.
- Own the RAG platform end-to-end for internal company documentation—retrieval optimization, chunking and context engineering, plus regression test suites that gate every change before it reaches production.
- Lead context engineering as a discipline, helping the organization structure and bucket its internal knowledge so it is actually consumable by LLMs, and advising on which data matters for long-term decision-making.
- Fine-tuned models with LoRA on internal company documents and deployed them through Azure AI Foundry; cut inference cost and latency through semantic caching, agent-level semantic memory, and dynamic model routing.
- Built "company brain" knowledge graphs with Cognee and Graphiti over internal repositories, including specialized code graphs that map microservice architecture so agents can query real system structure when making decisions.
- Designed an end-to-end agentic pipeline running from company discovery through to production deployment with no human intervention, with targeted human-in-the-loop checkpoints placed to guarantee quality.

### Co-Founder & Lead AI Architect
**KliverAI (Own Venture, closed Feb 2026)** | 03/2025 - 02/2026

- Founded and built Kliver—an AI platform that converts expert knowledge into scalable training simulations. Owned technical strategy and end-to-end delivery as senior-most engineer on a polyglot stack (Node.js/TypeScript, Python, .NET, Rust, Kubernetes, AWS) supporting 500+ users in dynamic roleplay scenarios.
- Rewrote the real-time layer from app-embedded SignalR to Azure SignalR Service with Redis-backed state, scaling concurrent users by 500% while holding sub-200ms latency on audio pipelines (OpenAI Realtime API).
- Benchmarked TTS/STT services (ElevenLabs, Deepgram, AssemblyAI, OpenAI Whisper, Play.ht) on latency, cost, and quality—getting latency to 90ms and word accuracy to nearly 95%.
- Integrated three LLM providers (OpenAI, Anthropic Claude, Google Gemini) with dynamic model routing across direct APIs and managed cloud services (AWS Bedrock, Azure OpenAI, Vertex AI), picking the best model per task to cut inference spend.
- Built an adaptive simulation engine with multi-agent architecture on LangGraph—state machines, conditional routing, ReAct-style reasoning, multi-step branching, and RAG-powered personalization with 90%+ context relevance.
- Shipped production RAG pipelines across Pinecone, Chroma, pgvector, and Redis with semantic search, hybrid retrieval, and cross-encoder reranking; implemented MCP (Model Context Protocol) servers and clients to standardize tool access.
- Designed a decentralized marketplace for human evaluation criteria using Zero-Knowledge proofs (Noir, Barretenberg, Garaga on StarkNet)—privacy-preserving, verifiable expert judgment at scale.
- Instrumented LLM evaluation and observability with LangSmith, RAGAS, DeepEval, Langfuse, and OpenTelemetry GenAI conventions; ran red-teaming and structured eval pipelines to reduce hallucination on critical paths.
- Built a Chrome Extension for real-time Google Meet capture, streaming transcripts via WebSocket into an automated AI evaluation pipeline.
- Hired and led a distributed team of up to 3 engineers; ran technical interviews, hiring decisions, and architectural reviews while remaining hands-on in code.

### Fractional CTO (Part-time, parallel to KliverAI)
**Rocking Product** | 04/2025 - 12/2025

- Came in as Fractional CTO to an 8-engineer team and restructured it in the first quarter without stepping away from the code—stabilizing release cadence and reducing sprint carryover; ran technical interviews and final hiring decisions.
- Built an image embeddings service (Azure AI Vision + CLIP) to improve product matching across brand comparisons, raising accuracy and lifting the client's revenue by 40%.
- Cut production bugs by 70% through team training and automated processes (testing, CI/CD, code review).
- Optimized LLM usage and cloud infrastructure through model selection, prompt compression, and semantic caching—cutting combined API and cloud spend by 45%.
- Designed a reusable base architecture on LangChain and LangGraph with Langfuse / LangSmith monitoring and prompt versioning; migrated the real-time LLM service from OpenAI to Azure AI Foundry for compliance and data retention, cutting latency and improving scalability.
- Introduced Spec-Driven Development (SDD) and AI-driven development workflows with autonomous agents automating code review, testing, deploys, and monitoring.
- Proposed and led a full-stack migration from a fragmented JavaScript codebase to .NET (ASP.NET Core, Entity Framework Core, Clean Architecture), modernizing the platform for long-term scalability.
- Shipped AI-powered features in Node.js/TypeScript and Python (FastAPI, LangChain); established the team's first LLM evaluation and monitoring practices including faithfulness and correctness scoring.
- Ran weekly public-speaking workshops to sharpen team communication, raising the quality of client meetings.

### Lead Software Engineer (Blockchain / MEV)
**Borderless Capital / CTF Capital** | 09/2021 - 03/2025

- Designed and operated production MEV searcher pipelines in Rust (tokio, async) and Python/Cython across EVM (Ethereum, Arbitrum, Optimism) and Solana, processing 10K+ opportunities/day from $50M+ in daily on-chain flow with $100K+ attributable annual P&L and execution under 10ms p99.
- Migrated the system from Python/Cython to Rust and took it to 20x more transactions per second—tuning tokio runtime parameters, async boundaries, and lock-free coordination patterns for sub-10ms targets.
- Built custom transaction delivery infrastructure with parallel broadcasting across RPC endpoints and direct validator/TPU routes, achieving sub-slot inclusion on Solana (~400ms) and improving inclusion probability by 35% under heavy mempool competition.
- Integrated the Flashbots stack (MEV-Boost, Suave, MEV-Share, PBS, relays) for Ethereum MEV execution and bundle submission, and the Jito ecosystem on Solana (bundles, BAM/Block Assembly Marketplace, BuilderNet, Agave, Jito-Solana fork) for validator routing.
- Built Node.js/TypeScript services that interact with DeFi protocols on-chain—AMMs (Uniswap V2/V3, Curve, Raydium, PumpSwap) and lending markets (Aave)—using ethers.js, viem, web3.js, and @solana/web3.js.
- Designed strategy logic including liquidation detection, multi-hop arbitrage across 5+ DEXs, and cross-chain flow modeling.
- Reverse-engineered Geth and Reth to improve transaction simulation and gas estimation; contributed to the REVM community.
- Ran technical due diligence on 5+ projects that ended up getting funded—architecture, risk, and feasibility—acting as the CTO's technical reference on the low-level side.
- Implemented low-latency observability with Prometheus and custom Rust telemetry, tracking 50+ real-time metrics for slot timing, validator rotation, and execution outcomes.
- Conducted research and PoC on Zero-Knowledge technologies and L2 ecosystems (StarkNet, Cairo, account abstraction/ERC-4337), evaluating applicability for next-generation MEV tooling.
- Owned 24/7 production reliability and incident response (on-call rotation, post-mortems); helped build the blockchain team, which grew from 4 to 10 engineers—code review, mentoring, and technical interviewing for Rust and distributed-systems hires.

### Senior Software Architect
**Paramo Technology** | 10/2020 - 09/2021

- Owned the end-to-end architecture of a high-traffic online casino (iGaming) platform handling real-time money operations and regulatory reporting, working directly with the CTO.
- Spotted the issues slowing teams down and designed action plans that raised productivity by 40%, measured by features shipped and fewer errors.
- Designed and rolled out event-driven microservices in .NET (C#, ASP.NET Core) handling real-time game state, wallet operations, and regulatory reporting with strict consistency requirements; migrated relational databases to MongoDB where it made sense.
- Implemented distributed tracing across all services (OpenTelemetry, Application Insights, Datadog) to catch bugs early and resolve production issues faster.
- Brought in Kubernetes to scale; built automated deploy pipelines; helped migrate services to newer .NET versions.
- Applied Domain-Driven Design (aggregates, value objects, domain events), design patterns, and CQRS for read/write separation across complex gambling and wallet domains.
- Led part of the hiring and designed the technical entry exam; created and delivered internal training programs on architecture patterns, testing discipline, and operational best practices.

### Software Architect (Full-Stack)
**CloudX (Software Consultancy) — first employee** | 09/2017 - 10/2020

- Was the company's first employee; led architecture decisions across several enterprise product lines, often working on-site with clients, and helped build the team as it grew.
- Built microservices backends in Node.js/TypeScript and .NET (C#, ASP.NET) across multiple enterprise product lines using Domain-Driven Design and Clean Architecture / Hexagonal patterns.
- Designed Angular and React frontends with reusable component libraries and TypeScript shared across enterprise products.
- Built a distributed system over geospatial data with PostGIS for a UK client.
- Delivered technical training and conference talks to partners and internal engineering teams; collaborated directly with clients on requirements gathering and technical adoption.

### Software Architect (Angular / .NET)
**Majestic Hotel Group** | 01/2014 - 08/2017

- Designed and built full-stack features in Angular and .NET for internal hotel management platforms, first as Team Lead and later as architect.
- Led the migration from AngularJS to Angular 2, improving maintainability, performance, and code consistency across the platform.
- Redesigned the data model toward an event-oriented architecture, reducing coupling across integrations and simplifying long-term maintenance.
- Defined and documented backend and frontend development processes to streamline deployments and team collaboration.

### .NET Web Developer
**Plus54** | 2011 - 2014

- Built .NET web applications and internal tools, delivering features across backend and frontend.
- Designed and built early mobile application components, collaborating with senior developers on architecture and UX.
- Integrated external services and APIs, implementing unit tests and ensuring reliable data exchange between systems.

### Software Developer
**Acsys** | 2009 - 2011

- Developed and maintained .NET web applications and internal client solutions end-to-end across backend and frontend.
- Participated in requirements gathering and delivery for multiple business-line projects.

### Junior Developer
**IBM** | 2008 - 2009

- Started professional career at IBM contributing to enterprise .NET projects.
- Worked alongside senior engineers on backend features, integration work, and quality processes.

---

## 🛠️ Skills

💻 **Languages:** Rust (tokio, async), Go, C# / .NET (8/9, ASP.NET Core, EF Core), TypeScript, JavaScript, Python (FastAPI, async), Cython, C++, Solidity, Cairo

• **AI / LLM Systems:** Multi-provider LLM orchestration (OpenAI, Anthropic Claude, Google Gemini, AWS Bedrock, Azure OpenAI, Vertex AI), dynamic model routing, MCP (Model Context Protocol) servers & clients, LangChain, LangGraph, knowledge graphs & ontologies (Neo4j, pgvector), code graphs, RAG, multi-agent (supervisor/ReAct), evals as release gates (LLM-as-judge, record-and-replay), function calling, structured outputs (JSON schema), prompt engineering, inference cost optimization

• **Real-Time AI & Voice:** OpenAI Realtime API, Deepgram (STT), ElevenLabs (TTS), AssemblyAI, Whisper, SignalR, Azure SignalR Service, WebSocket streaming, sub-200ms TTFT

• **Vector DBs & RAG:** Pinecone, Chroma, pgvector, Redis (RediSearch), semantic search, hybrid retrieval, cross-encoder reranking, chunking strategies

• **LLM Eval & Observability:** LangSmith, RAGAS, DeepEval, Langfuse, OpenTelemetry GenAI conventions, red-teaming, faithfulness / correctness scoring

• **Blockchain & Web3:** EVM (Ethereum, Arbitrum, Optimism, Base), Solana, StarkNet, Polkadot/Substrate (FRAME, XCM), MEV infrastructure, Flashbots stack (MEV-Boost, Suave, MEV-Share, PBS, relays), Jito (bundles, BAM, BuilderNet, Agave), Zero-Knowledge proofs (Noir, Barretenberg, Garaga, Cairo), account abstraction (ERC-4337)

• **Web3 Tooling & Clients:** ethers.js, viem, web3.js, @solana/web3.js, Foundry/Forge, Anchor, Hardhat, Geth (reverse-engineered), Reth, REVM (contributor)

• **Distributed Systems:** tokio / async runtimes, low-latency networking (sub-10ms p99), P2P, consensus protocols (GRANDPA / BABE, familiar with Raft), event-driven microservices, fault tolerance, gRPC, Protocol Buffers

• **Cloud & Infrastructure:** AWS (Lambda, Bedrock, ECS, S3, SNS/SQS, EventBridge, CloudFront), Azure (AKS, Service Bus, Cosmos DB, OpenAI Service, AI Search, AI Foundry, SignalR Service, Entra ID), GCP (Vertex AI), Docker, Kubernetes, Terraform, Bicep, ARM, CI/CD (GitHub Actions, Azure DevOps)

• **Databases & Storage:** PostgreSQL (pgvector), MySQL / Aurora, SQL Server / Azure SQL, MongoDB, Cosmos DB, Redis (cache, pub/sub, streams), DynamoDB, ClickHouse

• **Observability & Tooling:** Prometheus, OpenTelemetry, Application Insights, Datadog, Grafana, custom Rust telemetry (50+ production metrics), distributed tracing, structured logging

• **Security & Identity:** OAuth 2.0 / OIDC, Entra ID (Azure AD), IdentityServer / Duende, JWT, mTLS, OWASP Top 10, Zero Trust principles

• **Frontend:** React 18, Next.js 14+ (App Router, React Server Components), React Native (Expo, EAS), Angular, TypeScript, Tailwind, Zustand, Tanstack Query

• **Architecture & Patterns:** Microservices, Domain-Driven Design (tactical + strategic), CQRS, Event Sourcing, Saga (orchestration / choreography), Clean Architecture / Hexagonal, Vertical Slice, polyglot persistence

• **Engineering Practices & Leadership:** TDD, pair programming, code review, ADRs, design reviews, technical interviewing & hiring, mentoring, on-call & incident response, Spec-Driven Development (SDD), AI-driven development workflows

---

## 🎓 Education

- **Polkadot Builder Program** — Polkadot Blockchain Academy _(04/2026)_
- **Systems Engineer** — UAI - Universidad Abierta Interamericana _(01/2017 - 12/2021)_

---

## 🎤 Public Speaking

- 80+ international technical talks at .NET Conf, DevFest, NetCoreConf, vOpen, Global Azure Bootcamp, and meetups across LATAM & Europe
- Topics: Rust, Blockchain & MEV, Zero-Knowledge, .NET, Software Architecture, Design Patterns, AI / LLM systems, Distributed Systems
- Open-source contribution: contributed to the REVM community by reverse-engineering Geth and Reth internals during MEV infrastructure work at Borderless
- Active YouTube channel (youtube.com/@germankuber) with technical deep-dives on Rust, blockchain, AI, and software architecture

---

## 🎭 Performance Arts

- Stage Magic — Member of Círculo Mágico de España, performing live shows with storytelling and misdirection
- Stand-up Comedy — Open mics and comedy nights, developing improvisation under pressure
- Theater & Improv — 10+ years performing live, applied to team facilitation and high-stakes communication
- Hypnosis & Mentalism — Studying suggestion, non-verbal communication, and audience psychology

---

## 🔧 Build

```bash
npm install
npm run build    # Generate PDF + README
npm run pdf      # Generate PDF only
npm run readme   # Generate README only
```

---

<div align="center">
  <sub>⚡ Auto-generated from <a href="resume.html">resume.html</a></sub>
</div>
