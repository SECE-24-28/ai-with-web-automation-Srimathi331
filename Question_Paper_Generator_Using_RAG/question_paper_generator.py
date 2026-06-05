import os
from dotenv import load_dotenv

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from google import genai


# ====================================================
# LOAD API KEY
# ====================================================

load_dotenv()

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ====================================================
# LOAD PDF
# ====================================================

pdf_path = "ai_syllabus.pdf"

reader = PdfReader(pdf_path)

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"


print("\nPDF Loaded Successfully")
print("Characters:", len(full_text))


# ====================================================
# CHUNKING
# ====================================================

chunk_size = 500

chunks = []

for i in range(0, len(full_text), chunk_size):
    chunk = full_text[i:i + chunk_size]
    chunks.append(chunk)

print("Total Chunks:", len(chunks))


# ====================================================
# EMBEDDING MODEL
# ====================================================

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Embedding Model Loaded")


# ====================================================
# CHROMADB
# ====================================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

try:
    chroma_client.delete_collection("syllabus")
except:
    pass

collection = chroma_client.create_collection(
    name="syllabus"
)

print("Chroma Collection Created")


# ====================================================
# STORE EMBEDDINGS
# ====================================================

for idx, chunk in enumerate(chunks):

    embedding = embedding_model.encode(
        chunk
    ).tolist()

    collection.add(
        ids=[str(idx)],
        embeddings=[embedding],
        documents=[chunk]
    )

print("Embeddings Stored in ChromaDB")


# ====================================================
# USER INPUT
# ====================================================

print("\n==============================")
print("QUESTION PAPER GENERATOR")
print("==============================\n")

pattern = input(
    "Enter Question Paper Pattern:\n\n"
)

# Example:
#
# Part A:
# 10 Questions x 2 Marks
#
# Part B:
# 5 Questions x 13 Marks
#
# Cover all units.


# ====================================================
# RETRIEVAL
# ====================================================

query_embedding = embedding_model.encode(
    pattern
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

retrieved_chunks = "\n\n".join(
    results["documents"][0]
)

print("\nRelevant Syllabus Retrieved")


# ====================================================
# PROMPT
# ====================================================

prompt = f"""
You are an experienced university examiner.

Below is the syllabus content.

SYLLABUS:
{retrieved_chunks}

QUESTION PAPER PATTERN:
{pattern}

Instructions:

1. Follow the pattern exactly.
2. Cover all syllabus units.
3. Create meaningful questions.
4. Avoid duplicate questions.
5. Include section headings.
6. Generate a complete question paper.
"""


# ====================================================
# GEMINI GENERATION
# ====================================================

response = client_gemini.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n")
print("=" * 80)
print("GENERATED QUESTION PAPER")
print("=" * 80)
print("\n")

print(response.text)