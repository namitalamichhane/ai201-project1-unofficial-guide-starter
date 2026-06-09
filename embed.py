import os
import re
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean, chunk_text

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection("unofficial_guide")

# Load, clean, chunk documents
docs = load_documents()
all_chunks = []
for doc in docs:
    cleaned = clean(doc["text"])
    chunks = chunk_text(cleaned)
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "source": doc["source"],
            "text": chunk,
            "id": f"{doc['source']}_{i}"
        })

# Embed and store
texts = [c["text"] for c in all_chunks]
ids = [c["id"] for c in all_chunks]
metadatas = [{"source": c["source"]} for c in all_chunks]

print("Embedding chunks... this may take a minute")
embeddings = model.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

print(f"Stored {len(all_chunks)} chunks in ChromaDB")

# Test retrieval
def retrieve(query, k=4):
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results

# Test with 3 queries
test_queries = [
    "What do students say about Professor Hodges exams?",
    "Which professor is helpful outside of class?",
    "What do students say about homework load?"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    results = retrieve(query)
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"Source: {meta['source']}")
        print(f"Chunk: {doc[:200]}")
        print("---")