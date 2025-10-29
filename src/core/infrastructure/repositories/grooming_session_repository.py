from uuid import UUID
from core.infrastructure.database.database_client import DatabaseClient
from core.models.grooming_session import GroomingSession

class GroomingSessionRepository:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    async def create_grooming_session_async(self, id: UUID, name: str, real_time_channel_name: str) -> GroomingSession | None:
        sql = """
            INSERT INTO grooming_sessions (id, name, real_time_channel_name)
            VALUES (:id, :name, :real_time_channel_name)
            RETURNING *;
        """
        params = {
            "id": id,
            "name": name,
            "real_time_channel_name": real_time_channel_name,
        }
        result = await self.db_client.execute_sql_async(sql, params)
        return GroomingSession(**result[0]) if result else None
