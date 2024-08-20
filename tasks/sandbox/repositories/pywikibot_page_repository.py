import pywikibot

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.use_cases.update_page_use_case import PageRepository


class PywikibotPageRepository(PageRepository):
    def __init__(self):
        """
        Initializes the PywikibotPageRepository class.

        This method creates an instance of the PywikibotPageRepository class and sets the `site` attribute to the current site object obtained from the pywikibot library.

        Parameters:
            None

        Returns:
            None
        """
        self.site = pywikibot.Site()

    def save_page(self, page: PageEntity) -> None:
        """
        Saves a page using the Pywikibot library.

        Args:
            page (PageEntity): The page entity to be saved.

        Returns:
            None: This function does not return anything.

        Raises:
            pywikibot.Error: If there is an error while saving the page.

        This function takes a `PageEntity` object as input and saves it using the Pywikibot library. It creates a `pywikibot.Page` object with the `title` attribute of the `page` parameter and sets its `text` attribute to the `text` attribute of the `page` parameter. Finally, it saves the page with the `summary` attribute of the `page` parameter.

        Note:
            - The `PageEntity` object should have the `title` and `text` attributes.
            - The `summary` attribute of the `page` parameter is used as the summary for the page save operation.
        """
        pywikibot_page = pywikibot.Page(self.site, page.title)
        pywikibot_page.text = page.text
        pywikibot_page.save(summary=page.summary)
