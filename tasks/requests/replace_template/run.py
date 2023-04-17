import copy
import traceback

import pywikibot
import wikitextparser as wtp
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from core.utils.helpers import prepare_str
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 6

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(20)

    for request in session.scalars(stmt):

        template_from = request.from_title
        template_to = request.to_title

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(1000).all()

        for page in pages:
            try:
                p = pywikibot.Page(site, title=str(page.page_name), ns=page.namespace)
                if p.exists():
                    temp_text = p.text
                    parsed = wtp.parse(p.text)
                    for template in parsed.templates:
                        if prepare_str(template.name) == prepare_str(template_from):
                            temp_template = copy.deepcopy(template)
                            temp_template.name = str(template_to).replace("_", ' ')
                            temp_text = temp_text.replace(str(template), str(temp_template))

                    p.text = temp_text
                    p.save(
                        summary="بوت:[[ويكيبيديا:طلبات استبدال القوالب]] استبدال [[قالب:" + template_from + "]] ب [[قالب:" + template_to + "]]"
                    )
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
