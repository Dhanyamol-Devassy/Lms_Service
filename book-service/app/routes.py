from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookResponse
import requests

router = APIRouter(prefix="/books", tags=["Books"])

BOOK_SERVICE_URL = "http://borrowing-service:5003"  # Borrowing service URL

@router.post("/", response_model=BookResponse)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in update.dict(exclude_unset=True).items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.put("/borrow/{book_id}")
def update_book_availability(book_id: int, available: bool, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.available = available
    db.commit()
    db.refresh(book)
    return {"message": "Book availability updated"}
