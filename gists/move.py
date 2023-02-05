import datetime
import os
import re
import sqlite3
import time
import traceback

import pywikibot


def create_database_table():
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, "move.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    return conn, cursor


def save_pages_to_db(gen, conn, cursor):
    for entry in gen:
        try:
            title = entry
            cursor.execute("SELECT * FROM pages WHERE title = ?", (title,))
            if cursor.fetchone() is None:
                print("added : " + title)
                cursor.execute("INSERT INTO pages (title, status) VALUES (?, 0)", (title,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting the title {entry.title()} into the database: {e}")


def get_articles(cursor):
    cursor.execute("SELECT id, title FROM pages WHERE status=0 ORDER BY date ASC LIMIT 10")
    rows = cursor.fetchall()
    return rows



def check_status():
    site = pywikibot.Site()
    title = "مستخدم:LokasBot/إيقاف مهمة أفريقيا ← إفريقيا"
    page = pywikibot.Page(site,title)
    text = page.text
    if text == "لا":
        return True
    return False



class WikiLinkExtractor:
    def __init__(self, text):
        self.text = text
        self.links = []

    def extract_links(self):
        pattern = re.compile(r'\{\{.*?\}\}', re.IGNORECASE | re.DOTALL)
        templates = re.findall(pattern, self.text)

        for template in templates:
            self.text = self.text.replace(template, "")

        pattern = re.compile(r'\[\[([^:]*?)\]\]', re.IGNORECASE)

        matches = re.findall(pattern, self.text)
        for match in matches:
            if "تصنيف:" not in match.lower() and "Category:" not in match.lower():
                if "|" in match:
                    link = match.split("|")[0]
                else:
                    link = match
                site = pywikibot.Site()
                page_title = link
                tmp_page = pywikibot.Page(site,page_title)
                # if tmp_page.exists() and (not tmp_page.isRedirectPage()) and (tmp_page.namespace() == 0):
                self.links.append(link)
        return self.links


def process_article(site, cursor, conn, id, title):
    try:
        cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
        conn.commit()
        page = pywikibot.Page(site, title)
        if page.exists() and (not page.isRedirectPage()):
            o_title = page.title()
            result = re.search("أفريقي", o_title)
            # result = re.search("s", o_title)
            n_title = o_title[:result.start()] + "إفريقي" + o_title[result.end():]
            reason = 'طلب من [[خاص:فرق/61052388|ويكيبيديا:طلبات النقل]]'
            page.move(newtitle=n_title,reason=reason)
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


site = pywikibot.Site()
#
# user_page = pywikibot.Page(site,"مستخدم:لوقا/ملعب 5")
#
# extractor = WikiLinkExtractor(user_page.text)
# links = extractor.extract_links()

# conn, cursor = create_database_table()
#
# save_pages_to_db(links, conn, cursor)

for i in range(100):
    try:
        conn, cursor = create_database_table()
        rows = get_articles(cursor)
        if rows and check_status():
            for row in rows:
                process_article(site, cursor, conn, id=row[0], title=row[1])
                time.sleep(1)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")


# page_name = "جنوب أفريقيا"
#
# page = pywikibot.Page(site,page_name)
#
# print(site.username())
# # main page
# o_title = page.title()
# result = re.search("أفريقي", o_title)
# # result = re.search("s", o_title)
# n_title = o_title[:result.start()] + "إفريقي" + o_title[result.end():]
# reason = 'طلب من [[خاص:فرق/61052388|ويكيبيديا:طلبات النقل]]'
# page.move(newtitle=n_title,reason=reason)
#
#
# if page.toggleTalkPage():
#     talk_page = page.toggleTalkPage()
#     if talk_page.exists():
#         print(talk_page.title())