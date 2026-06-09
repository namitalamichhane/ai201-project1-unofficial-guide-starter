import os
import re

def load_documents(folder="documents"):
    docs = []
    for fname in os.listdir(folder):
        if fname.endswith(".txt"):
            with open(f"{folder}/{fname}", "r", encoding="utf-8") as f:
                docs.append({"source": fname, "text": f.read()})
    return docs

def clean(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&\w+;', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 20]

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    
    all_chunks = []
    for doc in docs:
        cleaned = clean(doc["text"])
        chunks = chunk_text(cleaned)
        for chunk in chunks:
            all_chunks.append({"source": doc["source"], "text": chunk})
    
    print(f"Total chunks: {len(all_chunks)}")
    print("\n--- 5 Sample Chunks ---")
    for chunk in all_chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(chunk['text'])
        print("---")