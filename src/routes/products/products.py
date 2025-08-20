"""
Module for handling product-related routes in the application.
"""

# pylint: disable=R0801

from typing import Dict

from src.handlers.fast_api_handler import FastApiHandler
from src.handlers.jwt_handler import JwtHandler
from src.handlers.sql_alchemy_handler import SqlAlchemyHandler
from src.routes.route import Route
from src.schemas.products.products import (
    DeleteProductsResponseSchema,
    DeleteProductsSchema,
    FetchTop10ProductsByCategoryResponseSchema,
    GetProductsByCategoryResponseSchema,
    RegisterProductsResponseSchema,
    RegisterProductsSchema,
    UpdateProductsResponseSchema,
    UpdateProductsSchema,
)
from src.tables.products import Products


class ProductsRoute(Route):
    """
    Class to define and manage product-related routes for the FastAPI application.
    """

    NAME = "products"

    def __init__(
        self,
        fast_api_instance: FastApiHandler,
        jwt_instance: JwtHandler,
        db_instance: SqlAlchemyHandler,
    ):
        """
        Initializes the ProductsRoute class.
        """
        super().__init__(
            fast_api_instance,
            jwt_instance,
            db_instance,
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
            "update_product": {
                Route.PATH: "/update_product",
                Route.HTTP_TYPE: Route.PUT,
                Route.METHOD: self._update_product,
                Route.MODEL: UpdateProductsResponseSchema,
            },
            "delete_product": {
                Route.PATH: "/delete_product",
                Route.HTTP_TYPE: Route.DELETE,
                Route.METHOD: self._delete_product,
                Route.MODEL: DeleteProductsResponseSchema,
            },
            "fetch_top_10_products_by_category": {
                Route.PATH: "/fetch_top_10_products_by_category",
                Route.HTTP_TYPE: Route.GET,
                Route.METHOD: self._fetch_top_10_products_by_category,
                Route.MODEL: FetchTop10ProductsByCategoryResponseSchema,
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
            await self.db_instance.insert_data(new_product)

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

            products = await self.db_instance.select_data(
                Products, category__eq=category.title()
            )

            return {
                "message": "Products successfully obtained!",
                "products": products,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))

    async def _update_product(self, form: UpdateProductsSchema) -> Dict:
        """
        Route to update a product.

        **Parameters:**
        - product_id: int - The id of the product.
        - name: str - The name of the product.
        - description: str - A description of the product.
        - category: str - The category of the product.
        - price: float - The price of the product.
        - image_url: str - The URL of the product image.

        **Returns:**
        - A JSON response with a success message.
        """
        try:
            product_id = form.product_id
            name = form.name.title()
            description = form.description.capitalize()
            category = form.category.title()
            price = form.price
            image_url = form.image_url

            if not all(
                [product_id, name, description, category, price, image_url]
            ):
                raise ValueError("There are required fields that are empty.")

            await self.db_instance.update_data_table(
                Products,
                {Products.id: product_id},
                {
                    Products.name: name,
                    Products.description: description,
                    Products.price: price,
                    Products.image_url: image_url,
                },
            )

            return {
                "message": f"Product {product_id} updated successfully.",
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))

    async def _delete_product(self, form: DeleteProductsSchema) -> Dict:
        """
        Route to delete a product.

        **Parameters:**
        - product_id: int - The id of the product.

        **Returns:**
        - A JSON response with a success message.
        """
        try:
            product_id = form.product_id

            if not product_id:
                raise ValueError("Product id should be informed.")

            await self.db_instance.delete_data_table(
                Products,
                {Products.id: product_id},
            )

            return {
                "message": f"Product {product_id} deleted successfully.",
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))

    async def _fetch_top_10_products_by_category(
        self,
    ) -> Dict:
        """
        Route to fetch the top 10 products by category.

        **Returns:**
        - A JSON response with the top 10 products for all categories.
        """
        try:
            products = await self.db_instance.select_data(Products)
            product_by_category = {}

            for product in products:
                category = product["category"]
                product_list = product_by_category.setdefault(category, [])

                if len(product_list) < 10:
                    product_list.append(product)

            return {
                "message": "Products grouped by category fetched successfully.",
                "products": product_by_category,
            }
        except Exception as e:
            self.fast_api_instance.raise_http_exception(str(e))
