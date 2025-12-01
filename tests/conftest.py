from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import User, table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')  # Creating sqlite in memory

    table_registry.metadata.create_all(engine)
    # Creating all tables in sqlite db

    with Session(engine) as session:
        yield session

    # Teardown
    table_registry.metadata.drop_all(engine)
    # Delete all tables created ensuring a clean db


@contextmanager
def _mock_db_time(model=User, time=datetime(2025, 12, 1)):
    """
        If an event occur in my database, this function could capture
        the datetime and return this time to the test
    """
    # Change every time the event occurs
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
    event.listen(model, 'before_insert', fake_time_hook)  # Listening

    yield time

    event.remove(model, 'before_insert', fake_time_hook)  # Teardown function


@pytest.fixture
def mock_db_time():
    return _mock_db_time
