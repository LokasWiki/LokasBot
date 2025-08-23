"""
Repository interface for database operations.

This interface defines the contract for data access operations
related to database queries, following the Repository pattern.
"""

from abc import ABC, abstractmethod
from typing import List
from tasks.distribute_medals.domain.entities.user import User


class DatabaseRepository(ABC):
    """
    Abstract repository interface for database operations.

    This interface defines the contract for data access operations
    related to database queries, allowing for different implementations
    (e.g., MySQL, PostgreSQL, in-memory).
    """

    @abstractmethod
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
        pass

    @abstractmethod
    def get_connection_info(self) -> dict:
        """
        Get information about the database connection.

        Returns:
            dict: Connection information
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns:
            bool: True if connection is successful
        """
        pass