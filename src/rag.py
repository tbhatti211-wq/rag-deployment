# src/rag.py
import argparse
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document

from utils import get_env, sanitize_text

load_dotenv()
STORE_DIR = Path("store/faiss")

def get_embeddings() -> Embeddings:
    backend = get_env("EMBEDDINGS_BACKEND", "LOCAL").upper()
    if backend == "OPENAI":
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        return OpenAIEmbeddings(model=get_env("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
                                api_key=get_env("OPENAI_API_KEY"))
    else:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=get_env("LOCAL_EMBED_MODEL", "all-MiniLM-L6-v2"))

def get_llm():
    backend = get_env("EMBEDDINGS_BACKEND", "LOCAL").upper()
    if backend == "OPENAI":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=get_env("OPENAI_API_KEY"))
    else:
        # Simple fallback: use a basic extractive response from sources if no LLM
        # (So LOCAL mode still returns useful text without a heavy model.)
        return None

def synthesize_answer(query: str, docs: list[Document], llm):
    if llm is None:
        # Concatenate top docs as a minimal answer
        combined = " ".join([d.page_content for d in docs])[:1200]
        return f"(LOCAL MODE) Top sources say: {sanitize_text(combined)}"
    else:
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        prompt = PromptTemplate.from_template(
            "You are a helpful assistant. Use ONLY the provided context to answer.\n"
            "If the answer isn't in the context, say you don't know.\n\n"
            "Question: {question}\n\n"
            "Context:\n{context}\n\n"
            "Answer concisely with citations."
        )
        context = "\n\n---\n\n".join([d.page_content for d in docs])
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(question=query, context=context)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", type=str, help="Your question")
    args = parser.parse_args()

    if not STORE_DIR.exists():
        raise SystemExit("FAISS store not found. Run: python src/build_index.py")

    embeddings = get_embeddings()
    vs = FAISS.load_local(str(STORE_DIR), embeddings, allow_dangerous_deserialization=True)

    # retrieve top-k chunks
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    docs = retriever.get_relevant_documents(args.question)

    llm = get_llm()
    answer = synthesize_answer(args.question, docs, llm)

    print("\n=== ANSWER ===")
    print(sanitize_text(answer))
    print("\n=== SOURCES ===")
    for i, d in enumerate(docs, 1):
        meta = d.metadata or {}
        source = meta.get("source", "unknown")
        print(f"{i}. {source}")

if __name__ == "__main__":
    main()