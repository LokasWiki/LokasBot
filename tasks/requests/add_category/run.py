import traceback

import pywikibot
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 1

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(100)

    for request in session.scalars(stmt):

        page_title = request.from_title
        page_new_title = request.to_title

        added_category = pywikibot.Category(site, request.from_name)

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(100).all()

        for page in pages:
            try:
                p = pywikibot.Page(site, page.page_name)
                if p.exists():
                    categories = p.categories()
                    has_category = False
                    for category in categories:
                        tem = pywikibot.Category(p.site, category.title())
                        if tem.title(with_ns=False).lower() == added_category.title(with_ns=False).lower():
                            has_category = True
                            break

                    if not has_category:
                        text = p.text
                        text += "\n[[" + added_category.title(with_ns=True) + "]]"
                        p.text = text
                        p.save(summary="بوت:إضافة تصنيف")

                    page.status = Status.COMPLETED
                    session.commit()
            except Exception as e:
                print(f"An error occurred where save : {e}")
                just_the_string = traceback.format_exc()
                print(just_the_string)
                session.rollback()

except Exception as e:
    print(f"An error occurred: {e}")
    just_the_string = traceback.format_exc()
    print(just_the_string)
