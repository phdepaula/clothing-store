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
        ..., max_length=100, description="Password for the user"
    )
    role: str = Field(
        ...,
        description="Role of the user, either 'admin' or 'user'",
    )


class RegisterUserResponseSchema(BaseModel):
    """
    Schema for the response after registering a user.
    """

    message: str = Field(
        "User registered successfully.",
        description="Confirmation message after successful registration",
    )
    access_token: str = Field(
        ..., description="JWT access token for the registered user"
    )


class LoginUserSchema(BaseModel):
    """
    Schema for user login.
    """

    username: str = Field(
        ..., max_length=50, description="Username of the user"
    )
    password: str = Field(
        ..., max_length=100, description="Password for the user"
    )


class LoginUserResponseSchema(BaseModel):
    """
    Schema for the response after user login.
    """

    message: str = Field(
        "User logged in successfully.",
        description="Confirmation message after successful login",
    )
    access_token: str = Field(
        ..., description="JWT access token for the logged-in user"
    )


class UpdateUserSchema(BaseModel):
    """
    Schema for update user.
    """

    username: str = Field(
        ..., max_length=50, description="Username of the user"
    )
    new_role: str = Field(
        ...,
        description="New role of the user, either 'admin' or 'user'",
    )
    new_password: str = Field(
        ..., max_length=100, description="New password for the user"
    )


class UpdateUserResponseSchema(BaseModel):
    """
    Schema for the response after updating a user.
    """

    message: str = Field(
        "User updated successfully.",
        description="Confirmation message after successful update",
    )
