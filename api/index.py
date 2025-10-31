import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the FastAPI app from your main module
from service_host.main import app

# Vercel expects an 'app' variable for FastAPI applications
# This is already imported from main.py, so we're good!