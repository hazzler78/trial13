from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import uvicorn
import openai
from config import get_settings
from database import engine
import models
from api.routes import router as api_router
from auth.routes import router as auth_router
from ai.routes import router as ai_router
from monitoring.middleware import RequestTracingMiddleware, ResponseTimeMiddleware
from monitoring.sentry import init_sentry
from monitoring.logger import get_logger
import logging

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = get_logger(__name__)

# Initialize Sentry
init_sentry()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Smart Meal Planner API",
    description="API for managing inventory, recipes, and shopping lists with AI-powered suggestions",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add monitoring middleware
app.add_middleware(RequestTracingMiddleware)
app.add_middleware(ResponseTimeMiddleware)

# Mount metrics endpoint
if settings.ENABLE_METRICS:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

# Include API routes
app.include_router(api_router)
app.include_router(auth_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Smart Meal Planner API",
        "features": [
            "User authentication",
            "Inventory management",
            "Recipe management",
            "Shopping list",
            "AI-powered recipe suggestions",
            "AI-powered meal planning"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.exception_handler(openai.RateLimitError)
async def rate_limit_handler(request, exc):
    logger.error(f"Rate limit error: {exc}")
    return JSONResponse(
        status_code=429,
        content={"detail": str(exc) or "Rate limit exceeded. Please try again later."}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 