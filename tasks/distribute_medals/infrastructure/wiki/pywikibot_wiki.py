"""
Pywikibot wiki implementation for medal distribution.

This module provides a concrete implementation of the WikiRepository
interface using Pywikibot for wiki operations.
"""

import logging
from typing import List
import pywikibot
from pywikibot.exceptions import Error as PywikibotError

from tasks.distribute_medals.domain.entities.template import Template
from tasks.distribute_medals.domain.repositories.wiki_repository import WikiRepository


class PywikibotWiki(WikiRepository):
    """
    Pywikibot implementation of WikiRepository.

    This class handles all wiki operations using Pywikibot,
    implementing the WikiRepository interface.
    """

    def __init__(self, site=None):
        """
        Initialize the Pywikibot wiki operations.

        Args:
            site (pywikibot.Site, optional): The wiki site to use
        """
        self.site = site or pywikibot.Site()
        self.logger = logging.getLogger(__name__)

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
        try:
            self.logger.info(f"Sending template to user: {template.username}")

            # Get the user object
            user = pywikibot.User(self.site, template.username)

            # Get the user's talk page
            talk_page = user.getUserTalkPage()

            # Get current page text
            current_text = talk_page.text if hasattr(talk_page, 'text') else ""

            # Add the new section
            new_content = current_text + "\n\n" + template.get_full_message()

            # Save the page
            summary = f"بوت: توزيع وسام {template.number} تعديل"

            talk_page.text = new_content
            talk_page.save(summary=summary, minor=False)

            self.logger.info(f"Template sent successfully to {template.username}")
            return True

        except PywikibotError as e:
            error_msg = f"Pywikibot error sending template: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error sending template: {str(e)}"
            self.logger.error(error_msg)
            raise

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
        try:
            user = pywikibot.User(self.site, username)

            # Get basic user info
            info = {
                'username': username,
                'exists': user.exists(),
                'registration_date': None,
                'edit_count': None,
                'groups': [],
                'blocked': False
            }

            if user.exists():
                try:
                    info['registration_date'] = user.registration_date
                    info['edit_count'] = user.edit_count
                    info['groups'] = list(user.groups())
                    info['blocked'] = user.is_blocked()
                except Exception as e:
                    self.logger.warning(f"Could not get full user info: {str(e)}")

            return info

        except Exception as e:
            error_msg = f"Failed to get user info for {username}: {str(e)}"
            self.logger.error(error_msg)
            raise

    def is_user_blocked(self, username: str) -> bool:
        """
        Check if a user is blocked.

        Args:
            username (str): The username to check

        Returns:
            bool: True if the user is blocked
        """
        try:
            user = pywikibot.User(self.site, username)
            return user.is_blocked()

        except Exception as e:
            self.logger.warning(f"Could not check block status for {username}: {str(e)}")
            return False

    def get_user_groups(self, username: str) -> List[str]:
        """
        Get the groups a user belongs to.

        Args:
            username (str): The username to check

        Returns:
            List[str]: List of user groups
        """
        try:
            user = pywikibot.User(self.site, username)
            return list(user.groups())

        except Exception as e:
            self.logger.warning(f"Could not get groups for {username}: {str(e)}")
            return []