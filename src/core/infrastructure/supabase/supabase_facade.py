from supabase import acreate_client, AsyncClient
from core.utils.env import get_required_env


class SupabaseFacade:
    _client: AsyncClient | None = None

    @classmethod
    async def get_client_async(cls) -> AsyncClient:
        if cls._client is None:
            url: str = get_required_env("SUPABASE_URL")
            key: str = get_required_env("SUPABASE_KEY")
            cls._client = await acreate_client(url, key)
        return cls._client