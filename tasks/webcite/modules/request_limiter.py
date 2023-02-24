"""
This module provides a class for rate-limiting HTTP requests.

The RequestLimiter class tracks the number of requests made within a given time
interval and blocks further requests if the limit is exceeded. It uses SQLite
database to store the request records.
"""

import os
import sqlite3
import time


class RequestLimiter:
    """
    A class for limiting the number of requests that can be made within a given time interval.

    Args:
        limit (int, optional): The maximum number of requests that
         can be made within the time interval.Defaults to 10.
        interval (int, optional): The time interval in seconds. Defaults to 60.

    Attributes:
        limit (int): The maximum number of requests that can be made within the time interval.
        interval (int): The time interval in seconds.
    """

    def __init__(self, limit=10, interval=60):
        self.limit = limit
        self.interval = interval
        self.db_conn = self._create_db_table()

    def _create_db_table(self):
        """
        Create the requests table in an SQLite database.

        Returns:
            sqlite3.Connection: A connection to the SQLite database.
        """
        home_path = os.path.expanduser("~")
        database_path = os.path.join(home_path, "request_limiter.db")

        conn = sqlite3.connect(database_path)
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
        """
        Check if a new request can be made based on the current request rate.

        Returns:
            bool: True if a new request can be made, False otherwise.
        """
        cursor = self.db_conn.cursor()
        # calculate the time interval before which requests are allowed
        min_time = int(time.time()) - self.interval
        # count the number of requests made in the time interval
        cursor.execute(f"SELECT COUNT(*) FROM requests WHERE timestamp >= {min_time}")
        count = cursor.fetchone()[0]
        return count < self.limit

    def add_request(self):
        """
        Add a new request to the database with the current timestamp.
        """
        cursor = self.db_conn.cursor()
        # insert a new request record with the current timestamp
        cursor.execute(f"INSERT INTO requests (timestamp) VALUES ({int(time.time())})")
        self.db_conn.commit()

    def clear_old_requests(self):
        """
        Clear old request records from the database that
        are older than the time interval plus a buffer.
        """
        cursor = self.db_conn.cursor()
        # delete request records that are older than the time interval
        min_time = int(time.time()) - self.interval - 120  # add 2 minute buffer
        cursor.execute(f"DELETE FROM requests WHERE timestamp < {min_time}")
        self.db_conn.commit()
