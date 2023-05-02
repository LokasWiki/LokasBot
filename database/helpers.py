from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Page, TaskName, Status


def is_page_present(session: Session, page_title: str, task_type: TaskName) -> bool:
    """
    Checks if a page with the given title is already present in the database
    """
    return session.query(Page).where(Page.title == page_title).where(Page.task_name == task_type).count() > 0


def update_page_statuses_to_pending(session: Session, task_name: TaskName):
    session.query(Page). \
        filter(Page.status != Status.PENDING). \
        filter(Page.task_name == task_name). \
        update({Page.status: Status.PENDING})

    session.commit()


def get_articles(session, thread_number, pages_type):
    if thread_number == 1:
        thread_number = 0

    now = func.now()

    query1 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=1). \
        filter(Page.update_date < now). \
        order_by(Page.update_date). \
        limit(200).offset(thread_number)
    query2 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=2). \
        filter(Page.update_date < now). \
        order_by(Page.update_date). \
        limit(200).offset(thread_number)

    query3 = session.query(Page.id, Page.title, Page.thread_number). \
        filter_by(status=Status.PENDING, task_name=pages_type, thread_number=3). \
        filter(Page.update_date < now). \
        order_by(Page.update_date). \
        limit(200).offset(thread_number)

    yield from query1.all()
    yield from query2.all()
    yield from query3.all()


def get_page_count(session, pages_type):
    now = func.now()

    query1 = session.query(func.count(Page.id)). \
        filter_by(status=Status.PENDING, task_name=pages_type). \
        filter(Page.update_date < now)

    count = query1.scalar()

    return count
