import pywikibot

from module import RequestsPage, RequestsScanner
from database import Query

# Create an instance of the RequestsPage class
site = pywikibot.Site()
site2 = pywikibot.Site("ar", "wikipedia")
requests_page = RequestsPage(site)
requests_page.title = "ويكيبيديا:طلبات توزيع بوابة"
requests_page.header_text = "{{/ترويسة}}"

requests_page.load_page()

db = Query()

type_of_request = 1

if requests_page.check_user_edits(0):
    scanner = RequestsScanner()
    scanner.pattern = r"\* \[\[:(?P<namespace>بوابة|تصنيف|قالب):(?P<source>.*)\]\](?P<extra>.*)>\[\[:بوابة:(?P<destination>.*)\]\]\n*"
    scanner.scan(requests_page.get_page_text())

    if scanner.have_requests:
        requests_page.start_request()
        for request in scanner.requests:

            source_page = pywikibot.Page(site2, f"{request['namespace']}:{request['source']}")
            destination_page = pywikibot.Page(site2, f"بوابة:{request['destination']}")

            print(source_page.title())
            print(destination_page.title())

            db.insert_request(source_page.pageid, source_page.namespace(), destination_page.namespace(),
                              destination_page.pageid, type_of_request, 0)

    else:
        requests_page.move_to_talk_page()
else:
    requests_page.move_to_talk_page()
# Get the page text after removing the header text
