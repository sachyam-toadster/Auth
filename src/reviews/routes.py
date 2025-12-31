from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.dependencies import RoleChecker, get_current_user
from src.db.main import get_db
from src.db.models import User

from .schemas import ReviewCreateModel
from .service import ReviewService

review_service = ReviewService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@review_router.get("/")
def get_all_reviews(session: Session = Depends(get_db)):
    reviews = review_service.get_all_reviews(session)

    return reviews


@review_router.get("/{review_uid}", dependencies=[user_role_checker])
def get_review(review_uid: str, session: Session = Depends(get_db)):
    review = review_service.get_review(review_uid, session)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review


@review_router.post("/book/{book_uid}", dependencies=[user_role_checker])
def add_review_to_books(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    new_review = review_service.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session,
    )

    return new_review


@review_router.delete("/{review_uid}", dependencies=[user_role_checker], status_code=status.HTTP_204_NO_CONTENT,)
def delete_review(
    review_uid: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    review_service.delete_review_to_from_book(
        review_uid=review_uid, user_email=current_user.email, session=session
    )

    return None