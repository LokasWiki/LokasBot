from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT
    DISTINCT page_title,el_index
FROM
    externallinks
        JOIN page ON el_from = page_id
WHERE
        el_index_60 LIKE 'mailto:%'
  AND page_namespace = 0
LIMIT
    1000;"""
file_path = 'stub/articles_containing_linked_email_addresses.txt'
page_name = "ويكيبيديا:إحصاءات/مقالات بها وصلات بريد إلكتروني"


def page_title(row, result, index):
    username = str(row['page_title'], 'utf-8')
    name = username
    return "[[" + username + "]]"


columns = [
    ("الرقم", None, index),
    ("المقالة", None, page_title),
    ("الرابط المقصود", "el_index"),
]

def main(*args: str) -> int:
    # Create an instance of the ArticleTables class
    tables = ArticleTables()
    tables.add_table("main_table", columns)

    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
