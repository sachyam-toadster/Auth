from pydantic import BaseModel
from src.reviews.schemas import ReviewModel
import uuid

class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

    class Config:
        from_attributes = True


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookwithReviewsModel(BookSchema):
    reviews: list[ReviewModel] = []

