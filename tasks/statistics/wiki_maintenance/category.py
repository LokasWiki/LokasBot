
import pymysql
from pywikibot import config as _config

from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """select
comment.comment_text  as "deleted_page",
revision.rev_timestamp as "date_of_delete",
wb_items_per_site.ips_site_page   as "name_of_page"

from revision

join page on page.page_id = revision.rev_page
join comment on comment.comment_id = revision.rev_comment_id
join wb_items_per_site on wb_items_per_site.ips_item_id=REPLACE(page.page_title,"Q","")

where comment.comment_text like "%clientsitelink-remove%" and comment.comment_text like "%enwiki%"
and rev_timestamp > (NOW() - INTERVAL 1 MONTH)
and wb_items_per_site.ips_site_id like "arwiki"
and comment.comment_text like '%Category%'
"""

connection = pymysql.connect(
    host=_config.db_hostname_format.format("wikidatawiki"),
    read_default_file=_config.db_connect_file,
    db=_config.db_name_format.format("wikidatawiki"),
    charset='utf8mb4',
    port="4712",
    cursorclass=pymysql.cursors.DictCursor,
)

file_path = 'stub/wiki_maintenance/category.txt'
page_name = "مستخدم:فيصل/تصانيف"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def delete_page(row, result, index):
    page_title = str(row['deleted_page'], 'utf-8')
    return "[[:en:" + page_title.rsplit("*/", 1)[-1] + "|"+page_title.rsplit("*/", 1)[-1]+"]]"


def ar_page(row, result, index):
    page_title = str(row['name_of_page'], 'utf-8')
    return "[[:" + page_title + "]]"


def date_of_delete(row, result, index):
    date_delete = str(row['date_of_delete'], 'utf-8')
    return "{{نسخ:#time:G:i، j F Y|" + date_delete + "}}"


columns = [
    ("الرقم", None, index),
    ("التصنيف المحذوفه", None, delete_page),
    ("التصنيف العربي", None, ar_page),
    ("حذف بتاريخ", None, date_of_delete),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables, connection=connection)
updater.update()
