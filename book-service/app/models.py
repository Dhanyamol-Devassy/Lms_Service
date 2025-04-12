from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(100), unique=True, index=True, nullable=False)
    available = Column(Boolean, default=True) # Indicates if the book is currently borrowable

    