from uuid import UUID
from core.infrastructure.database.database_client import DatabaseClient


class EstimationTurnRepository:
    def __init__(self, db_client: DatabaseClient) -> None:
        self.db_client = db_client

    async def create_estimation_turn_async(self, grooming_session_id: UUID) -> UUID | None:
        query = """
            INSERT INTO estimation_turns (grooming_session_id)
            VALUES (:grooming_session_id)
            RETURNING id
        """
        params = {"grooming_session_id": grooming_session_id}
        results = await self.db_client.execute_sql_async(query, params)
        return results[0]["id"] if results else None

    async def complete_estimation_turn_async(self, estimation_turn_id: UUID):
        query = """
            UPDATE estimation_turns
            SET is_completed = TRUE
            WHERE id = :estimation_turn_id
        """
        params = {"estimation_turn_id": estimation_turn_id}
        await self.db_client.execute_sql_async(query, params)
