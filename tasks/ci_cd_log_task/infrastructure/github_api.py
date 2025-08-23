"""
Infrastructure layer for GitHub API operations.

This module provides the concrete implementation of the GitHubRepository interface,
handling all external GitHub API interactions.
"""

import logging
import requests
from typing import List
from tasks.ci_cd_log_task.domain.entities.commit_info import CommitInfo
from tasks.ci_cd_log_task.domain.repositories.github_repository import GitHubRepository


class GitHubAPI(GitHubRepository):
    """
    Concrete implementation of GitHubRepository using the GitHub API.

    This class handles all interactions with the GitHub API,
    implementing the GitHubRepository interface.
    """

    def __init__(self, base_url: str = "https://api.github.com"):
        """
        Initialize the GitHubAPI with configuration.

        Args:
            base_url (str): Base URL for GitHub API (default: official API)
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

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
            requests.RequestException: If the API request fails
        """
        try:
            # Get branch information
            branch_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/branches/{branch}"
            self.logger.info(f"Fetching branch info from: {branch_url}")

            response = requests.get(branch_url)
            response.raise_for_status()
            branch_data = response.json()

            # Get commit SHA
            commit_sha = branch_data['commit']['sha']
            self.logger.info(f"Latest commit SHA: {commit_sha}")

            # Get detailed commit information
            commit_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
            self.logger.info(f"Fetching commit details from: {commit_url}")

            commit_response = requests.get(commit_url)
            commit_response.raise_for_status()
            commit_data = commit_response.json()

            # Extract commit information
            commit_message = commit_data['commit']['message']
            commit_date = commit_data['commit']['committer']['date']
            commit_html_url = commit_data['html_url']
            last_commit_author = commit_data['commit']['committer']['name']

            return CommitInfo(
                commit_message=commit_message,
                commit_date=commit_date,
                commit_html_url=commit_html_url,
                last_commit_author=last_commit_author
            )

        except requests.RequestException as e:
            error_msg = f"Failed to fetch commit from GitHub API: {str(e)}"
            self.logger.error(error_msg)
            raise
        except KeyError as e:
            error_msg = f"Unexpected response format from GitHub API: {str(e)}"
            self.logger.error(error_msg)
            raise requests.RequestException(error_msg)

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
            requests.RequestException: If the API request fails
        """
        try:
            contributors_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/contributors"
            self.logger.info(f"Fetching contributors from: {contributors_url}")

            response = requests.get(contributors_url)
            response.raise_for_status()
            contributors_data = response.json()

            # Format contributors list
            contributors = []
            for contributor in contributors_data:
                name = contributor['login']
                contributions = contributor['contributions']
                contributors.append(f"{name} ({contributions} مساهمة)")

            self.logger.info(f"Fetched {len(contributors)} contributors")
            return contributors

        except requests.RequestException as e:
            error_msg = f"Failed to fetch contributors from GitHub API: {str(e)}"
            self.logger.error(error_msg)
            raise
        except KeyError as e:
            error_msg = f"Unexpected response format from GitHub API: {str(e)}"
            self.logger.error(error_msg)
            raise requests.RequestException(error_msg)