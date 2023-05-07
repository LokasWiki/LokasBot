import pywikibot
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils.wikidb import Database
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 7
# todo:add page_namespace to in select
template_query = """select page_from.page_title as "prt_title",page_from.page_namespace as "prt_namespace" from templatelinks
inner join linktarget on linktarget.lt_id = templatelinks.tl_target_id
inner join page page_from on page_from.page_id = templatelinks.tl_from
where templatelinks.tl_from_namespace in (0,14) 
and  linktarget.lt_title in (select page_title from page where page_id in (FROM_ID) and page_namespace = 10)
"""

category_query = """SELECT  page_from.page_title as "prt_title",page_from.page_namespace as "prt_namespace"  FROM  categorylinks 
inner join page page_from on page_from.page_id = categorylinks.cl_from
where cl_type  like "page"
and page_from.page_namespace in (0,14) 
and categorylinks.cl_to in (select page_title from page where page_id in (FROM_ID) and page_namespace = 14)
"""
portal_query = """select page_from.page_title as "prt_title",page_from.page_namespace as "prt_namespace"  from pagelinks
inner join page page_from on page_from.page_id = pagelinks.pl_from
where pagelinks.pl_from_namespace in (0,14) 
and pagelinks.pl_namespace in (100)
and  pagelinks.pl_title in (select page_title from page where page_id in (FROM_ID) and page_namespace = 100)"""

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            database = Database()
            try:
                to_page = pywikibot.Page(site, title=request.to_name, ns=request.to_namespace)
                if to_page.exists():
                    from_id = to_page.pageid
                    # template
                    if to_page.namespace() == 10:
                        database.query = template_query.replace("FROM_ID", str(from_id))
                        database.get_content_from_database()
                        gen = database.result
                    elif to_page.namespace() == 100:
                        database.query = portal_query.replace("FROM_ID", str(from_id))
                        database.get_content_from_database()
                        gen = database.result
                    elif to_page.namespace() == 14:
                        database.query = category_query.replace("FROM_ID", str(from_id))
                        database.get_content_from_database()
                        gen = database.result
            except Exception as e:
                # todo:add some code like log or alert send to wiki
                print(e)

            pages = []
            for row in gen:
                page_title = str(row['prt_title'], 'utf-8')
                pages.append(Page(
                    title=page_title,
                    namespace=row['prt_namespace']
                ))
            request.status = Status.RECEIVED
            request.pages = pages
            session.commit()

        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
