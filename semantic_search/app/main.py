import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.settings import settings
from app.services.embedding_service import get_embedding_service
from app.services.vector_store import get_vector_store

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_embedding_service()  # pré-carrega modelo na inicialização
    get_vector_store()
    yield

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(router, prefix="/api/v1", tags=["Semantic Search"])

    @app.get("/health")
    def health():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app

app = create_app()