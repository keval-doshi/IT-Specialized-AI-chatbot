from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.llm_fallback import LLMFallback
from backend.config import FAISS_INDEX_DIR, SIMILARITY_THRESHOLD, TOP_K_RESULTS

# ===============================
# FREE LOCAL EMBEDDINGS (NO API)
# ===============================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ===============================
# Load FAISS Index
# ===============================
vectorstore = FAISS.load_local(
    str(FAISS_INDEX_DIR),
    embeddings,
    allow_dangerous_deserialization=True
)

# ===============================
# LLM Fallback (Gemini optional)
# ===============================
llm_fallback = LLMFallback()

# ===============================
# Query Function
# ===============================
def query_knowledge_base(user_query: str):

    results = vectorstore.similarity_search_with_score(
        user_query,
        k=TOP_K_RESULTS
    )

    if not results:
        return {
            "source": "llm",
            "solution": llm_fallback.get_response(user_query)
        }

    top_doc, score = results[0]
    confidence= round(1 / (1 + float(score)), 2)
    if confidence >= SIMILARITY_THRESHOLD:
        return {
            "source": "knowledge_base",
            "tool": top_doc.metadata.get("tool"),
            "problem": top_doc.metadata.get("problem"),
            "solution": top_doc.page_content,
            "confidence": round(1 / (1 + float(score)), 2)

        }

    return {
        "source": "llm",
        "solution": llm_fallback.get_response(user_query)
    }
