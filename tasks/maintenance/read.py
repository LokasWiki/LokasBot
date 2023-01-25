import datetime
import itertools
import os
from pywikibot import pagegenerators
import time
import sqlite3
import pywikibot
import sys


site = pywikibot.Site()

time_before_start = int(sys.argv[1])

start = pywikibot.Timestamp.now() - datetime.timedelta(minutes=time_before_start)
end = pywikibot.Timestamp.now()


gen1 = pagegenerators.RecentChangesPageGenerator(site=site, start=start, end=end, namespaces=[0], reverse=True)
gen2 = pagegenerators.LogeventsPageGenerator(logtype="review", total=3000, site=site, start=start, end=end, namespace=0,
                                             reverse=True)

merged_gen = itertools.chain(gen1, gen2)

# To remove duplicate pages from the generator
gen = set(merged_gen)

# To remove deleted pages from the generator,
gen = filter(lambda page: page.exists(), gen)

# This will create a pages.db file in the home directory of the user running the script.
home_path = os.path.expanduser("~")
database_path = os.path.join(home_path, "maintenance.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create the table with a status column
cursor.execute('''CREATE TABLE IF NOT EXISTS pages (title TEXT PRIMARY KEY, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

for entry in gen:
    page1 = pywikibot.Page(site, entry.title())
    if not page1.isRedirectPage():
        time.sleep(1)
        try:
            title = entry.title()
            cursor.execute("SELECT * FROM pages WHERE title = ?", (title,))
            if cursor.fetchone() is None:
                print("added : " + title)
                cursor.execute("INSERT INTO pages (title, status) VALUES (?, 0)", (title,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting the title {title} into the database: {e}")



