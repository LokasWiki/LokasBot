import logging
from random import random

from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import is_page_present
from database.models import Page, TaskName
from tasks.maintenance.module import get_pages


def main(*args: str) -> int:
    # todo: mereg with read.py in webcite task
    try:
        thread_number = 1
        time_before_start = 1
        custom_query = """select distinct page.page_title as "pl_2_title"  from page_restrictions 
inner join page on page_restrictions.pr_page = page.page_id
where page.page_namespace in (0) and  pr_page  not in (
select page.page_id from templatelinks
inner join page on templatelinks.tl_from = page.page_id
inner join linktarget on templatelinks.tl_target_id = linktarget.lt_id
where lt_namespace = 10 and lt_title in (
 			"محمية",
            "protected",
            "حماية_خاصة",
            "حماية_نزاع",
            "pp-semi-template",
            "pp-semi-vandalism",
            "pp-dispute",
            "قفل",
            "pp-semi-protected",
            "pp-move-indef",
            "pp-protected",
            "حماية_كلية",
            "حماية_حرب",
            "حماية_جزئية",
            "pp-semi",
            "حماية كاملة",
            "حماية",
            "صفحة_محمية",
            "semi-protection",
            "pp-semi-indef",
            "شبه_محمي",
            "حماية_تخريب"
) and tl_from_namespace in(0))"""
        pages = get_pages(time_before_start, custom_query=custom_query)

        with Session(engine) as maintenance_session:
            for page_title in pages:
                if not is_page_present(maintenance_session, page_title=page_title, task_type=TaskName.MAINTENANCE):
                    print("add : " + page_title)

                    temp_model = Page(
                        title=page_title,
                        thread=random.randint(1, 3),
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
