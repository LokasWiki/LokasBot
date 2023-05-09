import configparser
import os

import pymysql
import pywikibot

home_path = os.path.expanduser("~")

config_path = os.path.join(home_path, 'config.ini')

# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Get the MySQL connection details from the configuration file
username = config.get('copypatrol_db', 'username')
password = config.get('copypatrol_db', 'password')
host = config.get('copypatrol_db', 'host')
port = config.get('copypatrol_db', 'port')
database = config.get('copypatrol_db', 'database')

# Connect to the database
conn = pymysql.connect(
    host=host,
    port=int(port),
    user=username,
    password=password,
    database=database
)

# Create a cursor
cursor = conn.cursor()

# Execute the query
cursor.execute(' select count(id) from copyright_diffs where lang ="ar" and project = "wikipedia" and status is null')

# Get the result
openCasesCount = cursor.fetchone()[0]

site = pywikibot.Site()
page_name = "قالب:إحصاءات أداء كشف خرق حقوق النشر"
page = pywikibot.Page(site, page_name)
text = """[https://copypatrol.toolforge.org/ar/ أداة كشف خرق حقوق النشر] (OPENEDNUMBER)

<noinclude>
[[تصنيف:قوالب صيانة ويكيبيديا]]
</noinclude>"""
text = text.replace("OPENEDNUMBER", str(openCasesCount))
page.text = text
page.save("تحديث v1.0.0")
# Close the cursor and connection
cursor.close()
conn.close()
