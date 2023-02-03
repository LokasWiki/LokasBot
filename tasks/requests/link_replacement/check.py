import pywikibot

from module import Query,RequestsPage,RequestsScanner

requests_query = Query('requests.db')

# Create an instance of the RequestsPage class
site = pywikibot.Site()

requests_page = RequestsPage(site)
requests_page.title = "ويكيبيديا:طلبات استبدال الوصلات"
requests_page.header_text = "{{/ترويسة}}"

requests_page.load_page()


if requests_page.check_user_edits():
    scanner = RequestsScanner()
    scanner.pattern = r"\*\s*\[\[:(?P<source>.*)\]\](?P<extra>.*)>\[\[:(?P<destination>.*)\]\]"
    scanner.scan(requests_page.get_page_text())

    if scanner.have_requests:
        requests_page.start_request()
        for request in scanner.requests:
            print( request['source'],request['destination'])
            requests_query.insert_request((request['source'], request['destination'], 0))
    else:
        requests_page.move_to_talk_page()
else:
    requests_page.move_to_talk_page()
# Get the page text after removing the header text
