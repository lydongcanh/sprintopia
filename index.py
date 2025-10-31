# Root-level FastAPI entry point for Vercel
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the FastAPI app
from service_host.main import app

# Vercel will automatically use this 'app' variable