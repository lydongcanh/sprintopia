from supabase import acreate_client, AsyncClient
from core.utils.env import get_required_env


class SupabaseFacade:
    def __init__(self):
        self.client: AsyncClient | None = None

    async def get_client_async(self) -> AsyncClient:
        if self.client is None:
            url: str = get_required_env("SUPABASE_URL")
            key: str = get_required_env("SUPABASE_KEY")
            self.client = await acreate_client(url, key)
        return self.client