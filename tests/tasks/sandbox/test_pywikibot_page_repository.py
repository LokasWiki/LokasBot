import unittest
from unittest.mock import Mock, patch

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.repositories.pywikibot_page_repository import PywikibotPageRepository


class TestPywikibotPageRepository(unittest.TestCase):
    @patch('tasks.sandbox.repositories.pywikibot_page_repository.pywikibot.Page')
    @patch('tasks.sandbox.repositories.pywikibot_page_repository.pywikibot.Site')
    def test_save_page(self, mock_site, mock_page):
        """
        Test case for the `save_page` method of the `PywikibotPageRepository` class.

        This test case verifies that the `save_page` method of the `PywikibotPageRepository` class
        correctly saves a page using the `pywikibot` library. It does this by mocking the `pywikibot.Page`
        and `pywikibot.Site` classes and asserting that the `save_page` method calls the appropriate methods
        on the mocked objects.

        Parameters:
            - self: The test case instance.
            - mock_site: A mock object representing the `pywikibot.Site` class.
            - mock_page: A mock object representing the `pywikibot.Page` class.

        Returns:
            None
        """
        # Arrange
        mock_site.return_value = Mock()
        mock_page_instance = Mock()
        mock_page.return_value = mock_page_instance

        repository = PywikibotPageRepository()
        page = PageEntity(
            title="Test Title",
            text="Test Text",
            summary="Test Summary"
        )

        # Act
        repository.save_page(page)

        # Assert
        mock_page.assert_called_once_with(mock_site.return_value, page.title)
        mock_page_instance.text = page.text
        mock_page_instance.save.assert_called_once_with(summary=page.summary)


if __name__ == "__main__":
    unittest.main()
