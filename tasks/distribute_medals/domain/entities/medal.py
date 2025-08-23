"""
Domain entity representing a medal configuration.

This entity encapsulates the core data and behavior related to
medal configurations, following Domain-Driven Design principles.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Medal:
    """
    Represents a medal configuration for distribution.

    Attributes:
        number (int): The medal number/threshold
        query (str): SQL query to find eligible users
        template_stub (str): Template string for the medal message
        description (Optional[str]): Optional description of the medal
    """

    number: int
    query: str
    template_stub: str
    description: Optional[str] = None

    def __post_init__(self):
        """Validate the medal configuration after initialization."""
        if self.number <= 0:
            raise ValueError("Medal number must be positive")
        if not self.query or not isinstance(self.query, str):
            raise ValueError("Query must be a non-empty string")
        if not self.template_stub or not isinstance(self.template_stub, str):
            raise ValueError("Template stub must be a non-empty string")

    def __str__(self) -> str:
        """String representation of the Medal entity."""
        desc = self.description or 'No description'
        return f"Medal(number={self.number}, description='{desc}')"

    def __repr__(self) -> str:
        """Detailed string representation of the Medal entity."""
        return (
            f"Medal(number={self.number}, "
            f"query='{self.query[:50]}...', "
            f"template_stub='{self.template_stub[:50]}...', "
            f"description='{self.description}')"
        )

    def get_formatted_template(self, username: str, signature: str) -> str:
        """
        Format the template with the given username and signature.

        Args:
            username (str): The username to insert
            signature (str): The signature to insert

        Returns:
            str: Formatted template message
        """
        return self.template_stub.replace('NUMBER', str(self.number)).replace(
            'USERNAME', username
        ).replace('SIGNATURE', signature)

    def get_page_title(self) -> str:
        """
        Get the wiki page title for this medal.

        Returns:
            str: Formatted page title
        """
        return f"وسام {self.number} تعديل"