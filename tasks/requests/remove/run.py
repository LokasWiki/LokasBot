import traceback

import pywikibot
import wikitextparser as wtp
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from core.utils.helpers import prepare_str
from core.utils.pipeline import Pipeline
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page
from tasks.requests.remove.bot.portals_bar import PortalsBar
from tasks.requests.remove.bot.portals_merge import PortalsMerge
from tasks.requests.remove.bot.remove_portal import RemovePortal

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 7

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
                    # for remove template
                    if request.from_namespace == 10:
                        for template in parsed.templates:
                            if prepare_str(template.name) == prepare_str(template_from):
                                temp_text = temp_text.replace(str(template), str(""))

                    if request.from_namespace == 14:
                        for link in parsed.wikilinks:
                            if link.title.startswith("تصنيف:"):
                                if prepare_str(link.title.replace("تصنيف:", "")) == prepare_str(template_from):
                                    temp_text = str(temp_text).replace(str(link), "")

                    if request.from_namespace == 100:

                        step_one = RemovePortal(p.text, template_from)
                        step_one.start_remove()
                        if p.namespace() == 0:
                            pipeline = Pipeline(p, step_one.tem_text, str("remove"), [
                                PortalsMerge,
                                PortalsBar,
                            ], [])
                            processed_text, processed_summary = pipeline.process()
                            temp_text = processed_text
                        else:
                            temp_text = step_one.tem_text
                    p.text = temp_text

                    word = "تصنيف"
                    if request.from_namespace == 10:
                        word = "قالب"
                    elif request.from_namespace == 100:
                        word = "بوابة"

                    p.save(
                        summary="بوت:[[ويكيبيديا:طلبات إزالة (بوابة، تصنيف، قالب)]] حذف [[" + word + ":" + template_from + "]] "
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
