import pytest
from flask import Flask
from app.routes import bp as borrowing_bp
from app.database import db
from app.models import Borrowing
from unittest.mock import patch

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(borrowing_bp)

    with app.app_context():
        db.create_all()
        yield app.test_client()

@patch("app.routes.requests.get")
@patch("app.routes.requests.put")
@patch("app.routes.requests.post")
def test_borrow_book(mock_post, mock_put, mock_get, client):
    mock_get.side_effect = [
        MockResponse({"id": 1, "name": "User"}, 200),
        MockResponse({"id": 2, "title": "Book", "available": True}, 200)
    ]
    mock_put.return_value = MockResponse({}, 200)
    mock_post.return_value = MockResponse({}, 200)

    response = client.post("/borrow", json={"user_id": 1, "book_id": 2})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book borrowed successfully"

@patch("app.routes.requests.put")
@patch("app.routes.requests.post")
def test_return_book(mock_post, mock_put, client):
    # Add a borrowing record to return
    with client.application.app_context():
        borrowing = Borrowing(user_id=1, book_id=2)
        db.session.add(borrowing)
        db.session.commit()

    mock_put.return_value = MockResponse({}, 200)
    mock_post.return_value = MockResponse({}, 200)

    response = client.put(f"/return/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book returned successfully"

class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data
