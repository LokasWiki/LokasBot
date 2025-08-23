"""
Domain entity representing a user signature.

This entity encapsulates the core data and behavior related to
user signatures for medal distribution, following Domain-Driven Design principles.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Signature:
    """
    Represents a user signature for medal distribution.

    Attributes:
        text (str): The signature text
        user_name (str): The username associated with the signature
    """

    text: str
    user_name: str

    def __post_init__(self):
        """Validate the signature data after initialization."""
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Signature text must be a non-empty string")
        if not self.user_name or not isinstance(self.user_name, str):
            raise ValueError("Username must be a non-empty string")

    def __str__(self) -> str:
        """String representation of the Signature entity."""
        return f"Signature(user='{self.user_name}')"

    def __repr__(self) -> str:
        """Detailed string representation of the Signature entity."""
        return f"Signature(text='{self.text}', user_name='{self.user_name}')"

    @property
    def is_valid(self) -> bool:
        """
        Check if the signature is valid.

        Returns:
            bool: True if the signature appears to be valid
        """
        return bool(self.text.strip() and self.user_name.strip())

    @property
    def clean_text(self) -> str:
        """
        Get the cleaned signature text.

        Returns:
            str: Cleaned signature text
        """
        return self.text.strip()

    @classmethod
    def create_from_wiki_text(cls, wiki_text: str, user_name: str) -> 'Signature':
        """
        Create a Signature instance from wiki text.

        Args:
            wiki_text (str): The wiki text containing the signature
            user_name (str): The username

        Returns:
            Signature: A Signature instance
        """
        return cls(text=wiki_text.strip(), user_name=user_name)

    @classmethod
    def create_default(cls) -> 'Signature':
        """
        Create a default signature.

        Returns:
            Signature: A default Signature instance
        """
        return cls(
            text="[[مستخدم:لوقا|لوقا]] ([[نقاش المستخدم:لوقا|نقاش]])",
            user_name="لوقا"
        )