"""
Schema for product data validation in a clothing store application.
"""

from typing import Dict, List, Union

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
        description=(
            "Confirmation message after successful product registration"
        ),
    )


class GetProductsByCategoryResponseSchema(BaseModel):
    """
    Schema for the response after getting a product.
    """

    message: str = Field(
        "Products successfully obtained!",
        description=(
            "Confirmation message returned when products "
            + "are retrieved successfully."
        ),
    )
    products: List = Field(description="List of all products in the category")


class UpdateProductsSchema(BaseModel):
    """
    Schema for updating a product.
    """

    product_id: int = Field(description="The id of the product.")
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


class UpdateProductsResponseSchema(BaseModel):
    """
    Schema for the response after updating a product.
    """

    message: str = Field(
        "Product updated successfully.",
        description="Confirmation message after successful update.",
    )


class DeleteProductsSchema(BaseModel):
    """
    Schema for deleting a product.
    """

    product_id: int = Field(description="The id of the product.")


class DeleteProductsResponseSchema(BaseModel):
    """
    Schema for the response after deleting a product.
    """

    message: str = Field(
        "Product deleted successfully.",
        description="Confirmation message after successful delete.",
    )


class FetchTop10ProductsByCategoryResponseSchema(BaseModel):
    """
    Schema for the response to fetch top 10 products \
    by category.
    """

    message: str = Field(
        "Products grouped by category fetched successfully.",
        description="Confirmation message after successful fetch.",
    )
    products: Dict[str, List[Dict[str, Union[str, int]]]] = Field(
        description="List with the top 10 products of each category."
    )
