"""
Domain entity representing commit information from GitHub.

This entity encapsulates the core data and behavior related to
GitHub commit information, following Domain-Driven Design principles.
"""

from datetime import datetime


class CommitInfo:
    """
    Represents commit information from GitHub.

    Attributes:
        commit_message (str): The commit message
        commit_date (str): The commit date in ISO format
        commit_html_url (str): The HTML URL to the commit on GitHub
        last_commit_author (str): The name of the commit author
    """

    def __init__(
        self,
        commit_message: str,
        commit_date: str,
        commit_html_url: str,
        last_commit_author: str
    ):
        """
        Initialize a new CommitInfo entity.

        Args:
            commit_message (str): The commit message
            commit_date (str): The commit date in ISO format
            commit_html_url (str): The HTML URL to the commit on GitHub
            last_commit_author (str): The name of the commit author
        """
        self.commit_message = commit_message
        self.commit_date = commit_date
        self.commit_html_url = commit_html_url
        self.last_commit_author = last_commit_author

    def __str__(self) -> str:
        """String representation of the CommitInfo entity."""
        short_msg = self.commit_message[:50]
        return f"CommitInfo(message='{short_msg}...', author='{self.last_commit_author}')"

    def __repr__(self) -> str:
        """Detailed string representation of the CommitInfo entity."""
        return (
            "CommitInfo(commit_message='{self.commit_message}', "
            "commit_date='{self.commit_date}', "
            "commit_html_url='{self.commit_html_url}', "
            "last_commit_author='{self.last_commit_author}')"
        )

    def __eq__(self, other) -> bool:
        """Check equality based on commit HTML URL (primary identifier)."""
        if not isinstance(other, CommitInfo):
            return False
        return self.commit_html_url == other.commit_html_url

    def __hash__(self) -> int:
        """Hash based on commit HTML URL."""
        return hash(self.commit_html_url)

    def format_commit_date(self) -> str:
        """
        Format the commit date for display.

        Returns:
            str: Formatted commit date string
        """
        if self.commit_date == "غير متوفر":
            return self.commit_date

        try:
            # Parse ISO format and format for display
            iso_date = self.commit_date.replace('Z', '+00:00')
            dt = datetime.fromisoformat(iso_date)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, AttributeError):
            return self.commit_date

    @classmethod
    def create_unavailable(cls) -> 'CommitInfo':
        """
        Create a CommitInfo instance with default unavailable values.

        Returns:
            CommitInfo: A CommitInfo instance with unavailable values
        """
        return cls(
            commit_message="غير متوفر",
            commit_date="غير متوفر",
            commit_html_url="غير متوفر",
            last_commit_author="غير متوفر"
        )