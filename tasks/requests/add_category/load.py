import os, sys
import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select

from tasks.requests.core.module import PageProcessor, RequestsPage, RequestsScanner
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page
from core.utils.wikidb import Database

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 1

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            database = Database()
            if request.to_namespace == 10:
                to_page = pywikibot.Page(site, request.to_name)
                if to_page.exists():
                    database.query = """select lt_title as prt_title from pagelinks
inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
where pl_from = {} and pagelinks.pl_from_namespace = 10 and linktarget.lt_namespace = 0;""".format(to_page.pageid)
                    database.get_content_from_database()
                    gen = database.result
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
                pages.append(Page(
                    title=page_title,
                    namespace=0
                ))
            request.status = Status.RECEIVED
            request.pages = pages
            session.commit()
        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
