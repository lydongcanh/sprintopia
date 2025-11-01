"""
Health and utility endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint returning API status."""
    return {"message": "Sprintopia API is running!", "status": "ok"}


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}