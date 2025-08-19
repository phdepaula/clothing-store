"""
Tests for src/util/custom_error.py
"""

from src.util.custom_error import CustomError


def test_custom_error_generation():
    """
    Test to test custom error.
    """
    code = 1
    message = "test message"

    instance = CustomError(message=message, code=code)

    assert str(instance) == f"Message: {message} (Code: {code})"
