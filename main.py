from fastapi import FastAPI, Header, status
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import initdb
from src.db.init import create_tables

version = 'v1'

#the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):    
    create_tables()
    yield
    print("server is stopping")


app = FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version,
    )

app.include_router(
    book_router,
    prefix="/books",
    tags=['books']
)

@app.get("/")
def root():
    return {
        "message": "Bookly API is running",
    }

