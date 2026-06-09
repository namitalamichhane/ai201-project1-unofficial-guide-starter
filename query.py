import os
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean, chunk_text
from dotenv import load_dotenv

load_dotenv()

# Set up models
model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Rebuild ChromaDB collection
client = chromadb.Client()
collection = client.get_or_create_collection("unofficial_guide")

# Load and embed if empty
if collection.count() == 0:
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
    texts = [c["text"] for c in all_chunks]
    ids = [c["id"] for c in all_chunks]
    metadatas = [{"source": c["source"]} for c in all_chunks]
    embeddings = model.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings,
                   ids=ids, metadatas=metadatas)

def ask(question, k=4):
    # Retrieve relevant chunks
    query_embedding = model.encode([question]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    context = "\n\n".join(chunks)

    # Generate grounded response
    prompt = f"""Answer the question using ONLY the information in the provided documents. 
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Always cite which document your answer comes from.

Documents:
{context}

Question: {question}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": list(set(sources))
    }