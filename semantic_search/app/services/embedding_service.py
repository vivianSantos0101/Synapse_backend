import logging
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.core.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        logger.info(f"Carregando modelo: {settings.EMBEDDING_MODEL}")
        self._model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed(self, texts: list[str]) -> list[list[float]]:
        # Normaliza capitalização — "Dashboard" e "dashboard" geram o mesmo vetor
        normalized = [t.lower() for t in texts]
        return self._model.encode(
            normalized,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).tolist()

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Singleton — modelo carregado apenas uma vez."""
    return EmbeddingService()