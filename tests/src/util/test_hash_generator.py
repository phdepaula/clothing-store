"""
Tests for src/util/hash_generator.py
"""

from src.util.hash_generator import HashGenerator


def test_get_password_hash():
    """
    Test to test get_password_hash method.
    """
    instance = HashGenerator()
    password = "password"
    hashed_password = instance.get_password_hash(password)

    assert password != hashed_password


def test_verify_password():
    """
    Test to test verify_password method.
    """
    instance = HashGenerator()
    password = "password"
    hashed_password = instance.get_password_hash(password)

    verify_status_password = instance.verify_password(
        password, hashed_password
    )
    verify_status_other_password = instance.verify_password(
        "test", hashed_password
    )

    assert verify_status_password is True
    assert verify_status_other_password is False
