import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.module import PageProcessor, RequestsPage, RequestsScanner
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 5

try:

    requests_page = RequestsPage(site)
    requests_page.title = "ويكيبيديا:طلبات إزالة (بوابة، تصنيف، قالب)"
    requests_page.header_text = "{{/ترويسة}}"

    requests_page.load_page()
    requests_page.start_request()

    # Get the page text after removing the header text
except Exception as e:
    print(f"An error occurred: {e}")