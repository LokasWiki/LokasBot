"""
Domain entity representing a Wiki Page.

This entity encapsulates the core data and behavior of a wiki page,
following Domain-Driven Design principles.
"""


class Page:
    """
    Represents a wiki page with its essential properties.

    Attributes:
        title (str): The title of the wiki page
        content (str): The content/text of the wiki page
        creation_message (str): The message to use when creating the page
    """

    def __init__(self, title: str, content: str, creation_message: str = ""):
        """
        Initialize a new Page entity.

        Args:
            title (str): The title of the wiki page
            content (str): The content/text of the wiki page
            creation_message (str, optional): The message to use when
                creating the page. Defaults to empty string.
        """
        self.title = title
        self.content = content
        self.creation_message = creation_message

    def __str__(self) -> str:
        """String representation of the Page entity."""
        content_len = len(self.content)
        return f"Page(title='{self.title}', content_length={content_len})"

    def __repr__(self) -> str:
        """Detailed string representation of the Page entity."""
        content_preview = self.content[:50] if self.content else ""
        return (f"Page(title='{self.title}', "
                f"content='{content_preview}...', "
                f"creation_message='{self.creation_message}')")

    def __eq__(self, other) -> bool:
        """Check equality based on title (primary identifier)."""
        if not isinstance(other, Page):
            return False
        return self.title == other.title

    def __hash__(self) -> int:
        """Hash based on title."""
        return hash(self.title)