import os
import datetime
from datetime import timedelta

import pywikibot
from pywikibot import Timestamp
import wikitextparser as wtp
import antispam

from core.utils.file import File
from core.utils.wikidb import Database


class Load:
    def __init__(self, content_text, ai_model, names, page_title, site, users=None):
        if users is None:
            users = []
        self.stub_content = content_text
        self.ai_model = ai_model
        self.list_of_names = names
        self.page_title = page_title
        self.site = site
        self.username_bot = self.site.username()
        self.page = None
        self.text = ""
        self.users = users

    def load_page(self):
        self.page = pywikibot.Page(self.site, self.page_title)
        return self

    def build_table(self):

        # start create page
        table_body = ""

        num = 1
        # add old users if found
        for user in self.users:
            table_body += """|{0}||{1}||{2}||{3}||\n|-
                                      """.format(num, user[1], user[2], user[3], user[4])
            num += 1

        for user_name in self.list_of_names:

            try:
                msg1 = user_name.strip().lower().replace(" ", "_")

                if self.ai_model.score(msg1) >= 0.9 or len(msg1) >= 20 or len(msg1) <= 2:
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


class LastCheck:
    def __init__(self, site):
        self.users = []
        self.site = site

    def check(self):
        status = False
        page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص/تشغيل البوت"
        page = pywikibot.Page(self.site, page_title)
        if page.exists():
            edit_time = page.latest_revision.timestamp

            # Get the current time
            current_time = Timestamp.utcnow()

            # Calculate the difference between the timestamp and the current time
            time_difference = current_time - edit_time

            # Check if the time difference is less than 24 hours
            if time_difference > timedelta(hours=24):
                status = True

        return status

    def get_users_from_table(self):
        page_title = "مستخدم:لوقا/ملعب 22"
        page = pywikibot.Page(self.site, page_title)
        if page.exists():
            text = page.text
            parsed = wtp.parse(str(text))
            table = parsed.tables[0].data()
            for row in table:
                status = row[3]
                if status.strip().lower() == "نعم".strip().lower() or status.strip().lower() == "لا".strip().lower():
                    self.users.append(row)


def main(*args: str) -> int:
    try:

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
        yesterday = datetime.date.today() - datetime.timedelta(days=2)

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
        and user.user_id NOT IN (SELECT ipb_user FROM ipblocks)""".format(start_time_sql, last_time_sql)
        db.get_content_from_database()
        names = []
        for row in db.result:
            name = str(row['q_log_title'], 'utf-8')
            names.append(name)

        page_title = "مستخدم:لوقا/ملعب 22"
        # page_title = "مستخدم:لوقا/ملعب 20"

        site = pywikibot.Site()

        users = []
        try:
            last_check_obj = LastCheck(site)
            if last_check_obj.check():
                last_check_obj.get_users_from_table()
                users = last_check_obj.users
        except Exception as e:
                print(f"An error occurred while init last_check_obj : {e}")

        load_obj = Load(content_text=content, ai_model=ai_model, names=names, page_title=page_title, site=site,
                        users=users)
        load_obj.load_page().build_table().save_page()

    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
