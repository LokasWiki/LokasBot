import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select


from tasks.requests.core.module import PageProcessor, RequestsPage, RequestsScanner
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status,Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 2

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            page = pywikibot.Page(site, request.from_name)
            gen = page.backlinks(follow_redirects=False, namespaces=[0, 14, 10, 6], content=True)
            pages = []
            for p in gen:
                pages.append(Page(
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
