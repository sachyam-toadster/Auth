from fastapi import FastAPI, HTTPException, status, APIRouter, Depends
from .schemas import BookSchema, BookUpdateModel
from .book_data import books
from typing import List
from datetime import datetime
from sqlmodel import Session
from src.db.main import get_db
import uuid
from src.books.models import Book


book_router = APIRouter()

@book_router.get("/")
async def root():
    return {"message": "Welcome to the Bookly API!"}


@book_router.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@book_router.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@book_router.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/book/{book_id}")
async def update_book(book_id: int,book_update_data:BookUpdateModel) -> dict:

    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.post("/test-book")
def create_test_book(db: Session = Depends(get_db)):
    book = Book(
        uid=uuid.uuid4(),
        title="Atomic Habits",
        author="James Clear",
        publisher="Penguin",
        published_date="2018",
        page_count=320,
        language="English",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

@book_router.get("/test-books", response_model=List[Book])
def get_test_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@book_router.get("/test-book/{book_id}", response_model=Book)
def get_test_book(book_id: uuid.UUID, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.uid == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book 