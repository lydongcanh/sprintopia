#!/usr/bin/env python3
"""
Main entry point for the Sprintopia API application.
This file serves as the production entry point for deployment platforms like Render.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the FastAPI app
from service_host.main import app

# Make the app available at module level for uvicorn
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)