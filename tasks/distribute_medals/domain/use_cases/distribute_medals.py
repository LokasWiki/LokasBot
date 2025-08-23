"""
Use case for distributing medals to eligible users.

This use case encapsulates the business logic for the complete
medal distribution workflow, following Clean Architecture principles.
"""

import logging
from typing import List, Dict, Any
from tasks.distribute_medals.domain.entities.medal import Medal
from tasks.distribute_medals.domain.entities.user import User
from tasks.distribute_medals.domain.entities.template import Template
from tasks.distribute_medals.domain.repositories.database_repository import DatabaseRepository
from tasks.distribute_medals.domain.repositories.wiki_repository import WikiRepository
from tasks.distribute_medals.domain.repositories.signature_repository import SignatureRepository


class DistributeMedals:
    """
    Use case for distributing medals to eligible users.

    This class contains the business logic for the complete medal distribution
    workflow, coordinating between different repositories and handling errors.
    """

    def __init__(
        self,
        database_repo: DatabaseRepository,
        wiki_repo: WikiRepository,
        signature_repo: SignatureRepository
    ):
        """
        Initialize the DistributeMedals use case.

        Args:
            database_repo (DatabaseRepository): Repository for database operations
            wiki_repo (WikiRepository): Repository for wiki operations
            signature_repo (SignatureRepository): Repository for signature operations
        """
        self.database_repo = database_repo
        self.wiki_repo = wiki_repo
        self.signature_repo = signature_repo
        self.logger = logging.getLogger(__name__)

    def execute(self, medal: Medal) -> Dict[str, Any]:
        """
        Execute the medal distribution workflow.

        Args:
            medal (Medal): The medal configuration to distribute

        Returns:
            Dict[str, Any]: Result containing success status and details
        """
        result = {
            'success': False,
            'medal': medal,
            'eligible_users': [],
            'distributed_count': 0,
            'skipped_count': 0,
            'errors': []
        }

        try:
            self.logger.info(f"Starting distribution for medal {medal.number}")

            # Step 1: Fetch eligible users
            eligible_users = self._fetch_eligible_users(medal)
            result['eligible_users'] = eligible_users

            if not eligible_users:
                self.logger.info("No eligible users found")
                result['success'] = True
                return result

            # Step 2: Distribute to each eligible user
            distributed_count = 0
            skipped_count = 0

            for user in eligible_users:
                try:
                    if self._should_skip_user(user):
                        self.logger.info(f"Skipping user {user.name}")
                        skipped_count += 1
                        continue

                    # Get random signature
                    signature = self.signature_repo.get_random_signature(user.name)

                    # Create template
                    template = Template(
                        stub=medal.template_stub,
                        number=medal.number,
                        signature=signature.text,
                        username=user.name
                    )

                    # Send template to user
                    success = self.wiki_repo.send_template(template)

                    if success:
                        self.logger.info(f"Successfully sent template to {user.name}")
                        distributed_count += 1
                    else:
                        self.logger.error(f"Failed to send template to {user.name}")
                        result['errors'].append(f"Failed to send to {user.name}")

                except Exception as e:
                    error_msg = f"Error processing user {user.name}: {str(e)}"
                    self.logger.error(error_msg)
                    result['errors'].append(error_msg)

            result['distributed_count'] = distributed_count
            result['skipped_count'] = skipped_count
            result['success'] = True

            self.logger.info(
                f"Distribution completed: {distributed_count} distributed, "
                f"{skipped_count} skipped"
            )

        except Exception as e:
            error_msg = f"Distribution failed: {str(e)}"
            self.logger.error(error_msg)
            result['errors'].append(error_msg)

        return result

    def _fetch_eligible_users(self, medal: Medal) -> List[User]:
        """
        Fetch users eligible for the medal.

        Args:
            medal (Medal): The medal configuration

        Returns:
            List[User]: List of eligible users
        """
        try:
            return self.database_repo.fetch_eligible_users(medal.query, medal.number)
        except Exception as e:
            self.logger.error(f"Failed to fetch eligible users: {str(e)}")
            return []

    def _should_skip_user(self, user: User) -> bool:
        """
        Determine if a user should be skipped.

        Args:
            user (User): The user to check

        Returns:
            bool: True if the user should be skipped
        """
        try:
            # Check if user is blocked
            if self.wiki_repo.is_user_blocked(user.name):
                return True

            # Check if user is a bot
            user_groups = self.wiki_repo.get_user_groups(user.name)
            if "BOT" in [group.upper() for group in user_groups]:
                return True

            return False

        except Exception as e:
            self.logger.warning(f"Error checking user {user.name}: {str(e)}")
            # If we can't determine, skip to be safe
            return True