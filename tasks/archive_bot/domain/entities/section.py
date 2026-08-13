"""Domain entity representing a wiki section."""

from dataclasses import dataclass


@dataclass
class Section:
    """A discussion section (thread) on a talk page.

    Attributes:
        heading: The heading text without the surrounding ``=`` markers,
            e.g. ``"عنوان"`` for ``== عنوان ==``.
        content: The raw content that follows the heading line (it starts
            with a newline) up to the next heading or the end of the text.
        heading_markup: The original heading line (e.g. ``== عنوان ==``) used
            for faithful reconstruction. When empty, the heading is rebuilt
            as ``==heading==``.
    """

    heading: str
    content: str
    heading_markup: str = ""

    def to_wikitext(self, level: int = 2) -> str:
        """Return the section as wikitext (heading line + content)."""
        if self.heading_markup:
            return self.heading_markup + self.content
        marker = "=" * level
        return f"{marker}{self.heading}{marker}{self.content}"

    @property
    def size(self) -> int:
        """Return the byte size of the section (MediaWiki page-size style)."""
        return len(self.to_wikitext().encode("utf-8"))
