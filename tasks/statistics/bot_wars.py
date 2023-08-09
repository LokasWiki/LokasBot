import pywikibot

from tasks.statistics.module import UpdatePage, ArticleTables, index

site = pywikibot.Site()

# Set the parameters for the update
query = """SELECT
  article.page_title,
  article.page_namespace,
  count(distinct actor.actor_name) as "bot_users",
  GROUP_CONCAT(DISTINCT actor.actor_name)  as "bot_users_named",
  TIMESTAMP(max(rev_timestamp))  as "last_edit_on_page",
  COUNT(*) AS edits
FROM revision
INNER JOIN page article ON  article.page_id = rev_page  #AND article.page_namespace = 0
INNER JOIN  actor ON actor_id = rev_actor
WHERE 
	rev_timestamp > DATE_SUB(NOW(), INTERVAL 2 day)
            AND actor_name IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'bot')
GROUP BY article.page_id
having count(*) > 10
ORDER BY edits DESC;
  """
file_path = 'stub/bot_wars.txt'
page_name = "مستخدم:LokasBot/حروب البوت"


def page_name_with_namespace(row, result, index):
    namespace = "{{ns:" + str(row['page_namespace']) + "}}"
    temp_title = str(row['page_title'], 'utf-8')
    return f"[[{namespace}:{temp_title}]]"


columns = [
    ("الرقم", None, index),
    ("اسم الصفحة", None, page_name_with_namespace),
    ("عدد البوتات", None, lambda row, result, index: row['bot_users']),
    ("اسماء البوتات", None, lambda row, result, index: str(row['bot_users_named'], 'utf-8')),
    ("اخر تعديل", None, lambda row, result, index: row['last_edit_on_page']),
    ("عدد التعديلات", None, lambda row, result, index: row['edits']),
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
