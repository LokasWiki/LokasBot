"""
Domain entity representing a Photo Workshop request.

This entity represents a photo request extracted from the main requests page,
containing the page name and related metadata.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PhotoRequest:
    """
    Entity representing a photo workshop request.
    
    Attributes:
        page_name: The name of the page being requested (extracted from template)
        template_text: The full template text as it appears on the main page
        has_perspective: Whether the request page has a "منظور" template
        request_page_title: The full title of the request page
    """
    page_name: str
    template_text: str
    has_perspective: bool = False
    request_page_title: str = ""
    
    def __post_init__(self):
        """Initialize derived attributes after construction."""
        if not self.request_page_title:
            self.request_page_title = f"ويكيبيديا:ورشة الصور/طلبات/{self.page_name}"
    
    def __str__(self) -> str:
        """String representation of the photo request."""
        perspective_status = "has perspective" if self.has_perspective else "no perspective"
        return f"PhotoRequest(page='{self.page_name}', {perspective_status})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"PhotoRequest(page_name='{self.page_name}', "
                f"template_text='{self.template_text[:50]}...', "
                f"has_perspective={self.has_perspective}, "
                f"request_page_title='{self.request_page_title}')")
    
    def mark_as_archivable(self) -> None:
        """Mark this request as ready for archiving (has perspective template)."""
        self.has_perspective = True
    
    def is_ready_for_archive(self) -> bool:
        """Check if this request is ready to be archived."""
        return self.has_perspective
