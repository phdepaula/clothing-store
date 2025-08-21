"""
Tests for src/routes/route.py
"""

"""
Tests for src/routes/route.py using real handler classes.
"""

import pytest
from fastapi import APIRouter

from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.handlers.sql_alchemy_handler import SqlAlchemyHandler
from src.routes.route import Route
from src.util.custom_error import CustomError


# Dummy subclass for Route to implement abstract methods
class DummyRoute(Route):
    """Creating dummy route"""

    NAME = "dummy"

    def __init__(
        self,
        fast_api_instance: FastApiHandler,
        jwt_instance: JwtHandler,
        db_instance: SqlAlchemyHandler,
    ):
        """
        Initializes the ProductsRoute class.
        """
        super().__init__(
            fast_api_instance,
            jwt_instance,
            db_instance,
            self.NAME,
            [self._token_dependency],
        )

    def _get_endpoints(self):
        return {
            "test": {
                self.PATH: "/test",
                self.HTTP_TYPE: self.GET,
                self.METHOD: lambda: "ok",
            }
        }


@pytest.fixture
def fast_api():
    """
    Create fastapi instance.
    """
    instance = FastApiHandler("title", "description", "version", "host", 5000)
    instance.create_app()

    return instance


@pytest.fixture
def jwt():
    """
    Use a dummy secret for testing
    """
    return JwtHandler("teste", "HS256")


@pytest.fixture
def db():
    """
    Use an in-memory SQLite database for testing
    """
    return SqlAlchemyHandler("sqlite:///:memory:")


def test_create_app(fast_api, jwt, db):
    """
    Test to test app initialization.
    """
    route_instance = DummyRoute(fast_api, jwt, db)

    assert isinstance(route_instance.route_app, APIRouter)
    assert route_instance.route_app.prefix == "/dummy"


def test_create_route(fast_api, jwt, db):
    """
    Test to test create_route method.
    """
    route_instance = DummyRoute(fast_api, jwt, db)

    def dummy_method():
        return "ok"

    route_instance._create_route("/test_create", "GET", dummy_method)

    current_routes = [route.path for route in route_instance.route_app.routes]

    assert ("/dummy/test_create" in current_routes) is True


def test_token_dependency_success(jwt, fast_api, db):
    """
    Method to test token_dependency succesfully.
    """
    route_instance = DummyRoute(fast_api, jwt, db)
    token = jwt.create_access_token({"user_id": 1})

    class Creds:
        credentials = token

    payload = route_instance._token_dependency(Creds())

    assert payload["user_id"] == 1


def test_token_dependency_no_token(fast_api, jwt, db):
    """
    Method to test token_dependency with no token.
    """
    error = None
    route_instance = DummyRoute(fast_api, jwt, db)

    class Creds:
        credentials = None

    try:
        route_instance._token_dependency(Creds())
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 52
    assert error.message == "Error in token_dependency: No token provided"


def test_token_dependency_invalid_token(fast_api, jwt, db):
    """
    Method to test token dependecy with invalid token.
    """
    error = None
    route_instance = DummyRoute(fast_api, jwt, db)

    class Creds:
        credentials = "invalid"

    try:
        route_instance._token_dependency(Creds())
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 52
    assert (
        error.message
        == "Error in token_dependency: Message: Invalid token: Not enough segments (Code: 32)"
    )


def test_build_routes(fast_api, jwt, db):
    """
    Method to test build_routes.
    """
    route_instance = DummyRoute(fast_api, jwt, db)
    route_instance.build_routes()

    current_routes = [route.path for route in route_instance.route_app.routes]

    assert ("/dummy/test" in current_routes) is True
