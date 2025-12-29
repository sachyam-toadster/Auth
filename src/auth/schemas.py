from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


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