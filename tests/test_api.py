from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from main import app
import pytest

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_program(test_db):
    response = client.post(
        "/api/v1/programs/",
        json={"name": "Test Program"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Program"
    assert "id" in data

def test_create_client(test_db):
    response = client.post(
        "/api/v1/clients/",
        json={
            "name": "John Doe",
            "age": 30,
            "gender": "male",
            "contact": "1234567890"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["age"] == 30

def test_enroll_client(test_db):
    # First create a program
    program_response = client.post(
        "/api/v1/programs/",
        json={"name": "Test Program"}
    )
    program_id = program_response.json()["id"]
    
    # Then create a client
    client_response = client.post(
        "/api/v1/clients/",
        json={
            "name": "John Doe",
            "age": 30,
            "gender": "male",
            "contact": "1234567890"
        }
    )
    client_id = client_response.json()["id"]
    
    # Now enroll the client in the program
    response = client.post(
        "/api/v1/enrollments/",
        json={
            "program_id": program_id,
            "client_id": client_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["programs"]) == 1
    assert data["programs"][0]["id"] == program_id 