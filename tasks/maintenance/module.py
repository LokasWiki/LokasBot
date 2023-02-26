import sqlite3

import pywikibot
import os
import datetime
import traceback

from core.utils.wikidb import Database
from tasks.maintenance.bots.has_categories import HasCategories
from tasks.maintenance.bots.orphan import Orphan
from tasks.maintenance.bots.portals_bar import PortalsBar
from tasks.maintenance.bots.portals_merge import PortalsMerge
from tasks.maintenance.bots.unreferenced import Unreferenced
from tasks.maintenance.bots.unreviewed_article import UnreviewedArticle

def create_database_table():
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, "maintenance.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,thread INTEGER)''')

    return conn, cursor


def get_pages(start):
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


def save_pages_to_db(gen, conn, cursor, thread_number):
    for entry in gen:
        try:
            title = entry
            cursor.execute("SELECT * FROM pages WHERE title = ?", (title,))
            if cursor.fetchone() is None:
                print("added : " + title)
                cursor.execute("INSERT INTO pages (title, status,thread) VALUES (?, 0,?)", (title, int(thread_number)))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting the title {entry.title()} into the database: {e}")


def get_articles(cursor, thread_number):
    cursor.execute("SELECT id, title,thread FROM pages WHERE thread=? and status=0 ORDER BY date ASC LIMIT 20", (int(thread_number),))
    rows = cursor.fetchall()
    return rows


class Pipeline:
    def __init__(self, page, text, summary, steps, extra_steps):
        self.page = page
        self.text = text
        self.summary = summary
        self.steps = steps
        self.extra_steps = extra_steps
        self.oldText = text

    def process(self):
        for step in self.steps:
            obj = step(self.page, self.text, self.summary)
            self.text, self.summary = obj()

        if self.hasChange():
            for step in self.extra_steps:
                obj = step(self.page, self.text, self.summary)
                self.text, self.summary = obj()

        return self.text, self.summary

    def hasChange(self):
        return self.text != self.oldText


def check_status():
    site = pywikibot.Site()
    title = "مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"
    page = pywikibot.Page(site, title)
    text = page.text
    if text == "لا":
        return True
    return False


def process_article(site, cursor, conn, id, title, thread_number):
    try:
        cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
        conn.commit()
        page = pywikibot.Page(site, title)
        steps = [
            UnreviewedArticle,
            HasCategories,
            PortalsBar,
            Unreferenced,
            Orphan,
            # DeadEnd,
            # Underlinked
        ]
        extra_steps = [
            PortalsMerge,
            PortalsBar
        ]
        if page.exists() and (not page.isRedirectPage()):
            text = page.text
            summary = "بوت:صيانة V4.8.8"
            pipeline = Pipeline(page, text, summary, steps, extra_steps)
            processed_text, processed_summary = pipeline.process()
            # write processed text back to the page
            if pipeline.hasChange() and check_status():
                print("start save " + page.title())
                page.text = processed_text
                page.save(summary=processed_summary)
            else:
                print("page not changed " + page.title())

        cursor.execute("DELETE FROM pages WHERE id = ?", (id,))
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
