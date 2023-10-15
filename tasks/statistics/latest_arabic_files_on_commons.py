import pymysql
from pywikibot import config as _config

from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
"""
The query has only been updated. The original query was taken from Alaa (علاء)
w:ar:User:2023, علاء, https://quarry.wmcloud.org/query/34651
"""
query = """
SELECT
  page_title AS file,
  actor_name AS username
FROM page
INNER JOIN revision
  ON rev_page = page_id
  AND rev_timestamp > NOW() - INTERVAL 1 DAY
  AND rev_parent_id = 0
INNER JOIN actor
  ON actor_id = rev_actor
WHERE page_namespace = 6
  AND page_title REGEXP '[أ-ي]+'
  AND page_title NOT REGEXP 'پ|چ|ژ|ک|گ|ی|ۀ'
LIMIT 500;
"""
file_path = 'stub/latest_arabic_files_on_commons.txt'
page_name = f'ويكيبيديا:تقارير قاعدة البيانات/أحدث الملفات العربية على كومنز'
prefix = f'commonswiki'

connection = pymysql.connect(
    host=_config.db_hostname_format.format(prefix),
    read_default_file=_config.db_connect_file,
    db=_config.db_name_format.format(prefix),
    charset='utf8mb4',
    port=_config.db_port,
    cursorclass=pymysql.cursors.DictCursor,
)


def file_name(row, result, index):
    name = str(row['file'], 'utf-8')
    return f"[https://commons.wikimedia.org/wiki/File:{name} {name}]"


def file_image(row, result, index):
    name = str(row['file'], 'utf-8')
    return "[[ملف:" + name + "|150px]]"


def username_link(row, result, index):
    username = str(row['username'], 'utf-8').replace(" ", "_")
    return f"[https://commons.wikimedia.org/w/index.php?title=User:{username} {username}]"


columns = [
    ("الرقم", None, index),
    ("اسم الملف", None, file_name),
    ("الصورة الملف", None, file_image),
    ("اسم المستخدم", None, username_link)
]


def main() -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables, connection=connection)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
