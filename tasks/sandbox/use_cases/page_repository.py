from abc import ABC, abstractmethod
from tasks.sandbox.entities.page_entity import PageEntity


class PageRepository(ABC):
    @abstractmethod
    def save_page(self, page: PageEntity) -> None:
        """Save or update a page with new content"""
        pass

    @abstractmethod
    def get_page(self, title: str) -> PageEntity:
        """Get a page by its title"""
        pass 