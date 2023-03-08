import pymysql
from pywikibot import config as _config
from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT page_title, count(*) as editcount
FROM langlinks JOIN page on ll_from = page_id
WHERE page_namespace = 0 AND page_is_redirect = 0
AND NOT EXISTS (
    SELECT * FROM langlinks as t
    WHERE t.ll_lang='ar' and t.ll_from = langlinks.ll_from)
GROUP BY ll_from
ORDER BY count(*) DESC
LIMIT 1000;"""


def main(*args: str) -> int:
    languages = ['en', 'fr', 'de', 'es', 'fa', 'he', 'pt', 'tr']
    for language in languages:
        file_path = 'stub/articles_not_found_by_number_of_language_links.txt'
        page_name = f'ويكيبيديا:إحصاءات/المقالات غير الموجودة حسب عدد وصلات اللغات/{language}'
        prefix = f'{language}wiki'

        connection = pymysql.connect(
            host=_config.db_hostname_format.format(prefix),
            read_default_file=_config.db_connect_file,
            db=_config.db_name_format.format(prefix),
            charset='utf8mb4',
            port=_config.db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )

        # todo: edit this to make it outside main def
        def page_title(row, result, index):
            username = str(row['page_title'], 'utf-8')
            name = username
            return "[[:" + language + ":" + username + "|" + name + "]]"

        columns = [
            ("الرقم", None, index),
            ("المقالة", None, page_title),
            ("عدد وصلات اللغات", "editcount"),
        ]

        # Create an instance of the ArticleTables class
        tables = ArticleTables()

        tables.add_table("main_table", columns)

        # Create an instance of the updater and update the page
        updater = UpdatePage(query, file_path, page_name, tables, connection=connection)
        updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
