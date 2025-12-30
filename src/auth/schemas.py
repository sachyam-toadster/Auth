from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


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