from pydantic import BaseModel, Field

class IndexReadmeRequest(BaseModel):
    repo_name: str = Field(..., description="Ex: 'empresa/meu-projeto'")
    content: str = Field(..., description="Conteúdo completo do README.md")
    metadata: dict = Field(default_factory=dict, description="Metadados extras (team, language...)")

class IndexReadmeResponse(BaseModel):
    repo_name: str
    chunks_indexed: int
    message: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=0.30, ge=0.0, le=1.0)

class SearchResult(BaseModel):
    repo_name: str
    section: str = "(sem seção)"
    score: float
    excerpt: str
    metadata: dict

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]

class CollectionStats(BaseModel):
    total_chunks: int
    unique_repos: int
    collection_name: str