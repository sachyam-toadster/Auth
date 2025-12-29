from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db.main import engine
from src.books.routes import book_router
from src.books import models  # 👈 IMPORTANT (forces model import)

app = FastAPI()

# 👇 THIS CREATES TABLES
SQLModel.metadata.create_all(engine)

app.include_router(book_router, prefix="/books", tags=["books"])
