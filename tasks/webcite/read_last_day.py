import logging
import sys

from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import is_page_present
from database.models import Page, TaskName
from tasks.webcite.module import get_pages


def main(*args: str) -> int:
    try:

        with Session(engine) as session:
            # Calculate the time difference in minutes
            time_diff = int(sys.argv[1])
            print(f"time_diff: {time_diff}")

            for page_title in get_pages(time_diff + 3):
                if not is_page_present(session, page_title=page_title, task_type=TaskName.WEBCITE):
                    print("add : " + page_title)
                    temp_model = Page(
                        title=page_title,
                        thread_number=3,
                        task_name=TaskName.WEBCITE
                    )
                    session.add(temp_model)

            session.commit()

        print("Added pages to the database successfully.")
    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
