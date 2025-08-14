"""
Class to handle SQLAlchemy operations for the application.

This class provides methods to interact with the database using SQLAlchemy ORM.
It includes methods for creating, reading, updating, and deleting records in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from src.util.custom_error import CustomError


class SqlAlchemyHandler:
    """
    SqlAlchemyHandler is responsible for managing the SQLAlchemy session and engine.
    """

    BASE = declarative_base()

    def __init__(self, database_url: str):
        """
        Initializes the SqlAlchemyHandler with the given database URL.
        """
        self._engine = None
        self._session = None

        self._create_engine(database_url)

    def _create_engine(self, database_url: str) -> None:
        """
        Creates the SQLAlchemy engine with the provided database URL.
        If the database does not exist, it will be created.
        Raises a CustomError if there is an issue creating the engine.
        """
        try:
            self._engine = create_engine(
                database_url,
                echo=False,
                connect_args={"check_same_thread": False},
            )
        except Exception as e:
            message = f"Error creating engine with database URL {database_url}: {str(e)}"
            code = 1

            raise CustomError(message, code) from e

    def create_all_metadata(self) -> None:
        """
        Creates all tables in the database based on the defined metadata.
        If the database does not exist, it will be created.
        """
        try:
            db_url = self._engine.url

            if not database_exists(db_url):
                create_database(db_url)

            self.BASE.metadata.create_all(self._engine)
        except Exception as e:
            message = f"Error creating database tables: {str(e)}"
            code = 2

            raise CustomError(message, code) from e

    def _create_session(self) -> None:
        """
        Creates a new SQLAlchemy session.
        """
        try:
            session_maker = sessionmaker(bind=self._engine)
            self._session = session_maker()
        except Exception as e:
            message = f"Error creating session: {str(e)}"
            code = 3

            raise CustomError(message, code) from e

    def _close_session(self) -> None:
        """
        Closes the current SQLAlchemy session.
        """
        if self._session:
            self._session.close()

    def insert_data(self, data: object) -> None:
        """
        Inserts data into the database.
        """
        self._create_session()

        try:
            self._session.add(data)
            self._session.commit()
        except Exception as e:
            self._session.rollback()

            message = f"Error inserting data: {str(e)}"
            code = 4

            raise CustomError(message, code) from e
        finally:
            self._close_session()
