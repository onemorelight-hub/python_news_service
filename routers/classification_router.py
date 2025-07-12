from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from loguru import logger
from services.logistic_classification_service import predict_category
from services.naive_bayes_classification_service import predict_category as predict_naive

router = APIRouter()


class ClassificationRequest(BaseModel):
    text: str


class ClassificationResponse(BaseModel):
    category: str


@router.post("/classify/logistic", response_model=ClassificationResponse)
async def classify_news(request: str = Body(...)):
    """Classify the news text into a category"""
    try:
        category = predict_category(request)
        return ClassificationResponse(category=category)
    except Exception as e:
        logger.error(f"Error classifying news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/classify/naive_bayes", response_model=ClassificationResponse)
async def classify_news(request: str = Body(...)):
    """Classify the news text into a category"""
    try:
        category = predict_naive(request)
        return ClassificationResponse(category=category)
    except Exception as e:
        logger.error(f"Error classifying news: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
