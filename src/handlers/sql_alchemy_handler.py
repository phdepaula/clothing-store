"""
Class to handle SQLAlchemy operations for the application.

This class provides methods to interact with the database using SQLAlchemy ORM.
It includes methods for creating, reading, updating, and deleting records in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists


class SQLAlchemyHandler:
    """
    SQLAlchemyHandler is responsible for managing the SQLAlchemy session and engine.
    """

    BASE = declarative_base()

    def __init__(self, database_url: str):
        """
        Initializes the SQLAlchemyHandler with the given database URL.
        """
        self._engine = create_engine(
            database_url, echo=False, connect_args={"check_same_thread": False}
        )

    def create_all_metadata(self) -> None:
        """
        Creates all tables in the database based on the defined metadata.
        If the database does not exist, it will be created.
        """
        db_url = self._engine.url

        if not database_exists(db_url):
            create_database(db_url)

        self.BASE.metadata.create_all(self._engine)
