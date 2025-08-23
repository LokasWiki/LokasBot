"""
MySQL database implementation for medal distribution.

This module provides a concrete implementation of the DatabaseRepository
interface using MySQL and pymysql for database operations.
"""

import logging
from typing import List
import pymysql
from pymysql.connections import Connection
from pywikibot import config as _config

from tasks.distribute_medals.domain.entities.user import User
from tasks.distribute_medals.domain.repositories.database_repository import DatabaseRepository


class MySQLDatabase(DatabaseRepository):
    """
    MySQL implementation of DatabaseRepository.

    This class handles all database operations using MySQL and pymysql,
    implementing the DatabaseRepository interface.
    """

    def __init__(self):
        """
        Initialize the MySQL database connection.
        """
        self._connection = None
        self.logger = logging.getLogger(__name__)

    @property
    def connection(self) -> Connection:
        """
        Get the database connection, creating it if necessary.

        Returns:
            Connection: The MySQL database connection

        Raises:
            pymysql.err.OperationalError: If connection cannot be established
        """
        if self._connection is not None:
            return self._connection

        try:
            self._connection = pymysql.connect(
                host=_config.db_hostname_format.format("arwiki"),
                read_default_file=_config.db_connect_file,
                db=_config.db_name_format.format("arwiki"),
                charset='utf8mb4',
                port=_config.db_port,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.logger.info("Database connection established successfully")
            return self._connection

        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def fetch_eligible_users(self, query: str, number_count: int) -> List[User]:
        """
        Fetch users eligible for a medal based on the query.

        Args:
            query (str): The SQL query to execute
            number_count (int): The medal number for replacement in query

        Returns:
            List[User]: List of eligible users

        Raises:
            Exception: If the query execution fails
        """
        try:
            # Replace placeholders in query
            formatted_query = query.replace("NUMBER_COUNT", str(number_count))

            self.logger.info(
                f"Executing query for {number_count} edits, "
                f"query length: {len(formatted_query)}"
            )

            with self.connection.cursor() as cursor:
                cursor.execute(formatted_query)
                results = cursor.fetchall()

            # Convert database rows to User entities
            users = []
            for row in results:
                try:
                    user = User.create_from_db_row(row)
                    users.append(user)
                except Exception as e:
                    self.logger.warning(f"Failed to create user from row: {str(e)}")

            self.logger.info(f"Fetched {len(users)} eligible users")
            return users

        except Exception as e:
            self.logger.error(f"Failed to fetch eligible users: {str(e)}")
            raise

    def get_connection_info(self) -> dict:
        """
        Get information about the database connection.

        Returns:
            dict: Connection information
        """
        try:
            info = {
                'host': _config.db_hostname_format.format("arwiki"),
                'database': _config.db_name_format.format("arwiki"),
                'port': _config.db_port,
                'charset': 'utf8mb4',
                'connected': self._connection is not None and self._connection.open
            }
            return info

        except Exception as e:
            self.logger.error(f"Failed to get connection info: {str(e)}")
            return {'error': str(e)}

    def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns:
            bool: True if connection is successful
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

            return result is not None

        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False

    def close_connection(self):
        """
        Close the database connection.
        """
        if self._connection is not None:
            try:
                self._connection.close()
                self._connection = None
                self.logger.info("Database connection closed")
            except Exception as e:
                self.logger.error(f"Error closing connection: {str(e)}")

    def __del__(self):
        """
        Destructor to ensure connection is closed.
        """
        self.close_connection()