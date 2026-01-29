# src/ingest.py
from utils import load_documents, chunk_documents

def main():
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"Loaded {len(docs)} docs; produced {len(chunks)} chunks.")
    for i, c in enumerate(chunks[:3]):
        print(f"Chunk {i+1} preview:", c.page_content[:200].replace("\n"," "), "...")

if __name__ == "__main__":
    main()