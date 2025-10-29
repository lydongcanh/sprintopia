from dotenv import load_dotenv
from fastapi import FastAPI

from core.infrastructure.database.database_client import DatabaseClient
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository

from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest
from core.services.grooming_session_service import GroomingSessionService

# Setup
load_dotenv()
app = FastAPI()
api_prefix = "/api/v1"

db_client = DatabaseClient()
grooming_session_repository = GroomingSessionRepository(db_client)
grooming_session_service = GroomingSessionService(grooming_session_repository)


# Sessions
@app.post(f"{api_prefix}/grooming-sessions")
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest) -> GroomingSession | None:
    return await grooming_session_service.create_grooming_session_async(session_data.name)
