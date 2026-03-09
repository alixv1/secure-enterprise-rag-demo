
"""
rag_pipeline_example.py

A simplified example of an Identity‑Aware RAG pipeline with a Policy
Enforcement Point (PEP). The goal is to demonstrate the architecture:

User → Auth → Retriever → Policy Enforcement → LLM

This is NOT production code. It illustrates where authorization checks
must occur before sending context to the LLM.
"""

from typing import List, Dict


# -----------------------------
# Mock user + document store
# -----------------------------

USERS = {
    "alice": {"groups": ["marketing"]},
    "bob": {"groups": ["hr"]},
}

DOCUMENTS = [
    {"id": 1, "text": "Marketing strategy for 2025", "allowed_groups": ["marketing"]},
    {"id": 2, "text": "Employee salary bands", "allowed_groups": ["hr"]},
    {"id": 3, "text": "Public company values document", "allowed_groups": ["marketing", "hr"]},
]


# -----------------------------
# Retriever (simulated)
# -----------------------------

def retrieve(query: str) -> List[Dict]:
    """Pretend this is Azure AI Search returning candidate chunks."""
    results = []
    for doc in DOCUMENTS:
        if query.lower() in doc["text"].lower():
            results.append(doc)
    return results


# -----------------------------
# Policy Enforcement Point
# -----------------------------

def authorize(user: str, chunks: List[Dict]) -> List[Dict]:
    """Filter retrieved chunks based on user permissions."""
    user_groups = USERS[user]["groups"]
    allowed = []

    for chunk in chunks:
        if any(group in user_groups for group in chunk["allowed_groups"]):
            allowed.append(chunk)

    return allowed


# -----------------------------
# Mock LLM
# -----------------------------

def call_llm(question: str, context: List[Dict]) -> str:
    """Pretend we send context to Azure OpenAI."""
    combined = "\n".join([c["text"] for c in context])
    return f"QUESTION: {question}\n\nCONTEXT USED:\n{combined}"


# -----------------------------
# Orchestrator
# -----------------------------

def rag_pipeline(user: str, query: str):
    print("User:", user)
    print("Query:", query)

    retrieved = retrieve(query)
    print("\nRetrieved chunks:", retrieved)

    authorized = authorize(user, retrieved)
    print("\nAuthorized chunks:", authorized)

    response = call_llm(query, authorized)
    print("\nLLM RESPONSE")
    print(response)


if __name__ == "__main__":
    rag_pipeline("alice", "strategy")
