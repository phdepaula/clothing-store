"""
Module for building routes in a FastAPI application.
"""

# pylint: disable=R0913,R0917

from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.handlers.sql_alchemy_handler import SqlAlchemyHandler
from src.util.custom_error import CustomError


class Route(ABC):
    """
    Class to define and manage routes for the FastAPI application.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATH = "path"
    HTTP_TYPE = "http_type"
    METHOD = "method"
    MODEL = "model"
    DEPENDENCIES = "dependencies"

    def __init__(
        self,
        fast_api_instance: FastApiHandler,
        jwt_instance: JwtHandler,
        db_instance: SqlAlchemyHandler,
        name: str,
        dependencies: List[Callable] = None,
    ):
        """
        Initializes the Routes class.
        """
        self.fast_api_instance = fast_api_instance
        self.jwt_instance = jwt_instance
        self.db_instance = db_instance
        self.name = name
        self.dependencies = [] if dependencies is None else dependencies
        self.route_app = self._create_app()

    def _create_app(self) -> APIRouter:
        """
        Creates the FastAPI application instance.
        """
        try:
            prefix = f"/{self.name.lower().strip()}"

            return self.fast_api_instance.create_router(
                prefix, self.dependencies
            )
        except Exception as e:
            message = f"Error creating FastAPI app: {str(e)}"
            code = 50
            raise CustomError(message, code) from e

    def _create_route(
        self,
        path: str,
        http_type: str,
        method: Callable,
        response_model: BaseModel = None,
        dependencies: List[Callable] = None,
    ):
        """
        Creates a route based on the type specified.
        """
        try:
            tag_name = self.name.title()
            kwargs = {"tags": [tag_name]}

            if response_model:
                kwargs["response_model"] = response_model

            if dependencies:
                kwargs["dependencies"] = (
                    self.fast_api_instance.generate_dependencies(dependencies)
                )

            self.route_app.add_api_route(
                path=path,
                endpoint=method,
                methods=[http_type.upper()],
                **kwargs,
            )
        except Exception as e:
            message = f"Error creating route: {str(e)}"
            code = 51
            raise CustomError(message, code) from e

    def _token_dependency(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> Dict:
        """
        Dependency to extract and decode the JWT token from the
        HTTP authorization credentials.
        Raises CustomError if no token is provided or
        if the token is invalid.
        """
        try:
            token = credentials.credentials if credentials else None

            if not token:
                raise ValueError("No token provided")

            payload = self.jwt_instance.decode_jwt(token)

            return payload
        except Exception as e:
            message = f"Error in token_dependency: {str(e)}"
            code = 52

            raise CustomError(message, code) from e

    def build_routes(self):
        """
        Abstract method to build routes. Must be implemented by subclasses.
        """
        endpoints = self._get_endpoints()

        for routes_detail in endpoints.values():
            self._create_route(
                path=routes_detail[self.PATH],
                http_type=routes_detail[self.HTTP_TYPE],
                method=routes_detail[self.METHOD],
                response_model=routes_detail.get(self.MODEL, None),
                dependencies=routes_detail.get(self.DEPENDENCIES, None),
            )

        self.fast_api_instance.include_router(self.route_app)

    @abstractmethod
    def _get_endpoints(self) -> Dict:
        """
        Abstract method to get the endpoints of the route.
        Must be implemented by subclasses.
        """
