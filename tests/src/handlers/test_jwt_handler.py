"""
Tests for src/handlers/jwt_handler.py
"""

from src.handlers.jwt_handler import JwtHandler
from src.util.custom_error import CustomError


def create_jwt_instance(secret_key: str, algorithm: str) -> JwtHandler:
    """
    Method to create jwt instance
    """
    return JwtHandler(secret_key, algorithm)


def test_create_access_token():
    """
    Test to test create_access_token method.
    """
    instance = create_jwt_instance("teste", "HS256")
    data = {"sub": "user_test"}

    access_token = instance.create_access_token(data)
    print(access_token)

    assert isinstance(access_token, str) is True


def test_create_access_token_with_error():
    """
    Test to test create_access_token method.
    """
    instance = create_jwt_instance("teste", "teste")
    data = {"sub": "user_test"}
    error = None

    try:
        instance.create_access_token(data)
    except CustomError as custom_error:
        error = custom_error

    assert error.code == 30
    assert (
        error.message
        == "Error creating access token: Algorithm teste not supported."
    )


def test_decode_jwt():
    """
    Test to test decode_jwt method.
    """
    instance = create_jwt_instance("test_decode_jwt", "HS256")
    data = {"sub": "user_decode_jwt"}
    access_token = instance.create_access_token(data)
    print(access_token)
    payload = instance.decode_jwt(access_token)

    assert payload["sub"] == "user_decode_jwt"
    assert payload["exp"] is not None


def test_decode_jwt_with_error():
    """
    Test to test decode_jwt method with error.
    """
    instance = create_jwt_instance("test_decode_jwt", "HS256")

    error_expired_token = None

    try:
        instance.decode_jwt(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2RlY29kZV9qd3QiLCJleHAiOjE3NTU2MjA3MDl9.lUIGBhS32A-CQh72SkmIKqEZwk5HFQuI6Oa9cz29210"
        )
    except CustomError as custom_error:
        error_expired_token = custom_error

    error_invalid_token = None

    try:
        instance.decode_jwt("invalid")
    except CustomError as custom_error:
        error_invalid_token = custom_error

    assert error_expired_token.code == 31
    assert error_expired_token.message == "Token has expired"
    assert error_invalid_token.code == 32
    assert error_invalid_token.message == "Invalid token: Not enough segments"
