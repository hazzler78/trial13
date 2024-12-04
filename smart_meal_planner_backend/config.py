from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Base settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./smart_meal_planner.db"
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Monitoring settings
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    LOG_LEVEL: str = "INFO"
    ENABLE_REQUEST_LOGGING: bool = True
    ENABLE_API_LOGGING: bool = True
    
    # Rate limiting settings
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    RATE_LIMIT_MAX_REQUESTS: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()