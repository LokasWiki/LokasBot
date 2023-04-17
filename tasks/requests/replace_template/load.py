import pywikibot
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils.wikidb import Database
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 6

template_query = """select page.page_title as "prt_title",page.page_namespace as "prt_namespace" from templatelinks 
inner join page on page.page_id = templatelinks.tl_from
inner join linktarget on linktarget.lt_id = templatelinks.tl_target_id 
where linktarget.lt_title in (select page_title from page where page_id in (FROM_ID)) and linktarget.lt_namespace = 10 and page.page_namespace in (0,14,6,10) 
and page.page_is_redirect = 0
"""

category_query = """"""

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            database = Database()
            from_page = pywikibot.Page(site, title=request.from_name)
            to_page = pywikibot.Page(site, title=request.to_name)
            if to_page.exists():
                from_id = from_page.pageid
                # template
                if request.extra is None:
                    database.query = template_query.replace("FROM_ID", str(from_id))
                    database.get_content_from_database()
                    gen = database.result

            pages = []
            for row in gen:
                page_title = str(row['prt_title'], 'utf-8')
                pages.append(Page(
                    title=page_title,
                    namespace=row['prt_namespace']
                ))
            request.status = Status.RECEIVED
            request.pages = pages
            session.commit()

        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
