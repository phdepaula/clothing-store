"""
Module for handling user-related routes.
"""

from typing import Dict

from src.app.db_app import DB_APP
from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.routes.route import Route
from src.schemas.users.users import (
    LoginUserResponseSchema,
    LoginUserSchema,
    RegisterUserResponseSchema,
    RegisterUserSchema,
)
from src.tables.users import Users
from src.util.hash_generator import HashGenerator


class UsersRoute(Route):
    """
    Class to define and manage user-related routes for the FastAPI application.
    """

    NAME = "users"

    def __init__(
        self, fast_api_instance: FastApiHandler, jwt_instance: JwtHandler
    ):
        """
        Initializes the UsersRoute class.
        """
        super().__init__(fast_api_instance, jwt_instance, self.NAME)

        self.hash_generator = HashGenerator()

    def _get_endpoints(self) -> Dict:
        """
        Method to get the endpoints of the UsersRoute class.
        """
        endpoints = {
            "login_user": {
                Route.PATH: "/login_user",
                Route.HTTP_TYPE: Route.POST,
                Route.METHOD: self.login_user,
                Route.MODEL: LoginUserResponseSchema,
            },
            "register_user": {
                Route.PATH: "/register_user",
                Route.HTTP_TYPE: Route.POST,
                Route.METHOD: self.register_user,
                Route.MODEL: RegisterUserResponseSchema,
            },
        }

        return endpoints

    async def login_user(self, form: LoginUserSchema) -> Dict:
        """
        Route to log in a user.

        **Parameters:**
        - username: str - The username of the user.
        - password: str - The password of the user.

        **Returns:**
        - A JSON response with a success message and an access token.
        """
        try:
            username = form.username
            password = form.password

            if not username or not password:
                raise ValueError("Username and password are required.")

            user_record = DB_APP.select_data(Users, username=username)

            if not user_record:
                raise ValueError("Invalid username.")

            password_valid = self.hash_generator.verify_password(
                password, user_record[0].password
            )

            if not password_valid:
                raise ValueError("Invalid password.")

            access_token = self.jwt_instance.create_access_token(
                data={"sub": username}
            )

            return {
                "message": "User logged in successfully.",
                "access_token": access_token,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))

    async def register_user(self, form: RegisterUserSchema) -> Dict:
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
                "message": "User registered successfully.",
                "access_token": access_token,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))
