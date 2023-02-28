import os
import datetime
import pywikibot

from core.utils.file import File
from core.utils.wikidb import Database

script_dir = os.path.dirname(__file__)
site = pywikibot.Site()
import datetime

# Define the month you want to query
month = datetime.date(2021, 11, 1)  # January 2022

# Calculate the first and last days of the month
first_day_of_month = month.replace(day=1)
last_day_of_month = first_day_of_month.replace(day=28) + datetime.timedelta(days=4)
last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)

# Format the start and end times for the month in the format "%Y%m%d%H%M%S"
start_time = first_day_of_month.strftime("%Y%m%d") + '000000'
end_time = last_day_of_month.strftime("%Y%m%d") + '235959'

# Use these values in your SQL query
sql_query = f"SELECT * FROM my_table WHERE date BETWEEN '{start_time}' AND '{end_time}'"

# text stub
file = File(script_dir=script_dir)
file_path = 'stub/update.txt'
file.set_stub_path(file_path)
file.get_file_content()
content = file.contents

# page_title = "ويكيبيديا:إحصاءات الشهر"
page_title = "مستخدم:لوقا/ملعب 21"

page = pywikibot.Page(site, page_title)

db = Database()
db.query = f"select count(*) as 'block_count' from logging where log_type= 'block' and log_action = 'block' and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
block_count = str(db.result[0]['block_count'])

db.query = f"select count(*) as 'newusers_count' from logging where log_type= 'newusers' and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
newusers_count = str(db.result[0]['newusers_count'])

db.query = f"select count(*) as 'delete_count' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
delete_count = str(db.result[0]['delete_count'])

db.query = f"select count(rev_id) as 'total_edits' from revision where rev_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
total_edits = str(db.result[0]['total_edits'])

db.query = f"select count(*) as 'upload_count' from logging where log_type= 'upload' and log_action in ('upload','overwrite') and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
upload_count = str(db.result[0]['upload_count'])

db.query = f"select count(*) as 'delete_count',log_namespace as 'namespace' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}' group by log_namespace;"
db.get_content_from_database()
deleted_count_by_namespace = []
for row in db.result:
    deleted_count_by_namespace.append(["deleted_count_" + str(row['namespace']), row['delete_count']])

text = str(content).replace("BLOCK_COUNT", block_count).replace("NEWUSERS_COUNT", newusers_count).replace(
    "DELETE_COUNT", delete_count).replace("TOTAL_EDITS", total_edits).replace("UPLOAD_COUNT", upload_count)

for dcbn in deleted_count_by_namespace:
    text = str(text).replace(str(dcbn[0].upper().strip()), str(dcbn[1]))

# new pages
db.query = """

SELECT  count(*) as "new_pages", page_namespace as "namespace"
FROM (
    SELECT page_id, page_namespace, MIN(rev_timestamp) as first_revision
    FROM page
    JOIN revision ON page_id = rev_page
    WHERE page_is_redirect = 0
    GROUP BY page_id
) as temp
WHERE first_revision >= "START_DATE"
AND first_revision <= "END_DATE"
GROUP BY page_namespace;
""".replace("START_DATE", start_time).replace("END_DATE", end_time)
db.get_content_from_database()
new_pages_count_by_namespace = []
for row in db.result:
    new_pages_count_by_namespace.append(["new_pages_count_" + str(row['namespace']), row['new_pages']])

for npcbn in new_pages_count_by_namespace:
    text = str(text).replace(str(npcbn[0].upper().strip()), str(npcbn[1]))

page.text = text

page.save("تحديث")
