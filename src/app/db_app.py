"""
Module responsible for creating application instance for database operations.
"""

import os

from dotenv import load_dotenv

from src.handlers.sql_alchemy_handler import SqlAlchemyHandler

# Load environment variables from a .env file
load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_APP = SqlAlchemyHandler(database_url=DB_URL)
