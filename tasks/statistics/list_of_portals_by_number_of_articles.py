from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT main.page_title as portal_name, COUNT(*) - 1 as sub_page_count,
    (SELECT COUNT(*) FROM pagelinks WHERE pl_title = main.page_title and pl_from_namespace = 0 and pl_namespace = 100) as links_count
FROM page AS p
INNER JOIN (
    SELECT page_title
    FROM page
    WHERE page_namespace = 100
    AND page_is_redirect = 0
)AS main ON main.page_title = SUBSTRING_INDEX(p.page_title, '/', 1)
WHERE p.page_namespace = 100
GROUP BY portal_name
ORDER BY links_count DESC;
"""
file_path = 'stub/list_of_portals_by_number_of_articles.txt'
page_name = "ويكيبيديا:إحصاءات/قائمة البوابات حسب عدد المقالات"


# Create an instance of the ArticleTables class
tables = ArticleTables()


def portal_name(row, result,index):
    username = str(row['portal_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[بوابة:" + username + "|" + name + "]]"

def sub_page_count(row, result,index):
    return  format(row['sub_page_count'], ',').replace(',', '٬')

def links_count(row, result,index):
    return  format(row['links_count'], ',').replace(',', '٬')


columns = [
    ("الرقم", None, index),
    ("اسم البوابة", None, portal_name),
    ("عدد الصفحات الفرعية",None, sub_page_count),
    ("عدد المقالات",None, links_count),
]

tables.add_table("main_table", columns)

def main(*args: str) -> int:
    # Create an instance of the updater and update the page
    updater = UpdatePage(query, file_path, page_name, tables)
    updater.update()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
