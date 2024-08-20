from typing import Protocol

from tasks.sandbox.entities.page_entity import PageEntity


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
        Initializes a new instance of the `UpdatePageUseCase` class.

        Args:
            repository (PageRepository): The repository object used to save the page.

        Returns:
            None
        """
        self.repository = repository

    def execute(self, page: PageEntity) -> None:
        """
        Execute the update page use case.

        This method updates a page entity by saving it to the repository.

        Parameters:
            page (PageEntity): The page entity to be saved.

        Returns:
            None: This function does not return anything.
        """
        self.repository.save_page(page)
