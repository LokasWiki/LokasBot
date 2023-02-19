import sqlite3
import time


class RequestLimiter:
    def __init__(self, limit, interval):
        self.limit = limit
        self.interval = interval
        self.db_conn = self._create_db_table()

    def _create_db_table(self):
        conn = sqlite3.connect("request_limiter.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER
            )
        """)
        conn.commit()
        return conn

    def can_make_request(self):
        cursor = self.db_conn.cursor()
        # calculate the time interval before which requests are allowed
        min_time = int(time.time()) - self.interval
        # count the number of requests made in the time interval
        cursor.execute(f"SELECT COUNT(*) FROM requests WHERE timestamp >= {min_time}")
        count = cursor.fetchone()[0]
        return count < self.limit

    def add_request(self):
        cursor = self.db_conn.cursor()
        # insert a new request record with the current timestamp
        cursor.execute(f"INSERT INTO requests (timestamp) VALUES ({int(time.time())})")
        self.db_conn.commit()

    def clear_old_requests(self):
        cursor = self.db_conn.cursor()
        # delete request records that are older than the time interval
        min_time = int(time.time()) - self.interval - 120  # add 2 minute buffer
        cursor.execute(f"DELETE FROM requests WHERE timestamp < {min_time}")
        self.db_conn.commit()
