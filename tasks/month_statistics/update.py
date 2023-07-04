# todo: make it run every week and in the end of the month
# todo: covert it to class
# todo : add main function
import datetime
import json
import logging
import os

import pywikibot
import requests

from core.utils.file import File
from core.utils.wikidb import Database

script_dir = os.path.dirname(__file__)
site = pywikibot.Site()

#  get current day
current_day = datetime.datetime.now()
#  if current day is 1 then get previous month else get current month
if current_day.day == 1:
    month = current_day - datetime.timedelta(days=1)
    #  if month is 1 then get previous year else get current year
    if month.month == 1:
        current_month = datetime.date(month.year, 12, 1)
    else:
        current_month = datetime.date(month.year, month.month, 1)
else:
    current_month = datetime.date(current_day.year, current_day.month, 1)

# stop this script if current day not 1
if current_day.day != 1:
    print("Current day is not 1")
    exit()

# Calculate the first and last days of the month
first_day_of_month = current_month.replace(day=1)
last_day_of_month = first_day_of_month.replace(day=28) + datetime.timedelta(days=4)
last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)

# Format the start and end times for the month in the format "%Y%m%d%H%M%S"
start_time = first_day_of_month.strftime("%Y%m%d") + '000000'
end_time = last_day_of_month.strftime("%Y%m%d") + '235959'

# text stub
file = File(script_dir=script_dir)
file_path = 'stub/update.txt'
file.set_stub_path(file_path)
file.get_file_content()
content = file.contents

page_title = "ويكيبيديا:إحصاءات الشهر"
# page_title = "مستخدم:لوقا/إحصاءات الشهر"

page = pywikibot.Page(site, page_title)

db = Database()
db.query = f"select count(*) as 'block_count' from logging where log_type= 'block' and log_action = 'block' and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
block_count = str(db.result[0]['block_count'])
# print(block_count)
# print(db.query)
db.query = f"select count(*) as 'newusers_count' from logging where log_type= 'newusers' and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
newusers_count = str(db.result[0]['newusers_count'])
# print(newusers_count)
# print(db.query)
db.query = f"select count(*) as 'delete_count' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
delete_count = str(db.result[0]['delete_count'])
# print(delete_count)
# print(db.query)
db.query = f"select count(rev_id) as 'total_edits' from revision where rev_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
total_edits = str(db.result[0]['total_edits'])
# print(total_edits)
# print(db.query)
db.query = f"select count(*) as 'upload_count' from logging where log_type= 'upload' and log_action in ('upload','overwrite') and log_timestamp between '{start_time}' and '{end_time}';"
db.get_content_from_database()
upload_count = str(db.result[0]['upload_count'])
# print(upload_count)
# print(db.query)
db.query = f"select count(*) as 'delete_count',log_namespace as 'namespace' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}' group by log_namespace;"
db.get_content_from_database()
deleted_count_by_namespace = []
for row in db.result:
    # print(row)
    if row['namespace'] in [0,10,14,6]:
        deleted_count_by_namespace.append(["deleted_count_" + str(row['namespace']), row['delete_count']])
# print(deleted_count_by_namespace)
# print(db.query)

text = str(content).replace("BLOCK_COUNT", block_count).replace("NEWUSERS_COUNT", newusers_count).replace(
    "DELETE_COUNT", delete_count).replace("TOTAL_EDITS", total_edits).replace("UPLOAD_COUNT", upload_count)

for dcbn in deleted_count_by_namespace:
    # print("=====================================")
    # print(str(dcbn[0].upper().strip()))
    # print(str(dcbn[1]))
    # print(text)
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
    # print(row)
    if row['namespace'] in [0, 10, 14, 6]:
        new_pages_count_by_namespace.append(["new_pages_count_" + str(row['namespace']), row['new_pages']])

for npcbn in new_pages_count_by_namespace:
    text = str(text).replace(str(npcbn[0].upper().strip()), str(npcbn[1]))

total_views = 0

try:
    # Set the URL for the Wikimedia API and the parameters for the pageviews request
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/ar.wikipedia.org/all-access/user/daily/" + first_day_of_month.strftime(
        "%Y%m%d") + "00/" + last_day_of_month.strftime("%Y%m%d") + "00"
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)

    # Convert the response content to a JSON object
    data = json.loads(response.content)
    # Print the pageviews data for each day in April 2023
    for item in data['items']:
        total_views += item['views']
#  add exception with log
except Exception as e:
    print("Error in getting pageviews data")
    print(e)
    logging.error("Error in getting pageviews data")
    logging.error(e)

text = str(text).replace("TOTAL_VIEWS", str(total_views))

# print(new_pages_count_by_namespace)
# print(db.query)
page.text = text

page.save("v3.0.0 تحديث")
