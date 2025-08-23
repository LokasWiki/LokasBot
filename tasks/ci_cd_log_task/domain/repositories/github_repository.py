"""
Repository interface for GitHub operations.

This interface defines the contract for GitHub data access operations,
following the Repository pattern to abstract data access from business logic.
"""

from abc import ABC, abstractmethod
from typing import List
from tasks.ci_cd_log_task.domain.entities.commit_info import CommitInfo


class GitHubRepository(ABC):
    """
    Abstract repository interface for GitHub operations.

    This interface defines the contract for data access operations
    related to GitHub, allowing for different implementations
    (e.g., GitHub API, mock implementations).
    """

    @abstractmethod
    def fetch_latest_commit(
        self,
        repo_owner: str,
        repo_name: str,
        branch: str = 'main'
    ) -> CommitInfo:
        """
        Fetch the latest commit from a GitHub repository.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name
            branch (str): The branch to fetch from (default: 'main')

        Returns:
            CommitInfo: The latest commit information

        Raises:
            Exception: If the commit data cannot be fetched
        """
        pass

    @abstractmethod
    def fetch_contributors(
        self,
        repo_owner: str,
        repo_name: str
    ) -> List[str]:
        """
        Fetch the list of contributors from a GitHub repository.

        Args:
            repo_owner (str): The repository owner/organization
            repo_name (str): The repository name

        Returns:
            List[str]: List of contributor names with contribution info

        Raises:
            Exception: If the contributor data cannot be fetched
        """
        pass