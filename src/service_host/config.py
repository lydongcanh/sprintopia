"""
Application configuration and settings.
"""

import os
from typing import List


class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    API_TITLE: str = "Sprintopia API"
    API_VERSION: str = "1.0.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "https://localhost:5173",
        "https://sprintopia.vercel.app",
    ]
    
    CORS_ALLOW_HEADERS: List[str] = [
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Mx-ReqToken",
        "Keep-Alive",
        "X-Requested-With",
        "If-Modified-Since",
    ]
    
    # Authentication
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    @property
    def cors_enabled(self) -> bool:
        """Check if CORS should be enabled."""
        return bool(self.CORS_ORIGINS)


# Global settings instance
settings = Settings()