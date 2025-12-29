from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(
    settings.database_url,

)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        print("DATABASE URL:", settings.database_url)
        yield db
    finally:
        db.close()


def initdb():
    return engine
