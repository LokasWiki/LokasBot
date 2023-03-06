import threading
import sqlite3
import traceback

import pywikibot

from core.utils.sqlite import create_database_table, maintenance_db_name
from module import get_articles, process_article, check_status


def read(thread_number):
    try:
        site = pywikibot.Site()
        conn, cursor = create_database_table(maintenance_db_name)

        rows = get_articles(cursor, thread_number)
        if len(rows) > 0 and check_status():
            for row in rows:
                process_article(site, cursor, conn, id=row[0], title=row[1], thread_number=thread_number)
        else:
            if thread_number == 1:
                rows = get_articles(cursor, 2)
            else:
                rows = get_articles(cursor, 1)
            for row in rows:
                process_article(site, cursor, conn, id=row[0], title=row[1], thread_number=thread_number)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
        just_the_string = traceback.format_exc()
        print(just_the_string)


def run_threads():
    # create threads
    threads = [
        threading.Thread(target=read, args=(1,)),
        threading.Thread(target=read, args=(2,)),
        threading.Thread(target=read, args=(3,))
    ]

    # start threads
    for thread in threads:
        thread.start()

    # wait for all threads to complete
    for thread in threads:
        thread.join()


def main():
    run_threads()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
