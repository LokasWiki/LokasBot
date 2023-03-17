import json
import logging
import os
import pywikibot
import datetime

from sqlalchemy.orm import Session

from core.utils.file import File
from core.utils.helpers import check_status, prepare_str, check_edit_age
from core.utils.pipeline import Pipeline
from core.utils.wikidb import Database
from database.models import Page

from tasks.maintenance.bots.dead_end import DeadEnd
from tasks.maintenance.bots.has_categories import HasCategories
from tasks.maintenance.bots.orphan import Orphan
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.maintenance.bots.rename_template_parameters import RenameTemplateParameters
from tasks.maintenance.bots.template_redirects import TemplateRedirects
from tasks.maintenance.bots.underlinked import UnderLinked
from tasks.maintenance.bots.unreferenced import Unreferenced
from tasks.maintenance.bots.unreviewed_article import UnreviewedArticle
from tasks.maintenance.bots.stub import Stub


def get_pages(start, custom_query=None):
    query = """SELECT pl_2_title
FROM (
    SELECT DISTINCT log_title AS "pl_2_title"
    FROM logging
    WHERE log_type IN ("review")
    AND log_namespace IN (0)
    AND log_timestamp > DATE_SUB( now(), INTERVAL MINUTE_SUB_NUMBER MINUTE )
    UNION
    SELECT DISTINCT page.page_title AS "pl_2_title"
    FROM revision
    INNER JOIN page ON revision.rev_page = page.page_id
    WHERE page.page_namespace IN (0)
    AND rev_timestamp > DATE_SUB( now(), INTERVAL MINUTE_SUB_NUMBER MINUTE ) and page_is_redirect = 0
    UNION
    select page.page_title AS "pl_2_title" from categorylinks
    inner join page on page.page_id = categorylinks.cl_from
    # تصنيف:مقالات تحتوي بوابات مكررة
    # تصنيف:صفحات_تحتوي_بوابات_مكررة_باستخدام_قالب_بوابة
    where cl_to in (select page.page_title from page where page_id in (6202012,6009002))
    and cl_type = "page"
    and page.page_namespace = 0
    UNION
    select page_title as "pl_2_title" from page
    where page.page_is_redirect = 0
    and page.page_namespace = 0
    and page_id in (select fp_page_id from flaggedpages where fp_page_id = page_id)
    and page_id in (select cl_from from categorylinks where cl_to like "جميع_المقالات_غير_المراجعة")
    UNION
    select page_title as "pl_2_title" from page
    where page.page_is_redirect = 0
    and page.page_namespace = 0
    and page_id not in (select fp_page_id from flaggedpages where fp_page_id = page_id)
    and page_id not in (select cl_from from categorylinks where cl_to like "جميع_المقالات_غير_المراجعة")
) AS pages_list"""
    database = Database()

    if custom_query is None:
        database.query = query.replace("MINUTE_SUB_NUMBER", str(start))
    else:
        database.query = custom_query

    database.get_content_from_database()
    gen = []
    for row in database.result:
        title = str(row['pl_2_title'], 'utf-8')
        gen.append(title)

    gen = set(gen)
    return gen


def get_skip_pages():
    home_path = os.path.expanduser("~")
    file = File(script_dir=home_path)
    file_path = prepare_str('maintenance_skip.txt')
    file.set_stub_path(file_path)
    file.get_json_content()
    templates = json.loads(file.contents)
    return templates


class PipelineTasks:
    steps = [
        UnreviewedArticle,
        HasCategories,
        PortalsBar,
        Unreferenced,
        Orphan,
        DeadEnd,
        UnderLinked,
        # Stub
    ]

    extra_steps = [
        PortalsMerge,
        PortalsBar,
        TemplateRedirects,
        RenameTemplateParameters
    ]

    @staticmethod
    def method1():
        pass


def process_article(site, session: Session, id: int, title: str, thread_number: int):
    try:
        # get page object
        page = pywikibot.Page(site, title)

        # Check if the page has already been processed
        page_query = session.query(Page).filter_by(id=id, status=0).one_or_none()
        if page_query is not None:
            # Update the status of the page to indicate that it is being processed
            page_query.status = 1
            session.commit()

            # todo:make it same with prepare_str
            if page.title() not in get_skip_pages():
                # todo:need more refactor
                if check_edit_age(page=page):
                    if page.exists() and (not page.isRedirectPage()):
                        text = page.text
                        summary = "بوت:صيانة V5.6.5"
                        pipeline = Pipeline(page, text, summary, PipelineTasks.steps, PipelineTasks.extra_steps)
                        processed_text, processed_summary = pipeline.process()
                        # write processed text back to the page
                        if pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                            logging.info("start save " + page.title())
                            page.text = processed_text
                            # to remove duplicate summary
                            if str(processed_summary).count("، تعريب"):
                                processed_summary = str(processed_summary).replace("، تعريب", "")
                                processed_summary += "، تعريب"

                            page.save(summary=processed_summary)
                        else:
                            logging.info("page not changed " + page.title())

                    # Delete the page from the database
                    session.delete(page_query)
                    session.commit()

                else:
                    logging.info("skip need more time to edit it")
                    # Update the status of the page to indicate that it needs to be processed again later
                    delta = datetime.timedelta(hours=1)
                    new_date = datetime.datetime.now() + delta
                    page_query.status = 0
                    page_query.date = new_date
                    session.commit()
    except Exception as e:
        logging.error(f"An error occurred while processing {title}: {e}")
        logging.exception(e)

        # Update the status of the page to indicate that it needs to be processed again later
        delta = datetime.timedelta(hours=1)
        new_date = datetime.datetime.now() + delta
        page_query.status = 0
        page_query.date = new_date
        session.commit()
