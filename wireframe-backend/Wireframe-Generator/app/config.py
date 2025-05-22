import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


#load evironment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Application Settings"""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Wireframe Generation API"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # LLM API keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")


    # LangSmith tracing (optional)
    LANGSMITH_TRACING: str = os.getenv("LANGSMITH_TRACING", "false")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "wireframe-generator")
    LANGSMITH_ENDPOINT: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")


    # Model settings
    DEFAULT_MODEL: str = "gemini-2.5-flash-preview-04-17"
    MODEL_TEMPERATURE: float = 0.3

    # Cache settings
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # Time to live in seconds
    
    class Config:
        case_sensitive = True


settings = Settings()

