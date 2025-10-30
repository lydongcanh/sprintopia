from pydantic import BaseModel, Field
from core.models.base_entity import BaseEntity


class GroomingSession(BaseEntity):
    name: str
    real_time_channel_name: str = Field(..., title="Supabase Real-Time Channel Name")


class CreateGroomingSessionRequest(BaseModel):
    name: str
    