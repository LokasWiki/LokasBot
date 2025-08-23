"""
Repository interface for wiki operations.

This interface defines the contract for wiki operations,
following the Repository pattern to abstract wiki interactions.
"""

from abc import ABC, abstractmethod
from typing import List
from tasks.distribute_medals.domain.entities.template import Template


class WikiRepository(ABC):
    """
    Abstract repository interface for wiki operations.

    This interface defines the contract for wiki operations,
    allowing for different implementations (e.g., Pywikibot, API-based).
    """

    @abstractmethod
    def send_template(self, template: Template) -> bool:
        """
        Send a template to a user's talk page.

        Args:
            template (Template): The template to send

        Returns:
            bool: True if successful

        Raises:
            Exception: If the operation fails
        """
        pass

    @abstractmethod
    def get_user_info(self, username: str) -> dict:
        """
        Get information about a wiki user.

        Args:
            username (str): The username to look up

        Returns:
            dict: User information

        Raises:
            Exception: If the user is not found or operation fails
        """
        pass

    @abstractmethod
    def is_user_blocked(self, username: str) -> bool:
        """
        Check if a user is blocked.

        Args:
            username (str): The username to check

        Returns:
            bool: True if the user is blocked
        """
        pass

    @abstractmethod
    def get_user_groups(self, username: str) -> List[str]:
        """
        Get the groups a user belongs to.

        Args:
            username (str): The username to check

        Returns:
            List[str]: List of user groups
        """
        pass