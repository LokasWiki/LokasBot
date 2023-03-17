from sqlalchemy.orm import Session

from database.models import Page, TaskName, Status


def is_page_present(session: Session, page_title: str, task_type: TaskName) -> bool:
    """
    Checks if a page with the given title is already present in the database
    """
    return session.query(Page).where(Page.title == page_title).where(Page.task_name == task_type).count() > 0


def get_articles(session, thread_number, pages_type):
    if thread_number == 1:
        thread_number = 0

    query1 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=1). \
        order_by(Page.create_date). \
        limit(200).offset(thread_number)

    query2 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=2). \
        order_by(Page.create_date). \
        limit(200).offset(thread_number)

    query3 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=3). \
        order_by(Page.create_date). \
        limit(200).offset(thread_number)

    yield from query1.all()
    yield from query2.all()
    yield from query3.all()
