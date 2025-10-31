from core.infrastructure.repositories.user_repository import UserRepository
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.models.user import User, CreateUserRequest


class UserService:
    def __init__(self, user_repository: UserRepository, supabase: SupabaseFacade):
        self.user_repository = user_repository
        self.supabase = supabase

    async def create_user_async(self, user_data: CreateUserRequest) -> User | None:
        user = await self.user_repository.create_user_async(user_data)
        if not user:
            return None

        supabase_client = await self.supabase.get_client_async()
        await supabase_client.auth.admin.update_user_by_id(user_data.external_auth_id, {"user_metadata": { "internal_user_id": str(user.id) }})

        return user
