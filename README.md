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

Frontend (Next.js) → FastAPI Backend → SQLite DB

↓

RAG Pipeline → ChromaDB (Vector Store)

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

pgagi-screening/

pgagi-screening/

├── backend/

│   ├── main.py

│   ├── routers/

│   │   ├── resume.py

│   │   ├── sessions.py

│   │   └── questions.py

│   ├── rag/

│   │   ├── ingestor.py

│   │   ├── retriever.py

│   │   └── question_generator.py

│   ├── models.py

│   ├── schemas.py

│   └── db.py

├── frontend/

│   ├── app/

│   │   ├── page.tsx

│   │   ├── interview/page.tsx

│   │   └── results/page.tsx

│   └── lib/

│       └── api.ts

└── knowledge_base/

└── ml_hundred_page.pdf

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `backend/`:

DB_URL=sqlite:///./interviews.db

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

KNOWLEDGE_BASE_DIR=../knowledge_base

Ingest knowledge base:
```bash
python -m rag.ingestor
```

Start backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/parse` | Parse resume, extract skills |
| POST | `/api/sessions/create` | Create interview session |
| POST | `/api/questions/generate` | Generate RAG-based question |
| POST | `/api/sessions/{id}/answer` | Save candidate answer |
| POST | `/api/sessions/{id}/evaluate` | Evaluate full session |
| GET | `/api/sessions/{id}/history` | Get session Q&A history |

---

## Key Design Decisions

**Why ChromaDB?** Lightweight, no external service needed, persistent storage, perfect for local RAG demos.

**Why all-MiniLM-L6-v2?** Fast inference, small model size, strong semantic similarity — ideal for interview question retrieval.

**Why SQLite?** Zero-config persistence for session and answer storage. Easy to swap for PostgreSQL in production via DB_URL env var.

**Why 1000-char chunks with 200 overlap?** Preserves enough context per chunk while overlap prevents concepts from being split across boundaries.

---

## Submission

- GitHub: https://github.com/Aswathyvk/pgagi-screening
- Demo Video: [link to be added]
