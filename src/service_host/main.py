from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.infrastructure.database.database_client import DatabaseClient
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.infrastructure.repositories.estimation_turn_repository import EstimationTurnRepository
from core.infrastructure.repositories.user_repository import UserRepository

from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest
from core.models.user import User, CreateUserRequest

from core.services.grooming_session_service import GroomingSessionService
from core.services.user_service import UserService


# Setup
load_dotenv()
app = FastAPI(title="Sprintopia API", version="1.0.0")
api_prefix = "/api/v1"

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


db_client = DatabaseClient()
supabase_facade = SupabaseFacade()
grooming_session_repository = GroomingSessionRepository(db_client)
user_repository = UserRepository(db_client)
estimation_turn_repository = EstimationTurnRepository(db_client)
grooming_session_service = GroomingSessionService(grooming_session_repository, estimation_turn_repository, user_repository, supabase_facade)
user_service = UserService(user_repository, supabase_facade)


# Utilities
@app.get("/")
async def root():
    return {"message": "Sprintopia API is running!", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Grooming Sessions
@app.post(f"{api_prefix}/grooming-sessions/{{session_id}}/estimation-turns")
async def start_new_estimation_turn_async(session_id: UUID):
    await grooming_session_service.start_new_estimation_turn_async(session_id)

@app.post(f"{api_prefix}/grooming-sessions/{{session_id}}/estimations")
async def submit_estimation_async(
        session_id: UUID, 
        user_id: UUID = Body(..., embed=True), 
        estimation_value: float = Body(..., embed=True)
    ):
    await grooming_session_service.submit_estimation_async(session_id, user_id, estimation_value)

@app.post(f"{api_prefix}/grooming-sessions/{{session_id}}/estimation-turns/{{estimation_turn_id}}/end")
async def end_estimation_turn_async(session_id: UUID, estimation_turn_id: UUID):
    return await grooming_session_service.end_estimation_turn_async(session_id, estimation_turn_id)

@app.post(f"{api_prefix}/grooming-sessions")
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest) -> GroomingSession | None:
    return await grooming_session_service.create_grooming_session_async(session_data.name)

@app.get(f"{api_prefix}/grooming-sessions/{{session_id}}")
async def get_grooming_session_by_id_async(session_id: UUID) -> GroomingSession | None:
    return await grooming_session_service.get_grooming_session_by_id_async(session_id)

@app.get(f"{api_prefix}/grooming-sessions")
async def get_active_grooming_sessions_async():
    return await grooming_session_service.get_active_grooming_sessions_async()


# Users
@app.post(f"{api_prefix}/users")
async def create_user_async(user_data: CreateUserRequest) -> User | None:
    return await user_service.create_user_async(user_data)
