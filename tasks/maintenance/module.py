import pywikibot
import datetime
import traceback
from datetime import timedelta
from pywikibot import Timestamp

from core.utils.helpers import check_status
from core.utils.pipeline import Pipeline
from core.utils.wikidb import Database
from tasks.maintenance.bots.dead_end import DeadEnd
from tasks.maintenance.bots.has_categories import HasCategories
from tasks.maintenance.bots.orphan import Orphan
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.maintenance.bots.template_redirects import TemplateRedirects
from tasks.maintenance.bots.underlinked import UnderLinked
from tasks.maintenance.bots.unreferenced import Unreferenced
from tasks.maintenance.bots.unreviewed_article import UnreviewedArticle


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


def process_article(site, cursor, conn, id, title, thread_number):
    try:
        cursor.execute("SELECT status FROM pages WHERE id = ? LIMIT 1", (id,))
        row = cursor.fetchone()
        if row is not None:
            status = row[0]
            if status == 0:
                cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
                conn.commit()
                page = pywikibot.Page(site, title)

                # get first revision
                revisions = page.revisions(reverse=True, total=1)
                first_edit = None
                for revision in revisions:
                    first_edit = revision['timestamp']
                    break
                status = False

                # Get the current time
                current_time = Timestamp.utcnow()

                # Calculate the difference between the timestamp and the current time
                time_difference = current_time - first_edit

                # Check if the time difference is less than 3 hours
                if time_difference > timedelta(hours=3):
                    status = True
                if status:
                    steps = [
                        UnreviewedArticle,
                        HasCategories,
                        PortalsBar,
                        Unreferenced,
                        Orphan,
                        DeadEnd,
                        UnderLinked
                    ]
                    extra_steps = [
                        PortalsMerge,
                        PortalsBar,
                        TemplateRedirects
                    ]
                    if page.exists() and (not page.isRedirectPage()):
                        text = page.text
                        summary = "بوت:صيانة V5.4.0"
                        pipeline = Pipeline(page, text, summary, steps, extra_steps)
                        processed_text, processed_summary = pipeline.process()
                        # write processed text back to the page
                        if pipeline.hasChange() and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
                            print("start save " + page.title())
                            page.text = processed_text
                            page.save(summary=processed_summary)
                        else:
                            print("page not changed " + page.title())

                    cursor.execute("DELETE FROM pages WHERE id = ?", (id,))
                    conn.commit()
                else:
                    print("skip need more time to edit it")
                    # todo:move it to one function
                    delta = datetime.timedelta(hours=1)
                    new_date = datetime.datetime.now() + delta
                    cursor.execute("UPDATE pages SET status = 0, date = ? WHERE id = ?",
                                   (new_date, id))
                    conn.commit()
    except Exception as e:
        print(f"An error occurred while processing {title}: {e}")
        just_the_string = traceback.format_exc()
        print(just_the_string)
        delta = datetime.timedelta(hours=1)
        new_date = datetime.datetime.now() + delta
        cursor.execute("UPDATE pages SET status = 0, date = ? WHERE id = ?",
                       (new_date, id))
        conn.commit()
