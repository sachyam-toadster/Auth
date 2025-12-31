from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import Session


from src.auth.dependencies import RoleChecker
from src.db.main import get_db
from src.db.models import Book
from .schemas import TagAddModel, TagCreateModel, TagModel
from .service import TagService

tags_router = APIRouter()
tag_service = TagService()
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@tags_router.get("/", response_model=List[TagModel], dependencies=[user_role_checker])
def get_all_tags(session: Session = Depends(get_db)):
    tags = tag_service.get_tags(session)

    return tags


@tags_router.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[user_role_checker],
)
async def add_tag(
    tag_data: TagCreateModel, session: Session = Depends(get_db)
) -> TagModel:

    tag_added = tag_service.add_tag(tag_data=tag_data, session=session)

    return tag_added


@tags_router.post(
    "/book/{book_uid}/tags", response_model=Book, dependencies=[user_role_checker]
)
def add_tags_to_book(
    book_uid: str, tag_data: TagAddModel, session: Session = Depends(get_db)
) -> Book:

    book_with_tag = tag_service.add_tags_to_book(
        book_uid=book_uid, tag_data=tag_data, session=session
    )

    return book_with_tag


@tags_router.put(
    "/{tag_uid}", response_model=TagModel, dependencies=[user_role_checker]
)
async def update_tag(
    tag_uid: str,
    tag_update_data: TagCreateModel,
    session: Session = Depends(get_db),
) -> TagModel:
    updated_tag = tag_service.update_tag(tag_uid, tag_update_data, session)

    return updated_tag


@tags_router.delete(
    "/{tag_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[user_role_checker],
)
def delete_tag(
    tag_uid: str, session: Session = Depends(get_db)
) -> None:
    updated_tag = tag_service.delete_tag(tag_uid, session)

    return updated_tag