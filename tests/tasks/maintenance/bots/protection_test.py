import unittest
from unittest.mock import MagicMock, Mock
from unittest.mock import patch
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

    def test_run_not_have_protection_and_not_have_template(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"
        page.protection.return_value = {}
        text = "Some text without the template."
        summary = "Test summary"

        pb = Protection(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "Some text without the template.")
        self.assertEqual(new_summary, "Test summary")

    def test_run_not_have_protection_and_have_template(self):

        list_of_stub_template = []

        for template in self.templates:
            list_of_stub_template.append("{{" + template + "|1}}")
            list_of_stub_template.append("{{" + template + "|2}}")
            list_of_stub_template.append("{{" + template + "|3}}")
            list_of_stub_template.append("{{" + template + "|4}}")
            list_of_stub_template.append("{{" + template + "|تحويلة}}")
            list_of_stub_template.append("{{" + template + "|نقل}}")
            list_of_stub_template.append("{{" + template + "}}")

        for template in list_of_stub_template:
            page = unittest.mock.Mock()
            page.title.return_value = "Example Page"
            page.protection.return_value = {}
            text = f"{template}Some text without the template."
            summary = "Test summary"

            pb = Protection(page, text, summary)
            new_text, new_summary = pb.__call__()

            self.assertEqual(new_text, text.replace(template, ""),f"error in template {template}")
            self.assertEqual(new_summary, "Test summary، إزالة قالب الحماية",f"error in template {template}")

if __name__ == '__main__':
    unittest.main()
