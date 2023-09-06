from tasks.statistics.module import UpdatePage, ArticleTables, index

# Set the parameters for the update
query = """SELECT
  actor_name AS name,
  count(logging.log_id) as score
FROM logging
INNER JOIN actor ON log_actor = actor.actor_id
and log_type = "review" and  log_action in ('approve','approve-ia','approve-a','approve2-i','approve-i','approve2','unapprove','unapprove2')
#and log_namespace = 0
and ucase(actor_name) not like ucase("%BOT") COLLATE utf8mb4_general_ci
  and actor_name not like "%بوت%" collate utf8mb4_general_ci
  and actor_name Not IN (SELECT user_name
                         FROM user_groups
                                  INNER JOIN user ON user_id = ug_user
                         WHERE ug_group = "bot")
  and actor_id NOT IN ("2579643")
  and actor_user not in (137877)

GROUP BY actor_name
ORDER BY score desc,actor_name
limit 100"""
file_path = 'stub/list_of_wikipedians_by_number_of_revision_edits.txt'
page_name = "ويكيبيديا:تقارير قاعدة البيانات/قائمة الويكيبيديين حسب عدد مراجعة التعديلات"


def username(row, result, index):
    user_name = str(row['name'], 'utf-8')
    name = user_name.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + user_name + "|" + name + "]]"


def total_edits(row, result, index):
    user_name = str(row['name'], 'utf-8')
    number = format(row['score'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + user_name + "|" + number + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("عدد المراجعات", None, total_edits),
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
