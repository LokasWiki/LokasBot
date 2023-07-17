# pip install urlextract
import sqlite3
import time

import pywikibot
from urlextract import URLExtract

extractor = URLExtract()

# initialize the database file path and connect to it
# db_file_path = "run751073identifiers.sqlite"
db_file_path = "/home/lokas/Downloads/run751073identifiers.sqlite"

# start the connection
conn = sqlite3.connect(db_file_path)

# get the cursor
c = conn.cursor()

# get the rows that have  status false and limit the number of rows to 1000

# create table if not exists that have id,url,source (which store sources_of_identifiers id)
c.execute('''CREATE TABLE IF NOT EXISTS identifiers
                (id INTEGER PRIMARY KEY AUTOINCREMENT, url text, source integer)''')

c.execute("select id,page_title,main_edit,prev_edit from sources_of_identifiers where status is false limit 10")

# get the rows
rows = c.fetchall()
# initialize the site
site = pywikibot.Site('ar', 'wikipedia')

number_index = 0
# iterate over the rows
for row in rows:
    number_index += 1
    # sleep for 5 seconds every 100 rows
    if number_index % 150 == 0:
        time.sleep(5)
    try:
        page_title = row[1]
        main_edit = row[2]
        prev_edit = row[3]
        # get the page
        page = pywikibot.Page(site, page_title)
        # get the text of the main edit
        main_edit_text = page.getOldVersion(main_edit)
        # get the text of the prev edit
        prev_edit_text = page.getOldVersion(prev_edit)
        # get the added text

        oldUrls = extractor.find_urls(prev_edit_text)
        newUrls = extractor.find_urls(main_edit_text)

        # get added urls
        addedUrls = list(set(newUrls) - set(oldUrls))
        print("id of page {}", row[0])
        for url in addedUrls:
            # insert the url and the source id
            try:
                print("added url: {}".format(url))
                c.execute("insert into identifiers (url,source) values (?,?)", (url, row[0]))
                # commit the changes
                conn.commit()
            except Exception as e:
                print("error in adding url: {}".format(url))
                print(e)
                continue

        # update the row and set status to true and diff_text to added_text
        c.execute("update sources_of_identifiers set status = true where id = ?", (row[0],))
        # commit the changes
        conn.commit()

    except Exception as e:
        print(e)
        # update the row and set status to true and diff_text to added_text
        c.execute("update sources_of_identifiers set status = true where id = ?", (row[0],))
        # commit the changes
        conn.commit()
        continue

# close the connection
conn.close()
