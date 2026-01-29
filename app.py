# app.py
"""
Flask API for RAG Assistant - Phase 3: Web API Service
Deploy the RAG system as a web service with REST API endpoints.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our RAG components
from src.rag import get_embeddings, get_llm, is_technical_question
from src.general_responses import get_general_response
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.utils import sanitize_text

load_dotenv()

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
CORS(app)  # Enable CORS for web access

# Global variables for the RAG system
STORE_DIR = Path("store/faiss")
embeddings = None
vs = None
llm = None
retriever = None

def initialize_rag():
    """Initialize the RAG system components"""
    global embeddings, vs, llm, retriever

    if not STORE_DIR.exists():
        raise RuntimeError("FAISS store not found. Run: python src/build_index.py")

    embeddings = get_embeddings()
    vs = FAISS.load_local(str(STORE_DIR), embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()

# Initialize on startup
initialize_rag()

@app.route('/', methods=['GET'])
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "RAG Assistant API is running",
        "version": "3.0-api",
        "topics": ["machine learning", "web development", "data science", "cloud computing"]
    })

@app.route('/ask', methods=['POST'])
def ask_question():
    """Main endpoint for asking questions"""
    try:
        # Get question from request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "error": "Missing question parameter",
                "usage": {"question": "Your question here"}
            }), 400

        question = data['question'].strip()
        if not question:
            return jsonify({
                "error": "Question cannot be empty"
            }), 400

        # Determine question type
        question_type = "technical" if is_technical_question(question) else "general"

        # Get answer based on question type
        if question_type == "technical":
            # Use RAG for technical questions
            docs = retriever.get_relevant_documents(question)

            # Check if we have relevant documents
            relevant_docs = []
            query_words = set(question.lower().split())
            for doc in docs:
                content_lower = doc.page_content.lower()
                if any(word in content_lower for word in query_words if len(word) > 2):
                    relevant_docs.append(doc)

            if not relevant_docs:
                answer = get_general_response(question)
                sources = []
            else:
                # Generate answer from relevant docs
                if llm is None:
                    # Local mode
                    combined = " ".join([d.page_content for d in relevant_docs[:3]])[:1000]
                    answer = f"Based on my knowledge: {sanitize_text(combined)}"
                else:
                    # Use LLM for synthesis
                    from langchain.prompts import PromptTemplate
                    from langchain.chains import LLMChain

                    prompt = PromptTemplate.from_template(
                        "You are a knowledgeable assistant. Answer the question using ONLY the provided context.\n"
                        "Structure your answer clearly with:\n"
                        "1. Direct answer to the question\n"
                        "2. Key supporting details\n"
                        "3. Source references\n\n"
                        "Question: {question}\n\n"
                        "Context:\n{context}\n\n"
                        "Answer:"
                    )

                    context = "\n\n---\n\n".join([f"Source: {d.metadata.get('source', 'Unknown')}\n{d.page_content}" for d in relevant_docs[:3]])
                    chain = LLMChain(llm=llm, prompt=prompt)
                    answer = chain.run(question=question, context=context)

                # Format sources
                sources = []
                for i, doc in enumerate(relevant_docs[:3], 1):
                    meta = doc.metadata or {}
                    sources.append({
                        "id": i,
                        "source": Path(meta.get("source", "unknown")).name,
                        "page": meta.get("page", "N/A"),
                        "preview": doc.page_content[:100].replace('\n', ' ')
                    })
        else:
            # Use general response handler for non-technical questions
            answer = get_general_response(question)
            sources = []

        return jsonify({
            "question": question,
            "answer": sanitize_text(answer),
            "question_type": question_type,
            "sources": sources,
            "source_count": len(sources)
        })

    except Exception as e:
        app.logger.error(f"Error processing question: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/topics', methods=['GET'])
def get_topics():
    """Get available topics"""
    return jsonify({
        "topics": [
            {
                "name": "Machine Learning",
                "description": "AI, algorithms, models, training",
                "examples": ["What is supervised learning?", "How does neural network work?"]
            },
            {
                "name": "Web Development",
                "description": "Frontend, backend, frameworks, APIs",
                "examples": ["How does React work?", "What is Node.js?"]
            },
            {
                "name": "Data Science",
                "description": "Analysis, visualization, statistics",
                "examples": ["What is data cleaning?", "How to use pandas?"]
            },
            {
                "name": "Cloud Computing",
                "description": "AWS, Azure, deployment, scalability",
                "examples": ["What is serverless?", "How does Docker work?"]
            }
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
