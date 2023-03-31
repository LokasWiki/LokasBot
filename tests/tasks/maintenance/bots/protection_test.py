import unittest
from unittest.mock import MagicMock

from tasks.maintenance.bots.protection import Protection


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.templates = [
            "محمية",
            "Protected",
            "حماية خاصة",
            "حماية نزاع",
            "Pp-semi-template",
            "Pp-semi-vandalism",
            "Pp-dispute",
            "قفل",
            "Pp-semi-protected",
            "Pp-move-indef",
            "Pp-protected",
            "حماية كلية",
            "حماية حرب",
            "حماية جزئية",
            "Pp-semi",
            "حماية كاملة",
            "حماية",
            "صفحة محمية",
            "Semi-protection",
            "Pp-semi-indef",
            "شبه محمي",
            "حماية تخريب"
        ]

    def test_check_page_and_this_page_not_have_protection(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.")
        self.assertEqual(new_summary, "Test summary")

        # for Redirect
        page.isRedirectPage.return_value = True

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.")
        self.assertEqual(new_summary, "Test summary")

    def test_check_page_and_this_page_not_have_protection_but_have_protection_banner(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {}
        page.isRedirectPage.return_value = False
        text = "{{محمية}}Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.")
        self.assertEqual(new_summary, "Test summary، إزالة قالب الحماية")

        # for Redirect
        page.isRedirectPage.return_value = True

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.")
        self.assertEqual(new_summary, "Test summary، إزالة قالب الحماية")

    def test_check_page_and_this_page_have_autoconfirmed_protection_but_not_have_protection_banner(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {'edit': ('autoconfirmed', 'infinity'), 'move': ('autoconfirmed', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|1}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for move only
        page.protection.return_value = {'move': ('autoconfirmed', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|نقل}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for Redirect
        page.isRedirectPage.return_value = True

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.\n{{محمية|تحويلة}}")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

    def test_check_page_and_this_page_have_editautoreviewprotected_protection_but_not_have_protection_banner(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {'edit': ('editautoreviewprotected', 'infinity'),
                                        'move': ('editautoreviewprotected', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|4}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for move only
        page.protection.return_value = {'move': ('editautoreviewprotected', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|نقل}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for Redirect
        page.isRedirectPage.return_value = True

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.\n{{محمية|تحويلة}}")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

    def test_check_page_and_this_page_have_editeditorprotected_protection_but_not_have_protection_banner(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {'edit': ('editeditorprotected', 'infinity'),
                                        'move': ('editeditorprotected', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|2}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for move only
        page.protection.return_value = {'move': ('editeditorprotected', 'infinity')}
        page.isRedirectPage.return_value = False
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "{{محمية|نقل}}\nSome text without the template.")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")

        # for Redirect
        page.isRedirectPage.return_value = True

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.\n{{محمية|تحويلة}}")
        self.assertEqual(new_summary, "Test summary، بوت:إضافة قالب حماية")


if __name__ == '__main__':
    unittest.main()
