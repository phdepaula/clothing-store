"""
Class to handle SQLAlchemy operations for the application.

This class provides methods to interact with the database using SQLAlchemy ORM.
It includes methods for creating, reading, updating, and deleting records in the database.
"""

from typing import List

from sqlalchemy import and_, create_engine
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

    def select_data(
        self,
        model: object,
        order_by: str = None,
        order_desc: bool = False,
        **filters,
    ) -> List:
        """
        Selects data from the database with flexible filters and ordering.

        Filters:
            attr=value           -> Equal to
            attr__eq=value       -> Equal to
            attr__gt=value       -> Greater than
            attr__lt=value       -> Less than
            attr__ge=value       -> Greater than or equal to
            attr__le=value       -> Less than or equal to
            attr__like=value     -> LIKE '%value%'

        Ordering:
            order_by="column"    -> Order by the specified column
            order_desc=True      -> Descending order

        Example:
            select_data(User, name__like="Ped", age__gt=18, order_by="age", order_desc=True)
        """
        # pylint: disable=R0914,R0912
        self._create_session()

        try:
            query = self._session.query(model)
            conditions = []

            # Build filters
            for key, value in filters.items():
                if "__" in key:
                    attr, op = key.split("__", 1)
                else:
                    attr, op = key, "eq"

                if not hasattr(model, attr):
                    raise ValueError(
                        f"Attribute '{attr}' does not exist in model '{model.__name__}'."
                    )

                column = getattr(model, attr)

                if op == "eq":
                    conditions.append(column == value)
                elif op == "gt":
                    conditions.append(column > value)
                elif op == "lt":
                    conditions.append(column < value)
                elif op == "ge":
                    conditions.append(column >= value)
                elif op == "le":
                    conditions.append(column <= value)
                elif op == "like":
                    conditions.append(column.like(f"%{value}%"))
                else:
                    raise ValueError(f"Operator '{op}' is not supported.")

            # Apply filters
            if conditions:
                query = query.filter(and_(*conditions))

            # Apply ordering
            if order_by:
                if not hasattr(model, order_by):
                    raise ValueError(
                        f"Attribute '{order_by}' does not exist in model '{model.__name__}'."
                    )

                column_order = getattr(model, order_by)

                if order_desc:
                    column_order = column_order.desc()

                query = query.order_by(column_order)

            return query.all()
        except Exception as e:
            self._session.rollback()

            message = f"Error selecting data: {str(e)}"
            code = 5

            raise CustomError(message, code) from e
        finally:
            self._close_session()
