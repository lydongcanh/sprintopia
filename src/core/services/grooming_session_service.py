import uuid
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.models.grooming_session import GroomingSession


class GroomingSessionService:
    def __init__(self, repository: GroomingSessionRepository) -> None:
        self.repository = repository

    async def create_grooming_session_async(self, name: str) -> GroomingSession | None:
        session_id = uuid.uuid4()
        real_time_channel_name = f"grooming_sessions:{session_id}"

        session = await self.repository.create_grooming_session_async(session_id, name, real_time_channel_name)
        if not session:
            return None
        
        supabase = await SupabaseFacade.get_client_async()
        supabase.channel(real_time_channel_name)

        return GroomingSession(
            id=session.id,
            created_at=session.created_at,
            updated_at=session.updated_at,
            status=session.status,
            name=session.name,
            real_time_channel_name=real_time_channel_name,
        )