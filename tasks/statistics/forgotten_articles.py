from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT DATE_FORMAT(MAX(rev_timestamp),'%Y-%m-%d %H:%i:%s') AS lastedit, COUNT(rev_id) AS editcount, page_title
FROM revision,
     (SELECT rev_timestamp as lastedit, page_id, page_title
      FROM page,
           revision
      WHERE page_title NOT IN (SELECT page_title FROM page WHERE page_title LIKE '%توضيح%')
        AND page_id IN (SELECT page_id FROM page WHERE page_namespace = 0 AND page_is_redirect = 0)
        AND rev_id = page_latest
      ORDER BY lastedit ASC
      LIMIT 1000) as InnerQuery
WHERE rev_page = page_id
  AND lastedit < DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 2 YEAR), '%Y%m%d%H%i%s')
GROUP BY InnerQuery.page_id, InnerQuery.page_title
ORDER BY lastedit ASC, editcount ASC;"""
file_path = 'stub/forgotten_articles.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/مقالات منسية"


def page_title(row, result, index):
    user_name = str(row['page_title'], 'utf-8')
    return "[[" + user_name + "]]"


def lastedit(row, result, index):
    return row['lastedit']


columns = [
    ("الرقم", None, index),
    ("المقالة", None, page_title),
    ("عدد التعديلات", "editcount"),
    ("آخر تعديل", None, lastedit),
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
