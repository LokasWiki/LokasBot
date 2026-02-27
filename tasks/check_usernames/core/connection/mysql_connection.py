from __future__ import annotations

import pymysql

from tasks.check_usernames.core.connection.base_connection import BaseConnection


class MySQLBaseConnection(BaseConnection):
    """
    Implementation of the BaseConnection interface for MySQL databases using the pymysql library.
    """

    def __init__(self, host: str, port: str | int, database: str, db_connect_file: str = None, user: str = None,
                 password: str = None):
        """
        Initializes a MySQLBaseConnection object with the provided connection parameters.

        Parameters:
            host (str): The host name or IP address of the MySQL server.
            port (int): The port number of the MySQL server.
            database (str): The name of the MySQL database to connect to.
            db_connect_file (str, optional): The path to the MySQL database connection file. Defaults to None.
            user (str, optional): The name of the MySQL user. Defaults to None.
            password (str, optional): The password of the MySQL user. Defaults to None.
        """

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.db_connect_file = db_connect_file

    def connect(self):
        """
        Connects to the MySQL database using the provided parameters.

        Raises:
            pymysql.err.OperationalError: If the connection fails.
        """
        if self.db_connect_file is not None:
            self.connection = pymysql.connect(
                host=self.host,
                read_default_file=self.db_connect_file,
                db=self.database,
                charset='utf8mb4',
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor,
            )
        else:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                charset='utf8mb4',
                user=self.user,
                password=self.password,
                db=self.database
            )

    def disconnect(self):
        """
        Disconnects from the MySQL database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def check(self):
        """
        Checks the status of the MySQL database connection.

        Returns:
            bool: True if the connection is open, False otherwise.
        """
        if self.connection:
            return self.connection.open
        return False
