import uuid
from datetime import datetime
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel


class BookService:


    def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )

        result = session.exec(statement)

        return result.all()

    def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.user_uid = user_uid

        session.add(new_book)

        session.commit()
        session.refresh(new_book)
        return new_book

    def get_book_by_uid(
        self, book_uid: str, session: AsyncSession
    ) -> Book | None:
        statement = select(Book).where(Book.uid == book_uid)

        result = session.execute(statement)

        return result.scalar_one_or_none()
