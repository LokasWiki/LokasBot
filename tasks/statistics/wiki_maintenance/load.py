import datetime,os
import sqlite3

from core.utils.wikidb import Database
import pywikibot
import pymysql
from pywikibot import config as _config


# Set start and end dates
start_date = datetime.date(1999, 1, 1)
end_date = datetime.date(2023, 12, 31)

home_path = os.path.expanduser("~")
database_path = os.path.join(home_path, "mydatabase.sqlite")

# Connect to SQLite database
conn = sqlite3.connect(database_path)
c = conn.cursor()

# Create table if it does not exist
c.execute('''
    CREATE TABLE IF NOT EXISTS deleted_pages
    (deleted_page TEXT, date_of_delete TEXT, name_of_page TEXT)
''')

# Iterate over months
current_date = start_date
while current_date <= end_date:
    # Calculate start and end times for current month
    start_time = datetime.datetime(current_date.year, current_date.month, 1)
    if current_date.month == 12:
        end_time = datetime.datetime(current_date.year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_time = datetime.datetime(current_date.year, current_date.month + 1, 1) - datetime.timedelta(seconds=1)

    # Format start and end times as MySQL datetime strings
    start_time_str = start_time.strftime("%Y%m%d%H%M%S")
    end_time_str = end_time.strftime("%Y%m%d%H%M%S")


    print(start_time_str)
    print(end_time_str)
    # Build SQL query
    sql_query = f"""
        SELECT
            comment.comment_text AS "deleted_page",
            revision.rev_timestamp AS "date_of_delete",
            wb_items_per_site.ips_site_page AS "name_of_page"
        FROM
            revision
            JOIN page ON page.page_id = revision.rev_page
            JOIN comment ON comment.comment_id = revision.rev_comment_id
            JOIN wb_items_per_site ON wb_items_per_site.ips_item_id = REPLACE(page.page_title, "Q", "")
        WHERE
            comment.comment_text LIKE "%clientsitelink-remove%" AND
            comment.comment_text LIKE "%enwiki%" AND
            rev_timestamp BETWEEN {start_time_str} AND {end_time_str} AND
            wb_items_per_site.ips_site_id LIKE "arwiki"
    """

    connection = pymysql.connect(
        host=_config.db_hostname_format.format("wikidatawiki"),
        read_default_file=_config.db_connect_file,
        db=_config.db_name_format.format("wikidatawiki"),
        charset='utf8mb4',
        port=_config.db_port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    db = Database()
    db.query = sql_query
    db.connection = connection
    db.get_content_from_database()

    # Insert data into SQLite table
    for row in db.result:
        deleted_page = str(row['deleted_page'],'utf-8')
        date_of_delete = str(row['date_of_delete'],'utf-8')
        name_of_page = str(row['name_of_page'],'utf-8')
        c.execute('INSERT INTO deleted_pages VALUES (?, ?, ?)', (deleted_page, date_of_delete, name_of_page))
    conn.commit()

    # Move to next month
    current_date = current_date + datetime.timedelta(days=31)

# Close connection to SQLite database
conn.close()
