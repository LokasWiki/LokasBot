import re
import sqlite3

file_path = "/home/lokas/PycharmProjects/pythonProject3/code/gists/ar_pages_delete_from_en_site/quarry-72431-نقاش-ويكيبيديا_مشروع-ويكي-الصيانة-بدون-إنترويكي-نسخة-أولية-run778938.csv"
db_path = "/home/lokas/PycharmProjects/pythonProject3/code/gists/ar_pages_delete_from_en_site/ar_pages_delete_from_en_site.db"

# create sqlite db
conn = sqlite3.connect(db_path)

# create table to store data from csv and check if it exists
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS identifiers
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
          en_page text null,
          date text null,
          ar_page text null,
          namespace text null,
          exites_in_en text null,
          comment text null,
          year text null,
          en_page_without_namespace text null,
          en_first_letter text null,
          ar_first_letter text null    
    )
    ''')

# read csv
with open(file_path, 'r') as f:
    next(f)  # Skip the header row.
    line_count = 0
    for line in f:
        # log the progress every 1000 lines
        if line_count % 1000 == 0:
            print("line: " + str(line_count) + " done")
        try:
            line_count += 1
            # split the line by comma
            rows = line.split(",")
            # skip any row has any site else enwiki like "enwikisource" etc
            # print(rows[0])
            if re.search("enwiki\s\*/", rows[0]) is None:
                print("skipped")
                print(rows)
                continue
            # for some case that title have " like this
            # ['"/* clientsitelink-remove:1||enwiki */ Alex (footballer', ' born 2001)"', '20230803133941', 'أليكس (لاعب كرة قدم مواليد 2001)\n']
            if len(rows) != 3:
                print(rows)
                en_page = re.sub(r'/\*.*?\*/', '', rows[0] + rows[1]).strip()
                if en_page.startswith("\""):
                    en_page = en_page[1:]
                if en_page.endswith("\""):
                    en_page = en_page[:-1]

                rows[1] = rows[2]
                rows[2] = rows[3]
                rows[3] = rows[4]
            else:
                en_page = re.sub(r'/\*.*?\*/', '', rows[0]).strip()
            print(en_page)
            print(rows[0])
            date = rows[1].strip()
            ar_page = rows[2].strip()
            namespace = "main" if ":" not in en_page else en_page.split(":")[0]
            en_page_without_namespace = en_page.split(":")[1] if ":" in en_page else en_page
            # well will check if the page exist in enwiki after store by api
            exites_in_en = None
            comment = None
            year = date[0:4]
            en_first_letter = en_page_without_namespace[0]
            ar_first_letter = ar_page[0]

            # check if en_page exist in table
            c.execute("SELECT * FROM identifiers WHERE en_page = ?", (en_page,))
            result = c.fetchone()
            if result:
                continue
            # insert the data into the table
            c.execute("""
                INSERT INTO identifiers
                (en_page, date, ar_page, namespace, exites_in_en, comment, year, en_page_without_namespace, en_first_letter, ar_first_letter)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            en_page, date, ar_page, namespace, exites_in_en, comment, year, en_page_without_namespace, en_first_letter,
            ar_first_letter))

            conn.commit()

        except:
            print("error in line: " + str(line_count))
            print(line)
