from typing import Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash

class UserService:

    def get_user_by_email(self, email: str, session: Session):
        statement = select(User).where(User.email == email)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def user_exists(self, email: str, session: Session) -> bool:
        return self.get_user_by_email(email, session) is not None

    def create_user(self, user_data: UserCreateModel, session: Session):
        data = user_data.model_dump()

        new_user = User(
            email=data["email"],
            username=data["username"],
            password_hash=generate_password_hash(data["password"]),
            is_verified=False
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    
    def update_user(self, user,update_data: Dict[str, Any], session: Session):
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user
