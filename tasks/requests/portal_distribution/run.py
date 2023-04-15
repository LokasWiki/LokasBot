import traceback

import pywikibot
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from core.utils.helpers import prepare_str
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
        func.count(Page.id) == func.count(distinct(Page.id))).limit(1)

    for request in session.scalars(stmt):

        page_title = request.from_title
        page_new_title = request.to_title

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(1000).all()

        for page in pages:
            try:
                p = pywikibot.Page(site, title=str(page.page_name), ns=0)
                if p.exists():
                    # check if portal is found in page with different name
                    found = False
                    for p2 in p.linkedPages(namespaces=100, content=False):
                        if prepare_str(p2.title(with_ns=False)) == prepare_str(page_new_title):
                            found = True
                            break
                    if not found:
                        # if not found start add portal to page
                        text = p.text
                        text += "\n"
                        text += "{{شريط بوابات|" + page_new_title + "}}"

                        pipeline = PipelineWithExtraSteps(p, text, "", [
                            PortalsMerge,
                            PortalsBar,
                        ], [])

                        processed_text, processed_summary = pipeline.process()

                        p.text = processed_text
                        p.save(summary=f"بوت:[[ويكيبيديا:طلبات توزيع بوابة]] أضاف ([[بوابة:{page_new_title}]] )")

                    # start change page status in database
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
