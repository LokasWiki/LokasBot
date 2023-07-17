import sqlite3
from urllib.parse import urlparse

db_file_path = "/home/lokas/Downloads/run751073identifiers_v2.sqlite"

# start the connection
conn = sqlite3.connect(db_file_path)

# get the cursor
c = conn.cursor()

# create table to store domain name not url and the number of times it appears
c.execute('''CREATE TABLE IF NOT EXISTS domains
                (id INTEGER PRIMARY KEY AUTOINCREMENT, domain text, count integer)''')

# get all urls from identifiers table
c.execute("select url from identifiers order by id asc")

# get the rows
rows = c.fetchall()
index = 0
for row in rows:
    index += 1

    if index % 1000 == 0:
        print("index now is " + str(index))
    try:
        url = row[0]
        # archive.org  in url and have two http
        if "archive.org" in url and url.count("http") > 1:
            try:
                # remove from start to the first archive.org
                url = url.split("archive.org")[1]
                # remove from before tp first http
                url = url.split("http")[1]
                url = "http" + url
            except Exception as e:
                print(url)

        domain = urlparse(url).netloc
        c.execute("select * from domains where domain = ?", (domain,))
        domain_row = c.fetchone()
        if domain_row is None:
            c.execute("insert into domains (domain,count) values (?,?)", (domain, 1))
        else:
            c.execute("update domains set count = ? where domain = ?", (domain_row[2] + 1, domain))
        conn.commit()
    except Exception as e:
        print(e)
        continue
