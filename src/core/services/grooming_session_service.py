import uuid
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.models.grooming_session import GroomingSession


class GroomingSessionService:
    def __init__(self, repository: GroomingSessionRepository, supabase: SupabaseFacade) -> None:
        self.repository = repository
        self.supabase = supabase

    async def create_grooming_session_async(self, name: str) -> GroomingSession | None:
        session_id = uuid.uuid4()
        real_time_channel_name = f"grooming_sessions:{session_id}"

        session = await self.repository.create_grooming_session_async(session_id, name, real_time_channel_name)
        if not session:
            return None
        
        supabase_client = await self.supabase.get_client_async()
        supabase_client.channel(real_time_channel_name)

        return GroomingSession(
            id=session.id,
            created_at=session.created_at,
            updated_at=session.updated_at,
            status=session.status,
            name=session.name,
            real_time_channel_name=real_time_channel_name,
        )
    
    async def get_grooming_session_by_id_async(self, session_id: uuid.UUID) -> GroomingSession | None:
        return await self.repository.get_grooming_session_by_id_async(session_id)
    
    async def get_active_grooming_sessions_async(self):
        return await self.repository.get_active_grooming_sessions_async()
    
    async def get_active_grooming_channels_async(self):
        try:
            supabase_client = await self.supabase.get_client_async()
            channels = supabase_client.get_channels()
            return [{
                "topic": channel.topic,
                "state": channel.state,
            } for channel in channels]
        except Exception as e:
            print(f"Error retrieving active grooming channels: {e}")
            return {"error": str(e)}
