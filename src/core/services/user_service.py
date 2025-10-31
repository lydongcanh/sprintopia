from core.infrastructure.repositories.user_repository import UserRepository
from core.models.user import User, CreateUserRequest


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user_async(self, user: CreateUserRequest) -> User | None:
        return await self.user_repository.create_user_async(user)
