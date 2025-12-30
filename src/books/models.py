from typing import Optional
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

class Book(SQLModel , table=True):
    __tablename__ = "books"

    uid:uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            nullable=False
        )
    )

    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language:str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow))

    def __repr__(self) -> str:
        return f"<Book {self.title}>"