import logging
import random

from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import is_page_present
from database.models import Page, TaskName
from tasks.maintenance.module import get_pages

custom_query = """select page_title AS "pl_2_title" from page
where page.page_is_redirect = 0
and page.page_namespace = 0
and page_id not in (select fp_page_id from flaggedpages where fp_page_id = page_id)
and page_id not in (select cla.cl_from from categorylinks cla inner join linktarget lt ON cla.cl_target_id = lt.lt_id where lt.lt_title like "جميع_المقالات_غير_المراجعة" and lt.lt_namespace = 14);"""


def main(*args: str) -> int:
    # todo: mereg with read.py in webcite task
    try:
        thread_number = 1
        time_before_start = 1
        pages = get_pages(time_before_start, custom_query=custom_query)

        with Session(engine) as maintenance_session:
            for page_title in pages:
                if not is_page_present(maintenance_session, page_title=page_title, task_type=TaskName.MAINTENANCE):
                    print("add : " + page_title)

                    temp_model = Page(
                        title=page_title,
                        thread_number=random.randint(1, 3),
                        task_name=TaskName.MAINTENANCE
                    )
                    maintenance_session.add(temp_model)

            maintenance_session.commit()

    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
