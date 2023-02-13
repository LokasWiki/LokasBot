import unittest
import unittest.mock

from tasks.sandbox.clear import page_title, page_text, page_summary, main


class TestMain(unittest.TestCase):
    @unittest.mock.patch("pywikibot.Site")
    @unittest.mock.patch("pywikibot.Page")
    def test_main_sets_page_text_and_summary(self, mock_Page, mock_Site):
        mock_site = mock_Site.return_value
        mock_page = mock_Page.return_value

        main()

        mock_Page.assert_called_with(mock_site, page_title)
        self.assertEqual(mock_page.text, page_text)
        mock_page.save.assert_called_with(summary=page_summary)

    @unittest.mock.patch("pywikibot.Site")
    @unittest.mock.patch("pywikibot.Page")
    def test_main_sets_default_text_when_page_does_not_exist(self, mock_Page, mock_Site):
        mock_site = mock_Site.return_value
        mock_page = mock_Page.return_value
        mock_page.exists.return_value = False

        main()

        self.assertEqual(mock_page.text, page_text)

    @unittest.mock.patch("pywikibot.Site")
    @unittest.mock.patch("pywikibot.Page")
    def test_main_raises_exception_when_saving_page_fails(self, mock_Page, mock_Site):
        mock_site = mock_Site.return_value
        mock_page = mock_Page.return_value
        mock_page.save.side_effect = Exception("Failed to save page")

        with self.assertRaises(Exception):
            main()

    @unittest.mock.patch("pywikibot.Site")
    @unittest.mock.patch("pywikibot.Page")
    def test_main_returns_zero(self, mock_Page, mock_Site):
        result = main()
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
