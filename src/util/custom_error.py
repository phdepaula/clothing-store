"""
Module for custom error handling in the application.

This module defines a custom error class for handling
application-specific errors.
It extends the built-in Exception class to provide
additional context and functionality.
"""


class CustomError(Exception):
    """
    CustomError is used to handle application-specific errors.
    """

    def __init__(self, message: str, code: int):
        """
        Initializes the CustomError with a message and an optional status code.
        """
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        """
        Returns a string representation of the CustomError.
        """
        return f"Message: {self.message} (Code: {self.code})"
