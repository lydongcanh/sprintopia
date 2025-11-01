"""
Main entry point for the Sprintopia API service.
"""

from .app import create_app

# Create the FastAPI application
app = create_app()
