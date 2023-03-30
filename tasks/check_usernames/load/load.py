import configparser
import datetime
import logging
import os
import re
import time
from datetime import timedelta

import pywikibot
import requests
import wikitextparser as wtp
from pywikibot import Timestamp

from core.utils.file import File
from core.utils.helpers import check_status
from core.utils.wikidb import Database

home_path = os.path.expanduser("~")
""""
config.ini example

[mysql]
username=your_username
password=your_password
host=your_host
port=your_port
database=your_database
[ai_api]
key = my_key
url= ai_flask_url
"""

config_path = os.path.join(home_path, 'config.ini')


# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

def get_spam_predictions(usernames):
    # Define the API endpoint URL
    url = config.get('ai_api', "url")

    # Set the request headers
    headers = {"X-Api-Key": config.get('ai_api', "key"), "Content-Type": "application/json"}

    # Replace underscores with spaces in the usernames
    usernames = [username.replace("_", " ") for username in usernames]

    # Split the list of usernames into batches of 100
    batches = [usernames[i:i + 100] for i in range(0, len(usernames), 100)]

    # Create a list to store the results from each batch
    results = []
    num = 0
    # Loop over the batches and send a POST request to the API endpoint for each batch
    for batch in batches:
        # Create the request data as a dictionary
        data = {"usernames": batch}
        print(num)
        num += 1
        # Send the POST request to the API endpoint
        response = requests.post(url, headers=headers, json=data)

        # Parse the response JSON and append it to the results list
        batch_results = response.json()["results"]
        results.extend(batch_results)
        time.sleep(5)
    # Return the list of usernames and their spam predictions
    return results


class Load:
    def __init__(self, content_text, names, page_title, site, users=None):
        if users is None:
            users = []
        self.stub_content = content_text
        self.list_of_names = get_spam_predictions(names)
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
            table_body += """|{}||{}||{}||{}||\n|-
                                      """.format(num, user[1], user[2], user[3], user[4])
            num += 1

        for user_name in self.list_of_names:

            user_name['prediction']['score']
            try:
                msg1 = user_name['username'].strip().lower().replace(" ", "_")

                if user_name['prediction']['label'] == "LABEL_1":
                    table_body += """|{0}||{2}||{1}||لا||\n|-
                  """.format(num, "{{مس|" + user_name['username'] + "}}", str(user_name['prediction']['score']))
                    num += 1
                elif len(msg1) <= 2:
                    table_body += """|{0}||{2}||{1}||لا||\n|-
                                      """.format(num, "{{مس|" + user_name['username'] + "}}",
                                                 str("كود عادي (الاسم قصير)"))
                elif len(re.findall(r'\w+', msg1)) >= 5:
                    table_body += """|{0}||{2}||{1}||لا||\n|-
                                          """.format(num, "{{مس|" + user_name['username'] + "}}",
                                                     str("كود عادي (الاسم طويل)"))
                    num += 1
            except Exception as e:
                logging.error("Error occurred while adding pages to the database.")
                logging.exception(e)
                table_body += """|{0}||{2}||{1}||لا||\n|-
                      """.format(num, "{{مس|" + user_name['username'] + "}}", "غير معروف")
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
        self.page.save("بوت:فحص V2.0.2")
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
        page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"
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
        if check_status("مستخدم:LokasBot/إخطار الإداريين/أسماء مستخدمين للفحص"):
            script_dir = os.path.dirname(__file__)

            # text stub
            file = File(script_dir=script_dir)
            file_path = 'stub/load.txt'
            file.set_stub_path(file_path)
            file.get_file_content()
            content = file.contents

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
            # start_time_sql = 20221207000000
            last_time_sql = last_time.strftime("%Y%m%d%H%M%S")
            # last_time_sql = 20230322235959

            print(start_time_sql)
            print(last_time_sql)

            db.query = """
            select log_title as "q_log_title"
            from logging 
            where log_type in ("newusers") 
            and log_timestamp BETWEEN {} AND {}
            and log_title not in (
              select page.page_title from categorylinks 
              inner join page on page.page_id = categorylinks.cl_from
              where cl_to like "أسماء_مستخدمين_مخالفة_مرشحة_للمنع" 
              and cl_type in ("page")
            )
            and log_title not in (
                select replace(user.user_name," ","_") as "user_name_temp" from ipblocks
                inner join user on ipblocks.ipb_user = user.user_id
            )
            """.format(start_time_sql, last_time_sql)
            db.get_content_from_database()
            names = []
            for row in db.result:
                name = str(row['q_log_title'], 'utf-8')
                names.append(name)

            page_title = "ويكيبيديا:إخطار الإداريين/أسماء مستخدمين للفحص"
            # page_title = "مستخدم:لوقا/أسماء مستخدمين للفحص"
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

            load_obj = Load(content_text=content, names=names, page_title=page_title, site=site,
                            users=users)
            load_obj.load_page().build_table().save_page()
        else:
            print("check wiki site")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
