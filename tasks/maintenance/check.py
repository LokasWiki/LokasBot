import logging
import threading
import pywikibot
from sqlalchemy.orm import Session

from database.engine import engine
from database.helpers import get_articles
from module import process_article
from database.models import  TaskName

def read(thread_number):
    try:
        print(thread_number)
        site = pywikibot.Site()
        with Session(engine) as session:
            for row in get_articles(session, thread_number,pages_type=TaskName.MAINTENANCE):
                print(row)
                process_article(site=site,session=session, id=row[0], title=row[1], thread_number=thread_number)

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
    run_threads()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
