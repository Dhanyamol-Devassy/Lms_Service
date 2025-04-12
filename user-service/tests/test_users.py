import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base, User  # ⬅ Import models here!

# Setup in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3 Create tables AFTER override
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# ----------------------------------------
# Unit Tests
# ----------------------------------------

def test_register_user():
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_update_user():
    response = client.put("/users/1", json={
        "name": "Updated Name",
        "email": "updated@example.com",
        "password": "newpass"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_add_and_remove_borrowed_book():
    # Add book
    response = client.post("/users/1/add-borrowed", json={"book_id": 101})
    assert response.status_code == 200

    # Remove book
    response = client.post("/users/1/remove-borrowed", json={"book_id": 101})
    assert response.status_code == 200

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
