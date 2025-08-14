"""
Schema for user-related operations in the clothing store application.
"""

from pydantic import BaseModel, Field


class RegisterUserSchema(BaseModel):
    """
    Schema for registering a new user.
    """

    username: str = Field(
        ..., max_length=50, description="Username of the user"
    )
    password: str = Field(
        ..., min_length=8, max_length=100, description="Password for the user"
    )
    role: str = Field(
        ...,
        description="Role of the user, either 'admin' or 'user'",
    )
