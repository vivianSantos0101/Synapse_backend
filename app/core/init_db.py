import logging
import psycopg
from app.core.settings import settings

logger = logging.getLogger(__name__)

_DIM = settings.VECTOR_DIMENSION

# SQL idempotente — pode ser executado múltiplas vezes sem efeito colateral
INIT_SQL = f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_name   TEXT NOT NULL,
    content     TEXT NOT NULL,
    metadata    JSONB NOT NULL DEFAULT '{{}}'::jsonb,
    embedding   vector({_DIM})
);

CREATE INDEX IF NOT EXISTS idx_chunks_repo
    ON chunks (repo_name);

CREATE INDEX IF NOT EXISTS idx_chunks_embedding_cosine
    ON chunks USING hnsw (embedding vector_cosine_ops);
"""


def init_db() -> None:
    logger.info("Inicializando banco de dados...")
    with psycopg.connect(settings.DATABASE_URL) as conn:
        conn.execute(INIT_SQL)
        conn.commit()
    logger.info("Banco de dados pronto.")
