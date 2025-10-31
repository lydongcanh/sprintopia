from pydantic import BaseModel
from core.models.base_entity import BaseEntity


class User(BaseEntity):
    email: str
    full_name: str
    external_auth_id: str

class CreateUserRequest(BaseModel):
    email: str
    full_name: str
    external_auth_id: str