import datetime
import os
import time
import sqlite3

import pywikibot


from module import create_database_table,get_unreviewed_articles,process_unreviewed_article




def main():
    try:
        site = pywikibot.Site()
        conn, cursor = create_database_table()
        rows = get_unreviewed_articles(cursor)
        if rows:
            for row in rows:
                time.sleep(2)
                id = row[0]
                title = row[1]
                print(title)
                process_unreviewed_article(site, cursor, conn, id, title)
        else:
            time.sleep(60)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while interacting with the database: {e}")
    return 0


if __name__ == "__main__":
    main()
