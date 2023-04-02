import traceback

import pywikibot
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils.wikidb import Database
from database.engine import engine as engine_webcite
from database.helpers import is_page_present
from database.models import Page as PageWebCite, TaskName
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 4

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            database = Database()
            if request.to_namespace == 0:
                to_page = pywikibot.Page(site, request.from_name)
                if to_page.exists():
                    try:
                        with Session(engine_webcite) as session_webcite:
                            if not is_page_present(session_webcite, page_title=to_page.title(with_ns=False),
                                                   task_type=TaskName.WEBCITE):
                                print("add : " + to_page.title(with_ns=False))
                                temp_model = PageWebCite(
                                    title=to_page.title(with_ns=False),
                                    thread_number=1,
                                    task_name=TaskName.WEBCITE
                                )
                            session_webcite.add(temp_model)
                            session_webcite.commit()

                    except Exception as e:
                        print(f"An error occurred: {e}")
            else:
                from_page = pywikibot.Page(site, request.from_name)
                if from_page.exists():
                    database.query = """select page.page_title as prt_title from categorylinks
inner join page on page.page_id = categorylinks.cl_from
where cl_to in (select page.page_title from page where page_id = {})
and cl_type = "page"
and page.page_namespace = 0""".format(from_page.pageid)
                    database.get_content_from_database()
                    gen = database.result

                    pages = []
                    for row in gen:
                        page_title = str(row['prt_title'], 'utf-8')
                        pages.append(page_title)

                    for page in pages:
                        try:
                            with Session(engine_webcite) as session_webcite:
                                if not is_page_present(session_webcite, page_title=page,
                                                       task_type=TaskName.WEBCITE):
                                    print("add : " + page)
                                    temp_model = PageWebCite(
                                        title=page,
                                        thread_number=1,
                                        task_name=TaskName.WEBCITE
                                    )
                                session_webcite.add(temp_model)
                                session_webcite.commit()
                        except Exception as e:
                            print(f"An error occurred: {e}")

            request.status = Status.COMPLETED
            session.commit()
        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
            just_the_string = traceback.format_exc()
            print(just_the_string)
except Exception as e:
    print(f"An error occurred: {e}")
