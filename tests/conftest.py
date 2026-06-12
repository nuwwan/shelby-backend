import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from main import app


@pytest.fixture()
def client():
    """A TestClient backed by a fresh in-memory database for each test.

    We use an in-memory SQLite DB with a StaticPool so the whole test shares a
    single connection (otherwise each connection would get its own empty DB),
    and override the app's get_db dependency so no test ever touches items.db.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Note: instantiate TestClient without a context manager so the app's
    # lifespan (which calls create_all on the real engine) does not run.
    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
