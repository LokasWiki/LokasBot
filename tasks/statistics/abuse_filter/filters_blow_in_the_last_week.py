"""
ضربات المرشحات في آخر أسبوع (filters blows in the last week).

The old implementation read `abuse_filter_log`, which no longer exists on the
analytics replica (only abuse_filter / abuse_filter_action / abuse_filter_history
remain). Rebuilt on:
  1. the MediaWiki API `list=abuselog` (filter hits for the last 7 days), and
  2. the `abuse_filter` table on the arwiki_p replica (metadata: description,
     hidden flag, enabled/deleted status).
"""

import datetime

import pymysql
import pywikibot
from pywikibot import config as _config
from pywikibot.data.api import Request

from tasks.statistics.module import Page, File, ArticleTables


WEEK_DAYS = 7


def fetch_filter_metadata():
    """Return {af_id: (af_public_comments bytes, af_hidden int, af_enabled int, af_deleted int)}
    for all filters from the arwiki_p replica."""
    connection = pymysql.connect(
        host=_config.db_hostname_format.format("arwiki"),
        read_default_file=_config.db_connect_file,
        db=_config.db_name_format.format("arwiki"),
        charset='utf8mb4',
        port=_config.db_port,
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT af_id, af_public_comments, af_hidden, af_enabled, af_deleted "
                "FROM abuse_filter"
            )
            return {
                row['af_id']: (row['af_public_comments'], row['af_hidden'],
                               row['af_enabled'], row['af_deleted'])
                for row in cursor.fetchall()
            }
    finally:
        connection.close()


def fetch_log_entries(site, window_start):
    """Fetch (filter_id, timestamp) pairs from list=abuselog for the last 7 days.

    NOTE: the API's aflstart is an UPPER bound (entries with timestamp <= aflstart
    are returned in descending order), so we start from "now" and paginate back
    until the entries become older than window_start. Only local filters with a
    filter id are kept."""
    entries = []
    seen_ids = set()
    aflstart = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)) \
        .strftime('%Y-%m-%dT00:00:00Z')

    while True:
        request = Request(
            site=site, action='query', list='abuselog',
            aflstart=aflstart, afllimit=5000,
            aflprop='ids|filter|timestamp'
        )
        data = request.submit()
        rows = data.get('query', {}).get('abuselog', [])
        if not rows:
            break

        oldest = None
        for row in rows:
            log_id = row.get('id')
            filter_id = row.get('filter_id')
            timestamp = row.get('timestamp')
            # Skip global filters (e.g. 'global-110') and entries without a filter.
            if not filter_id or not filter_id.isdigit() or not timestamp or log_id in seen_ids:
                continue
            seen_ids.add(log_id)
            entries.append((filter_id, timestamp))
            if oldest is None or timestamp < oldest:
                oldest = timestamp

        # Stop when this batch has reached (or passed) the start of the window.
        if not oldest or oldest < window_start:
            break

        continuation = data.get('continue')
        if not continuation or 'aflstart' not in continuation:
            break
        aflstart = continuation['aflstart']

    return entries


def aggregate(entries, metadata):
    """Aggregate hit counts per enabled, non-deleted filter per day.

    Returns a list of dicts keyed like the old SQL result:
    afl_filter_id, af_public_comments, af_hidden, hit_in_day_1..hit_in_day_7.
    """
    today = datetime.date.today()
    counts = {}

    for filter_id, timestamp in entries:
        try:
            entry_time = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            continue

        days_ago = (today - entry_time.date()).days
        if days_ago < 0 or days_ago >= WEEK_DAYS:
            continue

        meta = metadata.get(int(filter_id))
        if meta is None:
            continue
        af_public_comments, af_hidden, af_enabled, af_deleted = meta
        if not af_enabled or af_deleted:
            continue

        bucket = 'hit_in_day_' + str(WEEK_DAYS - days_ago)
        if filter_id not in counts:
            counts[filter_id] = {
                'afl_filter_id': int(filter_id),
                'af_public_comments': af_public_comments,
                'af_hidden': af_hidden,
                'hit_in_day_1': 0,
                'hit_in_day_2': 0,
                'hit_in_day_3': 0,
                'hit_in_day_4': 0,
                'hit_in_day_5': 0,
                'hit_in_day_6': 0,
                'hit_in_day_7': 0,
            }
        counts[filter_id][bucket] += 1

    result = list(counts.values())
    result.sort(key=lambda row: row['afl_filter_id'])
    return result


def afl_filter_id(row, result, index):
    return "[[Special:AbuseFilter/" + str(row['afl_filter_id']) + "|" + str(row['afl_filter_id']) + "]]"


def afl_public_comments(row, result, index):
    af_public_comments = str(row['af_public_comments'], 'utf-8')
    return af_public_comments


def is_hidden(row, result, index):
    af_hidden = str(row['af_hidden'])
    return "{{نعم}}" if af_hidden == "1" else "{{لا}}"


def day_1(row, result, index):
    return str(row['hit_in_day_1'])


def day_2(row, result, index):
    return str(row['hit_in_day_2'])


def day_3(row, result, index):
    return str(row['hit_in_day_3'])


def day_4(row, result, index):
    return str(row['hit_in_day_4'])


def day_5(row, result, index):
    return str(row['hit_in_day_5'])


def day_6(row, result, index):
    return str(row['hit_in_day_6'])


def day_7(row, result, index):
    return str(row['hit_in_day_7'])


columns = [
    ("#", None, afl_filter_id),
    ("الوصف", None, afl_public_comments),
    ("مخفي", None, is_hidden),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-0 days}}}}", None, day_7),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-1 days}}}}", None, day_6),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-2 days}}}}", None, day_5),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-3 days}}}}", None, day_4),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-4 days}}}}", None, day_3),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-5 days}}}}", None, day_2),
    ("{{نسخ:#time:j F|{{نسخ:#time:Y-m-d|-6 days}}}}", None, day_1),
]


def main(*args: str) -> int:
    site = pywikibot.Site()

    # 1. Filter metadata from the replica
    metadata = fetch_filter_metadata()

    # 2. Log hits from the API (window: last 7 days, UTC)
    window_start = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=WEEK_DAYS - 1)) \
        .strftime('%Y-%m-%dT00:00:00Z')
    entries = fetch_log_entries(site, window_start)

    # 3. Aggregate per filter per day
    result = aggregate(entries, metadata)

    # 4. Build the table (same layout as the old SQL version)
    tables = ArticleTables()
    tables.add_table("main_table", columns)

    table_body = ""
    for table in tables.tables:
        table_body += table.build_table(
            result=result,
            end_row_in_table=table.add_end_row_to_table,
            header_text=table.add_header_text,
            footer_text=table.add_footer_text,
        )

    # 5. Load the stub, inject the table and save
    file_ = File()
    file_.set_stub_path('stub/filters_blow_in_the_last_week.txt')
    file_.get_file_content()

    page = Page()
    page.page_name = "ويكيبيديا:تقارير قاعدة البيانات/ضربات المرشحات في آخر أسبوع"
    page.set_contents(file_.contents.replace("BOT_TABLE_BODY", table_body))
    page.save_page()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
