# Enterprise RAG Architecture

This repository contains a reference implementation and guidance for
building a **secure, enterprise‑grade Retrieval‑Augmented Generation (RAG)**
platform on Azure. The code and documentation were developed during a
production deployment inside a heavily regulated organization where the
primary challenges were not model quality but data governance, access
control, and user trust.

You can use these materials to understand the architectural patterns,
technologies and operational lessons required to move from a simple
chatbot prototype to a system that complies with enterprise security
policies and actually gets used by employees.

---

## Key topics covered

* **Identity‑aware retrieval** – never trust the vector index; always
authorize based on the original data store.
* **Secure context construction** – dynamically filter retrieved chunks and
construct the prompt so the LLM only sees what the user is allowed to see.
* **Enterprise access control** – integrate with Entra ID, SharePoint ACLs,
Blob/SQL RBAC, and Graph API for real‑time permission checks.
* **Hallucination mitigation** – provide citations, encourage “I don’t
know” responses, and design the system as a knowledge interface rather
than a creative generator.
* **AI adoption in organizations** – planning for workshops, change
management, and the cultural shift from curiosity to task‑oriented use.

---

## Architecture

The solution is centred around an orchestrator service that handles
authentication (OBO flow), queries Azure AI Search for relevant document
fragments, and then passes the results through a **Policy Enforcement
Point (PEP)** before feeding them to Azure OpenAI. The PEP consults the
original sources (SharePoint, Blob storage, etc.) to ensure each
chunk is authorized.

A simple diagram in the repo illustrates this flow; see `Architecture/AzureArchitecture.svg`.

---

## Security

For a complete discussion of our security rationale and the
Identity‑Aware RAG concept, see `azure_identity_aware_rag_security.md`.

Key points:

* Do not rely on Azure AI Search for authorization.
* Treat all retrieved content as untrusted until validated.
* Enforce zero‑trust and domain separation to prevent cross‑domain leaks.

---

## Lessons learned

During the project we discovered that technical architecture is the
least of the battle. The real problems were:

1. **Knowledge locality** – the LLM has no inherent understanding of
   your internal procedures, so retrieval is essential for grounding.
2. **Access control** – a system that ignores permissions is a liability,
   not a productivity tool.
3. **User perception** – employees worry about data privacy more than
   hallucinations; transparent auditing and tracing builds trust.
4. **Adoption** – successful deployment requires education, pilots, and
   incremental rollout; without it users will simply ignore the assistant.

This repo captures the patterns and reference code that turned those
lessons into a repeatable architecture.
