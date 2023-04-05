from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update

query = """
SELECT
  article.page_title as "q_page_title",
  actor.actor_name as "q_user_name",
  article.page_len as "page_size"
FROM revision
# user
join actor on actor_id = rev_actor
# page
JOIN page article ON  article.page_id = rev_page AND article.page_namespace = 2
# externallinks
JOIN externallinks ON(page_id=el_from)
WHERE rev_parent_id = 0
AND revision.rev_timestamp > DATE_SUB(NOW(),INTERVAL 1 DAY)
AND article.page_title LIKE "%/ملعب%"
GROUP BY article.page_id
ORDER BY MIN(revision.rev_id) DESC;
"""
file_path = 'stub/latest_arabic_files_on_commons.txt'
page_name = f'مستخدم:لوقا/ملاعب مستخدمين تحتاج لمراجعة'


def page_sandbox_name(row, result, index):
    name = str(row['q_page_title'], 'utf-8')
    return f"[[مستخدم:{name}]]"


def page_size(row, result, index):
    name = row['page_size']
    return f"{name}"


columns = [
    ("الرقم", None, index),
    ("الملعب", None, page_sandbox_name),
    ("الحجم", None, page_size),
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
