from threading import Timer
from datetime import timedelta
import pywikibot
from pywikibot import Timestamp
import datetime
import traceback

from core.utils.helpers import check_status
from tasks.webcite.modules.parsed import Parsed
from core.utils.wikidb import Database


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


def process_article(site, cursor, conn, id, title, thread_number, limiter):
    def handle_timeout():
        print(f"Timeout while processing {title}")
        raise TimeoutError()

    try:
        cursor.execute("SELECT status FROM pages WHERE id = ? LIMIT 1", (id,))
        row = cursor.fetchone()
        if row is not None:
            status = row[0]
            if status == 0:
                cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
                conn.commit()
                page = pywikibot.Page(site, title)

                if page.exists() and (not page.isRedirectPage()):
                    summary = ""
                    bot = Parsed(page.text, summary, limiter)

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

                    # if status true can edit
                    if status:
                        new_text, new_summary = bot()
                        # write processed text back to the page
                        if new_text != page.text and check_status("مستخدم:LokasBot/الإبلاغ عن رابط معطوب أو مؤرشف"):
                            print("start save " + page.title())
                            page.text = new_text
                            page.save(new_summary)
                        else:
                            print("page not changed " + page.title())
                        # todo add option to not update page if have one or more links not archived
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

    except TimeoutError:
        delta = datetime.timedelta(hours=3)
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
