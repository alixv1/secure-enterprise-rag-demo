# What it actually takes to deploy a secure RAG system in a real enterprise

Over the past year, I worked on deploying an internal knowledge assistant powered by a large language model inside a regulated enterprise environment.

Like many organizations, we started with a simple experiment: connect an LLM to a chat interface and let users ask questions. Technically, it worked immediately.

Operationally, it failed.

The issue was not model quality, response latency, or integration complexity. The real problem was trust. After only a few incorrect or unverifiable answers, users simply stopped relying on it.

This experience forced us to realize something important:

> Deploying an LLM in an enterprise is not primarily an AI problem. It is a knowledge and reliability problem.

---

## Why a simple chatbot fails in enterprises

In consumer settings, approximate answers are often acceptable. In an enterprise environment, they are not.

Employees do not use an internal assistant for curiosity — they use it to perform tasks. Procedures, operational rules, and compliance constraints depend on the accuracy of the information provided.

A single confident but incorrect answer can permanently damage adoption. After that point, the tool is perceived as interesting but unreliable, and people revert to manual processes or colleagues.

### A concrete example: the debt hallucination

Early on, a treasury analyst asked the assistant: *"What is the current status of our Fund 1 exposure to Italian government bonds?"*

The assistant responded with confidence: *"Your portfolio holds €2.3M in Italian debt maturing in Q4 2024, with an estimated yield of 3.8%."*

The problem: the fund held no Italian bonds. The assistant had fabricated both the amount and the maturity date.

When the analyst verified this against actual holdings, the reaction was immediate and predictable. Within hours, word spread through the finance team. The assistant was not just unreliable — it was dangerously confident while being wrong.

For weeks afterward, even simple, factual questions went unanswered. Users defaulted to spreadsheets and manual checks instead.

That single hallucination cost us months of adoption momentum.

It taught us an uncomfortable truth: a system that occasionally hallucinates is worse than no system at all. Users would rather spend time on manual processes than risk acting on information they cannot verify.

This experience made one thing crystal clear: in regulated environments, confidence without accuracy is a liability, not a feature.

---

## The real problem: enterprise knowledge

We quickly understood that the model itself was not the main limitation.

The real limitation was knowledge locality.

Our organization’s knowledge did not live on the internet. It lived in internal procedures, operational documentation, and evolving operational practices. The LLM had no access to that information and therefore tried to compensate — which manifested as hallucinations.

The problem was not intelligence.

The problem was grounding.

---

## Why we moved to a RAG architecture

To address this, we implemented a Retrieval-Augmented Generation (RAG) architecture.

The objective was not to improve model creativity or stylistic quality.  
The objective was reliability.

By retrieving relevant internal documentation and constraining the model to answer based on explicit context, the assistant moved from *“knowledge generator”* to *“knowledge interface.”*

> RAG was not a technical optimization. It was a governance mechanism.

### Our RAG implementation

**Data sources**
We integrated knowledge retrieval from golden source websites and extracted structured data from internal PDF documentation. This ensured we operated from authoritative, up-to-date sources rather than relying on model training data.

**Indexing & embeddings**
All documents were processed and indexed in Azure AI Search, enabling semantic retrieval. Embeddings allowed the system to match user queries against relevant documentation with both keyword and meaning-based precision.

**Model orchestration**
We implemented a model router that evaluates incoming queries and selects the most appropriate LLM for the task. Different questions benefit from different model characteristics — some require conciseness, others need detailed reasoning.

**Environment isolation**
Given regulatory requirements, we maintained strict separation between data environments. Access control was enforced at the retrieval layer, ensuring users only received answers grounded in documents they were authorized to access.

This architecture transformed the system from a general-purpose chatbot into a controlled, governed knowledge interface tied directly to enterprise sources of truth.



**Ingestion pipeline**
Documents from web sources and internal repositories are automatically ingested. PDFs from external websites are extracted, processed, and indexed into Azure AI Search. This ensures the retrieval layer always operates on current, authoritative sources while maintaining document lineage for traceability.

**Authorization enforcement**
Before documents reach the context builder, the authorization layer validates user permissions against multiple identity sources — SharePoint, Blob Storage, SQL databases, and Microsoft Graph groups. Only authorized documents are returned to the LLM.

**System architecture**
The complete architecture is visualized in [Architecture/AzureArchitecture.svg](../Architecture/AzureArchitecture.svg), which shows the integration of data sources, indexing, retrieval, and authorization layers.

---

## The real challenges (beyond the architecture)

### 1. Access control

In a real organization, not every employee can access every document.

An assistant that ignores access rights is not a productivity tool — it is a data leak.

One of the first architectural constraints was ensuring that document retrieval respected existing permission models.

We implemented environment isolation, role-based access control, and regulatory compliance checks. For detailed security architecture, see [azure_identity_aware_rag_security.md](./azure_identity_aware_rag_security.md).

---

### 2. Sensitive data & user perception

Interestingly, many users were not initially worried about hallucinations.

They were worried about where their data was going.

- Are my questions logged?
- Is sensitive information exposed externally?
- Can this system leak confidential material?

Trust was as much about perception as it was about architecture.

---

### 3. Hallucinations and traceability

Even with RAG, hallucinations do not completely disappear.

What changes is detectability.

Providing document citations and allowing users to trace answers back to source material dramatically increased confidence.

We also learned that saying *“I don’t know”* is more valuable than guessing.

---

## Adoption: the under estimated challenge

The deployment succeeded not because the system was technically perfect, but because it was introduced progressively.

Workshops, demonstrations, and concrete use cases mattered more than model parameters.

The biggest risk was not technical failure.

> The biggest risk was indifference.
We introduced the system gradually, starting with a subset of trusted data sources and a small group of key business users. Rather than a broad rollout, we built the tool *with* the team, not *for* them. Training sessions were hands-on, focused on real workflows rather than abstract concepts.

Real adoption came later — when two things aligned:

First, users witnessed consistent accuracy. The assistant needed to prove itself on concrete tasks before skepticism turned into confidence.

Second, we made the evidence visible. By displaying source citations and allowing users to trace each answer back to specific documents, we transformed the assistant from a black box into a verifiable tool.

Trust followed predictably: once users could see *where* the answer came from, they stopped asking *if* it was correct.

---

## What I learned about enterprise AI

This project changed my understanding of applied AI in organizations.

Some key takeaways:

- Reliability matters more than raw model performance.
- Traceability increases trust more than fluency.
- Governance and UX are deeply connected.
- AI adoption is a workflow transformation problem, not a machine learning problem.

Most importantly:

> Organizations do not adopt AI because it is impressive.  
> They adopt it when it becomes dependable.

---

## Results

After implementing the RAG architecture, something shifted.

The metrics told one story: hallucinations on operational queries dropped to near zero. Response time stabilized under 2 seconds. The system scaled to support hundreds of daily queries across finance, operations, and compliance teams.

But the real result was simpler: people started using it.

What changed was not the technology. It was what the technology enabled.

Users stopped fact-checking every answer. Treasury analysts referenced the assistant in their workflows. Compliance officers used it to verify procedural questions without escalating to subject matter experts. The tool moved from "interesting experiment" to "part of how we work."

The most telling metric was not in the logs. It was in the calendar invites that stopped appearing — the meetings that no longer happened because an answer was now verifiable and immediate.

Adoption was not broad or immediate. It grew team by team, use case by use case, as confidence accumulated through consistent accuracy and visible sources.

That was the real result: not a system that works perfectly, but one that people trust enough to depend on.



## Final thoughts

Deploying LLM systems in enterprises is often presented as a machine learning challenge.

In practice, it is an architecture, trust, and change management challenge.

The technical stack matters — but long-term success depends on how well the system integrates into real operational workflows.

Applied AI is not about showcasing model capabilities.

It is about making intelligence usable.