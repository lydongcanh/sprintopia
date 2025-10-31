# Vercel FastAPI entry point - app.py
import sys
import os
from pathlib import Path

# Get the directory containing this file
current_dir = Path(__file__).parent
src_dir = current_dir / "src"

# Add the src directory to the Python path
sys.path.insert(0, str(src_dir))

# Import the FastAPI app
from service_host.main import app

# Vercel will automatically use this 'app' variable for FastAPI applications