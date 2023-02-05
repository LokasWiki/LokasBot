from database import Query, WikiDatabase

db = Query()

type_of_request = 1

template_query = """select p1.page_id,p1.page_title from pagelinks
            inner join page on page.page_title = pagelinks.pl_title 
            where pl_from in (FROM_ID)  and pl_namespace = 0  and pl_from_namespace= 10 and page.page_namespace = 0
            AND (p1.page_id, p1.page_title) NOT IN (
              select p1.page_id,p1.page_title from pagelinks 
              inner join page p1 on p1.page_id = pagelinks.pl_from 
              where pl_from_namespace = 0 and pl_namespace = 100 and pl_title in (select page_title from page where page_id in (TO_ID))
            )"""

category_query = """select  p1.page_id,p1.page_title from categorylinks 
        inner join page p1 on p1.page_id = categorylinks.cl_from
        where cl_to in (select page_title from page where page_id in (FROM_ID)) and cl_type in ("page") and p1.page_namespace = 0
        AND (p1.page_id, p1.page_title) NOT IN (
          select p1.page_id,p1.page_title from pagelinks 
          inner join page p1 on p1.page_id = pagelinks.pl_from 
          where pl_from_namespace = 0 and pl_namespace = 100 and pl_title in (select page_title from page where page_id in (TO_ID))
        )"""

portal_query = """select p1.page_id,p1.page_title from pagelinks 
            inner join page p1 on p1.page_id = pagelinks.pl_from 
            where pl_from_namespace = 0 and pl_namespace = 100 and pl_title in (select page_title from page where page_id in (FROM_ID))
            AND (p1.page_id, p1.page_title) NOT IN (
              select p1.page_id,p1.page_title from pagelinks 
              inner join page p1 on p1.page_id = pagelinks.pl_from 
              where pl_from_namespace = 0 and pl_namespace = 100 and pl_title in (select page_title from page where page_id in (TO_ID))
            )
            """
requests = db.get_new_requests(5, type_of_request)

for request in requests:
    wikidatabase = WikiDatabase()
    if request['from_namespace'] == 10:
        wikidatabase.query = template_query.replace("FROM_ID", str(request['from_id'])).replace("TO_ID", str(request['to_id']))
    elif request['from_namespace'] == 14:
        wikidatabase.query = category_query.replace("FROM_ID", str(request['from_id'])).replace("TO_ID", str(request['to_id']))
    elif request['from_namespace'] == 100:
        wikidatabase.query = portal_query.replace("FROM_ID", str(request['from_id'])).replace("TO_ID", str(request['to_id']))
    wikidatabase.get_content_from_database()
    for row in wikidatabase.result:
        print(row)
    db.update_request_status(request['id'],1)