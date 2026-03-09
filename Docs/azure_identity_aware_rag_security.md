# Azure Identity‑Aware RAG Security

When we started thinking about security for retrieval‑augmented systems in
Azure, one observation kept coming back: the vector index is not a safe
place to make access decisions. Search products such as Azure AI Search
are built for relevance, not for enforcing who can see what. Treating the
index as an authorization engine is a recipe for disaster.

This document explains the mindset and architecture that kept our
enterprise deployment from becoming a data leak.

---

## Why you must authorize **after** you retrieve

It’s tempting to hope that by segmenting documents in separate indexes or
using filters you can hide sensitive material from the model. In practice
the only thing the retriever can guarantee is that it will return
something relevant to the query. There is no concept of permissions inside
the embeddings.

So the moment a query returns chunks of text, those chunks must be treated
as untrusted. They are merely candidates. Before you ever hand context to
a large language model, an authorization check against the actual
business data store needs to occur.

### How the flow works

1.  A user signs in with Microsoft Entra ID and receives a token.
2.  Our orchestrator service exchanges that token for an on‑behalf‑of
    (OBO) token so it can act on the user’s behalf.
3.  The orchestrator sends the user’s query to Azure AI Search, which
    returns a ranked set of document fragments.
4.  **Each fragment is then validated against the source of truth** – the
    system that actually controls access:
    * SharePoint/Teams ACLs
    * Blob storage RBAC rules
    * SQL database permissions
    * Group membership through the Graph API
5.  Only those fragments that pass the authorization check are stitched
    together and forwarded to the LLM.

The difference between this and a naive architecture is subtle but
critical: authorization is performed by a component that understands the
organization’s real security model, not by Azure AI Search.

A simple diagram captures the sequence:

```
User → Entra ID → Orchestrator (OBO) → AI Search → Auth service →
filtered context → Azure OpenAI
```

---

## Why this matters in multi‑agent designs

Once you start combining a document‑retrieval agent with other
capabilities – for example, a SQL agent that can run queries against the
corporate database – the stakes escalate. Imagine a marketing analyst
asking a seemingly innocent question. The retriever might bring back HR
policies, IT playbooks and, via the SQL agent, financial figures.

There is nothing in the model that understands which domain those pieces
of information belong to. If all of them are handed to the LLM together,
the output can become a mash‑up containing sensitive data from areas the
user should never see.

We saw this scenario during PoCs: a single, poorly authorized call could
expose salary tables or legal documents. In a regulated environment such
as banking or healthcare, that is an intolerable compliance risk. The SQL
agent in particular becomes a high‑value attack surface if it is allowed
to execute queries on behalf of an unauthorized user.

This is why an intermediate authorization layer isn’t just nice to have –
it is the guardrail that prevents cross‑domain data leakage.

---

## Recommended Azure design: add a Policy Enforcement Point

Based on those lessons, our recommended pattern introduces a dedicated
component – the RAG Policy Enforcement Point (PEP).

The PEP lives between the retriever and the model. Its job is to:

* verify the user’s permissions using the real security sources;
* filter out any chunks the user shouldn’t see;
* enforce zones (INT/UAT/PRD) and zero‑trust principles.

In practical terms the PEP is a small service with access to the Graph API
and whatever ACL/RBAC APIs are required. It doesn’t care about embeddings
or similarity scores; it only cares about “can this user read this blob?”

A high‑level architecture looks like this:

```
User → Entra ID → Orchestrator (OBO token) → Retriever (Azure AI Search)
       ↓
   Authorization Service
     ├─ Graph groups
     ├─ SharePoint ACLs
     ├─ Storage RBAC
     └─ SQL permissions
       ↓
   Filtered context → Azure OpenAI
```

Having this explicit PEP made audits straightforward: we could show
security teams exactly how permissions were enforced and where logs
existed.

---

## The golden rule

A secure RAG system:

* ❌ never trusts the vector store for access control
* ✅ always enforces authorization at the business source level

In other words, treat the retriever as a relevance service and keep your
security logic where it belongs – next to the data. This pattern is what
we call **Identity‑Aware RAG**, and it is the foundation of any
enterprise‑grade deployment.

Applied to multiple agents and regulated workloads, it’s not optional.
It’s the difference between a useful assistant and a compliance headache.
