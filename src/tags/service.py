from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel import Session

from src.books.service import BookService
from src.db.models import Tag

from .schemas import TagAddModel, TagCreateModel

book_service = BookService()


server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)


class TagService:

    def get_tags(self, session: Session):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = session.execute(statement)
        return result.scalars().all() 

    def add_tags_to_book(
        self, book_uid: str, tag_data: TagCreateModel, session: Session
    ):
        """Add tags to a book"""

        book = book_service.get_book_by_uid(book_uid=book_uid, session=session)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        for tag_item in tag_data.tags:
            result = session.execute(
                select(Tag).where(Tag.name == tag_item.name)
            )

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book



    def get_tag_by_uid(self, tag_uid: str, session: Session):
        """Get tag by uid"""

        statement = select(Tag).where(Tag.uid == tag_uid)

        return session.execute(statement).scalars().one_or_none()

    def add_tag(self, tag_data: TagCreateModel, session: Session):
        """Create a tag"""

        statement = select(Tag).where(Tag.name == tag_data.name)

        result = session.execute(statement)

        tag = result.first()

        if tag:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Tag exists"
            )

        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)

        session.commit()

        return new_tag

    def update_tag(
        self, tag_uid: str, tag_update_data: TagCreateModel, session: Session
    ):
        """Update a tag"""

        tag = self.get_tag_by_uid(tag_uid, session)

        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        for k, v in tag_update_data.model_dump().items():
            setattr(tag, k, v)
    
        session.add(tag)
        session.commit()
        session.refresh(tag)
    
        return tag


    def delete_tag(self, tag_uid: str, session: Session):
        """Delete a tag"""

        tag = self.get_tag_by_uid(tag_uid,session)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tag does not exist"
            )

        session.delete(tag)

        session.commit()