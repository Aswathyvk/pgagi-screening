import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

def retrieve_context(query: str, role: str, n_results: int = 5) -> list:
    try:
        collection = client.get_collection(name=f"knowledge_{role}")
        query_embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        chunks = []
        for i, doc in enumerate(results["documents"][0]):
            chunks.append({
                "content": doc,
                "source": results["metadatas"][0][i].get("source", "unknown"),
                "distance": results["distances"][0][i]
            })
        return chunks
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []

def build_query(skills: list, role: str, topic: str = "") -> str:
    skill_str = ", ".join(skills[:5]) if skills else "general programming"
    if topic:
        return f"{role} interview questions about {topic} for someone who knows {skill_str}"
    return f"core concepts and fundamentals for {role} role involving {skill_str}"