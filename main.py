"""
Main entry point for the application.
This script initializes the application and starts the main event loop.
"""

# pylint: disable=W0611

from src.app.db_app import DB_APP
from src.app.fast_api_app import FAST_API_APP
from src.app.jwt_app import JWT_APP
from src.tables.products import Products
from src.tables.users import Users
from src.routes.users.users import UserRoute

if __name__ == "__main__":
    # Create database application
    DB_APP.create_all_metadata()

    # Register routes
    routes_to_register = [UserRoute]

    for route in routes_to_register:
        route_instance = route(
            fast_api_instance=FAST_API_APP,
            jwt_instance=JWT_APP,
        )
        route_instance.build_routes()

    # Run the FastAPI application
    FAST_API_APP.run_app()
