import uuid
import chromadb
from app.core.settings import settings

_COSINE_DIST_TO_SIMILARITY = lambda dist: 1.0 - dist
DEFAULT_MIN_SCORE = 0.30

class VectorStoreService:
    def __init__(self):
        self._client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert_chunks(self, chunks: list[dict], embeddings: list[list[float]]):
        if not chunks:
            return 0
            
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        metadatas = [{"repo_name": c["repo_name"]} for c in chunks]
        
        self._collection.upsert(
            ids=ids,
            documents=[c["text"] for c in chunks],
            embeddings=embeddings,
            metadatas=metadatas
        )
        return len(ids)

    def delete_repo(self, repo_name: str):
        results = self._collection.get(where={"repo_name": repo_name})
        if results and results["ids"]:
            self._collection.delete(ids=results["ids"])

    def search(self, query_embedding: list[float], top_k: int = 5, min_score: float = DEFAULT_MIN_SCORE):
        n_results = min(top_k * 3, max(1, self._collection.count()))
        if self._collection.count() == 0:
            return []
            
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        hits = []
        if not results["ids"] or not results["ids"][0]:
            return hits
            
        for i in range(len(results["ids"][0])):
            dist = results["distances"][0][i]
            score = _COSINE_DIST_TO_SIMILARITY(dist)
            
            if score < min_score:
                continue
                
            meta = results["metadatas"][0][i] or {}
            
            hits.append({
                "repo_name": meta.get("repo_name", "Desconhecido"),
                "score": score,
                "excerpt": results["documents"][0][i],
                "metadata": meta
            })
            
        hits.sort(key=lambda x: x["score"], reverse=True)
        return hits[:top_k]

    def stats(self) -> dict:
        all_metadata = self._collection.get(include=["metadatas"])["metadatas"]
        unique_repos = len(set(m.get("repo_name") for m in all_metadata if m and "repo_name" in m))
        
        return {
            "total_chunks": self._collection.count(),
            "unique_repos": unique_repos,
            "collection_name": self._collection.name
        }

def get_vector_store() -> VectorStoreService:
    return VectorStoreService()