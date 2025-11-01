from uuid import UUID
from core.infrastructure.database.database_client import DatabaseClient
from core.models.user import CreateUserRequest, User


class UserRepository:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client


    async def create_user_async(self, user: CreateUserRequest) -> User | None:
        query = """
            INSERT INTO users (email, full_name, external_auth_id)
            VALUES (:email, :full_name, :external_auth_id)
            RETURNING id, email, full_name, external_auth_id, created_at, updated_at, status;
        """
        params = {
            "email": user.email,
            "full_name": user.full_name,
            "external_auth_id": user.external_auth_id
        }
        result = await self.db_client.execute_sql_async(query, params)
        return User(**result[0]) if result else None
    

    async def create_user_estimation_turn_async(self, user_id, estimation_turn_id, estimation_value):
        query = """
            INSERT INTO user_estimation_turns (user_id, estimation_turn_id, estimation_value)
            VALUES (:user_id, :estimation_turn_id, :estimation_value);
        """
        params = {
            "user_id": user_id,
            "estimation_turn_id": estimation_turn_id,
            "estimation_value": estimation_value
        }
        await self.db_client.execute_sql_async(query, params)


    async def get_user_by_id_async(self, user_id: UUID) -> User | None:
        query = """
            SELECT id, email, full_name, external_auth_id, created_at, updated_at, status
            FROM users
            WHERE id = :user_id;
        """
        params = {"user_id": user_id}
        result = await self.db_client.execute_sql_async(query, params)
        return User(**result[0]) if result else None