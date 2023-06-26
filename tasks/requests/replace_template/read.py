import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request
from tasks.requests.core.module import RequestsPage, RequestsScanner

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 6

try:

    requests_page = RequestsPage(site)
    requests_page.title = "ويكيبيديا:طلبات استبدال القوالب"
    requests_page.header_text = "{{/ترويسة}}"

    requests_page.load_page()

    if requests_page.check_user_edits(3000) and requests_page.check_user_groups(group='editor'):
        scanner = RequestsScanner()
        scanner.pattern = r"\*\s*?\[\[:قالب:(?P<source>.*?)\]\]\s*>\s*\[\[:قالب:(?P<destination>.*?)\]\](?:\s*>\s*\[\[:تصنيف:(?P<extra>.*?)\]\])?\n*"
        scanner.scan(requests_page.get_page_text())

        if scanner.have_requests:
            requests_page.start_request()
            try:
                with Session(engine) as session:
                    for request in scanner.requests:
                        # source_page = pywikibot.Page(site, f"{request['source']}",ns=0)
                        # destination_page = pywikibot.Page(site, f"{request['destination']}",ns=0)
                        # if source_page.exists() and destination_page.exists() and source_page.namespace() == 0 and destination_page.namespace() == 0:
                        # todo:add check if template exists with send content to talk page
                        request_model = Request(
                            from_title=request['source'],
                            from_namespace=10,
                            to_title=request['destination'],
                            to_namespace=10,
                            request_type=type_of_request,
                            extra=request['extra']
                        )
                        session.add(request_model)
                    session.commit()
            except Exception as e:
                session.rollback()
                print("An error occurred while committing the changes:", e)

        else:
            print("no reqtest found")
            requests_page.move_to_talk_page()
    else:
        print("not allow for user")
        requests_page.move_to_talk_page()
    # Get the page text after removing the header text
except Exception as e:
    print(f"An error occurred: {e}")
