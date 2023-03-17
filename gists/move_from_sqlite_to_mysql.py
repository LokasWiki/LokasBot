import os
import sqlite3
import time

from sqlalchemy.orm import Session
print("get engine")
from database.engine import engine
from database.models import Page, TaskName

home_path = os.path.expanduser("~")
maintenance_database_path = os.path.join(home_path, "webcite.db")

# SQLite connection
sqlite_conn = sqlite3.connect(maintenance_database_path)
sqlite_cursor = sqlite_conn.cursor()
#

for i in range(1,1000):
    sqlite_cursor.execute('SELECT title,date,thread FROM pages LIMIT  1000 offset ' + str(i*1000))
    rows = sqlite_cursor.fetchall()
    print("start connect")
    with Session(engine) as session:
        for row in rows:
            print("add : " + row[0])
            temp_model = Page(
                title=row[0],
                thread_number=row[2],
                task_name=TaskName.WEBCITE,
                create_date=row[1]
            )
            session.add(temp_model)
        print("start save")
        session.commit()
    time.sleep(10)
sqlite_conn.close()



#
