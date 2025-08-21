"""
Tests for src/handlers/sql_alchemy_handler.py
"""

import pytest
import pytest_asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import BinaryExpression

from src.handlers.sql_alchemy_handler import SqlAlchemyHandler

# Create the base handler (outside fixtures, so we can use its BASE for table definition)
db_url = "sqlite:///:memory:"
test_handler = SqlAlchemyHandler(db_url)


# Define the dummy table using the handler's BASE
class DummyTable(test_handler.BASE):
    """
    Dummy Table creation.
    """

    __tablename__ = "dummy_table"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


@pytest.fixture(scope="module")
def handler():
    """
    Ensure tables are created before running the tests
    """
    test_handler.create_all_metadata()

    return test_handler


@pytest_asyncio.fixture
async def dummy_data(handler):
    """
    Create some dummy objects
    """
    obj_1 = DummyTable(name="Alice", age=30)
    obj_2 = DummyTable(name="Bob", age=25)
    obj_3 = DummyTable(name="Carol", age=35)
    obj_4 = DummyTable(name="Pedro", age=18)

    # Insert data into the database
    await handler.insert_data(obj_1)
    await handler.insert_data(obj_2)
    await handler.insert_data(obj_3)
    await handler.insert_data(obj_4)

    return [obj_1, obj_2, obj_3, obj_4]


def test_create_session(handler):
    """
    Test to test create session method.
    """
    handler._create_session()
    session = handler._session
    is_active = session.is_active

    assert isinstance(session, Session) is True
    assert is_active is True


def test_close_session(handler):
    """
    Test to test close_session method.
    """
    handler._create_session()
    handler._close_session()
    session = handler._session

    assert session is None


@pytest.mark.asyncio
async def test_select_all_data(handler, dummy_data):
    """
    Test to test select_data method with
    no condition.
    """
    data = await handler.select_data(DummyTable)

    assert data == [
        {"age": 30, "name": "Alice", "id": 1},
        {"age": 25, "name": "Bob", "id": 2},
        {"age": 35, "name": "Carol", "id": 3},
        {"age": 18, "name": "Pedro", "id": 4},
    ]


@pytest.mark.asyncio
async def test_select_all_data_ordered(handler):
    """
    Test to test select_data all data.
    """
    data = await handler.select_data(
        DummyTable, order_by="id", order_desc=True
    )

    assert data == [
        {"age": 18, "name": "Pedro", "id": 4},
        {"age": 35, "name": "Carol", "id": 3},
        {"age": 25, "name": "Bob", "id": 2},
        {"age": 30, "name": "Alice", "id": 1},
    ]


@pytest.mark.asyncio
async def test_select_equal_data(handler):
    """
    Test to test select_data with id = 1.
    """
    data = await handler.select_data(DummyTable, id=1)

    assert data == [
        {"age": 30, "name": "Alice", "id": 1},
    ]


@pytest.mark.asyncio
async def test_select_greater_than_data(handler):
    """
    Test to test select_data with with age > 25.
    """
    data = await handler.select_data(DummyTable, age__gt=25)

    assert data == [
        {"age": 30, "name": "Alice", "id": 1},
        {"age": 35, "name": "Carol", "id": 3},
    ]


@pytest.mark.asyncio
async def test_select_less_than_data(handler):
    """
    Test to test select_data with age < 25.
    """
    data = await handler.select_data(DummyTable, age__lt=25)

    assert data == [
        {"age": 18, "name": "Pedro", "id": 4},
    ]


@pytest.mark.asyncio
async def test_select_greater_equal_data(handler):
    """
    Test to test select_data with age >= 25.
    """
    data = await handler.select_data(DummyTable, age__ge=25)

    assert data == [
        {"age": 30, "name": "Alice", "id": 1},
        {"age": 25, "name": "Bob", "id": 2},
        {"age": 35, "name": "Carol", "id": 3},
    ]


@pytest.mark.asyncio
async def test_select_less_equal_data(handler):
    """
    Test to test select_data with age <= 25.
    """
    data = await handler.select_data(DummyTable, age__le=25)

    assert data == [
        {"age": 25, "name": "Bob", "id": 2},
        {"age": 18, "name": "Pedro", "id": 4},
    ]


@pytest.mark.asyncio
async def test_select_like_data(handler):
    """
    Test to test select_data with name wich contains "ro".
    """
    data = await handler.select_data(DummyTable, name__like="ro")

    assert data == [
        {"age": 35, "name": "Carol", "id": 3},
        {"age": 18, "name": "Pedro", "id": 4},
    ]


def test_create_filter(handler):
    """
    Test to test create_filter method.
    """
    filter = {DummyTable.age: 25, DummyTable.name: "Pedro"}
    filter_generated = handler._create_filter(filter)

    for filter_item in filter_generated:
        assert isinstance(filter_item, BinaryExpression)


@pytest.mark.asyncio
async def test_update_data_table(handler):
    """
    Test to test update_data_table method.
    """
    filter_update = {DummyTable.id: 1}
    new_data = {DummyTable.age: 23}

    rows = await handler.update_data_table(DummyTable, filter_update, new_data)
    data = await handler.select_data(DummyTable, id=1)

    assert rows == 1
    assert data == [
        {"age": 23, "name": "Alice", "id": 1},
    ]


@pytest.mark.asyncio
async def test_delete_data_table(handler):
    """
    Test to test delete_data_table method.
    """
    filter_delete = {DummyTable.id: 1}

    rows = await handler.delete_data_table(DummyTable, filter_delete)
    data = await handler.select_data(DummyTable, id=1)

    assert rows == 1
    assert data == []
