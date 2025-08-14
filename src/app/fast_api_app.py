"""
Module responsible for creating application instance for FastAPI.
"""

import os

from dotenv import load_dotenv

from src.handlers.fast_api_handler import FastApiHandler

# Load environment variables from a .env file
load_dotenv()

API_TITLE = os.getenv("API_TITLE")
API_DESCRIPTION = os.getenv("API_DESCRIPTION")
API_VERSION = os.getenv("API_VERSION")
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

FAST_API_APP = FastApiHandler(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    host=API_HOST,
    port=API_PORT,
)
FAST_API_APP.create_app()
