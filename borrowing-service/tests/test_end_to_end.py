import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_end_to_end_workflow():
    # Register a user
    user_resp = client.post("/users/", json={
        "name": "E2E Test User",
        "email": "e2e@example.com",
        "password": "pass123"
    })
    assert user_resp.status_code == 200
    user_id = user_resp.json()["id"]

    # Add a book
    book_resp = client.post("/books/", json={
        "title": "End-to-End Book",
        "author": "Author X",
        "isbn": "E2E-123",
        "available": True
    }, headers={"Authorization": "Bearer admin"})  # Adjust token or remove if auth is disabled
    assert book_resp.status_code == 200
    book_id = book_resp.json()["id"]

    # Borrow the book
    borrow_resp = client.post("/borrow", json={
        "user_id": user_id,
        "book_id": book_id
    })
    assert borrow_resp.status_code == 200

    # Return the book (assume borrowing id = 1 for simplicity)
    return_resp = client.put("/return/1")
    assert return_resp.status_code == 200

    # Cleanup
    del_user = client.delete(f"/users/{user_id}")
    assert del_user.status_code == 200

    del_book = client.delete(f"/books/{book_id}", headers={"Authorization": "Bearer admin"})
    assert del_book.status_code == 200
