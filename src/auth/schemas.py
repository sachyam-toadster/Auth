from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from src.db.models import Book, Review
import uuid

class UserCreateModel(BaseModel):
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

class UserResponseModel(BaseModel):
    uid: UUID
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str  = Field(min_length=6)

class UserReadModel(BaseModel):
    uid: UUID
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    is_verified: bool
    role: str
    created_at: datetime

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: Optional[datetime] = None


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[Review]  

class EmailModel(BaseModel):
    address: List[str]