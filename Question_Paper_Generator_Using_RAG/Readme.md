Question Paper Generator using RAG
Overview

This project is a Retrieval-Augmented Generation (RAG) based Question Paper Generator that automatically creates question papers from a syllabus PDF.

The system:

Reads the syllabus from a PDF file
Converts syllabus content into embeddings
Stores embeddings in ChromaDB
Retrieves relevant syllabus content based on the question paper pattern
Uses Google's Gemini model to generate a complete question paper

The entire application runs in the terminal and demonstrates the core concepts of a RAG pipeline.

Architecture
Syllabus PDF
      │
      ▼
Text Extraction (PyPDF)
      │
      ▼
Chunking
      │
      ▼
Embeddings (BGE Model)
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Similarity Retrieval
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Generated Question Paper
Features
PDF syllabus processing
Text chunking for efficient retrieval
Semantic embeddings using BAAI BGE model
Persistent vector storage using ChromaDB
Retrieval-Augmented Generation (RAG)
Dynamic question paper generation
User-defined question paper pattern
Terminal-based execution
Technologies Used
Technology	Purpose
Python	Core Programming Language
PyPDF	PDF Text Extraction
Sentence Transformers	Text Embeddings
BAAI/bge-small-en-v1.5	Embedding Model
ChromaDB	Vector Database
Gemini 2.5 Flash	Question Generation
python-dotenv	Environment Variable Management
Project Structure
Question_Paper_Generator_Using_RAG/
│
├── question_paper_generator.py
├── syllabus.pdf
├── .env
├── chroma_db/
└── README.md
Installation
Clone Repository
git clone <repository-url>
cd Question_Paper_Generator_Using_RAG
Install Dependencies
pip install pypdf sentence-transformers chromadb google-genai python-dotenv
Gemini API Setup

Generate an API key from:

https://aistudio.google.com/apikey

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY
How It Works
Step 1: Load Syllabus PDF

The system reads the syllabus PDF and extracts all textual content.

reader = PdfReader(pdf_path)
Step 2: Chunk the Text

The extracted text is divided into smaller chunks.

chunk_size = 500

Chunking helps in:

Better retrieval accuracy
Reduced embedding complexity
Efficient vector search
Step 3: Generate Embeddings

Each chunk is converted into a dense vector representation using:

BAAI/bge-small-en-v1.5

Example:

embedding = model.encode(chunk)

These vectors capture semantic meaning rather than exact keyword matching.

Step 4: Store in ChromaDB

Embeddings and associated text chunks are stored in ChromaDB.

collection.add(
    ids=[str(idx)],
    embeddings=[embedding],
    documents=[chunk]
)

This creates a searchable vector database.

Step 5: Retrieve Relevant Syllabus Content

The question paper pattern entered by the user is embedded and compared against stored vectors.

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

The most relevant syllabus chunks are retrieved.

Step 6: Generate Question Paper

Retrieved syllabus content and the question paper pattern are sent to Gemini.

Example prompt:

SYLLABUS:
<retrieved syllabus>

QUESTION PAPER PATTERN:
<user pattern>

Generate a complete question paper.

Gemini generates a syllabus-aware question paper.

Example Execution
Input
PART A

10 Questions × 2 Marks

PART B

5 Questions × 13 Marks

Cover all units.
Output
PART A (10 × 2 = 20 Marks)

1. Define Artificial Intelligence.
2. What is Machine Learning?
...

PART B (5 × 13 = 65 Marks)

11. Explain supervised learning with examples.
12. Discuss neural network architecture.
...
RAG Workflow
Retrieval Phase
PDF content is embedded
Stored in ChromaDB
Relevant chunks are retrieved
Generation Phase
Retrieved content is combined with the user prompt
Gemini generates the final question paper

This reduces hallucinations and ensures syllabus-based question generation.