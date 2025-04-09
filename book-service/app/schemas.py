from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    available: bool = True

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    available: bool | None = None

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True  # updated from orm_mode
