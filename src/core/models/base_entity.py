from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from core.models.entity_status import EntityStatus


class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    status: EntityStatus