from tasks.check_usernames.core.connection.base_connection import BaseConnection
from tasks.check_usernames.core.persistence.base_persistence import BasePersistence


class MySQLPersistence(BasePersistence):
    def __init__(self, connection: BaseConnection):
        """
        Initializes a new instance of the MySQLPersistence class.

        :param connection: The connection object to use for database operations.
        :type connection: BaseConnection
        """
        self.connection = connection

    def delete(self, query, params=None):
        """
        Deletes data from the database based on the given query and parameters.

        :param query: The SQL query used to delete data from the database.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        with self.connection.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.connection.commit()

    def execute(self, query, params=None):
        """
        Executes a custom SQL query.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        with self.connection.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.connection.commit()

    def update(self, query, params=None):
        """
        Updates data in the database based on the given query and parameters.

        :param query: The SQL query used to update data in the database.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]
        """
        with self.connection.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.connection.commit()

    def select(self, query, params=None):
        """
        Executes a SELECT query and returns the results as a list of rows.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]

        :return: A list of rows returned by the query.
        :rtype: list
        """
        with self.connection.connection.cursor() as cursor:
            print(query, params)
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result

    def select_one(self, query, params=None):
        """
        Executes a SELECT query and returns a single row.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]

        :return: A single row returned by the query, or None if no rows are found.
        :rtype: Union[tuple, None]
        """
        with self.connection.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
        return result
