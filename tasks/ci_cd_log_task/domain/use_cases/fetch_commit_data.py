"""
Use case for fetching commit data from GitHub.

This use case encapsulates the business logic for retrieving
the latest commit information from GitHub, following the Clean Architecture principles.
"""

import logging
from typing import Optional
from tasks.ci_cd_log_task.domain.entities.commit_info import CommitInfo
from tasks.ci_cd_log_task.domain.repositories.github_repository import GitHubRepository


class FetchCommitData:
    """
    Use case for fetching the latest commit data from GitHub.

    This class contains the business logic for retrieving commit information
    from GitHub, handling errors gracefully and providing fallback values.
    """

    def __init__(self, github_repository: GitHubRepository):
        """
        Initialize the FetchCommitData use case.

        Args:
            github_repository (GitHubRepository): Repository for GitHub operations
        """
        self.github_repository = github_repository
        self.logger = logging.getLogger(__name__)

    def execute(
        self,
        repo_owner: str,
        repo_name: str,
        branch: str = 'main'
    ) -> CommitInfo:
        """
        Execute the use case to fetch the latest commit data.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name
            branch (str): The branch to fetch from (default: 'main')

        Returns:
            CommitInfo: The commit information, or unavailable instance on error
        """
        try:
            self.logger.info(
                f"Fetching latest commit from {repo_owner}/{repo_name} "
                f"branch: {branch}"
            )

            commit_info = self.github_repository.fetch_latest_commit(
                repo_owner=repo_owner,
                repo_name=repo_name,
                branch=branch
            )

            self.logger.info(
                f"Successfully fetched commit: {commit_info.commit_message[:50]}..."
            )
            return commit_info

        except Exception as e:
            error_msg = (
                f"Failed to fetch commit data from {repo_owner}/{repo_name}: {str(e)}"
            )
            self.logger.error(error_msg)

            # Return unavailable commit info as fallback
            return CommitInfo.create_unavailable()

    def execute_with_fallback(
        self,
        repo_owner: str,
        repo_name: str,
        branch: str = 'main'
    ) -> tuple[CommitInfo, Optional[str]]:
        """
        Execute the use case with error information returned.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name
            branch (str): The branch to fetch from (default: 'main')

        Returns:
            tuple[CommitInfo, Optional[str]]: Commit info and error message if any
        """
        try:
            commit_info = self.github_repository.fetch_latest_commit(
                repo_owner=repo_owner,
                repo_name=repo_name,
                branch=branch
            )
            return commit_info, None

        except Exception as e:
            error_msg = f"Failed to fetch commit data: {str(e)}"
            self.logger.error(error_msg)
            return CommitInfo.create_unavailable(), error_msg