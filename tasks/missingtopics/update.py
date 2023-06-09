import logging
import re
import time

import pymysql
import pywikibot
import requests
import wikitextparser as wtp
from pymysql.converters import escape_string
from pywikibot import config as _config

from core.utils.wikidb import Database


def has_arabic_chars(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
    if arabic_pattern.search(text):
        return True
    else:
        return False


site = pywikibot.Site()

username_bot = site.username()
# todo: call this from text file and remove from here
# todo: use statistics package and add ability to pass data or get data from db
text = """
<center>
<div style="background: #E5E4E2; padding: 0.5em; font-family: Traditional Arabic; font-size: 130%;  -moz-border-radius: 0.3em; border-radius: 0.3em;">
تعرض هذه الصفحة قائمة وصلات حمراء مطلوبة حسب الموضوع ([[TYPE]]).<br/>

'''حَدَّث BOT_USER_NAME هذه القائمة في :  BOT_TIME_NOW (ت ع م) '''
</div>
</center>
<center>
<div style="background: #E5E4E2; padding: 0.5em;   -moz-border-radius: 0.3em; border-radius: 0.3em;">

{| class="wikitable sortable"
!style="background-color:#808080" align="center"|#
!style="background-color:#808080" align="center"|عدد الوصلات
!style="background-color:#808080" align="center"|اسم المقال
!style="background-color:#808080" align="center"|المقالة المقابلة في لغة أخرى
TABLE_BODY
|}

</div>
</center>

   """

db = Database()
db.query = """select replace(pl_title,"مقالات_مطلوبة_حسب_الاختصاص/","") as page_title from pagelinks 
where pl_from in (676775)
and pl_namespace in (4)
and pl_from_namespace in (4)
and pl_title not like "%وصلة_حمراء%"
order by pl_title
limit 1
"""
db.get_content_from_database()

list_of_pages = []
for row in db.result:
    list_of_pages.append(str(row['page_title'], "utf-8"))

for type in list_of_pages:
    type = type.replace("_", " ")
    page_name = f"ويكيبيديا:مقالات مطلوبة حسب الاختصاص/{type}"
    # page_name = "مستخدم:لوقا/ملعب 34"

    url = f"https://missingtopics.toolforge.org/?language=ar&project=wikipedia&article=&category={type}&depth=1&wikimode=1&nosingles=1&limitnum=1&doit=Run"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            parsed = wtp.parse(response.text)

            table = parsed.tables[0]

            data = table.data()[1:1001]

            """
            note: The maximum length for an SQL query in MySQL depends on the max_allowed_packet configuration variable.
            By default, its value is set to 4 MB (4,194,304 bytes).
            This means that the SQL query, including all its components (such as the query text, parameters, and overhead),
            cannot exceed this limit.
            """
            patch_size = 100
            found_pages = []
            for i in range(0, len(data), patch_size):
                try:
                    patch = data[i:i + patch_size]
                    titles = []

                    for item in patch:
                        # to remove [[ and ]]
                        # title = item[1][2: -2].replace(" ", "_")
                        title = item[1].replace(" ", "_").replace("[[", "").replace("]]", "")
                        # max title len 100 to skip title that have len >= 100 like "Primeval Beech Forests of the
                        # Carpathians and the Ancient Beech Forests of Germany aaaaaa aaaaaaaa"
                        if not has_arabic_chars(title) and len(title) <= 100:
                            titles.append(title)
                    # Escape and join the titles
                    escaped_titles = [escape_string(title) for title in titles]
                    titles_string = ','.join(["'" + title + "'" for title in escaped_titles])

                    en_db = Database()
                    en_db.connection = pymysql.connect(
                        host=_config.db_hostname_format.format("enwiki"),
                        read_default_file=_config.db_connect_file,
                        db=_config.db_name_format.format("enwiki"),
                        charset='utf8mb4',
                        # port=_config.db_port,
                        port=4701,
                        cursorclass=pymysql.cursors.DictCursor,
                    )
                    en_db.query = "select page.page_title as 'p_title' from page where page.page_title in ({}) and page.page_namespace in (0)".format(
                        titles_string)
                    en_db.get_content_from_database()
                    result = en_db.result
                    for item in result:
                        found_pages.append(str(item['p_title'], 'utf-8'))
                except Exception as e:
                    logging.error("Error occurred while get pages from the database.")
                    logging.exception(e)
                    print(e)
                time.sleep(3)

            table_body = ""
            for index, row in enumerate(data):
                en_title = ""

                # if row[1][2:-2].replace(" ", "_") in found_pages:
                if row[1].replace(" ", "_").replace("[[", "").replace("]]", "") in found_pages:
                    en_title = "[[:en:" + row[1][2:-2] + "]]"

                table_body += """
                    |-
                    |{}
                    |{}
                    |{}
                    |{}
                    """.format(str(int(index + 1)), row[0], row[1], en_title)

            page = pywikibot.Page(site, page_name)
            page.text = str(text).replace("TABLE_BODY", table_body).replace('BOT_USER_NAME',
                                                                            f"[[مستخدم:{username_bot}|{username_bot}]]").replace(
                "BOT_TIME_NOW", "{{نسخ:#time:H:i، j F Y}}").replace("TYPE", type)

            page.save("بوت:تحديث مقالات مطلوبة حسب الاختصاص v2.0.0")
        except:
            # todo: add more log here
            print(f"cand`t work with this page {type}")
