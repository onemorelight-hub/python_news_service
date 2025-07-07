from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from loguru import logger

from database import get_database
from services.news_service import NewsService
from schemas import NewsResponse, NewsArticle, DateRange

router = APIRouter()

def get_news_service():
    """Dependency to get news service instance"""
    db = get_database()
    return NewsService(db.collection)

@router.get("/news", response_model=NewsResponse)
async def get_news(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    date_range: Optional[DateRange] = Query(None, description="Filter by date range"),
    source_name: Optional[str] = Query(None, description="Filter by source name"),
    service: NewsService = Depends(get_news_service)
):
    """Get paginated news articles"""
    try:
        return await service.get_news_paginated(page, page_size, date_range, source_name)
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/news/search", response_model=NewsResponse)
async def search_news(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    date_range: Optional[DateRange] = Query(None, description="Filter by date range"),
    source_name: Optional[str] = Query(None, description="Filter by source name"),
    service: NewsService = Depends(get_news_service)
):
    """Search news articles by text"""
    try:
        return await service.search_news(q, page, page_size, date_range, source_name)
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/news/{article_id}", response_model=NewsArticle)
async def get_news_by_id(
    article_id: str,
    service: NewsService = Depends(get_news_service)
):
    """Get a specific news article by ID"""
    try:
        article = await service.get_news_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article {article_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/news/date/{date_range}")
async def get_news_by_date(
    date_range: DateRange,
    service: NewsService = Depends(get_news_service)
):
    """Get news articles for specific date range"""
    try:
        articles = await service.get_news_by_date_range(date_range)
        return {"articles": articles, "count": len(articles)}
    except Exception as e:
        logger.error(f"Error fetching news by date {date_range}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")