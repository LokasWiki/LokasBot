import re
import os, sys
import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.database.engine import engine
from core.database.models import Request, Status,Page


# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 2

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(10)

    for request in session.scalars(stmt):

        page_title = request.from_title
        page_new_title = request.to_title

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(100).all()

        for page in pages:
            try:
                p = pywikibot.Page(site, page.page_name)
                print(p.title())
                text = str(p.text)
                reg_str = r"\[\[(" + re.escape(page_title) + r")(\|(?:.*?))?\]\]"
                link_list = re.findall(reg_str, text)
                # if link_list:
                for r in link_list:
                    r_link = r[0]
                    r_title = r[1]
                    if r_title == '':
                        r_title = "|" + r_link
                    old_link = "[[" + r[0] + r[1] + "]]"
                    new_link = "[[" + page_new_title + r_title + "]]"
                    text = text.replace(old_link, new_link)

                p.text = text
                # print(text)
                p.save(
                    summary="بوت:[[ويكيبيديا:طلبات استبدال الوصلات]] استبدال [[" + page_title + "]] ب [[" + page_new_title + "]]")

                page.status = Status.COMPLETED
                session.commit()
            except Exception as e:
                print(f"An error occurred where save : {e}")
                session.rollback()

except Exception as e:
    print(f"An error occurred: {e}")
