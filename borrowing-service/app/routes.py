import requests
from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Borrowing, Book, User
from datetime import datetime

router = APIRouter()

# Correct URLs for the user-service and book-service
USER_SERVICE_URL = "http://user-service:5001/users/{user_id}"  # Replace with actual user-service URL
BOOK_SERVICE_URL = "http://book-service:5002/books/{book_id}"  # Replace with actual book-service URL

# Borrow Book
@router.post("/borrow")
def borrow_book(user_id: int, book_id: int):
    # Check if the user exists by calling the user service
    user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the book exists and is available by calling the book service
    book_response = requests.get(f"{BOOK_SERVICE_URL}/{book_id}")
    if book_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = book_response.json()
    if not book['available']:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    # Create the borrowing record
    borrowing = Borrowing(user_id=user_id, book_id=book_id)
    db.session.add(borrowing)
    db.session.commit()

    # Update book availability to False
    book['available'] = False
    requests.put(f"{BOOK_SERVICE_URL}/{book_id}", json=book)

    return {"message": "Book borrowed successfully"}

# Return Book
@router.put("/return/{borrow_id}")
def return_book(borrow_id: int):
    borrowing = Borrowing.query.get(borrow_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    borrowing.returned_at = datetime.utcnow()
    db.session.commit()

    # Update book availability to True
    book = requests.get(f"{BOOK_SERVICE_URL}/{borrowing.book_id}").json()
    book['available'] = True
    requests.put(f"{BOOK_SERVICE_URL}/{borrowing.book_id}", json=book)

    return {"message": "Book returned successfully"}
