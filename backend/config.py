from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ===============================
# PATHS
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
FAISS_INDEX_DIR = EMBEDDINGS_DIR / "faiss_index"

# ===============================
# GEMINI CONFIG
# ===============================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ❌ DO NOT CRASH SERVER HERE
# Let Gemini fail only when called
# ===============================
# RETRIEVAL CONFIG
# ===============================
SIMILARITY_THRESHOLD = 0.6
TOP_K_RESULTS = 1

