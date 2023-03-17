import logging
import threading

import pywikibot
from sqlalchemy.orm import Session

from database.engine import webcite_engine
from database.helpers import get_articles
from tasks.webcite.module import process_article
from tasks.webcite.modules.request_limiter import RequestLimiter


def read(thread_number):
    try:
        print(thread_number)
        limiter = RequestLimiter()
        site = pywikibot.Site()
        with Session(webcite_engine) as webcite_session:
            for row in get_articles(webcite_session, thread_number):
                process_article(site, id=row[0], title=row[1], thread_number=thread_number, limiter=limiter)

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
    limiter = RequestLimiter()
    run_threads()
    limiter.clear_old_requests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
