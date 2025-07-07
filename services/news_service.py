from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from bson import ObjectId
from pymongo import DESCENDING
import re

from schemas import DateRange, NewsArticle, NewsResponse

class NewsService:
    def __init__(self, collection):
        self.collection = collection
    
    async def get_news_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        date_range: Optional[DateRange] = None,
        source_name: Optional[str] = None
    ) -> NewsResponse:
        """Get paginated news articles"""
        
        # Build query filters
        query_filter = {}
        
        if date_range:
            date_filter = self._build_date_filter(date_range)
            query_filter.update(date_filter)
        
        if source_name:
            query_filter["sourceName"] = {"$regex": re.escape(source_name), "$options": "i"}
        
        # Calculate pagination
        skip = (page - 1) * page_size
        
        # Execute queries
        total = await self.collection.count_documents(query_filter)
        
        cursor = self.collection.find(query_filter).sort("crawledAt", DESCENDING).skip(skip).limit(page_size)
        articles = await cursor.to_list(length=page_size)
        
        # Convert to response model
        return self._build_news_response(articles, total, page, page_size)
    
    async def search_news(
        self,
        search_query: str,
        page: int = 1,
        page_size: int = 20,
        date_range: Optional[DateRange] = None,
        source_name: Optional[str] = None
    ) -> NewsResponse:
        """Search news articles by text"""
        
        # Build query filters
        query_filter = {"$text": {"$search": search_query}}
        
        if date_range:
            date_filter = self._build_date_filter(date_range)
            query_filter.update(date_filter)
        
        if source_name:
            query_filter["sourceName"] = {"$regex": re.escape(source_name), "$options": "i"}
        
        # Calculate pagination
        skip = (page - 1) * page_size
        
        # Execute search with text score
        total = await self.collection.count_documents(query_filter)
        
        cursor = self.collection.find(
            query_filter,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"}), ("crawledAt", DESCENDING)]).skip(skip).limit(page_size)
        
        articles = await cursor.to_list(length=page_size)
        
        return self._build_news_response(articles, total, page, page_size)
    
    async def get_news_by_id(self, article_id: str) -> Optional[NewsArticle]:
        """Get a specific news article by ID"""
        try:
            article = await self.collection.find_one({"_id": ObjectId(article_id)})
            if article:
                return NewsArticle(**self._convert_object_id(article))
            return None
        except Exception:
            return None
    
    async def get_news_by_date_range(self, date_range: DateRange) -> List[NewsArticle]:
        """Get news articles for specific date range"""
        date_filter = self._build_date_filter(date_range)
        
        cursor = self.collection.find(date_filter).sort("crawledAt", DESCENDING)
        articles = await cursor.to_list(length=None)
        
        return [NewsArticle(**self._convert_object_id(article)) for article in articles]
    
    def _build_date_filter(self, date_range: DateRange) -> Dict[str, Any]:
        """Build MongoDB date filter based on date range"""
        now = datetime.utcnow()
        
        if date_range == DateRange.TODAY:
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif date_range == DateRange.YESTERDAY:
            yesterday = now - timedelta(days=1)
            start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif date_range == DateRange.LAST_3_DAYS:
            start_date = (now - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            return {}
        
        return {
            "crawledAt": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
    
    def _convert_object_id(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB ObjectId to string"""
        if "_id" in article:
            article["_id"] = str(article["_id"])
        return article
    
    def _build_news_response(
        self,
        articles: List[Dict[str, Any]],
        total: int,
        page: int,
        page_size: int
    ) -> NewsResponse:
        """Build paginated news response"""
        total_pages = (total + page_size - 1) // page_size
        
        return NewsResponse(
            articles=[NewsArticle(**self._convert_object_id(article)) for article in articles],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
