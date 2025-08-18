"""
Schema for product data validation in a clothing store application.
"""

from pydantic import BaseModel, Field


class RegisterProductsSchema(BaseModel):
    """
    Schema for registering a new product.
    """

    name: str = Field(..., max_length=50, description="Name of the product")
    description: str = Field(
        ..., max_length=200, description="Description of the product"
    )
    category: str = Field(
        ..., max_length=50, description="Category of the product"
    )
    price: float = Field(
        ..., gt=0, description="Price of the product, must be greater than 0"
    )
    image_url: str = Field(..., description="URL of the product image.")


class RegisterProductsResponseSchema(BaseModel):
    """
    Schema for the response after registering a product.
    """

    message: str = Field(
        "Product registered successfully.",
        description="Confirmation message after successful product registration",
    )
