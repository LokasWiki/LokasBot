import traceback

import pywikibot
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from core.utils.pipeline import PipelineWithExtraSteps
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 5

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(100)

    for request in session.scalars(stmt):

        page_title = request.from_title
        page_new_title = request.to_title

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(100).all()

        for page in pages:
            try:
                p = pywikibot.Page(site, title=str(page.page_name), ns=0)
                if p.exists():
                    text = p.text
                    text += "\n"
                    text += "{{شريط بوابات|" + page_new_title + "}}"

                    pipeline = PipelineWithExtraSteps(p, text, "", [
                        PortalsMerge,
                        PortalsBar,
                    ], [])

                    processed_text, processed_summary = pipeline.process()

                    p.text = processed_text
                    p.save(summary="بوت:إضافة بوابة")
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
