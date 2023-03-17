from database.helpers import is_page_present
from module import get_pages
from tasks.webcite.module import get_pages
import logging
import random
from datetime import datetime

from database.engine import maintenance_engine, statistics_engine
from sqlalchemy.orm import Session
from database.models import Page, Statistic

LAST_QUERY_KEY = "maintenance_last_query_time"  # Unique key for the last query time statistic

def main(*args: str) -> int:
    try:
        # todo: mereg with read.py in maintenance task
        # Update the last query time in the statistics table
        now = datetime.now()

        # Get the last query time from the statistics table, if it exists
        with Session(statistics_engine) as session:
            last_query = session.query(Statistic).filter(Statistic.key == LAST_QUERY_KEY).first()
            last_query_time = datetime.fromisoformat(last_query.value) if last_query else now
            logging.info(f"Last query time: {last_query_time}")

            # Calculate the time difference in minutes
            time_diff = (now - last_query_time).seconds // 60
            logging.info(f"time_diff: {time_diff}")
            pages = get_pages(time_diff + 3)

            with Session(maintenance_engine) as maintenance_session:
                for page_title in pages:
                    if not is_page_present(maintenance_session, page_title=page_title):
                        logging.info("add : " + page_title)

                        temp_model = Page(
                            title=page_title,
                            thread=random.randint(1, 3),
                        )
                        maintenance_session.add(temp_model)

                maintenance_session.commit()

            # Update the last query time in the statistics table
            if last_query:
                last_query.value = now.isoformat()
            else:
                last_query = Statistic(key=LAST_QUERY_KEY, value=now.isoformat())
                session.add(last_query)
            session.commit()

        logging.info("Added pages to the database successfully.")
    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
