"""
Module responsible for defining product table structure.
"""

from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from src.app.db_app import DB_APP

BASE = DB_APP.BASE


class Products(BASE):
    """
    Class representing the products table in the database.
    """

    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("Name", "Category", name="unique_username"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    name = Column("Name", String(50), nullable=False)
    description = Column("Description", String(200), nullable=False)
    category = Column("Category", String(50), nullable=False)
    price = Column("Price", Float, nullable=False)
    image_url = Column("Image_Url", Text, nullable=True)
