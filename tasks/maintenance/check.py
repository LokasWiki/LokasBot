import threading
import sqlite3
import traceback

import pywikibot

from core.utils.helpers import check_status
from core.utils.sqlite import create_database_table, maintenance_db_name, get_articles
from module import process_article


def read(thread_number):
    try:
        print(thread_number)
        site = pywikibot.Site()
        conn, cursor = create_database_table(maintenance_db_name)
        rows = get_articles(cursor, thread_number)
        if len(rows) > 0 and check_status("مستخدم:LokasBot/إيقاف مهمة صيانة المقالات"):
            for row in rows:
                print(row)
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
