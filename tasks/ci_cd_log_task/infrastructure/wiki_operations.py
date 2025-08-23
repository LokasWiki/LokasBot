"""
Infrastructure layer for Wiki operations.

This module provides the concrete implementation of the WikiRepository interface,
handling all external wiki interactions using pywikibot.
"""

import logging
import pywikibot
from tasks.ci_cd_log_task.domain.entities.bot_log import BotLog
from tasks.ci_cd_log_task.domain.repositories.wiki_repository import WikiRepository


class WikiOperations(WikiRepository):
    """
    Concrete implementation of WikiRepository using pywikibot.

    This class handles all interactions with the wiki,
    implementing the WikiRepository interface.
    """

    def __init__(self, site_name: str = "ar"):
        """
        Initialize the WikiOperations with a specific wiki site.

        Args:
            site_name (str): The name of the wiki site (default: "ar" for Arabic)
        """
        self.site_name = site_name
        self.site = pywikibot.Site(site_name)
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Initialized WikiOperations for site: {site_name}")

    def save_log_message(self, bot_log: BotLog) -> None:
        """
        Save a bot log message to the wiki.

        Args:
            bot_log (BotLog): The bot log message to save

        Raises:
            Exception: If the log message cannot be saved
        """
        try:
            page_title = bot_log.get_page_title()
            wiki_message = bot_log.format_wiki_message()

            self.logger.info(f"Saving log message to page: {page_title}")

            # Get or create the page
            page = pywikibot.Page(self.site, page_title)
            page.text = wiki_message

            # Save the page
            summary = "إعلام البوت: التشغيل للمرة الأولى بعد سحب التحديثات"
            page.save(summary=summary)

            self.logger.info(f"Successfully saved log message to {page_title}")

        except Exception as e:
            error_msg = f"Failed to save log message to wiki: {str(e)}"
            self.logger.error(error_msg)
            raise

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
        try:
            self.logger.info(f"Getting content for page: {page_title}")

            page = pywikibot.Page(self.site, page_title)
            content = page.text

            self.logger.info(f"Successfully retrieved content for {page_title}")
            return content

        except Exception as e:
            error_msg = f"Failed to get page content for {page_title}: {str(e)}"
            self.logger.error(error_msg)
            raise

    def page_exists(self, page_title: str) -> bool:
        """
        Check if a wiki page exists.

        Args:
            page_title (str): The title of the page to check

        Returns:
            bool: True if the page exists, False otherwise
        """
        try:
            self.logger.info(f"Checking if page exists: {page_title}")

            page = pywikibot.Page(self.site, page_title)
            exists = page.exists()

            self.logger.info(f"Page {page_title} exists: {exists}")
            return exists

        except Exception as e:
            error_msg = f"Failed to check if page exists {page_title}: {str(e)}"
            self.logger.error(error_msg)
            # Return False on error to be safe
            return False

    def get_site_info(self) -> dict:
        """
        Get information about the current wiki site.

        Returns:
            dict: Dictionary containing site information
        """
        try:
            return {
                'site_name': self.site_name,
                'site_code': self.site.code,
                'site_family': self.site.family.name,
                'username': self.site.username()
            }
        except Exception as e:
            self.logger.error(f"Failed to get site info: {str(e)}")
            return {
                'site_name': self.site_name,
                'error': str(e)
            }