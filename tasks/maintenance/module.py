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
from database.models import Page, Status as Model_Status

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

TASK_SUMMARY = "بوت:صيانة V5.8.0"


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

    for row in database.result:
        title = str(row['pl_2_title'], 'utf-8')
        yield title


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

    portals_merge_steps = [
        UnreviewedArticle,
        HasCategories,
        PortalsBar,
        Unreferenced,
        Orphan,
        DeadEnd,
        UnderLinked,
        PortalsMerge,
        PortalsBar,
        # Stub
    ]

    @staticmethod
    def method1():
        pass


def clean_summary(processed_summary):
    temp_summary = processed_summary
    try:
        # to remove duplicate summary
        if str(temp_summary).count("، تعريب"):
            temp_summary = str(temp_summary).replace("، تعريب", "")
            temp_summary += "، تعريب"
    except Exception as e:
        logging.error(f"An error occurred while clean_summary processing {processed_summary}: {e}")
        logging.exception(e)
    return temp_summary


class ProcessArticle:
    def __init__(self, site: pywikibot.Site, session: Session, id: int, title: str, thread_number: int):
        # init base
        self.site = site
        self.session = session
        self.id = id
        self.title = title
        self.thread_number = thread_number
        self.summary = TASK_SUMMARY

    def start(self):
        try:
            # get page object
            self.page = pywikibot.Page(self.site, self.title)
            # Check if the page has already been processed
            self.page_query = self.session.query(Page).filter_by(id=self.id, status=Model_Status.PENDING).one_or_none()


            if self.page is None:
                self._delete_page()
            else:
                if self.page_query is not None:
                    # Update the status of the page to indicate that it is being processed
                    self.page_query.status = Model_Status.RECEIVED
                    self.session.commit()

                    if self.page.exists() and (not self.page.isRedirectPage()):
                        # if status true can edit
                        if check_edit_age(page=self.page):

                            try:

                                self.pipeline = Pipeline(self.page, self.page.text, TASK_SUMMARY, PipelineTasks.steps,
                                                         PipelineTasks.extra_steps)
                                processed_text, processed_summary = self.pipeline.process()
                                # write processed text back to the page
                                if self.pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                                    print("start save " + self.page.title())
                                    self.page.text = processed_text
                                    self.page.save(summary=clean_summary(processed_summary))
                                else:
                                    print("page not changed " + self.page.title())

                                self._delete_page()

                            except Exception as e:
                                logging.error(f"An error occurred while processing {self.title}: {e}")
                                logging.exception(e)
                                if self.page_query is not None:
                                    self._delay_page(hours=1)

                        else:
                            self._delay_page(hours=1)

                    else:
                        self._delete_page()


        except Exception as e:
            logging.error(f"An error occurred while processing {self.title}: {e}")
            logging.exception(e)
            if self.page_query is not None:
                self._delay_page(hours=1)

    def _delete_page(self):
        if self.page_query is not None:
            # Delete the page from the database
            self.session.delete(self.page_query)
            self.session.commit()

    def _delay_page(self, hours=1):
        # Update the status of the page to indicate that it needs to be processed again later
        if self.page_query is not None:
            delta = datetime.timedelta(hours=hours)
            new_date = datetime.datetime.now() + delta
            self.page_query.status = Model_Status.PENDING
            self.page_query.update_date = new_date
            self.session.commit()
