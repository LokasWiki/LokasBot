from database.helpers import is_page_present
from module import get_pages
from tasks.webcite.module import get_pages
import logging
import random
from datetime import datetime

from database.engine import engine
from sqlalchemy.orm import Session
from database.models import Page, Statistic, TaskName

LAST_QUERY_KEY = "maintenance_last_query_time"  # Unique key for the last query time statistic

def main(*args: str) -> int:
    try:
        # todo: mereg with read.py in maintenance task
        # Update the last query time in the statistics table
        now = datetime.now()

        # Get the last query time from the statistics table, if it exists
        with Session(engine) as session:
            last_query = session.query(Statistic).filter(Statistic.key == LAST_QUERY_KEY).first()
            last_query_time = datetime.fromisoformat(last_query.value) if last_query else now
            print(f"Last query time: {last_query_time}")

            # Calculate the time difference in minutes
            time_diff = (now - last_query_time).seconds // 60
            print(f"time_diff: {time_diff}")
            for page_title in get_pages(time_diff + 3):
                if not is_page_present(session, page_title=page_title, task_type=TaskName.MAINTENANCE):
                    print("add : " + page_title)

                    temp_model = Page(
                        title=page_title,
                        thread_number=random.randint(1, 3),
                        task_name=TaskName.MAINTENANCE
                    )
                    session.add(temp_model)

            session.commit()

            # Update the last query time in the statistics table
            if last_query:
                last_query.value = now.isoformat()
            else:
                last_query = Statistic(key=LAST_QUERY_KEY, value=now.isoformat())
                session.add(last_query)
            session.commit()

        print("Added pages to the database successfully.")
    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
