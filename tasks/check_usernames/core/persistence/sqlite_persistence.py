from tasks.check_usernames.core.connection.base_connection import BaseConnection
from tasks.check_usernames.core.persistence.base_persistence import BasePersistence


class SQLitePersistence(BasePersistence):
    def __init__(self, connection: BaseConnection):
        """
        Initializes a new instance of the SQLitePersistence class.

        :param connection: The SQLiteConnection object to use for database operations.
        :type connection: BaseConnection
        """
        self.connection = connection

    def delete(self, query: str, params=None):
        """
        Deletes data from the SQLite database based on the given query and parameters.

        :param query: The SQL query used to delete data from the database.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        self.connection.connect()
        cursor = self.connection.connection.cursor()
        if params is None:
            cursor.execute(query)
        elif isinstance(params, tuple):
            cursor.execute(query, params)
        elif isinstance(params, dict):
            cursor.execute(query, params)
        else:
            raise ValueError("Unsupported type for 'params' argument")
        self.connection.connection.commit()
        self.connection.disconnect()

    def execute(self, query: str, params=None):
        """
        Executes a custom SQL query against the SQLite database.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        self.connection.connect()
        cursor = self.connection.connection.cursor()
        if params is None:
            cursor.execute(query)
        elif isinstance(params, tuple):
            cursor.execute(query, params)
        elif isinstance(params, dict):
            cursor.execute(query, params)
        else:
            raise ValueError("Unsupported type for 'params' argument")
        self.connection.connection.commit()
        self.connection.disconnect()

    def update(self, query: str, params=None):
        """
        Updates data in the SQLite database based on the given query and parameters.

        :param query: The SQL query used to update data in the database.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        self.connection.connect()
        cursor = self.connection.connection.cursor()
        if params is None:
            cursor.execute(query)
        elif isinstance(params, tuple):
            cursor.execute(query, params)
        elif isinstance(params, dict):
            cursor.execute(query, params)
        else:
            raise ValueError("Unsupported type for 'params' argument")
        self.connection.connection.commit()
        self.connection.disconnect()

    def select(self, query: str, params=None):
        """
        Executes a SELECT query against the SQLite database and returns the results as a list of rows.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]

        :return: A list of rows returned by the query.
        :rtype: list
        """
        self.connection.connect()
        cursor = self.connection.connection.cursor()
        if params is None:
            cursor.execute(query)
        elif isinstance(params, tuple):
            cursor.execute(query, params)
        elif isinstance(params, dict):
            cursor.execute(query, params)
        else:
            raise ValueError("Unsupported type for 'params' argument")
        result = cursor.fetchall()
        self.connection.disconnect()
        return result

    def select_one(self, query: str, params=None):
        """
        Executes a SELECT query against the SQLite database and returns a single row.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]

        :return: A single row returned by the query, or None if no rows are found.
        :rtype: Union[tuple, None]
        """
        self.connection.connect()
        cursor = self.connection.connection.cursor()
        if params is None:
            cursor.execute(query)
        elif isinstance(params, tuple):
            cursor.execute(query, params)
        elif isinstance(params, dict):
            cursor.execute(query, params)
        else:
            raise ValueError("Unsupported type for 'params' argument")
        result = cursor.fetchone()
        self.connection.disconnect()
        return result
