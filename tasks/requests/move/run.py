import traceback

import pywikibot
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request_Move_Page, Status

# Create an instance of the RequestsPage class
site = pywikibot.Site()

try:
    session = Session(engine)

    pages = session.query(Request_Move_Page).filter(Request_Move_Page.status == Status.PENDING).order_by(
        Request_Move_Page.id.desc()).limit(1).all()

    for page in pages:
        try:
            print(page)
            page.status = Status.COMPLETED
            session.commit()
        except Exception as e:
            print(f"An error occurred where save : {e}")
            just_the_string = traceback.format_exc()
            print(just_the_string)
            session.rollback()

except Exception as e:
    print(f"An error occurred: {e}")
    just_the_string = traceback.format_exc()
    print(just_the_string)
