import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "news_crawler"
    MONGODB_COLLECTION: str = "news_articles"
    
    # Redis Configuration (optional for caching)
    REDIS_URL: Optional[str] = None
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "News Microservice"
    VERSION: str = "1.0.0"
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Search configuration
    SEARCH_CACHE_TTL: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()