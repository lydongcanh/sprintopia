from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.infrastructure.database.database_client import DatabaseClient
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.infrastructure.repositories.user_repository import UserRepository

from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest
from core.models.user import User, CreateUserRequest

from core.services.grooming_session_service import GroomingSessionService
from core.services.user_service import UserService


# Setup
load_dotenv()
app = FastAPI(title="Sprintopia API", version="1.0.0")
api_prefix = "/api/v1"
SERVICE_UNAVAILABLE_MSG = "Service not available"

# CORS
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://sprintopia.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with error handling
try:
    db_client = DatabaseClient()
    supabase_facade = SupabaseFacade()
    grooming_session_repository = GroomingSessionRepository(db_client)
    user_repository = UserRepository(db_client)
    grooming_session_service = GroomingSessionService(grooming_session_repository, supabase_facade)
    user_service = UserService(user_repository, supabase_facade)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    # Create dummy services for testing
    grooming_session_service = None
    user_service = None


# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Sprintopia API is running!", "status": "ok"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Test endpoint for API prefix
@app.get(f"{api_prefix}/test")
async def api_test():
    return {"message": "API v1 is working!", "prefix": api_prefix}


# Sessions
@app.post(f"{api_prefix}/grooming-sessions")
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest) -> GroomingSession | None:
    if grooming_session_service is None:
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE_MSG)
    return await grooming_session_service.create_grooming_session_async(session_data.name)

@app.get(f"{api_prefix}/grooming-sessions/{{session_id}}")
async def get_grooming_session_by_id_async(session_id: UUID) -> GroomingSession | None:
    if grooming_session_service is None:
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE_MSG)
    return await grooming_session_service.get_grooming_session_by_id_async(session_id)

@app.get(f"{api_prefix}/grooming-sessions")
async def get_active_grooming_sessions_async():
    if grooming_session_service is None:
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE_MSG)
    return await grooming_session_service.get_active_grooming_sessions_async()

@app.get(f"{api_prefix}/active-grooming-channels")
async def get_active_grooming_channels_async():
    if grooming_session_service is None:
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE_MSG)
    return await grooming_session_service.get_active_grooming_channels_async()


# Users
@app.post(f"{api_prefix}/users")
async def create_user_async(user_data: CreateUserRequest) -> User | None:
    if user_service is None:
        raise HTTPException(status_code=503, detail=SERVICE_UNAVAILABLE_MSG)
    return await user_service.create_user_async(user_data)
