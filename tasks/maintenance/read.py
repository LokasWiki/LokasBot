import datetime
import itertools
import os
from pywikibot import pagegenerators
import time
import sqlite3
import pywikibot
import sys


def create_database_table():
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, "maintenance.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    return conn, cursor


def get_pages(site, start, end):
    gen1 = pagegenerators.RecentChangesPageGenerator(site=site, start=start, end=end, namespaces=[0], reverse=True)
    gen2 = pagegenerators.LogeventsPageGenerator(logtype="review", total=3000, site=site, start=start, end=end,
                                                 namespace=0, reverse=True)
    merged_gen = itertools.chain(gen1, gen2)
    gen = set(merged_gen)

    # gen = filter(lambda page: page.exists(), gen)
    return gen


def save_pages_to_db(site, gen, conn, cursor):
    for entry in gen:
        page1 = pywikibot.Page(site, entry.title())
        if not page1.isRedirectPage():
            time.sleep(1)
            try:
                title = entry.title()
                cursor.execute("SELECT * FROM pages WHERE title = ?", (title,))
                if cursor.fetchone() is None:
                    print("added : " + title)
                    cursor.execute("INSERT INTO pages (title, status) VALUES (?, 0)", (title,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"An error occurred while inserting the title {entry.title()} into the database: {e}")


def main(*args: str) -> int:
    try:
        time_before_start = int(sys.argv[1])
        site = pywikibot.Site()
        start = pywikibot.Timestamp.now() - datetime.timedelta(minutes=time_before_start)
        end = pywikibot.Timestamp.now()
        pages = get_pages(site, start, end)

        conn, cursor = create_database_table()

        save_pages_to_db(site, pages, conn, cursor)

        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
