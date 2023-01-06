from module import UpdatePage, ArticleTables,index

# Set the parameters for the update
query = """SELECT DISTINCT(actor_name) ll_actor_name, concat(ug_group) AS user_groups,
               (SELECT MAX(rev_timestamp) FROM revision WHERE rev_actor = actor_id) AS last_edit_date
FROM actor_revision
         JOIN user_groups ON actor_user = ug_user
         JOIN user ON actor_user = user.user_id
         LEFT JOIN ipblocks ON actor_user = ipb_user
WHERE ug_group IN ('editor', 'autoreview', 'uploader')
  AND ipb_user IS NULL
  AND actor_id NOT IN (
    SELECT rev_actor
    FROM revision
    WHERE rev_timestamp > DATE_SUB(NOW(), INTERVAL 1 YEAR)
)
GROUP BY actor_name, user_groups"""
file_path = 'stub/inactive_users.txt'
page_name = "ويكيبيديا:إحصاءات/المستخدمين غير النشطين"

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
    ("تاريخ اخر مساهمة", None, user_registration),
    ("الصلاحية", None, user_groups),
]

tables.add_table("main_table", columns)

# Create an instance of the updater and update the page
updater = UpdatePage(query, file_path, page_name, tables)
updater.update()

#
# import pywikibot
# import pymysql
# from pywikibot import config as _config
# import os
#
# # Get the directory of the script
# script_dir = os.path.dirname(__file__)
#
# # Construct the file path
# file_path = os.path.join(script_dir, 'stub/inactive_users.txt')
#
# page_name = "ويكيبيديا:إحصاءات/المستخدمين غير النشطين"
# # page_name = "مستخدم:لوقا/قائمة الويكيبيديين بلا صلاحيات"
# summary = "تحديث (beta)"
#
# # Connect to the database
# connection = pymysql.connect(host=_config.db_hostname_format.format("arwiki"),
#                              read_default_file=_config.db_connect_file,
#                              db=_config.db_name_format.format("arwiki"),
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#
# try:
#     # Create a cursor object
#     with connection.cursor() as cursor:
#         # Construct the SELECT statement
#         sql = """SELECT DISTINCT(actor_name) ll_actor_name, concat(ug_group) AS user_groups,
#                (SELECT MAX(rev_timestamp) FROM revision WHERE rev_actor = actor_id) AS last_edit_date
# FROM actor_revision
#          JOIN user_groups ON actor_user = ug_user
#          JOIN user ON actor_user = user.user_id
#          LEFT JOIN ipblocks ON actor_user = ipb_user
# WHERE ug_group IN ('editor', 'autoreview', 'uploader')
#   AND ipb_user IS NULL
#   AND actor_id NOT IN (
#     SELECT rev_actor
#     FROM revision
#     WHERE rev_timestamp > DATE_SUB(NOW(), INTERVAL 1 YEAR)
# )
# GROUP BY actor_name, user_groups"""
#
#         # Execute the SELECT statement
#         cursor.execute(sql)
#
#         # Fetch all the rows of the result
#         result = cursor.fetchall()
#
#         # Open the file in read mode
#         with open(file_path, 'r') as file:
#             # Read the contents of the file
#             contents = file.read()
#
#         user_temp = ''
#         # Build the rows
#         for index, row in enumerate(result):
#             username = str(row['ll_actor_name'], 'utf-8')
#             user_groups = str(row['user_groups'], 'utf-8').replace("autoreview","مراجع تلقائي").replace("editor","محرر").replace("uploader","رافع ملفات")
#             name = username.replace("__", "[LOKA]").replace("_", " ").replace("[LOKA]", "_")
#             last_edit_date = str(row['last_edit_date'],'utf-8')
#             user_temp += "\n"
#             user_temp += f'|bgcolor="#808080"|{index + 1}||bgcolor="#D3D3D3"|[[مستخدم:{username}|{name}]]||bgcolor="#DCDCDC"|{user_groups}||bgcolor="#DCDCDC"|'
#             user_temp += "{{نسخ:#time:j F Y|"+last_edit_date+"}}"
#             user_temp += "\n"
#             if index != len(result) - 1:
#                 user_temp += '|-'
#                 user_temp += "\n"
#
#         # Connect to the site
#         site = pywikibot.Site()
#
#         # Get a Page object for the page
#         page = pywikibot.Page(site, page_name)
#
#         # Get the username of the bot account
#         username_bot = site.username()
#
#         # Set the text of the page
#         page.text = contents.replace('BOT_USER_NAME', "[[مستخدم:" + username_bot + "|" + username_bot + "]]").replace("BOT_TIME_NOW",
#                                                                             "{{نسخ:#time:H:i، j F Y}}").replace(
#             "BOT_TABLE_BODY", user_temp)
#
#         # Save the page
#         page.save(summary=summary)
#
# finally:
#     # Close the connection
#     connection.close()
