from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DateRange(str, Enum):
    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_3_DAYS = "last_3_days"

class NewsArticle(BaseModel):
    id: str = Field(alias="_id")
    title: str
    content: str
    sourceUrl: str
    sourceName: str
    contentHash: str
    crawledAt: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class NewsResponse(BaseModel):
    articles: List[NewsArticle]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    date_range: Optional[DateRange] = None
    source_name: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database_status: str