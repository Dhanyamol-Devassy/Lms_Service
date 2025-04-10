from flask import Blueprint, request, jsonify
from app.models import Borrowing
from app.database import db
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.json
    borrowing = Borrowing(user_id=data["user_id"], book_id=data["book_id"])
    db.session.add(borrowing)
    db.session.commit()
    return jsonify({"message": "Book borrowed"}), 201

@bp.route("/return/<int:borrow_id>", methods=["PUT"])
def return_book(borrow_id):
    borrowing = Borrowing.query.get(borrow_id)
    if borrowing is None:
        return jsonify({"message": "Borrowing not found"}), 404
    borrowing.returned_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Book returned"})

@bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Borrowing Service is Running!"})
