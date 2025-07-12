from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from loguru import logger
from services.classification_service import predict_category

router = APIRouter()


class ClassificationRequest(BaseModel):
    text: str


class ClassificationResponse(BaseModel):
    category: str


@router.post("/classify", response_model=ClassificationResponse)
async def classify_news(request: str = Body(...)):
    """Classify the news text into a category"""
    try:
        category = predict_category(request)
        return ClassificationResponse(category=category)
    except Exception as e:
        logger.error(f"Error classifying news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
