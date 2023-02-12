import os, sys


import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from app.core import engine
from app.core import Request, Status,Page
from models import WikiLinkExtractor

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 3

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            page = pywikibot.Page(site, request.from_name)

            extractor = WikiLinkExtractor(page.text)
            links = extractor.extract_links()
            pages = []
            for temlink in links:
                link = pywikibot.Page(site, temlink)
                if link.exists() and link.namespace() == 0:
                    pages.append(Page(
                        title=link.title(with_ns=False),
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
