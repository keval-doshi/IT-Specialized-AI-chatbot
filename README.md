Folder Structure
chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── __init__.py
│   │
│   ├── config.py
│   ├── llm.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── query_engine.py
│   ├── fallback.py
│
├── data/
│   ├── microsoft_365.md
│   ├── outlook.md
│
├── vector_store/
│   └── faiss/
│       ├── index.faiss
│       └── index.pkl
│
├── frontend/
│   ├── a.html

