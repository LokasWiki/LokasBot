"""
Use case for fetching contributors from GitHub.

This use case encapsulates the business logic for retrieving
contributor information from GitHub, following the Clean Architecture principles.
"""

import logging
from typing import List, Optional
from tasks.ci_cd_log_task.domain.repositories.github_repository import GitHubRepository


class FetchContributors:
    """
    Use case for fetching contributors from GitHub.

    This class contains the business logic for retrieving contributor information
    from GitHub, handling errors gracefully and providing fallback values.
    """

    def __init__(self, github_repository: GitHubRepository):
        """
        Initialize the FetchContributors use case.

        Args:
            github_repository (GitHubRepository): Repository for GitHub operations
        """
        self.github_repository = github_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, repo_owner: str, repo_name: str) -> List[str]:
        """
        Execute the use case to fetch contributors.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name

        Returns:
            List[str]: List of contributor names with contribution info
        """
        try:
            self.logger.info(f"Fetching contributors from {repo_owner}/{repo_name}")

            contributors = self.github_repository.fetch_contributors(
                repo_owner=repo_owner,
                repo_name=repo_name
            )

            contributor_count = len(contributors)
            self.logger.info(f"Successfully fetched {contributor_count} contributors")

            return contributors

        except Exception as e:
            error_msg = (
                f"Failed to fetch contributors from {repo_owner}/{repo_name}: {str(e)}"
            )
            self.logger.error(error_msg)

            # Return default unavailable contributor as fallback
            return ["غير متوفر"]

    def execute_with_fallback(
        self,
        repo_owner: str,
        repo_name: str
    ) -> tuple[List[str], Optional[str]]:
        """
        Execute the use case with error information returned.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name

        Returns:
            tuple[List[str], Optional[str]]: Contributors list and error message if any
        """
        try:
            contributors = self.github_repository.fetch_contributors(
                repo_owner=repo_owner,
                repo_name=repo_name
            )
            return contributors, None

        except Exception as e:
            error_msg = f"Failed to fetch contributors: {str(e)}"
            self.logger.error(error_msg)
            return ["غير متوفر"], error_msg