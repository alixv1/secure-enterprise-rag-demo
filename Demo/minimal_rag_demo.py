
"""
minimal_rag_demo.py

A tiny end‑to‑end RAG demo showing the key security idea:
ALWAYS filter retrieved context before sending it to the LLM.
"""

documents = [
    {"text": "Company revenue is 10M", "role": "finance"},
    {"text": "Marketing campaign launches in June", "role": "marketing"},
]

users = {
    "analyst": ["marketing"],
    "cfo": ["finance", "marketing"]
}


def retrieve(query):
    return [d for d in documents if query.lower() in d["text"].lower()]


def policy_filter(user, chunks):
    roles = users[user]
    return [c for c in chunks if c["role"] in roles]


def ask_llm(question, context):
    ctx = " ".join([c["text"] for c in context])
    return f"Answer based on: {ctx}"


def ask(user, question):
    candidates = retrieve(question)
    allowed = policy_filter(user, candidates)
    return ask_llm(question, allowed)


if __name__ == "__main__":
    print("Analyst asking about revenue:")
    print(ask("analyst", "revenue"))
    print()

    print("CFO asking about revenue:")
    print(ask("cfo", "revenue"))
