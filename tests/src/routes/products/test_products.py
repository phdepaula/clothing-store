"""
Tests for src/routes/products/products.py
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.routes.products.products import ProductsRoute
from src.schemas.products.products import (
    DeleteProductsSchema,
    RegisterProductsSchema,
    UpdateProductsSchema,
)


@pytest.fixture
def mock_fast_api():
    """
    Creating a mock for fast api.
    """
    mock = MagicMock()
    mock.raise_http_exception = MagicMock(
        side_effect=lambda msg, status_code=500: (_ for _ in ()).throw(
            HTTPException(status_code=status_code, detail=msg)
        )
    )

    return mock


@pytest.fixture
def mock_jwt():
    """
    Creating a mock for jwt.
    """
    return MagicMock()


@pytest.fixture
def mock_db():
    """
    Creating a mock for db.
    """
    mock = AsyncMock()
    mock.insert_data = AsyncMock()
    mock.select_data = AsyncMock()
    mock.update_data_table = AsyncMock()
    mock.delete_data_table = AsyncMock()

    return mock


@pytest.fixture
def products_route(mock_fast_api, mock_jwt, mock_db):
    """Instantiate ProductsRoute with mocks."""
    return ProductsRoute(mock_fast_api, mock_jwt, mock_db)


def test_get_endpoints(products_route):
    """Check that all endpoints exist."""
    endpoints = products_route._get_endpoints()

    assert "register_product" in endpoints
    assert "get_products_by_category" in endpoints
    assert "update_product" in endpoints
    assert "delete_product" in endpoints
    assert "fetch_top_10_products_by_category" in endpoints


# -------------------- register product --------------------


@pytest.mark.asyncio
async def test_register_product_success(products_route):
    """Test registering a product successfully."""
    form = RegisterProductsSchema(
        name="caderno",
        description="um caderno simples",
        category="papelaria",
        price=10.5,
        image_url="http://img.com/caderno.jpg",
    )

    result = await products_route._register_product(form)

    assert result["message"] == "Product registered successfully."


@pytest.mark.asyncio
async def test_register_product_missing_fields(products_route):
    """Test registering a product with missing fields."""
    form = RegisterProductsSchema(
        name="", description="", category="", price=1, image_url=""
    )

    with pytest.raises(HTTPException) as exc_info:
        await products_route._register_product(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "There are required fields that are empty."


# -------------------- get products by category --------------------


@pytest.mark.asyncio
async def test_get_products_by_category_success(products_route, mock_db):
    """Test getting products by category successfully."""
    mock_db.select_data.return_value = [{"id": 1, "category": "Books"}]

    result = await products_route._get_products_by_category("books")

    assert result["message"] == "Products successfully obtained!"
    assert result["products"] == [{"id": 1, "category": "Books"}]


@pytest.mark.asyncio
async def test_get_products_by_category_missing(products_route):
    """Test getting products without specifying category."""
    with pytest.raises(HTTPException) as exc_info:
        await products_route._get_products_by_category("")

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Category should be informed."


# -------------------- update product --------------------


@pytest.mark.asyncio
async def test_update_product_success(products_route):
    """Test updating a product successfully."""
    form = UpdateProductsSchema(
        product_id=1,
        name="lapis",
        description="lapis grafite",
        category="papelaria",
        price=1.5,
        image_url="http://img.com/lapis.jpg",
    )

    result = await products_route._update_product(form)

    assert result["message"] == "Product 1 updated successfully."


@pytest.mark.asyncio
async def test_update_product_missing_fields(products_route):
    """Test updating a product with missing fields."""
    form = UpdateProductsSchema(
        product_id=0,
        name="",
        description="",
        category="",
        price=1,
        image_url="",
    )

    with pytest.raises(HTTPException) as exc_info:
        await products_route._update_product(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "There are required fields that are empty."


# -------------------- delete product --------------------


@pytest.mark.asyncio
async def test_delete_product_success(products_route):
    """Test deleting a product successfully."""
    form = DeleteProductsSchema(product_id=1)

    result = await products_route._delete_product(form)

    assert result["message"] == "Product 1 deleted successfully."


@pytest.mark.asyncio
async def test_delete_product_missing_id(products_route):
    """Test deleting a product without specifying id."""
    form = DeleteProductsSchema(product_id=0)

    with pytest.raises(HTTPException) as exc_info:
        await products_route._delete_product(form)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Product id should be informed."


# -------------------- fetch top 10 products --------------------


@pytest.mark.asyncio
async def test_fetch_top_10_products_by_category(products_route, mock_db):
    """Test fetching top 10 products by category."""
    mock_db.select_data.return_value = [
        {"id": i, "category": "Books"} for i in range(15)
    ]

    result = await products_route._fetch_top_10_products_by_category()

    assert (
        result["message"]
        == "Products grouped by category fetched successfully."
    )
    assert "Books" in result["products"]
    assert len(result["products"]["Books"]) == 10
