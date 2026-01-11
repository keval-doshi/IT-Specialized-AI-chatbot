# import numpy as np
# from dotenv import load_dotenv
# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer

# from langchain_google_genai import GoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableLambda, RunnableSequence

# # ---------------- LOAD ENV ----------------
# load_dotenv()

# # ---------------- MODELS ----------------
# llm = GoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0.7,
#     max_output_tokens=150
# )

# embed_model = SentenceTransformer("all-MiniLM-L6-v2")
# parser = StrOutputParser()

# # ---------------- KNOWLEDGE BASE ----------------
# documents = [
#     {
#         "problem": "How to remove duplicate values in Excel?",
#         "solution": """Steps:
# 1. Select the dataset
# 2. Go to Data tab
# 3. Click Remove Duplicates
# 4. Select columns and press OK"""
#     },
#     {
#         "problem": "How to use VLOOKUP in Excel?",
#         "solution": """Steps:
# 1. Select result cell
# 2. Type =VLOOKUP(lookup_value, table_array, col_index, FALSE)
# 3. Press Enter"""
#     },
#     {
#         "problem": "How to freeze top row in Excel?",
#         "solution": """Steps:
# 1. Go to View tab
# 2. Click Freeze Panes
# 3. Select Freeze Top Row"""
#     },
#     {
#         "problem": "How to apply conditional formatting in Excel?",
#         "solution": """Steps:
# 1. Select cells
# 2. Go to Home tab
# 3. Click Conditional Formatting
# 4. Choose a rule"""
#     }
# ]

# doc_embeddings = embed_model.encode(
#     [doc["problem"] for doc in documents]
# )

# # ---------------- PROMPTS ----------------
# query_refine_prompt = PromptTemplate(
#     template="Rewrite the following Excel question clearly:\n{query}",
#     input_variables=["query"]
# )

# answer_prompt = PromptTemplate(
#     template="""
# You are an Excel assistant.
# Answer ONLY using the steps below.

# Problem:
# {problem}

# Solution:
# {solution}
# """,
#     input_variables=["problem", "solution"]
# )

# # ---------------- RAG FUNCTIONS ----------------
# def retrieve_solution(query: str):
#     query_embedding = embed_model.encode([query])
#     similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
#     best_index = np.argmax(similarities)
#     return documents[best_index]

# # ---------------- CHAIN ----------------
# excel_chain = RunnableSequence(
#     RunnableLambda(lambda q: {"query": q}),
#     query_refine_prompt,
#     llm,
#     parser,
#     RunnableLambda(
#         lambda refined_query: {
#             **retrieve_solution(refined_query),
#             "query": refined_query
#         }
#     ),
#     answer_prompt,
#     llm,
#     parser
# )

# # ---------------- RUN ----------------
# result = excel_chain.invoke("how do i remove repeated values in excel")
# print(result)







import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence

from fastapi.middleware.cors import CORSMiddleware

# ---------------- LOAD ENV ----------------
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_output_tokens=150
)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
parser = StrOutputParser()

# ---------------- KNOWLEDGE BASE ----------------
documents = [
    {
        "problem": "How to remove duplicate values in Excel?",
        "solution": """Steps:
1. Select the dataset
2. Go to Data tab
3. Click Remove Duplicates
4. Select columns and press OK"""
    },
    {
        "problem": "How to use VLOOKUP in Excel?",
        "solution": """Steps:
1. Select result cell
2. Type =VLOOKUP(lookup_value, table_array, col_index, FALSE)
3. Press Enter"""
    },
    {
        "problem": "How to delete VLOOKUP in Excel",
        "solution": """Steps:
1. Go to View tab
2. Click Freeze Panes
3. Select Freeze Top Row"""
    },
    {
        "problem": "How to apply conditional formatting in Excel?",
        "solution": """Steps:
1. Select cells
2. Go to Home tab
3. Click Conditional Formatting
4. Choose a rule"""
    }
]

doc_embeddings = embed_model.encode(
    [doc["problem"] for doc in documents]
)

# ---------------- PROMPTS ----------------
query_refine_prompt = PromptTemplate(
    template="Rewrite the following Excel question clearly:\n{query}",
    input_variables=["query"]
)

answer_prompt = PromptTemplate(
    template="""
You are an Excel assistant.
Answer ONLY using the steps below.

Problem:
{problem}

Solution:
{solution}
""",
    input_variables=["problem", "solution"]
)

# ---------------- RAG FUNCTION ----------------
def retrieve_solution(query: str):
    query_embedding = embed_model.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    best_index = np.argmax(similarities)
    return documents[best_index]

# ---------------- CHAIN ----------------
excel_chain = RunnableSequence(
    RunnableLambda(lambda q: {"query": q}),
    query_refine_prompt,
    llm,
    parser,
    RunnableLambda(
        lambda refined_query: {
            **retrieve_solution(refined_query),
            "query": refined_query
        }
    ),
    answer_prompt,
    llm,
    parser
)

# ---------------- API SCHEMA ----------------
class ChatRequest(BaseModel):
    query: str

# ---------------- API ENDPOINT ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    answer = excel_chain.invoke(req.query)
    return {"response": answer}

