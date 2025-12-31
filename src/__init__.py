from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db.main import engine
from src.books.routes import book_router
from src.db import models  # 👈 IMPORTANT (forces model import)


# 👇 THIS CREATES TABLES
SQLModel.metadata.create_all(engine)

