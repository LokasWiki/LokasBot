import logging
import sys
from database.engine import engine
from tasks.webcite.module import get_pages
from sqlalchemy.orm import Session
from database.models import Page, TaskName, Status


def is_page_present(session: Session, page_title: str, task_name: TaskName) -> bool:
    """
    Checks if a page with the given title is already present in the database
    """
    return session.query(Page).where(Page.title == page_title).where(Page.task_name == task_name).count() > 0


def main(*args: str) -> int:
    # todo: mereg with read.py in webcite task
    try:
        thread_number = 1
        time_before_start = int(sys.argv[1])
        if time_before_start == 2540:
            thread_number = 3
        elif time_before_start == 500:
            thread_number = 2
        pages = get_pages(time_before_start)
        with Session(engine) as session:
            for page_title in pages:
                if not is_page_present(session, page_title=page_title, task_name=TaskName.WEBCITE):
                    logging.info("add : " + page_title)
                    temp_model = Page(
                        title=page_title,
                        thread_number=thread_number,
                        task_name=TaskName.WEBCITE,
                    )
                    session.add(temp_model)
            session.commit()
        logging.info("Added pages to the database successfully.")

    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

