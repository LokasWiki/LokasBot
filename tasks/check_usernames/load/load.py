import os
import datetime
from core.utils.file import File
from core.utils.wikidb import Database

import pywikibot

import antispam


class Load:
    def __init__(self, content_text, ai_model, names, page_title, site):
        self.stub_content = content_text
        self.ai_model = ai_model
        self.list_of_names = names
        self.page_title = page_title
        self.site = site
        self.username_bot = self.site.username()
        self.page = None
        self.text = ""

    def load_page(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        return self

    def build_table(self):

        # start create page
        table_body = ""

        num = 1

        for user_name in self.list_of_names:

            try:
                msg1 = user_name.strip().lower().replace(" ", "_")

                if self.ai_model.score(msg1) >= 0.6 or len(msg1) >= 20 or len(msg1) <= 2:
                    table_body += """|{0}||{2}||{1}||لا||\n|-
                  """.format(num, "{{مس|" + user_name + "}}", str(self.ai_model.score(msg1)))
                    num += 1
            except:
                table_body += """|{0}||{2}||{1}||لا||\n|-
                      """.format(num, "{{مس|" + user_name + "}}", "غير معروف")
                num += 1

        # start add data to text stub
        self.text = self.stub_content.replace("BOT_TABLE_BODY", table_body).replace(
            'BOT_USER_NAME', f"[[مستخدم:{self.username_bot}|{self.username_bot}]]"
        ).replace(
            "BOT_TIME_NOW", "{{نسخ:#time:H:i، j F Y}}"
        )
        return self

    def save_page(self):
        # start save page
        self.page.text = self.text
        self.page.save("بوت:تحديث")
        return self


script_dir = os.path.dirname(__file__)

# text stub
file = File(script_dir=script_dir)
file_path = 'stub/load.txt'
file.set_stub_path(file_path)
file.get_file_content()
content = file.contents

# model file
model = File(script_dir=script_dir)
model_path = 'ai/models/v1/my_model.dat'
model.set_stub_path(model_path)

ai_model = antispam.Detector(model.file_path)

# database users list
db = Database()
# Get yesterday's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# Get start time for yesterday
start_time = datetime.datetime.combine(yesterday, datetime.time.min)

# Get last time for yesterday
last_time = datetime.datetime.combine(yesterday, datetime.time.max)

# Format dates for SQL query
start_time_sql = start_time.strftime("%Y%m%d%H%M%S")
last_time_sql = last_time.strftime("%Y%m%d%H%M%S")

db.query = """select logging.log_title as "q_log_title" from logging
inner join user on user.user_name = logging.log_title
where log_type in ("newusers")
and log_timestamp BETWEEN {} AND {}
and user.user_id NOT IN (SELECT ipb_user FROM ipblocks)""".format(start_time_sql,last_time_sql)
db.get_content_from_database()
names = []
for row in db.result:
    name = str(row['q_log_title'], 'utf-8')
    names.append(name)

page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"
# page_title = "مستخدم:لوقا/ملعب 20"

site = pywikibot.Site()

load_obj = Load(content_text=content, ai_model=ai_model, names=names, page_title=page_title, site=site)
load_obj.load_page().build_table().save_page()
