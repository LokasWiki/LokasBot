import unittest
from unittest.mock import MagicMock

from tasks.copypatrol.presentation.wiki_page_updater import WikiPageUpdater


class TestWikiPageUpdater(unittest.TestCase):
    def setUp(self):
        self.mock_site = MagicMock()
        self.mock_page = MagicMock()
        self.wiki_updater = WikiPageUpdater(site='ar', page_name="Test Page")
        self.wiki_updater.site = self.mock_site
        self.mock_site.Page.return_value = self.mock_page

    def test_update_page(self):
        # Act
        self.wiki_updater.update_page(10)

        # Assert
        expected_text = """[https://copypatrol.toolforge.org/ar/ أداة كشف خرق حقوق النشر] 10

<noinclude>
[[تصنيف:قوالب صيانة ويكيبيديا]]
</noinclude>"""
        self.mock_page.save.assert_called_once_with("تحديث v1.0.0")
        self.assertEqual(self.mock_page.text, expected_text)


if __name__ == '__main__':
    unittest.main()
