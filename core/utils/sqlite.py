import os
import sqlite3

maintenance_db_name = "maintenance.db"
webcite_db_name = "webcite.db"


def create_database_table(db_name):
    home_path = os.path.expanduser("~")
    database_path = os.path.join(home_path, db_name)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create the table with a status column
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, status INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,thread INTEGER)''')

    return conn, cursor


def save_pages_to_db(gen, conn, cursor, thread_number):
    for entry in gen:
        try:
            title = entry
            cursor.execute("SELECT * FROM pages WHERE title = ?", (title,))
            if cursor.fetchone() is None:
                print("added : " + title)
                cursor.execute("INSERT INTO pages (title, status,thread) VALUES (?, 0,?)", (title, int(thread_number)))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting the title {entry.title()} into the database: {e}")


def get_articles(cursor, thread_number):
    if thread_number == 1:
        thread_number = 0
    query1 = """
        SELECT id, title, thread
        FROM pages
        WHERE status = 0 AND thread = 1
        ORDER BY date ASC
        LIMIT 200 OFFSET ?;
    """

    query2 = """
        SELECT id, title, thread
        FROM pages
        WHERE status = 0 AND thread = 2
        ORDER BY date ASC
        LIMIT 150 OFFSET ?;
    """

    query3 = """
        SELECT id, title, thread
        FROM pages
        WHERE status = 0 AND thread = 3
        ORDER BY date ASC
        LIMIT 100 OFFSET ?;
    """

    cursor.execute(query1, (thread_number,))
    result1 = cursor.fetchall()

    cursor.execute(query2, (thread_number,))
    result2 = cursor.fetchall()

    cursor.execute(query3, (thread_number,))
    result3 = cursor.fetchall()

    rows = result1 + result2 + result3
    return rows
