"""
Mock implementation of WikiRepository for testing.
"""

from typing import List, Tuple

from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage
from tasks.photo_lab.domain.repositories.wiki_repository import WikiRepository


class MockWikiRepository(WikiRepository):
    """
    Mock implementation of WikiRepository for unit testing.
    
    This class provides a mock implementation that doesn't require
    actual wiki connectivity, useful for testing use cases.
    """
    
    def __init__(self):
        """Initialize the mock repository with empty data."""
        self.pages = {}  # page_title -> content
        self.templates_in_pages = {}  # page_title -> {template_name: count}
        self.archive_pages = []  # List of (page_number, page_title)
    
    def add_page(self, title: str, content: str) -> None:
        """Add a page to the mock repository."""
        self.pages[title] = content
    
    def add_template_to_page(self, page_title: str, template_name: str, count: int = 1) -> None:
        """Add template occurrence to a page."""
        if page_title not in self.templates_in_pages:
            self.templates_in_pages[page_title] = {}
        self.templates_in_pages[page_title][template_name] = count
    
    def add_archive_page(self, page_number: int, page_title: str) -> None:
        """Add an archive page."""
        self.archive_pages.append((page_number, page_title))
        self.archive_pages.sort(key=lambda x: x[0])
    
    # WikiRepository interface implementation
    
    def get_main_requests_page_content(self) -> str:
        """Get main requests page content."""
        return self.pages.get("ويكيبيديا:ورشة الصور/طلبات", "")
    
    def update_main_requests_page(self, content: str, summary: str) -> bool:
        """Update main requests page."""
        self.pages["ويكيبيديا:ورشة الصور/طلبات"] = content
        return True
    
    def get_request_page_content(self, page_title: str) -> str:
        """Get request page content."""
        return self.pages.get(page_title, "")
    
    def has_template(self, page_title: str, template_name: str) -> bool:
        """Check if page has template."""
        page_templates = self.templates_in_pages.get(page_title, {})
        return template_name in page_templates and page_templates[template_name] > 0
    
    def get_all_archive_pages(self, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> List[Tuple[int, str]]:
        """Get all archive pages."""
        return self.archive_pages.copy()
    
    def get_archive_page_content(self, page_number: int, base_prefix: str = "ويكيبيديا:ورشة الصور/أرشيف") -> str:
        """Get archive page content."""
        title = f"{base_prefix} {page_number}"
        return self.pages.get(title, "")
    
    def create_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """Create archive page."""
        self.pages[archive_page.title] = archive_page.get_content()
        self.add_archive_page(archive_page.page_number, archive_page.title)
        return True
    
    def update_archive_page(self, archive_page: ArchivePage, summary: str) -> bool:
        """Update archive page."""
        self.pages[archive_page.title] = archive_page.get_content()
        return True
    
    def page_exists(self, page_title: str) -> bool:
        """Check if page exists."""
        return page_title in self.pages
    
    def count_templates_in_page(self, page_title: str, template_name: str) -> int:
        """Count templates in page."""
        page_templates = self.templates_in_pages.get(page_title, {})
        return page_templates.get(template_name, 0)
