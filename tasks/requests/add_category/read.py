import os, sys
import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.module import PageProcessor, RequestsPage, RequestsScanner
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 2

try:

    requests_page = RequestsPage(site)
    requests_page.title = "ويكيبيديا:طلبات استبدال الوصلات"
    requests_page.header_text = "{{/ترويسة}}"

    requests_page.load_page()

    if requests_page.check_user_edits(1):
        scanner = RequestsScanner()
        scanner.pattern = r"\*\s*\[\[:(?P<source>.*)\]\](?P<extra>.*)\[\[:(?P<destination>.*)\]\]"
        scanner.scan(requests_page.get_page_text())

        if scanner.have_requests:
            requests_page.start_request()
            try:
                with Session(engine) as session:
                    for request in scanner.requests:
                        # source_page = pywikibot.Page(site, f"{request['source']}",ns=0)
                        # destination_page = pywikibot.Page(site, f"{request['destination']}",ns=0)
                        # if source_page.exists() and destination_page.exists() and source_page.namespace() == 0 and destination_page.namespace() == 0:

                        request_model = Request(
                            from_title=request['source'],
                            to_title=request['destination'],
                            from_namespace=0,
                            to_namespace=0,
                            request_type=type_of_request
                        )
                        session.add(request_model)
                    session.commit()
            except Exception as e:
                session.rollback()
                print("An error occurred while committing the changes:", e)

        else:
            requests_page.move_to_talk_page()
    else:
        requests_page.move_to_talk_page()
    # Get the page text after removing the header text
except Exception as e:
    print(f"An error occurred: {e}")