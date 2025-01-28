import unittest
from unittest.mock import Mock, patch

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.repositories.pywikibot_page_repository import PywikibotPageRepository


class TestPywikibotPageRepository(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.patcher = patch('pywikibot.Site')
        self.mock_site = self.patcher.start()
        self.repository = PywikibotPageRepository()
        self.page_entity = PageEntity(
            title="Test Title",
            text="Test Text",
            summary="Test Summary"
        )

    def tearDown(self):
        """Clean up after tests"""
        self.patcher.stop()

    @patch('pywikibot.Page')
    def test_save_page(self, mock_page_class):
        """Test saving a page using pywikibot"""
        # Setup mock
        mock_page = Mock()
        mock_page_class.return_value = mock_page

        # Execute
        self.repository.save_page(self.page_entity)

        # Verify
        mock_page_class.assert_called_once_with(self.repository.site, "Test Title")
        self.assertEqual(mock_page.text, "Test Text")
        mock_page.save.assert_called_once_with(summary="Test Summary")

    @patch('pywikibot.Page')
    def test_get_page(self, mock_page_class):
        """Test retrieving a page using pywikibot"""
        # Setup mock
        mock_page = Mock()
        mock_page.title.return_value = "Test Title"
        mock_page.text = "Existing Text"
        mock_page_class.return_value = mock_page

        # Execute
        result = self.repository.get_page("Test Title")

        # Verify
        mock_page_class.assert_called_once_with(self.repository.site, "Test Title")
        self.assertEqual(result.title, "Test Title")
        self.assertEqual(result.text, "Existing Text")
        self.assertEqual(result.summary, "")

    @patch('pywikibot.Page')
    def test_save_page_with_unicode(self, mock_page_class):
        """Test saving a page with unicode content"""
        # Setup
        page_with_unicode = PageEntity(
            title="صفحة تجريبية",
            text="محتوى تجريبي 🌟",
            summary="تلخيص التعديل"
        )
        mock_page = Mock()
        mock_page_class.return_value = mock_page

        # Execute
        self.repository.save_page(page_with_unicode)

        # Verify
        mock_page_class.assert_called_once_with(self.repository.site, "صفحة تجريبية")
        self.assertEqual(mock_page.text, "محتوى تجريبي 🌟")
        mock_page.save.assert_called_once_with(summary="تلخيص التعديل")

    @patch('pywikibot.Page')
    def test_get_nonexistent_page(self, mock_page_class):
        """Test getting a page that doesn't exist"""
        # Setup mock
        mock_page = Mock()
        mock_page.title.return_value = "Nonexistent Page"
        mock_page.text = ""
        mock_page_class.return_value = mock_page

        # Execute
        result = self.repository.get_page("Nonexistent Page")

        # Verify
        self.assertEqual(result.title, "Nonexistent Page")
        self.assertEqual(result.text, "")
        self.assertEqual(result.summary, "")


if __name__ == "__main__":
    unittest.main()
