from sqlmodel import SQLModel
from src.db.main import engine
from src.books.models import Book

def create_tables():
    SQLModel.metadata.create_all(engine)
