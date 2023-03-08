import sys

from core.utils.sqlite import create_database_table, maintenance_db_name, save_pages_to_db
from tasks.maintenance.module import get_pages
import traceback


def main(*args: str) -> int:
    # todo: mereg with read.py in webcite task
    try:
        thread_number = 1
        time_before_start = 1
        # https://quarry.wmcloud.org/query/72148 @ASammour
        custom_query = """SELECT page_title AS "pl_2_title",(select count(distinct pl_from) 
                from pagelinks 
                where pl_from_namespace = 0 
                and pl_title in (
                       select page_title from redirect inner join page on rd_from = page_id where page_namespace = 0 and rd_title = p.page_title
                and rd_namespace = 0)
                and pl_namespace = 0
                and pl_from in (select page_id
                                from page
                                where page_id = pl_from
                                and page_namespace = 0
                                and page_is_redirect = 0)
                and pl_from not in (select (pl_from)
                from pagelinks 
                where pl_from_namespace = 0 
                and pl_title = page_title
                and pl_namespace = 0
                and pl_from in (select page_id
                                from page
                                where page_id = pl_from
                                and page_namespace = 0
                                and page_is_redirect = 0))
               and pl_from <> page_id   
               )
				+
				(select count(distinct pl_from)
                from pagelinks 
                where pl_from_namespace = 0 
                and pl_title = page_title
                and pl_namespace = 0
                and pl_from in (select page_id
                                from page
                                where page_id = pl_from
                                and page_namespace = 0
                                and page_is_redirect = 0)
                 and pl_from <> page_id 
               )
               as counts
FROM page p
where page_namespace = 0
and page_is_redirect = 0
and page_id  in (select cl_from from categorylinks where cl_to like "%جميع_المقالات_اليتيمة%" and cl_from = page_id)
and page_id not in (select cl_from from categorylinks where cl_to like "%صفحات_توضيح%" and cl_from = page_id)
having counts >= 3;"""
        pages = get_pages(time_before_start,custom_query=custom_query)
        conn, cursor = create_database_table(maintenance_db_name)
        save_pages_to_db(pages, conn, cursor, thread_number=thread_number)
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        just_the_string = traceback.format_exc()
        print(just_the_string)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
