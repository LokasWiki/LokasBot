import os

import self as self

from core.utils.file import File
from core.utils.wikidb import Database

import pywikibot

import antispam

# text stub
file = File()
file_path = 'stub/load.txt'
file.set_stub_path(file_path)
file.get_file_content()
content = file.contents

# model file
model = File()
model_path = 'ai/models/v1/my_model.dat'
model.set_stub_path(model_path)

d = antispam.Detector(model.file_path)


# database users list
db = Database()
db.query = """select logging.log_title as "q_log_title" from logging
inner join user on user.user_name = logging.log_title
where log_type in ("newusers")
and log_timestamp > DATE_SUB(NOW(), INTERVAL 30 day)
and user.user_id NOT IN (SELECT ipb_user FROM ipblocks)"""
db.get_content_from_database()
names = []
for row in db.result:
    name = str(row['q_log_title'], 'utf-8')
    names.append(name)


page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"

site = pywikibot.Site()
page = pywikibot.Page(site, page_title)


# start create page
table_body = ""

num = 1

for name in names:

   try:
       msg1 = name.strip().lower().replace(" ", "_")

       if d.score(msg1) >= 0.6:
           table_body += """|{0}||{2}||{1}||لا||\n|-
          """.format(num, "{{مس|" + name + "}}", str(d.score(msg1)))
           num += 1
   except:
       table_body += """|{0}||{2}||{1}||لا||\n|-
              """.format(num, "{{مس|" + name + "}}", "غير معروف")
       num += 1

# start add data to text stub
username_bot = site.username()
content = content.replace("BOT_TABLE_BODY", table_body).replace(
    'BOT_USER_NAME', f"[[مستخدم:{username_bot}|{username_bot}]]"
).replace(
    "BOT_TIME_NOW", "{{نسخ:#time:H:i، j F Y}}"
)

# start save page
page.text = content

page.save("بوت:تحديث")
