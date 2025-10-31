from core.infrastructure.database.database_client import DatabaseClient
from core.models.user import CreateUserRequest, User


class UserRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

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
        result = await self.db.execute_sql_async(query, params)
        return User(**result[0]) if result else None