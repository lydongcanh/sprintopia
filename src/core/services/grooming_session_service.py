from uuid import UUID, uuid4
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.infrastructure.repositories.estimation_turn_repository import EstimationTurnRepository
from core.infrastructure.repositories.user_repository import UserRepository
from core.models.grooming_session import GroomingSession


class GroomingSessionService:
    def __init__(
        self, 
        grooming_session_repository: GroomingSessionRepository,
        estimation_turn_repository: EstimationTurnRepository,
        user_repository: UserRepository,
        supabase: SupabaseFacade
    ) -> None:
        self.grooming_session_repository = grooming_session_repository
        self.estimation_turn_repository = estimation_turn_repository
        self.user_repository = user_repository
        self.supabase = supabase


    def _build_real_time_channel_name(self, session_id: UUID) -> str:
        return f"grooming_sessions:{session_id}"
    

    async def start_new_estimation_turn_async(self, grooming_session_id: UUID):
        estimation_turn_id = await self.estimation_turn_repository.create_estimation_turn_async(grooming_session_id)
        if not estimation_turn_id:
            raise RuntimeError("Failed to create a new estimation turn.")

        real_time_channel_name = self._build_real_time_channel_name(grooming_session_id)
        supabase_client = await self.supabase.get_client_async()
        channel = supabase_client.channel(real_time_channel_name)
        await channel.subscribe()
        await channel.send_broadcast(event="start_estimation_turn", data={"estimation_turn_id": str(estimation_turn_id)})


    async def submit_estimation_async(self, session_id: UUID, user_id: UUID, estimation_value: float):
        await self.user_repository.create_user_estimation_turn_async(user_id, session_id, estimation_value)

        real_time_channel_name = self._build_real_time_channel_name(session_id)
        supabase_client = await self.supabase.get_client_async()
        channel = supabase_client.channel(real_time_channel_name)
        await channel.subscribe()
        await channel.send_broadcast(
            event="estimation_submitted", 
            data={
                "user_id": str(user_id),
                "estimation_value": estimation_value
            }
        )


    async def end_estimation_turn_async(self, grooming_session_id: UUID, estimation_turn_id: UUID):
        await self.estimation_turn_repository.complete_estimation_turn_async(estimation_turn_id)

        real_time_channel_name = self._build_real_time_channel_name(grooming_session_id)
        supabase_client = await self.supabase.get_client_async()
        channel = supabase_client.channel(real_time_channel_name)
        await channel.subscribe()
        await channel.send_broadcast(event="end_estimation_turn", data={"estimation_turn_id": str(estimation_turn_id)})


    async def create_grooming_session_async(self, name: str) -> GroomingSession | None:
        session_id = uuid4()
        real_time_channel_name = self._build_real_time_channel_name(session_id)

        session = await self.grooming_session_repository.create_grooming_session_async(session_id, name, real_time_channel_name)
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
    

    async def get_grooming_session_by_id_async(self, session_id: UUID) -> GroomingSession | None:
        return await self.grooming_session_repository.get_grooming_session_by_id_async(session_id)
    

    async def get_active_grooming_sessions_async(self):
        return await self.grooming_session_repository.get_active_grooming_sessions_async()
