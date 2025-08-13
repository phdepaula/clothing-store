"""
Main entry point for the application.
This script initializes the application and starts the main event loop.
"""

# pylint: disable=W0611

from src.app.db_app import DB_APP
from src.tables.products import Products
from src.tables.users import Users

if __name__ == "__main__":
    # Create database application
    DB_APP.create_all_metadata()
