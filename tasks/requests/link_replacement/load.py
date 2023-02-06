import os, sys
import pywikibot

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core import PageProcessor,RequestsPage,RequestsScanner,Query

db = Query()

# Create an instance of the RequestsPage class
site = pywikibot.Site("ar", "wikipedia")
site2 = pywikibot.Site()

type_of_request = 2


requests = db.get_new_requests(5, type_of_request)

for request in requests:
    page_title = request['from_title']
    page = pywikibot.Page(site, page_title,request['from_namespace'])

    gen = page.backlinks(follow_redirects=False, namespaces=[0, 14, 10, 6], content=True)

    for p in gen:
        db.insert_page(p.title(with_ns=False),p.namespace(),0,request['id'])
    db.update_request_status(request['id'],1)