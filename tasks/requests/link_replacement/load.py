import os, sys
import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.module import PageProcessor, RequestsPage, RequestsScanner
from core.database.engine import engine
from core.database.models import Request, Status,Pages

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 2

try:
    session = Session(engine)

    stmt = select(Request).where(Request.status.in_([Status.PENDING]))

    for request in session.scalars(stmt):
        try:
            page = pywikibot.Page(site, request.from_name)
            gen = page.backlinks(follow_redirects=False, namespaces=[0, 14, 10, 6], content=True)
            pages = []
            for p in gen:
                pages.append(Pages(
                    title=p.title(with_ns=False),
                    namespace=int(p.namespace())
                ))
            request.status = Status.RECEIVED
            request.pages = pages
            session.commit()
        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
