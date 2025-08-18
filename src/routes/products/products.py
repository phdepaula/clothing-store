"""
Module for handling product-related routes in the application.
"""

from typing import Dict

from src.app.db_app import DB_APP
from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.routes.route import Route
from src.schemas.products.products import (
    GetProductsByCategoryResponseSchema,
    RegisterProductsResponseSchema,
    RegisterProductsSchema,
)
from src.tables.products import Products


class ProductsRoute(Route):
    """
    Class to define and manage product-related routes for the FastAPI application.
    """

    NAME = "products"

    def __init__(
        self, fast_api_instance: FastApiHandler, jwt_instance: JwtHandler
    ):
        """
        Initializes the ProductsRoute class.
        """
        super().__init__(
            fast_api_instance,
            jwt_instance,
            self.NAME,
            [self._token_dependency],
        )

    def _get_endpoints(self):
        """
        Method to get the endpoints of the ProductsRoute class.
        """
        endpoints = {
            "register_product": {
                Route.PATH: "/register_product",
                Route.HTTP_TYPE: Route.POST,
                Route.METHOD: self._register_product,
                Route.MODEL: RegisterProductsResponseSchema,
            },
            "get_products_by_category": {
                Route.PATH: "/get_products_by_category",
                Route.HTTP_TYPE: Route.GET,
                Route.METHOD: self._get_products_by_category,
                Route.MODEL: GetProductsByCategoryResponseSchema,
            },
        }

        return endpoints

    async def _register_product(self, form: RegisterProductsSchema) -> Dict:
        """
        Route to register a product.

        **Parameters:**
        - name: str - The name of the product.
        - description: str - A description of the product.
        - category: str - The category of the product.
        - price: float - The price of the product.
        - image_url: str - The URL of the product image.

        **Returns:**
        - A JSON response with a success message.
        """
        try:
            name = form.name.title()
            description = form.description.capitalize()
            category = form.category.title()
            price = form.price
            image_url = form.image_url

            if not all([name, description, category, price, image_url]):
                raise ValueError("There are required fields that are empty.")

            new_product = Products(
                name=name,
                description=description,
                category=category,
                price=price,
                image_url=image_url,
            )
            DB_APP.insert_data(new_product)

            return {
                "message": "Product registered successfully.",
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))

    async def _get_products_by_category(
        self,
        category: str = FastApiHandler.get_query_parameter(
            "Category of the product"
        ),
    ) -> Dict:
        """
        Route to get products.

        **Parameters:**
        - category: str - The category of the product.

        **Returns:**
        - A JSON response with all products for informed category.
        """
        try:
            if not category:
                raise ValueError("Category should be informed.")

            products = DB_APP.select_data(
                Products, category__eq=category.title()
            )

            return {
                "message": "Products successfully obtained!",
                "products": products,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))
