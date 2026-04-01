from pydantic import BaseModel


class RAGChunk(BaseModel):
    content: str
    source: str
    score: float


class RAGSearchResult(BaseModel):
    chunks: list[RAGChunk]
    query: str
