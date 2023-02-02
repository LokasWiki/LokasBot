import datetime
import os
import time
import sqlite3

import pywikibot


from module import create_database_table,get_articles,process_article




def main():
    try:
        site = pywikibot.Site()
        conn, cursor = create_database_table()
        rows = get_articles(cursor)
        if rows:
            for row in rows:
                process_article(site, cursor, conn, id=row[0], title=row[1])
                time.sleep(1)
        else:
            time.sleep(60)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
    return 0


if __name__ == "__main__":
    main()
