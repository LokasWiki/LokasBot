"""
Domain entity representing a Wiki Category.

This entity encapsulates the core data and behavior of a wiki category,
following Domain-Driven Design principles.
"""


class Category:
    """
    Represents a wiki category with its essential properties.

    Attributes:
        name (str): The name of the wiki category
        template (str): The template content for the category
        creation_message (str): The message to use when creating the category
    """

    def __init__(self, name: str, template: str, creation_message: str = ""):
        """
        Initialize a new Category entity.

        Args:
            name (str): The name of the wiki category
            template (str): The template content for the category
            creation_message (str, optional): The message to use when
                creating the category. Defaults to empty string.
        """
        self.name = name
        self.template = template
        self.creation_message = creation_message

    def __str__(self) -> str:
        """String representation of the Category entity."""
        template_len = len(self.template)
        return f"Category(name='{self.name}', template_length={template_len})"

    def __repr__(self) -> str:
        """Detailed string representation of the Category entity."""
        template_preview = self.template[:50] if self.template else ""
        return (f"Category(name='{self.name}', "
                f"template='{template_preview}...', "
                f"creation_message='{self.creation_message}')")

    def __eq__(self, other) -> bool:
        """Check equality based on name (primary identifier)."""
        if not isinstance(other, Category):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on name."""
        return hash(self.name)