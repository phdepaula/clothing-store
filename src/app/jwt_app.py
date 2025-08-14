"""
Module for creating a instance for JWT operations.
"""

import os

from dotenv import load_dotenv

from src.handlers.jwt_handler import JwtHandler

# Load environment variables from a .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

JWT_APP = JwtHandler(secret_key=SECRET_KEY, algorithm=ALGORITHM)
