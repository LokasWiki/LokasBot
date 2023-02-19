import time
import sqlite3
import traceback

import pywikibot

from tasks.webcite.module import create_database_table, get_articles, process_article, check_status


def read(thread_number):
    try:
        site = pywikibot.Site()
        conn, cursor = create_database_table()
        rows = get_articles(cursor, 1)
        print(len(rows))
        if len(rows) > 0 and check_status():
            for row in rows:
                process_article(site, cursor, conn, id=row[0], title=row[1], thread_number=row[4])
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
        just_the_string = traceback.format_exc()
        print(just_the_string)


def main():
    # for 20 m
    read(1)
    # for 120 m
    read(2)
    # for 6 h
    read(3)
    # for 24 h
    read(4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
