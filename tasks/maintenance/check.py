import datetime
import os
import time
import sqlite3

import pywikibot

from bots.unreviewed_article.core import UnreviewedArticle


def create_database_table():
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, "maintenance.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    return conn, cursor


def get_unreviewed_articles(cursor):
    cursor.execute("SELECT id, title FROM pages WHERE status=0 ORDER BY date ASC LIMIT 50")
    rows = cursor.fetchall()
    return rows


def process_unreviewed_article(site, cursor, conn, id, title):
    try:
        cursor.execute("UPDATE pages SET status = 1 WHERE id = ?", (id,))
        conn.commit()
        page = UnreviewedArticle(site)
        page.title = title
        page.load_page()
        if not page.check():
            page.add_template()
        else:
            page.remove_template()
        cursor.execute("DELETE FROM pages WHERE id = ?", (id,))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while processing {title}: {e}")
        cursor.execute("UPDATE pages SET status = 0, date = date + ? WHERE id = ?",
                       (datetime.timedelta(hours=1), id))
        conn.commit()


def main():
    try:
        site = pywikibot.Site()
        conn, cursor = create_database_table()
        rows = get_unreviewed_articles(cursor)
        if rows:
            for row in rows:
                time.sleep(2)
                id = row[0]
                title = row[1]
                print(title)
                process_unreviewed_article(site, cursor, conn, id, title)
        else:
            time.sleep(60)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
    return 0


if __name__ == "__main__":
    main()
