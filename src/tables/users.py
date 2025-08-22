"""
Module responsible for defining user table structure.
"""

from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    UniqueConstraint,
)

from src.handlers.sql_alchemy_handler import SqlAlchemyHandler


class Users(SqlAlchemyHandler.BASE):
    """
    Class representing the users table in the database.
    """

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("Username", name="unique_username"),)

    id = Column("ID", Integer, primary_key=True, index=True)
    username = Column("Username", String(50), nullable=False)
    password = Column("Password", String(100), nullable=False)
    role = Column(
        "Role",
        String(5),
        CheckConstraint("Role IN ('admin','user')", name="check_role"),
    )
