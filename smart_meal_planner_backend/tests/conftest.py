import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def sample_recipe():
    return {
        "name": "Test Spaghetti",
        "description": "A simple pasta dish",
        "ingredients": [
            {"name": "Spaghetti", "quantity": 500, "unit": "g"},
            {"name": "Tomato Sauce", "quantity": 300, "unit": "ml"}
        ],
        "instructions": [
            "Boil water",
            "Cook pasta",
            "Add sauce"
        ],
        "prep_time": 20
    }

@pytest.fixture
def sample_inventory_item():
    return {
        "name": "Test Tomatoes",
        "quantity": 2.5,
        "unit": "kg",
        "expiry_date": "2024-12-31"
    } 