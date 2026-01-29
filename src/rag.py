# src/rag.py
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
        return HuggingFaceEmbeddings(
            model_name=get_env("LOCAL_EMBED_MODEL", "BAAI/bge-small-en-v1.5"),
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

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
            "You are a knowledgeable assistant. Answer the question using ONLY the provided context.\n"
            "Structure your answer clearly with:\n"
            "1. Direct answer to the question\n"
            "2. Key supporting details\n"
            "3. Source references\n\n"
            "If the context doesn't contain enough information, say so clearly.\n\n"
            "Question: {question}\n\n"
            "Context:\n{context}\n\n"
            "Answer:"
        )

        context = "\n\n---\n\n".join([f"Source: {d.metadata.get('source', 'Unknown')}\n{d.page_content}" for d in docs])
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(question=query, context=context)

def main():
    print("🤖 RAG Assistant - Ask me anything! (Type 'quit' or 'exit' to stop)")
    print("=" * 60)

    if not STORE_DIR.exists():
        raise SystemExit("FAISS store not found. Run: python src/build_index.py")

    embeddings = get_embeddings()
    vs = FAISS.load_local(str(STORE_DIR), embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()

    while True:
        try:
            question = input("\n❓ Your question: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not question:
                continue

            # retrieve top-k chunks
            docs = retriever.get_relevant_documents(question)

            answer = synthesize_answer(question, docs, llm)

            print(f"\n{'='*60}")
            print(f"QUESTION: {question}")
            print(f"{'='*60}")
            print(f"\nANSWER:")
            print(sanitize_text(answer))
            print(f"\n{'='*60}")
            print(f"SOURCES ({len(docs)} retrieved):")
            for i, d in enumerate(docs, 1):
                meta = d.metadata or {}
                source = meta.get("source", "unknown")
                page = meta.get("page", "N/A")
                print(f"{i}. {Path(source).name} (page {page})")
                # Show first 100 chars of content
                preview = d.page_content[:100].replace('\n', ' ')
                print(f"   Preview: {preview}...")
            print(f"{'='*60}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()