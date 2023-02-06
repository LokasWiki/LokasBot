import os, sys
import pywikibot

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core import PageProcessor,RequestsPage,RequestsScanner,Query

db = Query()

# Create an instance of the RequestsPage class
site = pywikibot.Site()
site2 = pywikibot.Site("ar", "wikipedia")

type_of_request = 2

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
        for request in scanner.requests:
            source_page = pywikibot.Page(site2, f"{request['source']}")
            destination_page = pywikibot.Page(site2, f"{request['destination']}")

            if source_page.exists() and destination_page.exists() and source_page.namespace() == 0 and destination_page.namespace() == 0:
                db.insert_request(source_page.pageid, 0, 0,
                                  destination_page.pageid, type_of_request, 0)
            else:
                # todo: add some action here
                print("some page is not exists")
                print(source_page.title())
                print(destination_page.title())

    else:
        requests_page.move_to_talk_page()
else:
    requests_page.move_to_talk_page()
# Get the page text after removing the header text
