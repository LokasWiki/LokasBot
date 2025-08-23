"""
Repository interface for Wiki operations.

This interface defines the contract for Wiki data access operations,
following the Repository pattern to abstract data access from business logic.
"""

from abc import ABC, abstractmethod
from tasks.ci_cd_log_task.domain.entities.bot_log import BotLog


class WikiRepository(ABC):
    """
    Abstract repository interface for Wiki operations.

    This interface defines the contract for data access operations
    related to Wiki operations, allowing for different implementations
    (e.g., pywikibot, mock implementations).
    """

    @abstractmethod
    def save_log_message(self, bot_log: BotLog) -> None:
        """
        Save a bot log message to the wiki.

        Args:
            bot_log (BotLog): The bot log message to save

        Raises:
            Exception: If the log message cannot be saved
        """
        pass

    @abstractmethod
    def get_page_content(self, page_title: str) -> str:
        """
        Get the content of a wiki page.

        Args:
            page_title (str): The title of the page to retrieve

        Returns:
            str: The content of the page

        Raises:
            Exception: If the page content cannot be retrieved
        """
        pass

    @abstractmethod
    def page_exists(self, page_title: str) -> bool:
        """
        Check if a wiki page exists.

        Args:
            page_title (str): The title of the page to check

        Returns:
            bool: True if the page exists, False otherwise
        """
        pass