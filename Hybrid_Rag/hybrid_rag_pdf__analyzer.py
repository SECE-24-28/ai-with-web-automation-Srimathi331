import os
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from groq import Groq


# =========================
# 1. PDF LOADING
# =========================
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# =========================
# 2. CHUNKING
# =========================
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # overlap for context continuity

    return chunks


# =========================
# 3. EMBEDDINGS MODEL
# =========================
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


def get_embeddings(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings).astype("float32")


# =========================
# 4. FAISS VECTOR STORE
# =========================
def create_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


# =========================
# 5. HYBRID SEARCH SETUP
# =========================
vectorizer = TfidfVectorizer()


def build_tfidf(chunks):
    return vectorizer.fit_transform(chunks)


def hybrid_search(query, chunks, faiss_index, tfidf_matrix, top_k=5):
    # -------- semantic search (FAISS) --------
    query_emb = model.encode([query]).astype("float32")
    _, I = faiss_index.search(query_emb, top_k)
    semantic_results = [chunks[i] for i in I[0]]

    # -------- keyword search (TF-IDF) --------
    query_vec = vectorizer.transform([query])
    scores = (tfidf_matrix @ query_vec.T).toarray().flatten()
    top_indices = np.argsort(scores)[-top_k:][::-1]
    keyword_results = [chunks[i] for i in top_indices]

    # -------- merge results --------
    combined = list(dict.fromkeys(semantic_results + keyword_results))

    return combined


# =========================
# 6. GROQ LLM
# =========================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(context, query):
    prompt = f"""
You are an assistant. Use the context below to answer.

Context:
{context}

Question:
{query}

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

    return response.choices[0].message.content


# =========================
# 7. MAIN PIPELINE
# =========================
def main(pdf_path, query):
    print("📄 Reading PDF...")
    text = extract_text(pdf_path)

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    print("🧠 Creating embeddings...")
    embeddings = get_embeddings(chunks)

    print("📦 Building FAISS index...")
    faiss_index = create_faiss_index(embeddings)

    print("🔤 Building TF-IDF index...")
    tfidf_matrix = build_tfidf(chunks)

    print("🔍 Running hybrid search...")
    retrieved_chunks = hybrid_search(query, chunks, faiss_index, tfidf_matrix)

    context = "\n\n".join(retrieved_chunks)

    print("🤖 Asking Groq LLM...")
    answer = ask_llm(context, query)

    print("\n================ ANSWER ================\n")
    print(answer)


# =========================
# 8. RUN
# =========================
if __name__ == "__main__":
    pdf_path = "AI_Engineer_Roadmap_5_Pages.pdf"   # 🔴 change this
    query = "explain clearly the content present in this document"  # 🔴 change this

    main(pdf_path, query)