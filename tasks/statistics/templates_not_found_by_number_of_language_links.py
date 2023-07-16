import pymysql
from pywikibot import config as _config

from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """
select page_title, count(ll_lang) as editcount  from langlinks
inner join page on page.page_id = langlinks.ll_from
where page.page_namespace = 10
AND NOT EXISTS (
    SELECT * FROM langlinks as t
    WHERE t.ll_lang='ar' and t.ll_from = langlinks.ll_from
)    
GROUP BY ll_from
ORDER BY count(ll_lang) DESC
LIMIT 1000;
"""


# todo: edit this to make it outside main def
def en_template_name(row, result, index):
    name = str(row['page_title'], 'utf-8')
    language = 'en'
    return "[[:" + language + ":Template:" + name + "|" + name + "]]"


def ar_template_name(row, result, index):
    name = str(row['page_title'], 'utf-8')
    language = 'ar'
    return "[[:" + language + ":قالب:" + name + "|" + name + "]]"


def main(*args: str) -> int:
    languages = ['en']
    for language in languages:
        file_path = 'stub/templates_not_found_by_number_of_language_links.txt'
        page_name = f'ويكيبيديا:إحصاءات/القوالب غير الموجودة حسب عدد وصلات اللغات/{language}'
        prefix = f'{language}wiki'

        connection = pymysql.connect(
            host=_config.db_hostname_format.format(prefix),
            read_default_file=_config.db_connect_file,
            db=_config.db_name_format.format(prefix),
            charset='utf8mb4',
            port=_config.db_port,
            cursorclass=pymysql.cursors.DictCursor,
        )

        columns = [
            ("الرقم", None, index),
            ("القالب بالإنجليزية", None, en_template_name),
            ("القالب بالعربية", None, ar_template_name),
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
