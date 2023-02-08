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
        pattern = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE)
        matches = re.findall(pattern, self.text)
        for match in matches:
            if "تصنيف:" not in match.lower() and "Category:" not in match.lower():
                if "|" in match:
                    link = match.split("|")[0]
                else:
                    link = match
                self.links.append(link)
        return self.links


site = pywikibot.Site()


def process_article(site, cursor, conn, id, title):
    try:
        cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
        conn.commit()

        page_name = title

        page = pywikibot.Page(site, page_name)

        extractor = WikiLinkExtractor(page.text)
        links = extractor.extract_links()
        text = page.text

        replace = []

        for temlink in links:
            link = pywikibot.Page(site, temlink)
            if link.exists() and link.namespace() == 0 and link.isRedirectPage():
                s = (link.title(), link.getRedirectTarget().title())
                replace.append(s)

        for item in replace:
            page_title = item[0]
            page_new_title = item[1]

            text = str(text)
            reg_str = r"\[\[(" + re.escape(page_title) + r")(\|(?:.*?))?\]\]"
            # print(reg_str)
            link_list = re.findall(reg_str, text)
            # if link_list:
            for r in link_list:
                print(r)
                r_link = r[0]
                r_title = r[1]
                if r_title == '':
                    r_title = "|" + r_link
                old_link = "[[" + r[0] + r[1] + "]]"
                new_link = "[[" + page_new_title + r_title + "]]"
                print(old_link)
                print(new_link)
                text = text.replace(old_link, new_link)

            text = text
            # print(text)
        if page.text != text:
            page.text = text
            page.save(summary="بوت: استبدال وصلات (طلب من [[خاص:فرق/61052388|ويكيبيديا:طلبات النقل]])")
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


for i in range(100):
    try:
        conn, cursor = create_database_table()
        rows = get_articles(cursor)
        if rows and check_status():
            for row in rows:
                print("start " + row[1])
                process_article(site, cursor, conn, id=row[0], title=row[1])
                time.sleep(1)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")


