from module import UpdatePage, ArticleTables,index

# Set the parameters for the update
query = """SELECT actor_name AS user_name, date(user_registration) AS user_registration,
        user_editcount AS total_edits,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_deleted = 0) AS live_edits,
       (SELECT COUNT(*) FROM revision WHERE rev_actor = actor_id AND rev_timestamp > DATE_SUB(NOW(), INTERVAL 1 MONTH)) AS edits_last_month
FROM actor
         join user on actor_user = user_id
         LEFT JOIN ipblocks ON actor_user = ipb_user
         LEFT JOIN user_groups ON actor_user = ug_user
WHERE ipb_user IS NULL AND ug_user IS NULL 
and actor_name not in ("JarBot","جار_الله","صالح","وسام","جار الله","FShbib","بندر","حساب ملغى 123321","مصعب العبود")
HAVING live_edits >= 400
       AND edits_last_month >= 10;"""
file_path = 'stub/wikipedians_without_permission.txt'
page_name = "ويكيبيديا:قائمة الويكيبيديين بلا صلاحيات"

# Create an instance of the ArticleTables class
tables = ArticleTables()


def username(row, result,index):
    username = str(row['user_name'], 'utf-8')
    name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
    return "[[مستخدم:" + username + "|" + name + "]]"


def user_registration(row, result,index):
    return row['user_registration']


def live_edits(row, result,index):
    username = str(row['user_name'], 'utf-8')
    number = format(row['live_edits'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + username + "|" + number + "]]"


def total_edits(row, result,index):
    username = str(row['user_name'], 'utf-8')
    number = format(row['total_edits'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + username + "|" + number + "]]"


def edits_last_month(row, result,index):
    username = str(row['user_name'], 'utf-8')
    number = format(row['edits_last_month'], ',').replace(',', '٬')
    return "[[خاص:مساهمات/" + username + "|" + number + "]]"


columns = [
    ("الرقم", None, index),
    ("المستخدم", None, username),
    ("تاريخ التسجيل", None, user_registration),
    ("عدد المساهمات", None, live_edits),
    ("عدد المساهمات الحية", None, total_edits),
    ("عدد المساهمات خلال 30 يوم", None, edits_last_month),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()
