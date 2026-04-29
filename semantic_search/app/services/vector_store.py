import logging
import uuid
from functools import lru_cache
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.settings import settings

logger = logging.getLogger(__name__)

# ChromaDB >= 1.0 com hnsw:space="cosine" retorna distâncias em [0, 1].
# Fórmula correta: similaridade = 1 - distância (NÃO 1 - dist/2).
_COSINE_DIST_TO_SIMILARITY = lambda dist: 1.0 - dist

DEFAULT_MIN_SCORE = 0.30


class VectorStoreService:
    def __init__(self):
        self._client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"ChromaDB pronto — {self._collection.count()} chunks.")

    def upsert_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        extra_metadata: dict,
    ) -> int:
        ids = [str(uuid.uuid4()) for _ in chunks]
        self._collection.upsert(
            ids=ids,
            documents=[c["text"] for c in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "repo_name": c["repo_name"],
                    "section": c.get("section", ""),
                    **extra_metadata,
                }
                for c in chunks
            ],
        )
        return len(ids)

    def delete_repo(self, repo_name: str) -> None:
        results = self._collection.get(where={"repo_name": repo_name})
        if results["ids"]:
            self._collection.delete(ids=results["ids"])

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> list[dict]:
        total = self._collection.count()
        if total == 0:
            logger.warning("Busca executada em coleção vazia.")
            return []

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 3, total),
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = _COSINE_DIST_TO_SIMILARITY(dist)

            logger.debug(
                f"repo={meta.get('repo_name')} | "
                f"section={meta.get('section')} | "
                f"dist={dist:.4f} | score={score:.4f}"
            )

            if score < min_score:
                continue

            hits.append({
                "repo_name": meta.get("repo_name", ""),
                "section": meta.get("section", "(sem seção)"),
                "score": round(score, 4),
                "excerpt": doc[:400],
                "metadata": {
                    k: v for k, v in meta.items()
                    if k not in ("repo_name", "section")
                },
            })

        hits.sort(key=lambda x: x["score"], reverse=True)
        return hits[:top_k]

    def stats(self) -> dict:
        all_meta = self._collection.get(include=["metadatas"])["metadatas"] or []
        return {
            "total_chunks": self._collection.count(),
            "unique_repos": len({m.get("repo_name") for m in all_meta}),
            "collection_name": settings.CHROMA_COLLECTION_NAME,
        }


@lru_cache(maxsize=1)
def get_vector_store() -> VectorStoreService:
    return VectorStoreService()