import re
import os, sys
import pywikibot
from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.database.engine import engine
from core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 3

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(10)

    for request in session.scalars(stmt):

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).limit(100).all()

        for page in pages:
            try:
                link = pywikibot.Page(site, page.page_name)
                if link.exists() and link.namespace() == 0:
                    template_found = False
                    for tpl in link.templates(content=False):
                        if tpl.title() == page.title():
                            template_found = True
                            break
                    print(link.title())
                    if not template_found:
                        if "أعلى" in request['extra']:
                            template_name = "{{" + request['from_title'] + "}}"
                            text = template_name + '\n' + text
                        else:
                            template_name = "{{" + request['from_title'] + "}}"
                            text = link.text
                            portal_template = '{{شريط بوابات'
                            stub_template = '{{بذرة'
                            category_template = '[[تصنيف:'
                            if portal_template in text:
                                text = text.replace(portal_template, template_name + '\n' + portal_template, 1)
                            elif stub_template in text:
                                text = text.replace(stub_template, template_name + '\n' + stub_template, 1)
                            elif category_template in text:
                                text = text.replace(category_template, template_name + '\n' + category_template, 1)
                            else:
                                text = text + '\n' + template_name
                        link.text = text
                        link.save("بوت:توزيع قالب")

                page.status = Status.COMPLETED
                session.commit()
            except Exception as e:
                print(f"An error occurred where save : {e}")
                session.rollback()

except Exception as e:
    print(f"An error occurred: {e}")
