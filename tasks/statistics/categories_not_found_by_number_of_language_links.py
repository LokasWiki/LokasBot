import time

import pymysql
from pywikibot import config as _config

from tasks.statistics.module import UpdatePage, ArticleTables, index

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
      AND NOT (
    		   cl_to LIKE "%rticle%"
    		OR cl_to LIKE "%ages%"
    		OR cl_to LIKE "%All%"
    		OR cl_to LIKE "%using%"
    		OR cl_to LIKE "%Good"
    		OR cl_to LIKE "%Wikipedia%"
    		OR cl_to LIKE "%missing%"
    		OR cl_to LIKE "%with%"
    		OR cl_to LIKE "%anguage%"
    		OR cl_to LIKE "%template%"
    		OR cl_to LIKE "%box%"
    		OR cl_to LIKE "%stub%"
    		OR cl_to LIKE "%Use%"
    		OR cl_to LIKE "%dmy%"
    		OR cl_to LIKE "%ikidata%"
    		OR cl_to LIKE "%CS1%"
    		OR cl_to LIKE "%list%"
    		OR cl_to LIKE "%image%"
    		OR cl_to LIKE "%mdy%"
    		OR cl_to LIKE "%TOC%"
    		OR cl_to LIKE "%mdy%"
    		OR cl_to LIKE "%ategory%"
    		OR cl_to LIKE "%edirect%"
    		OR cl_to LIKE "%Cite%"
    		OR cl_to LIKE "%link%"
    		OR cl_to LIKE "%need%"
    		OR cl_to LIKE "%Engvar%"
    		OR cl_to LIKE "%ommon%"
    	)
  GROUP BY cl_to
  ORDER BY COUNT(cl_from) DESC
  LIMIT 500;"""
file_path = 'stub/categories_not_found_by_number_of_language_links.txt'
page_name = f'ويكيبيديا:تقارير قاعدة البيانات/التصانيف غير الموجودة'

# Get the current time and day of the week
current_time = time.localtime()
day_of_week = current_time.tm_wday


def page_title(row, result, index):
    cat_name = str(row['cl_to'], 'utf-8')
    name = cat_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[:en:category:" + cat_name + "|" + name + "]]"


columns = [
    ("الرقم", None, index),
    ("التصنيفات غير الموجودة", None, page_title),
    ("عدد المقالات", "editcount"),
]


def main(*args: str) -> int:

    # Check if it's Monday
    if day_of_week == 0:

        # Create an instance of the ArticleTables class
        tables = ArticleTables()

        tables.add_table("main_table", columns)

        language = "en"

        prefix = f'{language}wiki'

        connection = pymysql.connect(
            host=_config.db_hostname_format.format(prefix),
            read_default_file=_config.db_connect_file,
            db=_config.db_name_format.format(prefix),
            charset='utf8mb4',
            port=_config.db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )

        # Create an instance of the updater and update the page
        updater = UpdatePage(query, file_path, page_name, tables, connection=connection)

        updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
