"""
Tests for src/handlers/fast_api_handler.py
"""

from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.params import Depends as DependsType
from fastapi.params import Query as QueryType

from src.handlers.fast_api_handler import FastApiHandler
from src.util.custom_error import CustomError


def create_instance(
    title: str, description: str, version: str, host: str, port: int
) -> FastApiHandler:
    """
    Method to create a FastApiHandler instance
    """
    instance = FastApiHandler(title, description, version, host, port)

    return instance


def test_create_app():
    """
    Test to test create_app method.
    """
    instance = create_instance(
        "Teste", "Teste Description", "0.0.0", "0.0.0.0", 8000
    )
    instance.create_app()

    assert isinstance(instance.app, FastAPI) is True
    assert instance.app.title == "Teste"
    assert instance.app.description == "Teste Description"
    assert instance.app.version == "0.0.0"


def test_create_app_with_error():
    """
    Test to test create_app method with error.
    """
    instance = create_instance(None, None, "0.0.0", "0.0.0.0", 8000)
    error = None

    try:
        instance.create_app()
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 20


def test_create_router():
    """
    Test to test create_router method.
    """
    instance = create_instance(
        "Teste", "Teste Description", "0.0.0", "0.0.0.0", 8000
    )
    instance.create_app()

    prefix = "/teste"
    dependencies = [create_instance]
    router = instance.create_router(prefix, dependencies)

    assert isinstance(router, APIRouter) is True
    assert router.prefix == prefix
    assert len(router.dependencies) == len(dependencies)


def test_create_router_with_error():
    """
    Test to test create_router method.
    """
    instance = create_instance(
        "Teste", "Teste Description", "0.0.0", "0.0.0.0", 8000
    )
    error = None

    try:
        prefix = None
        dependencies = []
        instance.create_router(prefix, dependencies)
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 21
    assert (
        error.message
        == "Error creating router: FastAPI application is not created yet. Call create_app() first."
    )


def test_include_router():
    """
    Test to test include_router method.
    """
    instance = create_instance(
        "Teste", "Teste Description", "0.0.0", "0.0.0.0", 8000
    )
    instance.create_app()

    prefix = "/teste"
    dependencies = [create_instance]
    router = instance.create_router(prefix, dependencies)

    @router.get("/ping")
    def ping():
        return {"ping": "pong"}

    instance.include_router(router)

    routes = [route.path for route in instance.app.routes]

    assert f"{prefix}/ping" in routes


def test_include_router_with_error():
    """
    Test to test include_router method with error.
    """
    instance = create_instance(
        "Teste", "Teste Description", "0.0.0", "0.0.0.0", 8000
    )
    instance.create_app()

    error = None

    try:
        instance.include_router(None)
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 22


def test_generate_dependencies():
    """
    Test to test method generate_dependencies.
    """

    def test_method():
        pass

    def test_method_2():
        pass

    list_of_methods = [test_method, test_method_2]
    dependencies = FastApiHandler.generate_dependencies(list_of_methods)

    assert (
        isinstance(dependencies[0], DependsType) is True
        and isinstance(dependencies[1], DependsType) is True
    )
    assert dependencies[0].dependency == test_method
    assert dependencies[1].dependency == test_method_2


def test_generate_dependencies_with_error():
    """
    Test to test method generate_dependencies with error.
    """
    error = None

    try:
        list_of_methods = None
        FastApiHandler.generate_dependencies(list_of_methods)
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 23


def test_raise_http_exception():
    """
    Test to test method raise_http_exception with error.
    """
    error = None

    try:
        detail = "teste"
        status_code = 300
        FastApiHandler.raise_http_exception(detail, status_code)
    except HTTPException as http_error:
        error = http_error

    assert isinstance(error, HTTPException) is True
    assert error.detail == detail
    assert error.status_code == status_code


def test_get_query_parameter():
    """
    Test to test method get_query_parameter with error.
    """
    description = "teste"
    query = FastApiHandler.get_query_parameter(description)

    assert isinstance(query, QueryType) is True
    assert query.description == description
