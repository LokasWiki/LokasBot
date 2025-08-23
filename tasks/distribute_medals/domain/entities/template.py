"""
Domain entity representing a medal template.

This entity encapsulates the core data and behavior related to
medal templates for distribution, following Domain-Driven Design principles.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    """
    Represents a formatted template for medal distribution.

    Attributes:
        stub (str): The template stub with placeholders
        number (int): The medal number
        signature (str): The signature to use
        username (str): The target username
    """

    stub: str
    number: int
    signature: str
    username: str

    def __post_init__(self):
        """Validate the template data after initialization."""
        if not self.stub or not isinstance(self.stub, str):
            raise ValueError("Template stub must be a non-empty string")
        if self.number <= 0:
            raise ValueError("Medal number must be positive")
        if not self.signature or not isinstance(self.signature, str):
            raise ValueError("Signature must be a non-empty string")
        if not self.username or not isinstance(self.username, str):
            raise ValueError("Username must be a non-empty string")

    def __str__(self) -> str:
        """String representation of the Template entity."""
        return f"Template(number={self.number}, user='{self.username}')"

    def __repr__(self) -> str:
        """Detailed string representation of the Template entity."""
        return (
            f"Template(stub='{self.stub[:30]}...', "
            f"number={self.number}, "
            f"signature='{self.signature[:20]}...', "
            f"username='{self.username}')"
        )

    @property
    def formatted_message(self) -> str:
        """
        Get the fully formatted template message.

        Returns:
            str: The formatted message ready for sending
        """
        return self.stub.replace('NUMBER', str(self.number)).replace(
            'USERNAME', self.username
        ).replace('SIGNATURE', self.signature)

    @property
    def page_title(self) -> str:
        """
        Get the wiki page title for this template.

        Returns:
            str: The page title
        """
        return f"وسام {self.number} تعديل"

    @property
    def section_title(self) -> str:
        """
        Get the section title for this template.

        Returns:
            str: The section title
        """
        return f"وسام {self.number} تعديل!"

    def get_full_message(self) -> str:
        """
        Get the complete message including section header.

        Returns:
            str: The complete formatted message
        """
        section = f"== {self.section_title} ==\n\n"
        return section + self.formatted_message