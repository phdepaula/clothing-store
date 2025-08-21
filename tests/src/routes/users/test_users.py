"""
Tests for src/routes/users/users.py
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.routes.users.users import UsersRoute
from src.schemas.users.users import (
    LoginUserSchema,
    RegisterUserSchema,
    UpdateUserSchema,
)


@pytest.fixture
def mock_fast_api():
    """
    Creating a mock for fast api.
    """
    mock = MagicMock()
    mock.raise_http_exception = MagicMock(
        side_effect=lambda detail, status_code=500: (_ for _ in ()).throw(
            HTTPException(status_code=status_code, detail=detail)
        )
    )

    return mock


@pytest.fixture
def mock_jwt():
    """
    Creating a mock for jwt.
    """
    mock = MagicMock()
    mock.create_access_token = MagicMock(return_value="fake_token")

    return mock


@pytest.fixture
def mock_db():
    """
    Creating a mock for db.
    """
    mock = AsyncMock()
    mock.insert_data = AsyncMock()
    mock.select_data = AsyncMock()
    mock.update_data_table = MagicMock()

    return mock


@pytest.fixture
def users_route(mock_fast_api, mock_jwt, mock_db):
    """
    Creating users route.
    """
    return UsersRoute(mock_fast_api, mock_jwt, mock_db)


def test_get_endpoints(users_route):
    endpoints = users_route._get_endpoints()

    assert "login_user" in endpoints
    assert "register_user" in endpoints
    assert "update_user" in endpoints


@pytest.mark.asyncio
async def test_login_user_success(users_route, mock_db):
    """
    Test to test login_user endpoint successfully.
    """
    form = LoginUserSchema(username="pedro", password="123")
    mock_db.select_data.return_value = [
        {"password": users_route.hash_generator.get_password_hash("123")}
    ]

    result = await users_route._login_user(form)

    assert result["message"] == "User logged in successfully."
    assert "access_token" in result


@pytest.mark.asyncio
async def test_login_without_username(users_route, mock_db):
    """
    Test to test login_user endpoint with empty username.
    """
    form = LoginUserSchema(username="", password="123")
    mock_db.select_data.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await users_route._login_user(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Username and password are required."


@pytest.mark.asyncio
async def test_login_user_invalid_username(users_route, mock_db):
    """
    Test to test login_user endpoint with invalid username.
    """
    form = LoginUserSchema(username="pedro", password="123")
    mock_db.select_data.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await users_route._login_user(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Invalid username."


@pytest.mark.asyncio
async def test_login_user_invalid_password(users_route, mock_db):
    """
    Test to test login_user endpoint with invalid password.
    """
    form = LoginUserSchema(username="pedro", password="wrong")
    mock_db.select_data.return_value = [
        {"password": users_route.hash_generator.get_password_hash("123")}
    ]

    with pytest.raises(HTTPException) as exc_info:
        await users_route._login_user(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Invalid password."


@pytest.mark.asyncio
async def test_register_user_success(users_route):
    """
    Test to test register_user method successfully.
    """
    form = RegisterUserSchema(username="pedro", password="123", role="user")
    result = await users_route._register_user(form)

    assert result["message"] == "User registered successfully."
    assert "access_token" in result


@pytest.mark.asyncio
async def test_register_user_without_username(users_route):
    """
    Test to test register_user with empty.
    """
    form = RegisterUserSchema(username="", password="123", role="guest")

    with pytest.raises(Exception) as exc_info:
        await users_route._register_user(form)

    assert exc_info.value.status_code == 500
    assert (
        exc_info.value.detail == "Username, password, and role are required."
    )


@pytest.mark.asyncio
async def test_register_user_invalid_role(users_route):
    """
    Test to test register_user with invalid role.
    """
    form = RegisterUserSchema(username="pedro", password="123", role="guest")

    with pytest.raises(Exception) as exc_info:
        await users_route._register_user(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Role must be either 'admin' or 'user'."


@pytest.mark.asyncio
async def test_update_user_success(users_route):
    """
    Test to test update_user method successfully.
    """
    form = UpdateUserSchema(
        username="pedro", new_password="1234", new_role="admin"
    )

    result = await users_route._update_user(form)

    assert result["message"] == "User pedro updated successfully."


@pytest.mark.asyncio
async def test_update_without_username(users_route):
    """
    Test to test update_user with empty role.
    """
    form = UpdateUserSchema(username="", new_password="1234", new_role="admin")

    with pytest.raises(Exception) as exc_info:
        await users_route._update_user(form)

    assert exc_info.value.status_code == 500
    assert (
        exc_info.value.detail
        == "Username, new password, and nw role are required."
    )


@pytest.mark.asyncio
async def test_update_user_invalid_role(users_route):
    """
    Test to test update_user with invalid role.
    """
    form = UpdateUserSchema(
        username="pedro", new_password="1234", new_role="super_admin"
    )

    with pytest.raises(Exception) as exc_info:
        await users_route._update_user(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Role must be either 'admin' or 'user'."
