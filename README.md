# PGAGI AI Candidate Screening System

An AI-powered role-based candidate screening system that dynamically generates interview questions using a RAG (Retrieval-Augmented Generation) pipeline based on the candidate's resume and selected job role.

---

## Demo Video

[Watch Demo Video](https://your-demo-video-link-here)

---

## System Architecture
## Tech Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Vector Store:** ChromaDB
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **PDF Parsing:** pypdf

---

## RAG Pipeline Design

### 1. Knowledge Ingestion
- PDFs from `knowledge_base/` are loaded using pypdf
- Text is chunked into 1000-character chunks with 200-character overlap to preserve context
- Chunks are embedded using all-MiniLM-L6-v2
- Embeddings stored in ChromaDB with persistent storage

### 2. Retrieval Mechanism
- Query is constructed from candidate skills + selected role
- Top-5 most semantically similar chunks retrieved from ChromaDB
- Retrieved context passed into question generation prompt

### 3. Question Generation
- Questions generated using retrieved context + candidate skills + role
- Each question includes difficulty level, topic tag, and a hint
- Prior Q&A pairs passed to avoid repeating questions

### 4. Resume Utilisation
- Resume parsed to extract skills and domain keywords
- Skills directly influence query construction, topic selection, question difficulty

---

## Project Structure
