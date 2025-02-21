import pywikibot
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils.wikidb import Database
from tasks.requests.core.database.engine import engine
from tasks.requests.core.database.models import Request, Status, Page

# Create an instance of the RequestsPage class
site = pywikibot.Site()

type_of_request = 5

template_query = """select p1.page_id,p1.page_title as "prt_title" from pagelinks
inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
inner join page on page.page_title = linktarget.lt_title
where pl_from in (FROM_ID)  and lt_namespace = 0  and pl_from_namespace= 10 and page.page_namespace = 0
AND (p1.page_id, p1.page_title) NOT IN (
	select p1.page_id,p1.page_title from pagelinks
  	inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
    inner join page p1 on p1.page_id = pagelinks.pl_from
    where pl_from_namespace = 0 and lt_namespace = 100 and lt_title in (select page_title from page where page_id in (TO_ID))
)"""

category_query = """select  p1.page_id,p1.page_title  as "prt_title" from categorylinks
        inner join page p1 on p1.page_id = categorylinks.cl_from
        where cl_to in (select page_title from page where page_id in (FROM_ID)) and cl_type in ("page") and p1.page_namespace = 0
        AND (p1.page_id, p1.page_title) NOT IN (
          select p1.page_id,p1.page_title from pagelinks
          inner join page p1 on p1.page_id = pagelinks.pl_from
          inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
          where pl_from_namespace = 0 and lt_namespace = 100 and lt_title in (select page_title from page where page_id in (TO_ID))
        )"""

portal_query = """select p1.page_id,p1.page_title  as "prt_title" from pagelinks
            inner join page p1 on p1.page_id = pagelinks.pl_from
            inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
            where pl_from_namespace = 0 and lt_namespace = 100 and lt_title in (select page_title from page where page_id in (FROM_ID))
            AND (p1.page_id, p1.page_title) NOT IN (
              select p1.page_id,p1.page_title from pagelinks
              inner join page p1 on p1.page_id = pagelinks.pl_from
              inner join linktarget ON linktarget.lt_id = pagelinks.pl_target_id
              where pl_from_namespace = 0 and lt_namespace = 100 and lt_title in (select page_title from page where page_id in (TO_ID))
            )
            """

try:
    session = Session(engine)

    stmt = select(Request).filter(Request.status == Status.PENDING, Request.request_type == type_of_request).limit(20)

    for request in session.scalars(stmt):
        try:
            gen = []
            pages = []
            database = Database()
            from_page = pywikibot.Page(site, title=request.from_name)
            to_page = pywikibot.Page(site, title=request.to_name)
            if from_page.exists() and to_page.exists():
                from_id = from_page.pageid
                to_id = to_page.pageid
                # template
                if request.from_namespace == 10:
                    database.query = template_query.replace("FROM_ID", str(from_id)).replace("TO_ID", str(to_id))
                    database.get_content_from_database()
                    gen = database.result
                # category
                elif request.from_namespace == 14:
                    database.query = category_query.replace("FROM_ID", str(from_id)).replace("TO_ID", str(to_id))
                    database.get_content_from_database()
                    gen = database.result
                # portal
                elif request.from_namespace == 100:
                    database.query = portal_query.replace("FROM_ID", str(from_id)).replace("TO_ID", str(to_id))
                    database.get_content_from_database()
                    gen = database.result
                elif request.from_namespace == 0:
                    pages.append(Page(
                        title=request.from_name,
                        namespace=0
                    ))

            for row in gen:
                page_title = str(row['prt_title'], 'utf-8')
                pages.append(Page(
                    title=page_title,
                    namespace=0
                ))
            request.status = Status.RECEIVED
            request.pages = pages
            session.commit()

        except Exception as e:
            session.rollback()
            print("An error occurred while committing the changes:", e)
except Exception as e:
    print(f"An error occurred: {e}")
