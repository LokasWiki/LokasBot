from sqlalchemy.orm import Session

from database.models import Page


def is_page_present(session: Session, page_title: str) -> bool:
    """
    Checks if a page with the given title is already present in the database
    """
    return session.query(Page).where(Page.title == page_title).count() > 0


def get_articles(session, thread_number):
    if thread_number == 1:
        thread_number = 0

    query1 = session.query(Page.id, Page.title, Page.thread). \
        filter_by(status=0, thread=1). \
        order_by(Page.date). \
        limit(200).offset(thread_number)

    query2 = session.query(Page.id, Page.title, Page.thread). \
        filter_by(status=0, thread=2). \
        order_by(Page.date). \
        limit(200).offset(thread_number)

    query3 = session.query(Page.id, Page.title, Page.thread). \
        filter_by(status=0, thread=3). \
        order_by(Page.date). \
        limit(200).offset(thread_number)

    yield from query1.all()
    yield from query2.all()
    yield from query3.all()
