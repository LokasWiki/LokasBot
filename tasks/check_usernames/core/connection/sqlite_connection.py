import sqlite3

from tasks.check_usernames.core.connection.base_connection import BaseConnection


class SQLiteBaseConnection(BaseConnection):
    """
    Implementation of the BaseConnection interface for SQLite databases using the sqlite3 library.
    """

    def __init__(self, database_file: str):
        """
        Initializes a SQLiteBaseConnection object with the path to the SQLite database file.

        Parameters:
            database_file (str): The path to the SQLite database file.
        """
        self.database_file = database_file
        self.connection = None

    def connect(self):
        """
        Connects to the SQLite database using the provided database file path.

        Raises:
            sqlite3.Error: If the connection fails.
        """
        self.connection = sqlite3.connect(self.database_file)

    def disconnect(self):
        """
        Disconnects from the SQLite database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def check(self):
        """
        Checks the status of the SQLite database connection.

        Returns:
            bool: True if the connection is open, False otherwise.
        """
        if self.connection:
            return True
        return False
