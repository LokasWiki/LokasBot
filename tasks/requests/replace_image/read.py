import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request
from tasks.requests.core.module import RequestsPage, RequestsScanner

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 8

try:

    requests_page = RequestsPage(site)
    requests_page.title = "ويكيبيديا:طلبات استبدال الصور"
    requests_page.header_text = "{{/ترويسة}}"

    requests_page.load_page()

    if requests_page.check_user_edits(3000) and requests_page.check_user_groups(group='editor'):
        scanner = RequestsScanner()
        scanner.pattern = r"\*\s*\[\[:ملف:(?P<source>.*)\]\](?P<extra>.*)\[\[:ملف:(?P<destination>.*)\]\]"
        scanner.scan(requests_page.get_page_text())

        if scanner.have_requests:
            requests_page.start_request()
            try:
                with Session(engine) as session:
                    for request in scanner.requests:
                        request_model = Request(
                            from_title=request['source'],
                            to_title=request['destination'],
                            from_namespace=6,
                            to_namespace=6,
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
