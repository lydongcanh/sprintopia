from uuid import UUID
from core.models.base_entity import BaseEntity


class EstimationTurn(BaseEntity):
    grooming_session_id: UUID
    is_completed: bool