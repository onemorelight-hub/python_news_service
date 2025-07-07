from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import sys
from datetime import datetime

# Import configuration and database
from config import settings
from database import connect_to_mongo, close_mongo_connection, db
from schemas import HealthCheck
from routers.news import router

# Configure logging
logger.remove()
logger.add(sys.stdout, format="{time} | {level} | {message}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up News Microservice")
    await connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down News Microservice")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade news microservice with MongoDB backend",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "News Microservice", "version": settings.VERSION}

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        await db.client.admin.command('ping')
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return HealthCheck(
        status="healthy" if db_status == "healthy" else "unhealthy",
        timestamp=datetime.utcnow(),
        version=settings.VERSION,
        database_status=db_status
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
