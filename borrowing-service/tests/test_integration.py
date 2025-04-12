import pytest
import requests_mock
from app import create_app, db as _db
from app.models import Borrowing
from flask.testing import FlaskClient

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()

def test_borrow_book_success(client):
    with requests_mock.Mocker() as m:
        m.get("http://user-service:5001/users/1", json={"id": 1, "name": "Test User"})
        m.get("http://book-service:5002/books/1", json={"id": 1, "title": "Test Book", "available": True})
        m.put("http://book-service:5002/books/borrow/1?available=false", status_code=200)
        m.post("http://user-service:5001/users/1/add-borrowed", status_code=200)

        response = client.post("/borrow", json={"user_id": 1, "book_id": 1})

        assert response.status_code == 200
        assert response.get_json()["message"] == "Book borrowed successfully"

def test_return_book_success(client):
    # Insert a borrow record directly into the DB
    borrowing = Borrowing(user_id=1, book_id=1)
    _db.session.add(borrowing)
    _db.session.commit()

    with requests_mock.Mocker() as m:
        m.put("http://book-service:5002/books/borrow/1?available=true", status_code=200)
        m.post("http://user-service:5001/users/1/remove-borrowed", status_code=200)

        response = client.put(f"/return/{borrowing.id}")

        assert response.status_code == 200
        assert response.get_json()["message"] == "Book returned successfully"
