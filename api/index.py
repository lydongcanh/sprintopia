import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.service_host.main import app

# Vercel will use this as the ASGI application
# No need for a custom handler function with FastAPI