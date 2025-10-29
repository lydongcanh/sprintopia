from pydantic import BaseModel
from core.models.base_entity import BaseEntity


class GroomingSession(BaseEntity):
    name: str
    real_time_channel_name: str


class CreateGroomingSessionRequest(BaseModel):
    name: str
    