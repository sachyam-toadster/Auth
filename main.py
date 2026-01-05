from fastapi import FastAPI, Header, status
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager
from src.db.main import initdb
from src.db.init import create_tables
from src.core.error_handlers import register_exception_handlers
from src.middleware import register_middleware

version = 'v1'

#the lifespan event
# @asynccontextmanager
# async def lifespan(app: FastAPI):    
#     create_tables()
#     yield
#     print("server is stopping")


app = FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version,
    # lifespan=lifespan,
    )

register_exception_handlers(app)
register_middleware(app)


app.include_router(
    book_router,
    prefix="/books",
    tags=['books']
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=['authentication']
)

app.include_router(
    review_router,
    prefix="/reviews",
    tags=['reviews']
)

app.include_router(
    tags_router,
    prefix="/tags",
    tags=['tags']
)

@app.get("/")
def root():
    return {
        "message": "Bookly API is running",
    }

