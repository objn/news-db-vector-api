
from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    message: str

class NewsEmbeddingRequest(BaseModel):
    news_desc: str

class NewsEmbeddingRequest_ID(BaseModel):
    news_id: str

class EmbeddingCompareRequest(BaseModel):
    news_desc: str
    embedding: Optional[str] = None
    threshold: Optional[float] = 0.9
    top_k: Optional[int] = 1