from typing import List, Protocol

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.use_cases.page_repository import PageRepository
from tasks.sandbox.observers.page_update_observer import PageUpdateObserver
from tasks.sandbox.use_cases.update_strategies import UpdateStrategy, ReplaceContentStrategy


class PageRepository(Protocol):
    def save_page(self, page: PageEntity) -> None:
        """
        Save a PageEntity object to the repository.

        Args:
            page (PageEntity): The PageEntity object to be saved.

        Returns:
            None: This function does not return anything.
        """
        ...


class UpdatePageUseCase:
    def __init__(self, repository: PageRepository):
        """
        Initialize the use case with a repository.

        Args:
            repository (PageRepository): The repository to use for page operations.
        """
        self.repository = repository
        self.observers: List[PageUpdateObserver] = []
        self.update_strategy: UpdateStrategy = ReplaceContentStrategy()

    def add_observer(self, observer: PageUpdateObserver) -> None:
        """Add an observer to monitor page updates"""
        self.observers.append(observer)

    def set_strategy(self, strategy: UpdateStrategy) -> None:
        """Set the strategy for updating page content"""
        self.update_strategy = strategy

    def notify_observers(self, page: PageEntity) -> None:
        """Notify all observers about a page update"""
        for observer in self.observers:
            observer.update(page)

    def execute(self, page: PageEntity) -> None:
        """
        Execute the use case to update a page.

        This will update the page content according to the selected strategy
        and notify all observers.

        Args:
            page (PageEntity): The page entity containing the new content.
        """
        # Get current page content if it exists
        try:
            current_page = self.repository.get_page(page.title)
            current_content = current_page.text
        except:
            current_content = ""

        # Prepare new content using the strategy
        page.text = self.update_strategy.prepare_content(current_content, page.text)

        # Save the page
        self.repository.save_page(page)

        # Notify observers
        self.notify_observers(page)
