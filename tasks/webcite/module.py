import logging
import pywikibot
import datetime

from sqlalchemy.orm import Session

from core.utils.helpers import check_status, check_edit_age
from database.models import Page,Status,TaskName


from tasks.webcite.modules.parsed import Parsed
from core.utils.wikidb import Database
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
    gen = []
    for row in database.result:
        title = str(row['pl_2_title'], 'utf-8')
        gen.append(title)

    gen = set(gen)
    return gen


def process_article(site: pywikibot.Site, session: Session, id: int, title: str, thread_number: int, limiter: RequestLimiter):
    try:
        # get page object
        page = pywikibot.Page(site, title)

        # Check if the page has already been processed
        page_query = session.query(Page).filter_by(id=id, status=Status.RECEIVED).one_or_none()
        if page_query is not None:
            # Update the status of the page to indicate that it is being processed
            page_query.status = 1
            session.commit()
            if page.exists() and (not page.isRedirectPage()):
                # if status true can edit
                if check_edit_age(page=page):

                    summary = "بوت:الإبلاغ عن رابط معطوب أو مؤرشف V1.5.0"

                    bot = Parsed(page.text, summary, limiter)

                    new_text, new_summary = bot()

                    # write processed text back to the page
                    if new_text != page.text and check_status("مستخدم:LokasBot/الإبلاغ عن رابط معطوب أو مؤرشف"):
                        logging.info("start save " + page.title())
                        page.text = new_text
                        page.save(new_summary)
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
                    page_query.status = Status.PENDING
                    page_query.date = new_date
                    session.commit()
            else:
                # Delete the page from the database
                session.delete(page_query)
                session.commit()
    except Exception as e:
        logging.error(f"An error occurred while processing {title}: {e}")
        logging.exception(e)

        # Update the status of the page to indicate that it needs to be processed again later
        delta = datetime.timedelta(hours=1)
        new_date = datetime.datetime.now() + delta
        page_query.status = Status.PENDING
        page_query.date = new_date
        session.commit()
