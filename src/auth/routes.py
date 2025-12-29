from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserResponseModel, UserLoginModel
from .service import UserService
from src.db.main import get_db
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from .utils import verify_password, create_access_token
from fastapi.responses import JSONResponse
from datetime import timedelta
from src.config import settings


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


@auth_router.post("/login")
def login_users(
    login_data: UserLoginModel, session: Session = Depends(get_db)
):
    email = login_data.email
    password = login_data.password

    user = user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=settings.REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )