"""
Module for handling user-related routes.
"""

from typing import Dict

from src.app.db_app import DB_APP
from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.routes.route import Route
from src.schemas.users.users import (
    RegisterUserResponseSchema,
    RegisterUserSchema,
)
from src.tables.users import Users
from src.util.hash_generator import HashGenerator


class UserRoute(Route):
    """
    Class to define and manage user-related routes for the FastAPI application.
    """

    NAME = "users"

    def __init__(
        self, fast_api_instance: FastApiHandler, jwt_instance: JwtHandler
    ):
        """
        Initializes the UserRoute class.
        """
        super().__init__(fast_api_instance, jwt_instance, self.NAME)

        self.hash_generator = HashGenerator()

    def _get_endpoints(self) -> Dict:
        """
        Method to get the endpoints of the UserRoute class.
        """
        endpoints = {
            "register_user": {
                Route.PATH: "/register_user",
                Route.HTTP_TYPE: Route.POST,
                Route.METHOD: self.register_user,
                Route.MODEL: RegisterUserResponseSchema,
            }
        }

        return endpoints

    async def register_user(self, form: RegisterUserSchema):
        """
        Route to register a user.

        **Parameters:**
        - username: str - The username of the user.
        - password: str - The password of the user.
        - role: str - The role of the user (e.g., 'admin', 'user').

        **Returns:**
        - A JSON response with a success message and an access token.
        """
        try:
            username = form.username
            password = form.password
            role = form.role

            if not username or not password or not role:
                raise ValueError("Username, password, and role are required.")

            if role not in ["admin", "user"]:
                raise ValueError("Role must be either 'admin' or 'user'.")

            access_token = self.jwt_instance.create_access_token(
                data={"sub": username}
            )

            hashed_password = self.hash_generator.get_password_hash(password)

            new_user = Users(
                username=username, password=hashed_password, role=role
            )
            DB_APP.insert_data(new_user)

            return {
                "message": "User registered successfully",
                "access_token": access_token,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))
