from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.container import Container
from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest
from core.models.user import User, CreateUserRequest


# Setup
load_dotenv()

# Initialize container
container = Container()

app = FastAPI(title="Sprintopia API", version="1.0.0")
api_prefix = "/api/v1"

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup - Database client initialized as singleton")

@app.on_event("shutdown") 
async def shutdown_event():
    logger.info("Application shutdown - Disposing database connections")
    db_client = container.database_client()
    await db_client.dispose_async()

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
    grooming_session_service = container.grooming_session_service()
    await grooming_session_service.start_new_estimation_turn_async(session_id)

@app.post(f"{api_prefix}/grooming-sessions/{{session_id}}/estimations")
async def submit_estimation_async(
    session_id: UUID, 
    user_id: UUID = Body(..., embed=True), 
    estimation_value: float = Body(..., embed=True)
):
    grooming_session_service = container.grooming_session_service()
    await grooming_session_service.submit_estimation_async(session_id, user_id, estimation_value)

@app.post(f"{api_prefix}/grooming-sessions/{{session_id}}/estimation-turns/{{estimation_turn_id}}/end")
async def end_estimation_turn_async(session_id: UUID, estimation_turn_id: UUID):
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.end_estimation_turn_async(session_id, estimation_turn_id)

@app.post(f"{api_prefix}/grooming-sessions")
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest) -> GroomingSession | None:
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.create_grooming_session_async(session_data.name)

@app.get(f"{api_prefix}/grooming-sessions/{{session_id}}")
async def get_grooming_session_by_id_async(session_id: UUID) -> GroomingSession | None:
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.get_grooming_session_by_id_async(session_id)

@app.get(f"{api_prefix}/grooming-sessions")
async def get_active_grooming_sessions_async():
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.get_active_grooming_sessions_async()


# Users
@app.post(f"{api_prefix}/users")
async def create_user_async(user_data: CreateUserRequest) -> User | None:
    user_service = container.user_service()
    return await user_service.create_user_async(user_data)
