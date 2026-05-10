import logging
import uuid

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

from app.core.settings import settings

logger = logging.getLogger(__name__)

DEFAULT_MIN_SCORE = 0.30


class VectorStoreService:

    def __init__(self):
        self._conn = psycopg.connect(
            settings.DATABASE_URL,
            row_factory=dict_row,
            autocommit=False,
        )
        register_vector(self._conn)
        logger.info("VectorStoreService conectado ao PostgreSQL.")

    def upsert_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        extra_metadata: dict | None = None,
    ) -> int:
        if not chunks:
            return 0

        extra_metadata = extra_metadata or {}

        with self._conn.cursor() as cur:
            for chunk, embedding in zip(chunks, embeddings):
                meta = {"repo_name": chunk["repo_name"]}
                meta.update(extra_metadata)

                cur.execute(
                    """
                    INSERT INTO chunks (id, repo_name, content, metadata, embedding)
                    VALUES (%s, %s, %s, %s::jsonb, %s::vector)
                    """,
                    (
                        str(uuid.uuid4()),
                        chunk["repo_name"],
                        chunk["text"],
                        psycopg.types.json.Json(meta),
                        embedding,
                    ),
                )

        self._conn.commit()
        return len(chunks)

    def delete_repo(self, repo_name: str) -> None:
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM chunks WHERE repo_name = %s", (repo_name,))
        self._conn.commit()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> list[dict]:
        # Operador <=> retorna distância cosseno (0 = idêntico). Convertemos para similaridade: score = 1 - distância.
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    repo_name,
                    content,
                    metadata,
                    1 - (embedding <=> %s::vector) AS score
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, query_embedding, top_k * 3),
            )
            rows = cur.fetchall()

        hits = []
        for row in rows:
            score = float(row["score"])
            if score < min_score:
                continue
            hits.append(
                {
                    "repo_name": row["repo_name"],
                    "score": score,
                    "excerpt": row["content"],
                    "metadata": row["metadata"] or {},
                }
            )

        hits.sort(key=lambda x: x["score"], reverse=True)
        return hits[:top_k]

    def stats(self) -> dict:
        with self._conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*)                    AS total_chunks,
                    COUNT(DISTINCT repo_name)   AS unique_repos
                FROM chunks
                """
            )
            row = cur.fetchone()

        return {
            "total_chunks": row["total_chunks"],
            "unique_repos": row["unique_repos"],
            "table_name": "chunks",
        }

    def close(self) -> None:
        self._conn.close()


_instance: VectorStoreService | None = None


def get_vector_store() -> VectorStoreService:
    global _instance
    if _instance is None:
        _instance = VectorStoreService()
    return _instance