"""
Class to handle with FastAPI operations for the application.

This class provides methods to interact with the FastAPI application.
It includes methods for setting up routes and initializing the application.
"""

# pylint: disable=R0913,R0917

from typing import Callable, List

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from src.util.custom_error import CustomError


class FastApiHandler:
    """
    FastAPIHandler is responsible for managing the FastAPI application.
    """

    def __init__(
        self, title: str, description: str, version: str, host: str, port: int
    ):
        self.title = title
        self.description = description
        self.version = version
        self.host = host
        self.port = port
        self.app = None

    def create_app(self) -> None:
        """
        Create and return a FastAPI application instance.
        """
        try:
            self.app = FastAPI(
                title=self.title,
                description=self.description,
                version=self.version,
                docs_url="/",
                redoc_url=None,
            )
        except Exception as e:
            message = f"Error creating FastAPI application: {str(e)}"
            code = 20

            raise CustomError(message, code) from e

    def create_router(
        self, prefix: str, dependencies: List[Callable] = None
    ) -> APIRouter:
        """
        Create and return a FastAPI router with the specified prefix and dependencies.
        """
        try:
            if self.app is None:
                raise ValueError(
                    "FastAPI application is not created yet. Call create_app() first."
                )

            protected_router = APIRouter(
                prefix=prefix,
                dependencies=(
                    []
                    if not dependencies
                    else self._generate_dependencies(dependencies)
                ),
            )

            return protected_router
        except Exception as e:
            message = f"Error creating router: {str(e)}"
            code = 21

            raise CustomError(message, code) from e

    def include_router(self, api_route: APIRouter) -> None:
        """
        Include a router in the FastAPI application.
        """
        try:
            self.app.include_router(api_route)
        except Exception as e:
            message = (
                f"Error including router in FastAPI application: {str(e)}"
            )
            code = 22

            raise CustomError(message, code) from e

    def _generate_dependencies(
        self, dependencies: List[Callable]
    ) -> List[Depends]:
        """
        Generate dependencies for the FastAPI application.
        """
        try:
            return [Depends(dep) for dep in dependencies]
        except Exception as e:
            message = f"Error generating dependencies: {str(e)}"
            code = 23

            raise CustomError(message, code) from e

    def run_app(self) -> None:
        """
        Run the FastAPI application.
        """
        try:
            if self.app is None:
                raise ValueError(
                    "FastAPI application is not created yet. Call create_app() first."
                )

            uvicorn.run(self.app, host=self.host, port=self.port)
        except Exception as e:
            message = f"Error running FastAPI application: {str(e)}"
            code = 24

            raise CustomError(message, code) from e

    def raise_http_exception(
        self, detail: str, status_code: int = 500
    ) -> HTTPException:
        """
        Raise an HTTPException with the specified status code and detail.
        """
        raise HTTPException(status_code=status_code, detail=detail)
