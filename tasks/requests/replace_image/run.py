import traceback

import pywikibot
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page
from tasks.requests.replace_image.models import ImageReplacer

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 8

try:
    session = Session(engine)

    stmt = select(Request).join(Page).filter(Request.status == Status.RECEIVED, Page.status == Status.PENDING,
                                             Request.request_type == type_of_request).group_by(Request).having(
        func.count(Page.id) == func.count(distinct(Page.id))).limit(100)

    for request in session.scalars(stmt):

        pages = session.query(Page).filter(Page.request == request, Page.status == Status.PENDING).order_by(
            Page.namespace.desc()).limit(10).all()

        for page in pages:
            try:

                page_name = page.page_name
                old_file_name = request.from_title
                new_file_name = request.to_title

                replacer = ImageReplacer(site, page_name)
                replacer.set_old_file_name(old_file_name)
                replacer.set_new_file_name(new_file_name)
                replacer.replace_image()
                replacer.replace_image_in_gallery_tag()
                replacer.replace_image_in_imagemap_tag()
                replacer.replace_image_in_custom_template()
                new_text = replacer.get_new_text()

                if replacer.page.text != new_text:
                    replacer.page.text = new_text
                    summary = "بوت:[[ويكيبيديا:طلبات استبدال الصور]] استبدال [[ملف:{}]] ب [[ملف:{}]]  (v0.0.6) (beta)".format(
                        old_file_name, new_file_name)
                    replacer.page.save(summary=summary)

                page.status = Status.COMPLETED
                session.commit()
            except Exception as e:
                print(f"An error occurred where save : {e}")
                just_the_string = traceback.format_exc()
                print(just_the_string)
                session.rollback()

except Exception as e:
    print(f"An error occurred: {e}")
