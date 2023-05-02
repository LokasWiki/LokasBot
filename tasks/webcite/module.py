import datetime
import logging

import pywikibot
from sqlalchemy.orm import Session

from core.utils.helpers import check_status, check_edit_age
from core.utils.wikidb import Database
from database.models import Page, Status as Model_Status
from tasks.webcite.modules.parsed import Parsed
from tasks.webcite.modules.request_limiter import RequestLimiter


def get_pages(start):
    query = """SELECT pl_2_title
FROM (
    SELECT DISTINCT page.page_title AS "pl_2_title"
    FROM revision
    INNER JOIN page ON revision.rev_page = page.page_id
    WHERE page.page_namespace IN (0)
    AND rev_timestamp > DATE_SUB( now(), INTERVAL MINUTE_SUB_NUMBER MINUTE ) and page_is_redirect = 0
) AS pages_list"""
    database = Database()
    database.query = query.replace("MINUTE_SUB_NUMBER", str(start))
    database.get_content_from_database()

    for row in database.result:
        title = str(row['pl_2_title'], 'utf-8')
        yield title


class ProcessArticle:
    def __init__(self,site: pywikibot.Site, session: Session, id: int, title: str, thread_number: int, limiter: RequestLimiter):
        # init base
        self.site = site
        self.session = session
        self.id = id
        self.title = title
        self.thread_number = thread_number
        self.limiter = limiter
        self.summary = "بوت:الإبلاغ عن رابط معطوب أو مؤرشف V1.6.3"

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
                                bot = Parsed(self.page.text, self.summary, self.limiter)
                                new_text, new_summary = bot()
                                # write processed text back to the page
                                if new_text != self.page.text and check_status(
                                        "مستخدم:LokasBot/الإبلاغ عن رابط معطوب أو مؤرشف"):
                                    print("start save " + self.page.title())
                                    self.page.text = new_text
                                    self.page.save(new_summary)
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
            if self.page_query is not  None:
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
