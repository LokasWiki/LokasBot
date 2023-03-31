import logging
import threading
import time

import pywikibot
from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import get_articles, get_page_count
from module import ProcessArticle
from database.models import TaskName


def read(thread_number):
    try:
        print(thread_number)
        site = pywikibot.Site()
        with Session(engine) as session:

            for row in get_articles(session, thread_number, pages_type=TaskName.MAINTENANCE):
                process_article = ProcessArticle(site=site, session=session, id=row[0], title=row[1],
                                                 thread_number=thread_number)
                process_article.start()


    except Exception as e:
        logging.error("Error occurred while adding pages to the database.")
        logging.exception(e)


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
    need_to_sleep = True
    with Session(engine) as session:
        need_to_sleep = get_page_count(session, pages_type=TaskName.MAINTENANCE)
    if not bool(need_to_sleep):
        # sleep for 10 mint To prevent  it from run again
        print("sleep for 10 mint To prevent  it from run again")
        time.sleep(600)
    else:
        run_threads()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
