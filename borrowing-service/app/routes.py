import requests
from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Borrowing
from datetime import datetime
import os

bp = Blueprint("borrowing", __name__)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5001/users")
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:5002/books")

@bp.route("/borrow", methods=["POST"])
def borrow_book():
    user_id = request.json.get("user_id")
    book_id = request.json.get("book_id")

    # Validate user
    try:
        user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
        if user_response.status_code == 404:
            return jsonify({"error": f"User {user_id} not found"}), 404
        elif user_response.status_code != 200:
            return jsonify({"error": "User service error"}), 502
    except requests.RequestException:
        return jsonify({"error": "Failed to connect to user service"}), 503

    # Validate book
    try:
        book_response = requests.get(f"{BOOK_SERVICE_URL}/{book_id}")
        if book_response.status_code == 404:
            return jsonify({"error": f"Book {book_id} not found"}), 404
        elif book_response.status_code != 200:
            return jsonify({"error": "Book service error"}), 502
        book = book_response.json()
    except requests.RequestException:
        return jsonify({"error": "Failed to connect to book service"}), 503

    if not book.get("available", False):
        return jsonify({"error": "Book is not available"}), 400

    # Create borrowing record
    borrowing = Borrowing(user_id=user_id, book_id=book_id)
    db.session.add(borrowing)
    db.session.commit()

    try:
        requests.put(f"{BOOK_SERVICE_URL}/borrow/{book_id}?available=false")
    except requests.RequestException:
        return jsonify({"error": "Failed to update book availability"}), 503

    try:
        requests.post(f"{USER_SERVICE_URL}/{user_id}/add-borrowed", json={"book_id": book_id})
    except requests.RequestException:
        return jsonify({"error": "Failed to update user borrowed list"}), 503

    return jsonify({"message": "Book borrowed successfully"}), 200


@bp.route("/return/<int:borrow_id>", methods=["PUT"])
def return_book(borrow_id):
    borrowing = Borrowing.query.get(borrow_id)
    if not borrowing:
        return jsonify({"error": "Borrowing record not found"}), 404

    borrowing.returned_at = datetime.utcnow()
    db.session.commit()

    try:
        requests.put(f"{BOOK_SERVICE_URL}/borrow/{borrowing.book_id}?available=true")
    except requests.RequestException:
        return jsonify({"error": "Failed to update book availability"}), 503

    try:
        requests.post(f"{USER_SERVICE_URL}/{borrowing.user_id}/remove-borrowed", json={"book_id": borrowing.book_id})
    except requests.RequestException:
        return jsonify({"error": "Failed to update user borrowed list"}), 503

    return jsonify({"message": "Book returned successfully"}), 200
