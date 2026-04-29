from pydantic import BaseModel, Field

class IndexReadmeRequest(BaseModel):
    repo_name: str = Field(...)
    content: str = Field(...)
    metadata: dict = Field(default_factory=dict)

class IndexReadmeResponse(BaseModel):
    repo_name: str
    chunks_indexed: int
    message: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=0.30)

class SearchResult(BaseModel):
    repo_name: str
    score: float
    excerpt: str
    metadata: dict = Field(default_factory=dict)

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResult]

class CollectionStats(BaseModel):
    total_chunks: int
    unique_repos: int
    collection_name: str