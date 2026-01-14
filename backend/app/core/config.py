"""Application configuration settings."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project metadata
    PROJECT_NAME: str = "VWAP Trading Strategy API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # TopstepX API credentials
    PROJECT_X_API_KEY: str = os.getenv("PROJECT_X_API_KEY", "")
    PROJECT_X_USERNAME: str = os.getenv("PROJECT_X_USERNAME", "")
    
    def validate_credentials(self):
        """Validate that required credentials are set."""
        if not self.PROJECT_X_API_KEY or not self.PROJECT_X_USERNAME:
            raise ValueError(
                "PROJECT_X_API_KEY and PROJECT_X_USERNAME must be set"
            )
    
    # Strategy configuration (with defaults)
    VWAP_DEVIATION: float = float(os.getenv("VWAP_DEVIATION", "2.0"))
    TIMER_INTERVAL: int = int(os.getenv("TIMER_INTERVAL", "1800"))
    CONTRACT_SIZE: int = int(os.getenv("CONTRACT_SIZE", "1"))
    INSTRUMENT: str = os.getenv("INSTRUMENT", "MGC")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

