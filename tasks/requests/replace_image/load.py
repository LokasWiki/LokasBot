import logging

import pywikibot
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils.wikidb import Database
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 8

sql_query = """select  page.page_title as "prt_title",page.page_namespace as "prt_namespace"
from imagelinks 
inner join page on page.page_id = imagelinks.il_from
where il_to in (
	select page_title from page where page_title like "PAGE_TITLE_TEMP" and page_namespace in (6)
)
and il_from_namespace in (0,14,10) 
"""

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            database = Database()
            try:
                database.query = sql_query.replace("PAGE_TITLE_TEMP", str(request.from_title).replace(" ", "_"))
                database.get_content_from_database()
                gen = database.result
            except Exception as e:
                print("an error occurred while getting the content from the database")
                print(e)
                logging.error("an error occurred while getting the content from the database")
                logging.error(e)

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
