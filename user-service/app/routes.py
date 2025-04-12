from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from app.auth import pwd_context, create_access_token
from app.schemas import LoginResponse, UserShort
from dotenv import load_dotenv

load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------------------------
# POST /users/
# ----------------------------------------------
@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        borrowed_books=[]
    )


# ----------------------------------------------
# GET /users/
# ----------------------------------------------
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            borrowed_books=u.borrowed_books.split(',') if u.borrowed_books else []
        ) for u in users
    ]


# ----------------------------------------------
# GET /users/{user_id}
# ----------------------------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        borrowed_books=user.borrowed_books.split(',') if user.borrowed_books else []
    )


# ----------------------------------------------
# PUT /users/{user_id}
# ----------------------------------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.name = user.name or existing_user.name
    existing_user.email = user.email or existing_user.email
    existing_user.password = hash_password(user.password) if user.password else existing_user.password

    db.commit()
    db.refresh(existing_user)

    return UserResponse(
        id=existing_user.id,
        name=existing_user.name,
        email=existing_user.email,
        borrowed_books=existing_user.borrowed_books.split(',') if existing_user.borrowed_books else []
    )


# ----------------------------------------------
# DELETE /users/{user_id}
# ----------------------------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}


# ----------------------------------------------
# POST /users/{user_id}/add-borrowed
# ----------------------------------------------
@router.post("/{user_id}/add-borrowed")
def add_borrowed_book(user_id: int, payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book_id = str(payload.get("book_id"))
    if not user.borrowed_books:
        user.borrowed_books = book_id
    elif book_id not in user.borrowed_books.split(','):
        user.borrowed_books += f",{book_id}"

    db.commit()
    return {"message": "Book added to borrowed list"}


# ----------------------------------------------
# POST /users/{user_id}/remove-borrowed
# ----------------------------------------------
@router.post("/{user_id}/remove-borrowed")
def remove_borrowed_book(user_id: int, payload: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book_id = str(payload.get("book_id"))
    books = user.borrowed_books.split(',') if user.borrowed_books else []
    if book_id in books:
        books.remove(book_id)
        user.borrowed_books = ','.join(books)
        db.commit()

    return {"message": "Book removed from borrowed list"}

@router.post("/login", tags=["Authentication"])
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}
