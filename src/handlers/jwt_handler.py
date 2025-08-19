"""
Class to handle JWT operations.

This class provides methods to create and verify JWT tokens for user authentication.
"""

from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from src.util.custom_error import CustomError


class JwtHandler:
    """
    JwtHandler is responsible for managing JWT operations.
    """

    def __init__(self, secret_key: str, algorithm: str):
        """
        Initializes the JwtHandler with the given secret key and algorithm.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self, data: Dict, minutes_to_expire: int = 15
    ) -> str:
        """
        Creates a JWT access token with the given data and expiration time.
        """
        try:
            to_encode = data.copy()
            expire = datetime.now().astimezone() + timedelta(
                minutes=minutes_to_expire
            )
            to_encode.update({"exp": expire})

            return jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
        except Exception as e:
            message = f"Error creating access token: {str(e)}"
            code = 30

            raise CustomError(message, code) from e

    def decode_jwt(self, token: str) -> Dict:
        """
        Decodes a JWT token and returns the payload.
        Raises CustomError if the token is invalid or expired.
        """
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )

            return payload
        except ExpiredSignatureError as e:
            message = "Token has expired"
            code = 31

            raise CustomError(message, code) from e
        except JWTError as e:
            message = f"Invalid token: {str(e)}"
            code = 32

            raise CustomError(message, code) from e
        except Exception as e:
            message = f"Error decoding JWT token: {str(e)}"
            code = 33

            raise CustomError(message, code) from e
