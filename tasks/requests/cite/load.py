
import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page
from core.utils.wikidb import Database

from tasks.webcite.module import create_database_table, get_pages, save_pages_to_db

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
                    page = to_page.title(with_ns=False)
            else:
                to_page = pywikibot.Page(site, request.to_name)
                if to_page.exists():
                    database.query = """select page.page_title as prt_title from categorylinks
inner join page on page.page_id = categorylinks.cl_from
where cl_to in (select page.page_title from page where page_id = {})
and cl_type = "page"
and page.page_namespace = 0""".format(to_page.pageid)
                    database.get_content_from_database()
                    gen = database.result

                    pages = []
                    for row in gen:
                        page_title = str(row['prt_title'], 'utf-8')
                        pages.append(page_title)

                    try:
                        thread_number = 1
                        conn, cursor = create_database_table()
                        save_pages_to_db(pages, conn, cursor, thread_number=thread_number)
                        conn.close()
                    except Exception as e:
                        print(f"An error occurred: {e}")

            request.status = Status.COMPLETED
            session.commit()
        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
