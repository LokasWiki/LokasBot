import unittest
import unittest.mock
import random
from tasks.maintenance.bots.portals_merge import PortalsMerge


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.list_of_templates = [
            "صندوق بوابات",
            "Portal box",
            "مجموعة بوابات",
            "Portail",
            "وصلة بوابة",
            "صندوق بوابة",
            "Portal bar",
            "شب",
            "شريط بوابة",
            "شريط البوابات",
            "شريط بوابات",
            "بوابة",
            "Portal"
        ]

    def test_run_if_no_portals_template_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "Some text without the template."
        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, text)
        self.assertEqual(new_summary, summary)


if __name__ == "__main__":
    unittest.main()
