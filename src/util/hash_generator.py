"""
Module responsible for generating hash values for various purposes.
This module is used to create secure hashes for passwords
and other sensitive data.
"""

from passlib.context import CryptContext


class HashGenerator:
    """
    Class to generate and verify hashes.
    """

    def __init__(self):
        """
        Initializes the HashGenerator with a specified hashing algorithm.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        """
        Generates a hash for the given password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        """
        Verifies if the plain password matches the hashed password.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
