# todo: make it run every week and in the end of the month
# todo: covert it to class
# todo : add main function
# Debug config (dev only)
DEBUG_MODE = False
DEBUG_YEAR = 2026
DEBUG_MONTH = 1
import datetime
import json
import logging
import os

import pywikibot
import requests

from core.utils.file import File
from core.utils.wikidb import Database

script_dir = os.path.dirname(__file__)


def setup_logging() -> None:
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    log_file_path = os.path.join(script_dir, "..", "..", "logs", "month_statistics.log")
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(),
        ],
    )


setup_logging()
logger = logging.getLogger(__name__)

site = pywikibot.Site()

logger.info("Starting month statistics update")

#  get current day
current_day = datetime.datetime.now()
if DEBUG_MODE:
    current_month = datetime.date(DEBUG_YEAR, DEBUG_MONTH, 1)
else:
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

# stop this script if current day not 1 (skip in debug mode)
if current_day.day != 1 and not DEBUG_MODE:
    logger.warning("Current day is not 1: %s", current_day.strftime("%Y-%m-%d"))
    exit()

# Calculate the first and last days of the month
first_day_of_month = current_month.replace(day=1)
last_day_of_month = first_day_of_month.replace(day=28) + datetime.timedelta(days=4)
last_day_of_month = last_day_of_month - datetime.timedelta(days=last_day_of_month.day)
logger.info(
    "Processing month range: %s to %s",
    first_day_of_month.strftime("%Y-%m-%d"),
    last_day_of_month.strftime("%Y-%m-%d"),
)

# Format the start and end times for the month in the format "%Y%m%d%H%M%S"
start_time = first_day_of_month.strftime("%Y%m%d") + '000000'
end_time = last_day_of_month.strftime("%Y%m%d") + '235959'
logger.debug("Computed start_time=%s end_time=%s", start_time, end_time)

# text stub
file = File(script_dir=script_dir)
file_path = 'stub/update.txt'
file.set_stub_path(file_path)
file.get_file_content()
content = file.contents
logger.info("Loaded stub content from %s", file_path)
logger.debug("Stub content length: %s", len(str(content)))

page_title = "ويكيبيديا:إحصاءات الشهر"
# page_title = "مستخدم:لوقا/إحصاءات الشهر"

page = pywikibot.Page(site, page_title)
logger.info("Target page title: %s", page_title)

db = Database()
db.query = f"select count(*) as 'block_count' from logging where log_type= 'block' and log_action = 'block' and log_timestamp between '{start_time}' and '{end_time}';"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
block_count = str(db.result[0]['block_count'])
logger.debug("block_count=%s", block_count)
# print(block_count)
# print(db.query)
db.query = f"select count(*) as 'newusers_count' from logging where log_type= 'newusers' and log_timestamp between '{start_time}' and '{end_time}';"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
newusers_count = str(db.result[0]['newusers_count'])
logger.debug("newusers_count=%s", newusers_count)
# print(newusers_count)
# print(db.query)
db.query = f"select count(*) as 'delete_count' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}';"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
delete_count = str(db.result[0]['delete_count'])
logger.debug("delete_count=%s", delete_count)
# print(delete_count)
# print(db.query)
db.query = f"select count(rev_id) as 'total_edits' from revision where rev_timestamp between '{start_time}' and '{end_time}';"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
total_edits = str(db.result[0]['total_edits'])
logger.debug("total_edits=%s", total_edits)
# print(total_edits)
# print(db.query)
db.query = f"select count(*) as 'upload_count' from logging where log_type= 'upload' and log_action in ('upload','overwrite') and log_timestamp between '{start_time}' and '{end_time}';"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
upload_count = str(db.result[0]['upload_count'])
logger.debug("upload_count=%s", upload_count)
# print(upload_count)
# print(db.query)
db.query = f"select count(*) as 'delete_count',log_namespace as 'namespace' from logging where log_type= 'delete' and log_action = 'delete'  and log_timestamp between '{start_time}' and '{end_time}' group by log_namespace;"
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
deleted_count_by_namespace = []
for row in db.result:
    # print(row)
    if row['namespace'] in [0,10,14,6]:
        deleted_count_by_namespace.append(["deleted_count_" + str(row['namespace']), row['delete_count']])
logger.debug("deleted_count_by_namespace=%s", deleted_count_by_namespace)
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
logger.debug("Executing query: %s", db.query)
db.get_content_from_database()
new_pages_count_by_namespace = []
for row in db.result:
    # print(row)
    if row['namespace'] in [0, 10, 14, 6]:
        new_pages_count_by_namespace.append(["new_pages_count_" + str(row['namespace']), row['new_pages']])
logger.debug("new_pages_count_by_namespace=%s", new_pages_count_by_namespace)

for npcbn in new_pages_count_by_namespace:
    text = str(text).replace(str(npcbn[0].upper().strip()), str(npcbn[1]))

total_views = 0

try:
    # Set the URL for the Wikimedia API and the parameters for the pageviews request
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate/ar.wikipedia.org/all-access/user/daily/" + first_day_of_month.strftime(
        "%Y%m%d") + "00/" + last_day_of_month.strftime("%Y%m%d") + "00"
    logger.debug("Pageviews URL: %s", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)
    logger.debug("Pageviews response status: %s", response.status_code)

    # Convert the response content to a JSON object
    data = json.loads(response.content)
    logger.debug("Pageviews response length: %s", len(response.content))
    # Print the pageviews data for each day in April 2023
    for item in data['items']:
        total_views += item['views']
    logger.info("Total views: %s", total_views)
#  add exception with log
except Exception as e:
    logger.exception("Error in getting pageviews data")

text = str(text).replace("TOTAL_VIEWS", str(total_views))

# print(new_pages_count_by_namespace)
# print(db.query)
page.text = text
logger.info("Saving page content")

page.save("v3.1.0 تحديث")
logger.info("Page saved successfully")
