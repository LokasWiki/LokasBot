import time

import pymysql
from pywikibot import config as _config
from tasks.statistics.module import UpdatePage, ArticleTables, index


def main(*args: str) -> int:
    # todo:add more languages like articles_not_found_by_number_of_language_links.py
    language = "en"
    # Set the parameters for the update
    """
    w:ar:User:Elph, 2023, https://quarry.wmcloud.org/query/6317
    """
    query = """SELECT  cl_to, COUNT(cl_from) as editcount
    FROM categorylinks
    WHERE cl_from IN (
            SELECT DISTINCT ll_from
            FROM langlinks
            WHERE ll_lang = "ar"
            )
        AND cl_to NOT IN (
            SELECT DISTINCT page_title
            FROM langlinks
            LEFT JOIN page ON page_id = ll_from
            WHERE ll_lang = "ar"
                AND page_namespace = 14
            )
         AND cl_to NOT IN
           (SELECT DISTINCT page_title FROM page
           WHERE page_title LIKE "%rticle%"
             OR  page_title LIKE "%ages%"
             OR  page_title LIKE "%All%"
             OR  page_title LIKE "%using%"
             OR  page_title LIKE "%Good"
             OR  page_title LIKE "%Wikipedia%"
             OR  page_title LIKE "%missing%"
             OR  page_title LIKE "%with%"
             OR  page_title LIKE "%anguage%"
             OR  page_title LIKE "%template%"
             OR  page_title LIKE "%box%"
             OR  page_title LIKE "%stub%"
             OR  page_title LIKE "%Use%"
             OR  page_title LIKE "%dmy%"
             OR  page_title LIKE "%ikidata%"
             OR  page_title LIKE "%CS1%"
             OR  page_title LIKE "%list%"
             OR  page_title LIKE "%image%"
             OR  page_title LIKE "%mdy%"
             OR  page_title LIKE "%TOC%"
             OR  page_title LIKE "%mdy%"
             OR  page_title LIKE "%ategory%"
             OR  page_title LIKE "%edirect%"
             OR  page_title LIKE "%Cite%"
             OR  page_title LIKE "%link%"
             OR  page_title LIKE "%need%"
             OR  page_title LIKE "%Engvar%"
             OR  page_title LIKE "%ommon%"
           )

    GROUP BY cl_to
    ORDER BY COUNT(cl_from) DESC
    LIMIT 500;"""
    file_path = 'stub/categories_not_found_by_number_of_language_links.txt'
    # page_name = f'ويكيبيديا:إحصاءات/المقالات غير الموجودة حسب عدد وصلات اللغات/{language}'
    page_name = f'ويكيبيديا:إحصاءات/التصانيف غير الموجودة'
    prefix = f'{language}wiki'

    # Get the current time and day of the week
    current_time = time.localtime()
    day_of_week = current_time.tm_wday

    # Check if it's Monday
    if day_of_week == 0:
        connection = pymysql.connect(
            host=_config.db_hostname_format.format(prefix),
            read_default_file=_config.db_connect_file,
            db=_config.db_name_format.format(prefix),
            charset='utf8mb4',
            port=_config.db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )
        # Create an instance of the ArticleTables class
        tables = ArticleTables()

        def page_title(row, result, index):
            cat_name = str(row['cl_to'], 'utf-8')
            name = cat_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
            return "[[:en:category:" + cat_name + "|" + name + "]]"

        columns = [
            ("الرقم", None, index),
            ("التصانيف غير الموجودة", None, page_title),
            ("عدد المقالات", "editcount"),
        ]

        tables.add_table("main_table", columns)

        # Create an instance of the updater and update the page
        updater = UpdatePage(query, file_path, page_name, tables, connection=connection)

        updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
