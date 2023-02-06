import sqlite3
import os
import pymysql
from pywikibot import config as _config


class WikiDatabase():
    """A class for interacting with a database.

    Attributes:
        _connection (pymysql.connections.Connection): A connection to the database.
        _query (str): The current SQL query.
        result (list): The result of the last executed query.
    """

    def __init__(self):
        """Initializes the Database with the connection and query attributes set to None, and result set to an empty list."""
        self._connection = None
        self._query = ""
        self.result = []

    @property
    def connection(self):
        """Returns the current connection to the database. If none exists, a new connection is established and returned.

        Returns:
            pymysql.connections.Connection: A connection to the database.
        """

        if self._connection is not None:
            return self._connection
        else:
            return pymysql.connect(
                host=_config.db_hostname_format.format("arwiki"),
                read_default_file=_config.db_connect_file,
                db=_config.db_name_format.format("arwiki"),
                charset='utf8mb4',
                port=_config.db_port,
                cursorclass=pymysql.cursors.DictCursor,
            )

    @property
    def query(self):
        """Returns the current SQL query.

        Returns:
            str: The current SQL query.
        """
        return self._query

    @query.setter
    def query(self, value):
        """Sets the current SQL query and replaces placeholders with the appropriate values.

        Args:
            value (str): The new SQL query.
        """
        self._query = value

    def get_content_from_database(self):
        """Executes the current SQL query and stores the result in the `result` attribute.

        Raises:
            pymysql.err.OperationalError: If a connection to the database cannot be established.
        """
        try:
            # Create a cursor page
            with self.connection.cursor() as cursor:
                # Execute the SELECT statement
                cursor.execute(self._query)
                # Fetch all the rows of the result
                self.result = cursor.fetchall()
        finally:
            # Close the connection
            self.connection.close()

    @connection.setter
    def connection(self, value):
        """Sets the current connection to the database.

        Args:
            value (pymysql.connections.Connection): The new connection to the database.
        """
        self._connection = value


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
                               from_title TEXT NOT NULL,
                               from_namespace INT NOT NULL,
                               to_namespace INT NOT NULL,
                               to_title TEXT NOT NULL,
                               request_type INT NOT NULL,
                               status INT)
                           """)
        self.conn.commit()

    def create_pages_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pages
                              (id INTEGER PRIMARY KEY,
                               title TEXT NOT NULL,
                               namespace INT NOT NULL,
                               date TEXT DEFAULT (datetime('now', 'localtime')),
                               status INT NOT NULL,
                               request_id INT NOT NULL,
                               FOREIGN KEY (request_id) REFERENCES requests(id))
                           """)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_request(self, from_title, from_namespace, to_namespace, to_title, request_type, status):
        self.cursor.execute("""INSERT INTO requests (from_title, from_namespace, to_namespace, to_title, request_type, status)
                               VALUES (?, ?, ?, ?, ?, ?)
                            """, (
        str(from_title), int(from_namespace), int(to_namespace), str(to_title), int(request_type), int(status)))
        self.conn.commit()

    def insert_page(self,title, namespace, status, request_id):
        self.cursor.execute("""INSERT INTO pages (title, namespace,status, request_id)
                               VALUES (?, ?,?, ?)
                            """, (str(title), int(namespace),int(status), int(request_id)))
        self.conn.commit()

    def get_requests(self, limit, request_type,status=0):
        self.cursor.execute("""SELECT * FROM requests WHERE status=? AND request_type=? LIMIT ?""",
                            (status,request_type, limit))
        requests = self.cursor.fetchall()
        requests_dict = []
        for request in requests:
            request_dict = {}
            request_dict["id"] = request[0]
            request_dict["from_title"] = request[1]
            request_dict["from_namespace"] = request[2]
            request_dict["to_namespace"] = request[3]
            request_dict["to_title"] = request[4]
            request_dict["request_type"] = request[5]
            request_dict["status"] = request[6]
            requests_dict.append(request_dict)
        return requests_dict

    def get_request(self,request_id):
        self.cursor.execute("""SELECT * FROM requests WHERE id= ?  LIMIT 1""",(request_id,))
        request = self.cursor.fetchone()
        request_dict = {}
        request_dict["id"] = request[0]
        request_dict["from_title"] = request[1]
        request_dict["from_namespace"] = request[2]
        request_dict["to_namespace"] = request[3]
        request_dict["to_title"] = request[4]
        request_dict["request_type"] = request[5]
        request_dict["status"] = request[6]

        return request_dict


    def get_new_pages(self, limit, request_type,status = 0):
        self.cursor.execute("""SELECT * FROM pages WHERE status=? AND request_id=? LIMIT ?""",
                            (status,request_type, limit))
        requests = self.cursor.fetchall()
        requests_dict = []
        for request in requests:
            request_dict = {}
            request_dict["id"] = request[0]
            request_dict["title"] = request[1]
            request_dict["namespace"] = request[2]
            request_dict["data"] = request[3]
            request_dict["status"] = request[4]
            request_dict["request_id"] = request[5]
            request_dict["request"] = self.get_request(int(request[5]))
            requests_dict.append(request_dict)

        print(requests_dict)
        return requests_dict

    def update_request_status(self, request_id, status):
        self.cursor.execute("""UPDATE requests SET status = ? WHERE id = ? """, (status, request_id))
        self.conn.commit()

    def delete_page(self,page_id):
        self.cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        self.conn.commit()