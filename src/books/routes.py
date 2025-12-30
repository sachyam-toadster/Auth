from fastapi import FastAPI, HTTPException, status, APIRouter, Depends
from .schemas import BookCreateModel, BookSchema, BookUpdateModel
from .book_data import books
from typing import List
from datetime import datetime
from sqlmodel import Session
from src.db.main import get_db
import uuid
from src.db.models import Book
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from .service import BookService


book_router = APIRouter()
acccess_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))
book_service = BookService()


@book_router.get("/")
async def root():
    return {"message": "Welcome to the Bookly API!"}



@book_router.get("/test-books", response_model=List[Book], dependencies=[role_checker])
def get_test_books(db: Session = Depends(get_db), token_details=Depends(acccess_token_bearer),):
    print(token_details)
    books = db.query(Book).all()
    return books

@book_router.get("/test-book/{book_id}", response_model=Book, dependencies=[role_checker])
def get_test_book(book_id: uuid.UUID, db: Session = Depends(get_db), token_details=Depends(acccess_token_bearer)):
    book = db.query(Book).filter(Book.uid == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book 

@book_router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
def delete_test_book(book_id: uuid.UUID, db: Session = Depends(get_db), token_details=Depends(acccess_token_bearer)):
    book = db.query(Book).filter(Book.uid == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return


@book_router.post("/books", response_model=Book, dependencies=[role_checker])
def create_book(book: Book, db: Session = Depends(get_db), token_details=Depends(acccess_token_bearer)):
    new_book = Book(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        published_date=book.published_date,
        page_count=book.page_count,
        language=book.language
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@book_router.patch("/book/{book_id}", response_model=Book, dependencies=[role_checker])
def update_test_book(book_id: uuid.UUID, book_update: Book, db: Session = Depends(get_db), token_details=Depends(acccess_token_bearer)):
    book = db.query(Book).filter(Book.uid == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book.title = book_update.title
    book.author = book_update.author
    book.publisher = book_update.publisher
    book.published_date = book_update.published_date
    book.page_count = book_update.page_count
    book.language = book_update.language
    book.updated_at = datetime.now()

    db.commit()
    db.refresh(book)
    return book

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker],)
async def create_a_book(book_data: BookCreateModel, session: Session = Depends(get_db), token_details: dict = Depends(acccess_token_bearer)) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = book_service.create_book(book_data, user_id, session)
    return new_book