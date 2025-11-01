"""
Grooming session related endpoints.
"""

from fastapi import APIRouter, Body, Request
from uuid import UUID
from typing import List

from core.container import Container
from core.models.grooming_session import GroomingSession, CreateGroomingSessionRequest

router = APIRouter(prefix="/api/v1/grooming-sessions", tags=["grooming-sessions"])


@router.post("/{session_id}/estimation-turns")
async def start_new_estimation_turn_async(session_id: UUID, request: Request):
    """Start a new estimation turn for a grooming session."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    await grooming_session_service.start_new_estimation_turn_async(session_id)


@router.post("/{session_id}/estimations")
async def submit_estimation_async(
    session_id: UUID, 
    request: Request,
    user_id: UUID = Body(..., embed=True), 
    estimation_value: float = Body(..., embed=True)
):
    """Submit an estimation for the current estimation turn."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    await grooming_session_service.submit_estimation_async(session_id, user_id, estimation_value)


@router.post("/{session_id}/estimation-turns/{estimation_turn_id}/end")
async def end_estimation_turn_async(session_id: UUID, estimation_turn_id: UUID, request: Request):
    """End an estimation turn and return results."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.end_estimation_turn_async(session_id, estimation_turn_id)


@router.post("", response_model=GroomingSession | None)
async def create_grooming_session_async(session_data: CreateGroomingSessionRequest, request: Request):
    """Create a new grooming session."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.create_grooming_session_async(session_data.name)


@router.get("/{session_id}", response_model=GroomingSession | None)
async def get_grooming_session_by_id_async(session_id: UUID, request: Request):
    """Get a specific grooming session by ID."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.get_grooming_session_by_id_async(session_id)


@router.get("")
async def get_active_grooming_sessions_async(request: Request):
    """Get all active grooming sessions."""
    container = request.app.state.container
    grooming_session_service = container.grooming_session_service()
    return await grooming_session_service.get_active_grooming_sessions_async()