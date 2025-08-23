"""
Use case for sending medal templates to users.

This use case encapsulates the business logic for creating
and sending medal templates to eligible users.
"""

import logging
from typing import Dict, Any
from tasks.distribute_medals.domain.entities.template import Template
from tasks.distribute_medals.domain.repositories.wiki_repository import WikiRepository


class SendMedalTemplate:
    """
    Use case for sending medal templates to users.

    This class contains the business logic for creating templates
    and sending them to users' talk pages.
    """

    def __init__(self, wiki_repo: WikiRepository):
        """
        Initialize the SendMedalTemplate use case.

        Args:
            wiki_repo (WikiRepository): Repository for wiki operations
        """
        self.wiki_repo = wiki_repo
        self.logger = logging.getLogger(__name__)

    def execute(self, template: Template) -> Dict[str, Any]:
        """
        Execute the use case to send a template to a user.

        Args:
            template (Template): The template to send

        Returns:
            Dict[str, Any]: Result containing success status and details
        """
        result = {
            'success': False,
            'template': template,
            'user': template.username,
            'errors': []
        }

        try:
            self.logger.info(f"Sending template to user: {template.username}")

            # Check if user should be skipped
            if self._should_skip_user(template.username):
                result['skipped'] = True
                result['skip_reason'] = 'User is blocked or bot'
                self.logger.info(f"Skipping user {template.username}")
                return result

            # Send the template
            success = self.wiki_repo.send_template(template)

            if success:
                result['success'] = True
                self.logger.info(f"Successfully sent template to {template.username}")
            else:
                result['errors'].append("Failed to send template")
                self.logger.error(f"Failed to send template to {template.username}")

        except Exception as e:
            error_msg = f"Error sending template: {str(e)}"
            result['errors'].append(error_msg)
            self.logger.error(error_msg)

        return result

    def execute_with_validation(self, template: Template) -> Dict[str, Any]:
        """
        Execute with additional validation and error handling.

        Args:
            template (Template): The template to send

        Returns:
            Dict[str, Any]: Detailed result with validation information
        """
        result = {
            'success': False,
            'template': template,
            'validation': {},
            'user_info': {},
            'errors': [],
            'warnings': []
        }

        try:
            # Validate template
            template_valid = self._validate_template(template)
            result['validation']['template_valid'] = template_valid

            if not template_valid:
                result['errors'].append("Template validation failed")
                return result

            # Get user information
            try:
                user_info = self.wiki_repo.get_user_info(template.username)
                result['user_info'] = user_info
            except Exception as e:
                result['warnings'].append(f"Could not get user info: {str(e)}")

            # Check user status
            is_blocked = self.wiki_repo.is_user_blocked(template.username)
            user_groups = self.wiki_repo.get_user_groups(template.username)

            result['validation']['is_blocked'] = is_blocked
            result['validation']['user_groups'] = user_groups

            if is_blocked:
                result['errors'].append("User is blocked")
                return result

            if "BOT" in [group.upper() for group in user_groups]:
                result['errors'].append("User is a bot")
                return result

            # Send template
            success = self.wiki_repo.send_template(template)
            result['success'] = success

            if success:
                self.logger.info(f"Template sent successfully to {template.username}")
            else:
                result['errors'].append("Failed to send template to wiki")

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            result['errors'].append(error_msg)
            self.logger.error(error_msg)

        return result

    def _should_skip_user(self, username: str) -> bool:
        """
        Determine if a user should be skipped.

        Args:
            username (str): The username to check

        Returns:
            bool: True if the user should be skipped
        """
        try:
            is_blocked = self.wiki_repo.is_user_blocked(username)
            user_groups = self.wiki_repo.get_user_groups(username)

            return is_blocked or "BOT" in [group.upper() for group in user_groups]

        except Exception as e:
            self.logger.warning(f"Error checking user {username}: {str(e)}")
            # Skip if we can't determine
            return True

    def _validate_template(self, template: Template) -> bool:
        """
        Validate a template before sending.

        Args:
            template (Template): The template to validate

        Returns:
            bool: True if the template is valid
        """
        return (
            template.username and
            template.number > 0 and
            template.stub and
            template.signature
        )