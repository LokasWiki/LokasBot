import sqlite3
import os
import datetime


class Query:
    def __init__(self):
        home_path = os.path.expanduser("~")
        database_path = os.path.join(home_path, "requests.db")
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.create_requests_table()
        self.create_pages_table()

    def create_requests_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS requests
                              (id INTEGER PRIMARY KEY, 
                               from_id INTEGER NOT NULL,
                               from_namespace INT NOT NULL, 
                               to_namespace INT NOT NULL, 
                               to_id INT NOT NULL,
                               request_type INT NOT NULL, 
                               status INT)
                           """)
        self.conn.commit()

    def create_pages_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pages
                              (id INTEGER PRIMARY KEY, 
                               date TEXT DEFAULT (datetime('now', 'localtime')), 
                               status INT NOT NULL,
                               request_id INT NOT NULL,
                               FOREIGN KEY (request_id) REFERENCES requests(id))
                           """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_request(self, from_id, from_namespace, to_namespace, to_id, request_type, status):
        self.cursor.execute("""INSERT INTO requests (from_id, from_namespace, to_namespace, to_id, request_type, status)
                               VALUES (?, ?, ?, ?, ?, ?)
                            """, (int(from_id), int(from_namespace), int(to_namespace), int(to_id), int(request_type), int(status)))
        self.conn.commit()

    def insert_page(self, status, request_id):
        self.cursor.execute("""INSERT INTO pages (status, request_id)
                               VALUES (?, ?)
                            """, (status, request_id))
        self.conn.commit()