from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT page_namespace,
                    page_title,
                    SUM( page_len ) / 1024 / 1024 AS total_size
                    FROM page
                    WHERE page_namespace MOD 2 = 1
                    GROUP BY page_namespace, page_title
                    ORDER BY total_size DESC
                    LIMIT 1000"""
file_path = 'stub/featured_articles_by_size.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/صفحات النقاش مرتبة حسب الحجم"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


columns = [
    ("الرقم", None, index),
    ("الاسم", None, page_name_with_namespace),
    ("النطاق", 'page_namespace'),
    ("الحجم (بالميجابايت)", 'total_size')
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
