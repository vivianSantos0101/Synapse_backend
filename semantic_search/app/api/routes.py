import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import *
from app.services.chunker import chunk_readme
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.services.vector_store import VectorStoreService, get_vector_store

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/index", response_model=IndexReadmeResponse, status_code=201)
def index_readme(
    body: IndexReadmeRequest,
    embedder: EmbeddingService = Depends(get_embedding_service),
    store: VectorStoreService = Depends(get_vector_store),
):
    store.delete_repo(body.repo_name)  # substitui se já existir
    chunks = chunk_readme(body.content, body.repo_name)
    if not chunks:
        raise HTTPException(422, "README muito curto ou sem conteúdo legível.")
    embeddings = embedder.embed([c["text"] for c in chunks])
    count = store.upsert_chunks(chunks, embeddings, extra_metadata=body.metadata)
    return IndexReadmeResponse(repo_name=body.repo_name, chunks_indexed=count, message=f"Indexado em {count} chunks.")

@router.delete("/index/{repo_name:path}", status_code=204)
def delete_repo(repo_name: str, store: VectorStoreService = Depends(get_vector_store)):
    store.delete_repo(repo_name)

@router.post("/search", response_model=SearchResponse)
def search(
    body: SearchRequest,
    embedder: EmbeddingService = Depends(get_embedding_service),
    store: VectorStoreService = Depends(get_vector_store),
):
    query_embedding = embedder.embed_one(body.query)
    hits = store.search(query_embedding, top_k=body.top_k, min_score=body.min_score)
    return SearchResponse(
        query=body.query,
        total_results=len(hits),
        results=[SearchResult(**h) for h in hits],
    )

@router.get("/stats", response_model=CollectionStats)
def stats(store: VectorStoreService = Depends(get_vector_store)):
    return CollectionStats(**store.stats())