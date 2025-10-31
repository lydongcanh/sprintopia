from uuid import UUID
from core.models.base_entity import BaseEntity


class UserEstimationTurn(BaseEntity):
    user_id: UUID
    estimation_turn_id: UUID
    estimation_value: float