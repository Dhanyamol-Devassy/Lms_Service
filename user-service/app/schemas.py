from pydantic import BaseModel,EmailStr
from typing import List

class BorrowedBook(BaseModel):
    borrow_id: int
    book_id: int
    title: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    borrowed_books: List[BorrowedBook] = []

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserShort(BaseModel):  # ✅ clean user info for token response
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class LoginResponse(BaseModel):
    user: UserShort
    access_token: str
    token_type: str = "bearer"
