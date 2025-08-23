"""
Use case for fetching eligible users for medal distribution.

This use case encapsulates the business logic for retrieving
users who are eligible for medal distribution.
"""

import logging
from typing import List
from tasks.distribute_medals.domain.entities.medal import Medal
from tasks.distribute_medals.domain.entities.user import User
from tasks.distribute_medals.domain.repositories.database_repository import DatabaseRepository


class FetchEligibleUsers:
    """
    Use case for fetching users eligible for a medal.

    This class contains the business logic for retrieving and filtering
    users who are eligible for medal distribution.
    """

    def __init__(self, database_repo: DatabaseRepository):
        """
        Initialize the FetchEligibleUsers use case.

        Args:
            database_repo (DatabaseRepository): Repository for database operations
        """
        self.database_repo = database_repo
        self.logger = logging.getLogger(__name__)

    def execute(self, medal: Medal) -> List[User]:
        """
        Execute the use case to fetch eligible users.

        Args:
            medal (Medal): The medal configuration

        Returns:
            List[User]: List of eligible users
        """
        try:
            self.logger.info(f"Fetching eligible users for medal {medal.number}")

            users = self.database_repo.fetch_eligible_users(medal.query, medal.number)

            # Filter to only include eligible users
            eligible_users = [user for user in users if user.is_eligible]

            self.logger.info(
                f"Found {len(users)} total users, {len(eligible_users)} eligible"
            )

            return eligible_users

        except Exception as e:
            self.logger.error(f"Failed to fetch eligible users: {str(e)}")
            return []

    def execute_with_details(self, medal: Medal) -> dict:
        """
        Execute with detailed information about the fetch operation.

        Args:
            medal (Medal): The medal configuration

        Returns:
            dict: Detailed result containing users and statistics
        """
        result = {
            'medal': medal,
            'total_users': 0,
            'eligible_users': [],
            'ineligible_users': [],
            'errors': []
        }

        try:
            users = self.database_repo.fetch_eligible_users(medal.query, medal.number)
            result['total_users'] = len(users)

            for user in users:
                if user.is_eligible:
                    result['eligible_users'].append(user)
                else:
                    result['ineligible_users'].append(user)

            self.logger.info(
                f"Fetched {len(users)} users: "
                f"{len(result['eligible_users'])} eligible, "
                f"{len(result['ineligible_users'])} ineligible"
            )

        except Exception as e:
            error_msg = f"Failed to fetch eligible users: {str(e)}"
            self.logger.error(error_msg)
            result['errors'].append(error_msg)

        return result