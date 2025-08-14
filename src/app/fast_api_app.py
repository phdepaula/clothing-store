"""
Module responsible for creating application instance for FastAPI.
"""

import os

from dotenv import load_dotenv

from src.app.jwt_app import JWT_APP
from src.handlers.fast_api_handler import FastApiHandler

# Load environment variables from a .env file
load_dotenv()

API_TITLE = os.getenv("API_TITLE")
API_DESCRIPTION = os.getenv("API_DESCRIPTION")
API_VERSION = os.getenv("API_VERSION")
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

fast_api_instance = FastApiHandler(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    host=API_HOST,
    port=API_PORT,
)
fast_api_app_unprotected = fast_api_instance.create_app()
fast_api_app_protected = fast_api_instance.include_router(
    prefix="/protected", dependencies=[JWT_APP.token_dependency]
)
