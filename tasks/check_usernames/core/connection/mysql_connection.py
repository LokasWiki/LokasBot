import pymysql
from abc import ABC, abstractmethod

from tasks.check_usernames.core.connection.base_connection import Connection


class MySQLConnection(Connection):
    """
    Implementation of the Connection interface for MySQL databases using the pymysql library.
    """

    def __init__(self, host, port, user, password, database):
        """
        Initializes a MySQLConnection object with the provided connection parameters.

        Parameters:
            host (str): The host name or IP address of the MySQL server.
            port (int): The port number of the MySQL server.
            user (str): The MySQL user name.
            password (str): The password for the MySQL user.
            database (str): The name of the MySQL database to connect to.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Connects to the MySQL database using the provided parameters.

        Raises:
            pymysql.err.OperationalError: If the connection fails.
        """
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
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
