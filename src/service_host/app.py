"""
Application factory and setup.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.container import Container
from .config import settings
from .middleware.auth_middleware import AuthMiddleware
from .routes import health, grooming_sessions, users

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize container
    container = Container()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="The joyful home for agile discussions and estimation."
    )
    
    # Store container in app state
    app.state.container = container
    
    # Add authentication middleware FIRST (it will be executed LAST due to middleware stack)
    auth_middleware = AuthMiddleware()
    app.middleware("http")(auth_middleware)
    
    # Configure CORS AFTER auth middleware (so CORS is processed BEFORE auth)
    if settings.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=settings.CORS_ALLOW_HEADERS,
        )
    
    # Add startup and shutdown events
    @app.on_event("startup")
    async def startup_event():
        logger.info("Application startup - Database client initialized as singleton")

    @app.on_event("shutdown") 
    async def shutdown_event():
        logger.info("Application shutdown - Disposing database connections")
        db_client = container.database_client()
        await db_client.dispose_async()
    
    # Include routers
    app.include_router(health.router)
    app.include_router(grooming_sessions.router)
    app.include_router(users.router)
    
    return app