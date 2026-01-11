from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.query_engine import query_knowledge_base

app = FastAPI(
    title="Company Internal Chatbot",
    version="1.0.0"
)

# ===============================
# CORS CONFIG (VERY IMPORTANT)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Request Model
# ===============================
class ChatRequest(BaseModel):
    query: str

# ===============================
# Health Check
# ===============================
@app.get("/")
def health():
    return {"status": "running"}

# ===============================
# Chat Endpoint
# ===============================
@app.post("/chat")
def chat(req: ChatRequest):
    return query_knowledge_base(req.query)
