import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.service import UserService
from src.books.service import BookService
from src.db.models import Review

from .schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()


class ReviewService:
    def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            book = book_service.get_book_by_uid(book_uid=book_uid, session=session)
            user = user_service.get_user_by_email(
                email=user_email, session=session
            )
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            if not book:
                raise HTTPException(
                    detail="Book not found", status_code=status.HTTP_404_NOT_FOUND
                )

            if not user:
                raise HTTPException(
                    detail="Book not found", status_code=status.HTTP_404_NOT_FOUND
                )

            new_review.user = user

            new_review.book = book

            session.add(new_review)

            session.commit()

            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                detail="Oops... somethig went wrong!",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = session.execute(statement)

        return result.scalar_one_or_none()

    def get_all_reviews(self, session: Session):
        statement = select(Review)
        result = session.execute(statement)
        return result.scalars().all()

    def delete_review_to_from_book(self, review_uid: str, user_email: str, session: Session):
        user = user_service.get_user_by_email(user_email, session)

        result = session.execute(select(Review).where(Review.uid == review_uid))
        review = result.scalars().first()

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
            )
        
        if review.user_uid != user.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this review",
            )

        session.delete(review)
        session.commit()