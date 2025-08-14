"""
Class to handle with FastAPI operations for the application.

This class provides methods to interact with the FastAPI application.
It includes methods for setting up routes and initializing the application.
"""

# pylint: disable=R0913,R0917

from typing import Callable, List

import uvicorn
from fastapi import APIRouter, Depends, FastAPI

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

    def create_app(self) -> FastAPI:
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

            return self.app
        except Exception as e:
            message = f"Error creating FastAPI application: {str(e)}"
            code = 20

            raise CustomError(message, code) from e

    def include_router(
        self, prefix: str, dependencies: List[Callable]
    ) -> APIRouter:
        """
        Include a router in the FastAPI application.
        """
        try:
            if self.app is None:
                raise ValueError(
                    "FastAPI application is not created yet. Call create_app() first."
                )

            protected_router = APIRouter(
                prefix=prefix,
                dependencies=self._generate_dependencies(dependencies),
            )
            self.app.include_router(protected_router)

            return protected_router
        except Exception as e:
            message = (
                f"Error including router in FastAPI application: {str(e)}"
            )
            code = 21

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
            code = 22

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
            code = 23

            raise CustomError(message, code) from e
