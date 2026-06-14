import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "../../knowledge_base")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_pdf(filepath: str, role: str):
    collection = client.get_or_create_collection(name=f"knowledge_{role}")
    reader = PdfReader(filepath)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    
    chunks = chunk_text(full_text)
    filename = os.path.basename(filepath)
    
    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:
            continue
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{filename}_chunk_{i}"],
            metadatas=[{"source": filename, "role": role, "chunk_index": i}]
        )
    print(f"Ingested {len(chunks)} chunks from {filename}")

def ingest_all():
    kb_path = os.path.abspath(KNOWLEDGE_BASE_PATH)
    if not os.path.exists(kb_path):
        print(f"Knowledge base folder not found at {kb_path}")
        return
    
    for filename in os.listdir(kb_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(kb_path, filename)
            role = "ai_ml"
            ingest_pdf(filepath, role)
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_all()