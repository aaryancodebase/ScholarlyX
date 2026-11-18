from pydantic import BaseModel, Field
from typing import Literal, Optional

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    method: Literal["bm25", "tfidf", "boolean", "semantic", "hybrid"] = "hybrid"
    limit: int = Field(default=20, ge=1, le=100)
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    category: Optional[str] = None
