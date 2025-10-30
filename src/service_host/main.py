from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID

from core.infrastructure.database.database_client import DatabaseClient
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository

from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest
from core.services.grooming_session_service import GroomingSessionService


# Setup
load_dotenv()
app = FastAPI(title="Sprintopia API", version="1.0.0")
api_prefix = "/api/v1"

# CORS
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_client = DatabaseClient()
grooming_session_repository = GroomingSessionRepository(db_client)
grooming_session_service = GroomingSessionService(grooming_session_repository)


# Sessions
@app.post(f"{api_prefix}/grooming-sessions")
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest) -> GroomingSession | None:
    return await grooming_session_service.create_grooming_session_async(session_data.name)

@app.get(f"{api_prefix}/grooming-sessions/{{session_id}}")
async def get_grooming_session_by_id_async(session_id: UUID) -> GroomingSession | None:
    return await grooming_session_service.get_grooming_session_by_id_async(session_id)
