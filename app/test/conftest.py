from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.db.engine import engine
from app.domain.product import Base
from app.main import app


@pytest.fixture(scope='session')
def engine_test():
    conn = engine.connect()
    conn.execute(text("CREATE DATABASE IF NOT EXISTS test_payhere"))
    conn.execute(text("USE test_payhere"))
    test_engine = create_engine(settings.MYSQL_TEST_DATABASE_URI)
    yield test_engine
    conn.execute(text("DROP DATABASE test_payhere"))
    conn.close()


@pytest.fixture(scope="function")
def session(engine_test) -> Generator:
    Base.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session
    Base.metadata.drop_all(engine_test)


@pytest.fixture(scope="function")
def client(session: Session) -> Generator:
    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_current_active_user] = lambda : None
    with TestClient(app) as c:
        yield c
