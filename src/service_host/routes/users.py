"""
User management endpoints.
"""

from fastapi import APIRouter, Request
from core.container import Container
from core.models.user import User, CreateUserRequest

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=User | None)
async def create_user_async(user_data: CreateUserRequest, request: Request):
    """Create a new user."""
    container = request.app.state.container
    user_service = container.user_service()
    return await user_service.create_user_async(user_data)