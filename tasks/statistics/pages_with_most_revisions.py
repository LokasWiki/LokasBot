from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT COUNT(*) AS revisions, rev_page, p.page_namespace, p.page_title FROM revision r
                   LEFT JOIN ( SELECT page_id, page_title, page_namespace FROM page ) p ON r.rev_page = p.page_id
                   GROUP BY rev_page
                   ORDER BY revisions DESC
                   LIMIT 1000"""
file_path = 'stub/pages_with_most_revisions.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/الصفحات التي تحتوي على أكبر عدد من المراجعات"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


columns = [
    ("الرقم", None, index),
    ("الاسم", None, page_name_with_namespace),
    ("النطاق", 'page_namespace'),
    ("عدد المراجعات", 'revisions')
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
