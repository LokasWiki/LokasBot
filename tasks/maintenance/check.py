import datetime
import os
import time
import sqlite3

import pywikibot

from bots.unreviewed_article.core import UnreviewedArticle

site = pywikibot.Site()

home_path = os.path.expanduser("~")
database_path = os.path.join(home_path, "maintenance.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()


# Create the table with a status column
cursor.execute('''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')


try:
    cursor.execute("SELECT title FROM pages WHERE status=0 ORDER BY date ASC LIMIT 50")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            time.sleep(2)
            title = row[0]
            print(title)
            try:
                cursor.execute("UPDATE pages SET status = 1 WHERE title = ?", (title,))
                conn.commit()
                page = UnreviewedArticle(site)
                page.title = title
                page.load_page()
                if not page.check():
                    page.add_template()
                else:
                    page.remove_template()
                cursor.execute("DELETE FROM pages WHERE title = ?", (title,))
                conn.commit()
            except Exception as e:
                print(f"An error occurred while processing {title}: {e}")
                cursor.execute("UPDATE pages SET status = 0, date = date + ? WHERE title = ?",
                               (datetime.timedelta(hours=1), title))
                conn.commit()
    else:
        time.sleep(60)
except sqlite3.Error as e:
    print(f"An error occurred while interacting with the database: {e}")