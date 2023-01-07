from module import UpdatePage, ArticleTables,index

# Set the parameters for the update
query = """SELECT DISTINCT(actor_name) ll_actor_name, concat(ug_group) AS user_groups,
               (SELECT MAX(rev_timestamp) FROM revision WHERE rev_actor = actor_id) AS last_edit_date
FROM actor_revision
         JOIN user_groups ON actor_user = ug_user
         JOIN user ON actor_user = user.user_id
         LEFT JOIN ipblocks ON actor_user = ipb_user
WHERE ug_group IN ('bot')
  AND ipb_user IS NULL
  AND actor_id NOT IN (
    SELECT rev_actor
    FROM revision
    WHERE rev_timestamp > DATE_SUB(NOW(), INTERVAL 1 YEAR)
)
GROUP BY actor_name, user_groups"""
file_path = 'stub/inactive_bots.txt'
page_name = "ويكيبيديا:إحصاءات/بوتات غير نشطة"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def username(row, result,index):
    username = str(row['ll_actor_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + username + "|" + name + "]]"

def user_groups(row, result,index):
    return str(row['user_groups'], 'utf-8').replace("autoreview","مراجع تلقائي").replace("editor","محرر").replace("uploader","رافع ملفات")

def user_registration(row, result,index):
    last_edit_date = str(row['last_edit_date'], 'utf-8')
    return "{{نسخ:#time:j F Y|"+last_edit_date+"}}"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("تاريخ آخر مساهمة", None, user_registration),
    ("الصلاحية", None, user_groups),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()

