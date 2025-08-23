"""
Domain entity representing a user eligible for medal distribution.

This entity encapsulates the core data and behavior related to
users who can receive medals, following Domain-Driven Design principles.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """
    Represents a user eligible for medal distribution.

    Attributes:
        name (str): The username
        edits_before (int): Number of edits before the period
        edits_total (int): Total number of edits during the period
    """

    name: str
    edits_before: int
    edits_total: int

    def __post_init__(self):
        """Validate the user data after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Username must be a non-empty string")
        if self.edits_before < 0:
            raise ValueError("Edits before must be non-negative")
        if self.edits_total < 0:
            raise ValueError("Total edits must be non-negative")

    def __str__(self) -> str:
        """String representation of the User entity."""
        return f"User(name='{self.name}', edits={self.edits_total})"

    def __repr__(self) -> str:
        """Detailed string representation of the User entity."""
        return (
            f"User(name='{self.name}', "
            f"edits_before={self.edits_before}, "
            f"edits_total={self.edits_total})"
        )

    @property
    def is_eligible(self) -> bool:
        """
        Check if the user is eligible for a medal.

        A user is eligible if they have new edits (edits_total > edits_before).

        Returns:
            bool: True if the user is eligible
        """
        return self.edits_total > self.edits_before

    @property
    def new_edits(self) -> int:
        """
        Get the number of new edits during the period.

        Returns:
            int: Number of new edits
        """
        return max(0, self.edits_total - self.edits_before)

    def get_user_talk_page(self) -> str:
        """
        Get the talk page title for this user.

        Returns:
            str: User talk page title
        """
        return f"نقاش المستخدم:{self.name}"

    @classmethod
    def create_from_db_row(cls, row: dict) -> 'User':
        """
        Create a User instance from database row data.

        Args:
            row (dict): Database row containing user data

        Returns:
            User: A User instance
        """
        return cls(
            name=str(row.get('actor_name', '')),
            edits_before=int(row.get('sum_yc', 0)),
            edits_total=int(row.get('sum_tc', 0))
        )