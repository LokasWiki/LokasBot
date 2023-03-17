from sqlalchemy.orm import Session

from database.models import Page


def is_page_present(session: Session, page_title: str) -> bool:
    """
    Checks if a page with the given title is already present in the database
    """
    return session.query(Page).where(Page.title == page_title).count() > 0
