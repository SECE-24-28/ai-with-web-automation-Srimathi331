# Hybrid RAG PDF Analyzer

A Retrieval-Augmented Generation (RAG) application that enables users to ask questions about PDF documents using Hybrid Search (Semantic + Keyword Retrieval), FAISS Vector Database, Hugging Face Embeddings, and Groq LLMs.

---

## Overview

This project extracts text from PDF documents, converts the content into vector embeddings, stores them in a FAISS vector database, and retrieves relevant information using a hybrid retrieval approach.

The retrieved context is then passed to a Groq-hosted Large Language Model (LLM) to generate accurate and context-aware responses.

---

## Problem Statement

Large Language Models cannot directly process lengthy PDF documents efficiently.

Challenges:

* Limited context window
* High token consumption
* Slow response generation
* Hallucination when document context is unavailable

This project solves these issues using Retrieval-Augmented Generation (RAG).

---

## Workflow

### Step 1: PDF Loading

The PDF document is loaded using `pdfplumber`.

```text
PDF
 ↓
Text Extraction
```

---

### Step 2: Text Chunking

The extracted text is split into smaller overlapping chunks.

Purpose:

* Preserve context
* Improve retrieval quality
* Reduce embedding size

```text
Document
 ↓
Chunk 1
Chunk 2
Chunk 3
...
```

---

### Step 3: Embedding Generation

Each chunk is converted into a dense vector representation using:

```text
all-MiniLM-L6-v2
```

from Hugging Face Sentence Transformers.

```text
Text Chunk
 ↓
Embedding Vector
```

---

### Step 4: Vector Storage

The generated embeddings are stored in a FAISS vector database.

```text
Embeddings
 ↓
FAISS Index
```

FAISS enables efficient similarity search over high-dimensional vectors.

---

### Step 5: Sparse Retrieval (Keyword Search)

TF-IDF is used to perform traditional keyword-based retrieval.

Benefits:

* Captures exact keyword matches
* Improves retrieval precision

```text
Query
 ↓
TF-IDF Search
```

---

### Step 6: Dense Retrieval (Semantic Search)

The query is embedded using the same embedding model and searched against FAISS.

Benefits:

* Understands semantic meaning
* Finds relevant content even when keywords differ

```text
Query
 ↓
Embedding
 ↓
FAISS Similarity Search
```

---

### Step 7: Hybrid Search

Results from:

* TF-IDF Search
* FAISS Semantic Search

are merged together.

```text
Keyword Search
       +
Semantic Search
       ↓
 Hybrid Retrieval
```

This improves retrieval accuracy compared to using either method alone.

---

### Step 8: Context Construction

The top retrieved chunks are combined into a single context.

```text
Retrieved Chunks
 ↓
Context
```

---

### Step 9: LLM Response Generation

The context and user query are sent to a Groq-hosted LLM.

Example:

```text
Context + Question
        ↓
     Groq LLM
        ↓
      Answer
```

---

## Architecture

```text
                ┌──────────────┐
                │     PDF      │
                └──────┬───────┘
                       │
                       ▼
               Text Extraction
                       │
                       ▼
                  Chunking
                       │
                       ▼
               Embedding Model
           (all-MiniLM-L6-v2)
                       │
                       ▼
                FAISS Index
                       │
       ┌───────────────┴───────────────┐
       │                               │
       ▼                               ▼
 Semantic Search               TF-IDF Search
       │                               │
       └───────────────┬───────────────┘
                       ▼
                 Hybrid Search
                       │
                       ▼
              Retrieved Context
                       │
                       ▼
                   Groq LLM
                       │
                       ▼
                 Final Answer
```

---

## Technologies Used

| Technology            | Purpose               |
| --------------------- | --------------------- |
| Python                | Programming Language  |
| pdfplumber            | PDF Text Extraction   |
| Sentence Transformers | Embedding Generation  |
| all-MiniLM-L6-v2      | Embedding Model       |
| FAISS                 | Vector Database       |
| TF-IDF                | Sparse Retrieval      |
| Groq API              | LLM Inference         |
| NumPy                 | Numerical Computation |
| Scikit-learn          | TF-IDF Implementation |

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Hybrid_Rag
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run the Project

```bash
python hybrid_rag_pdf__analyzer.py
```

---

## Example Query

```text
What are the key responsibilities of an AI Engineer?
```

### Example Output

```text
AI Engineers are responsible for building,
deploying, optimizing, and maintaining AI
systems using machine learning models,
vector databases, and LLM applications.
```

---

## Features

* PDF Question Answering
* Retrieval-Augmented Generation (RAG)
* Hybrid Search
* Semantic Retrieval
* Keyword Retrieval
* FAISS Vector Database
* Groq LLM Integration
* Modular Architecture

---

## Future Improvements

* BM25 Retrieval
* Query Expansion
* Cross-Encoder Re-ranking
* Agentic RAG
* Streamlit UI
* Multi-PDF Support
* Conversation Memory
* Persistent FAISS Storage

---

## Author

AI Engineer & Software Engineer Portfolio Project
