import logging
import threading
import time

import pywikibot
from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import get_articles, get_page_count, update_page_statuses_to_pending
from database.models import TaskName
from tasks.webcite.module import ProcessArticle
from tasks.webcite.modules.request_limiter import RequestLimiter


def read(thread_number):
    try:
        print(thread_number)
        limiter = RequestLimiter()
        site = pywikibot.Site()
        need_to_sleep = True

        with Session(engine) as session:
            for row in get_articles(session, thread_number,pages_type=TaskName.WEBCITE):
                need_to_sleep = False
                process_article = ProcessArticle(site=site,session=session, id=row[0], title=row[1], thread_number=thread_number, limiter=limiter)
                process_article.start()

        if not need_to_sleep:
            # sleep 10 min cos now rows found in db now
            print("sleep 10 min cos now rows found in db now ")
            time.sleep(600)

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
        need_to_sleep = get_page_count(session, pages_type=TaskName.WEBCITE)
    if not bool(need_to_sleep):
        # sleep for 10 mint To prevent  it from run again
        print("sleep for 10 mint To prevent  it from run again")
        time.sleep(600)
    else:
        limiter = RequestLimiter()
        run_threads()
        limiter.clear_old_requests()
    with Session(engine) as session:
        update_page_statuses_to_pending(session, TaskName.WEBCITE)
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
