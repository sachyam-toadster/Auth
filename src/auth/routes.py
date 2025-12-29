from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserResponseModel
from .service import UserService
from src.db.main import get_db
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
user_service = UserService()

@auth_router.post(
    "/signup",
    response_model=UserResponseModel,
    status_code=status.HTTP_201_CREATED,
)
def create_user_account(
    user_data: UserCreateModel,
    session: Session = Depends(get_db),
):
    email = user_data.email

    user_exists = user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = user_service.create_user(user_data, session)
    return new_user
