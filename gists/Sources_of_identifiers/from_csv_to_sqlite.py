import sqlite3

# get the csv file from https://quarry.wmflabs.org/query/75218
# and save it in the same directory as this script or change the path below
csv_file_path = "/home/lokas/Downloads/quarry-75218-مصادر-المعرفات-ميدان-التقنيه-run751073.csv"
# initialize the database file path and connect to it
db_file_path = "/home/lokas/Downloads/run751073identifiers.sqlite"
# start the connection
conn = sqlite3.connect(db_file_path)
# get the cursor
c = conn.cursor()
# Create table
"""
table data looks like this:
page_id	page_namespace	page_title	main_edit	prev_edit	comment_text
57737	0	.tn	23959023	21979899	بوت:إضافة مصدر
57726	0	.ax	23959025	21975169	بوت:إضافة مصدر
46304	0	.bb	23959026	21938780	بوت:إضافة مصدر
46310	0	.bh	23959027	22010192	بوت:إضافة مصدر
46822	0	.bo	23959028	20897960	بوت:إضافة مصدر
1590078	0	.bq	23959030	22775216	بوت:إضافة مصدر

id : auto increment id
page_id: page id in the database
page_namespace: page namespace in the database
page_title: page title in the database
main_edit: the edit id of the edit that added the identifier
prev_edit: the edit id of the edit that was before the edit that added the identifier and can be null
comment_text: the comment of the edit that added the identifier
status: the status of the identifier alows is false 
"""
# drop the table if it exists
c.execute('''DROP TABLE IF EXISTS sources_of_identifiers''')
# create the table
c.execute('''CREATE TABLE sources_of_identifiers
                (id INTEGER PRIMARY KEY AUTOINCREMENT, page_id integer, page_namespace integer, page_title text, main_edit integer, prev_edit integer, comment_text text, status boolean)''')

# Insert a row of data
with open(csv_file_path, 'r') as f:
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
            # check len of rows to insert null if prev_edit is empty
            if len(rows) == 6:
                c.execute("INSERT INTO sources_of_identifiers VALUES (null,?, ?, ?, ?, ?, ? , false)",
                          (rows[0], rows[1], rows[2], rows[3], rows[4], rows[5]))
            else:
                c.execute("INSERT INTO sources_of_identifiers VALUES (null,?, ?, ?, ?, ?, ?, false)",
                          (rows[0], rows[1], rows[2], rows[3], None, rows[4]))
        except:
            print("error in line: " + str(line_count))
            print(line)
            raise

# Save (commit) the changes
conn.commit()
