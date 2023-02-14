import unittest
from unittest.mock import MagicMock
import random
from tasks.maintenance.bots.portals_merge import PortalsMerge
import wikitextparser as wtp


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
        self.assertEqual(new_summary, "Test summary")

    def test_run_if_portals_template_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "{{شريط بوابات|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=True)
        new_text, new_summary = pb.__call__()

        self.assertEqual(len(new_text), len("{{شريط بوابات|نمط=قائمة|مصر|فيزياء|كيمياء}}\n"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_portals_template_found_with_all_not_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{شريط بوابات|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=False)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "test")
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_portals_template_found_with_one_not_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "{{شريط بوابات|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)

        def side_effect_func(value):
            if value == "مصر":
                return False
            return True

        pb.check_portal = MagicMock(side_effect=side_effect_func)
        new_text, new_summary = pb.__call__()

        self.assertEqual(len(new_text), len("{{شريط بوابات|نمط=قائمة|فيزياء|كيمياء}}\n"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_portals_template_found_with_not_same_temaplte(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "{{بوابة|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=True)
        new_text, new_summary = pb.__call__()

        self.assertEqual(len(new_text), len("{{شريط بوابات|نمط=قائمة|مصر|فيزياء|كيمياء}}\n"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_with_empty_portals_template(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{بوابة|        }}{{شريط بوابات|نمط=قائمة}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=True)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "test")
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_portals_template_found_with_not_same_temaplte_with_all_not_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{بوابة|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=False)
        new_text, new_summary = pb.__call__()

        self.assertEqual(new_text, "test")
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_portals_template_found_with_not_same_temaplte_with_one_not_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "{{بوابة|كيمياء|فيزياء}}{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)

        def side_effect_func(value):
            if value == "مصر":
                return False
            return True

        pb.check_portal = MagicMock(side_effect=side_effect_func)
        new_text, new_summary = pb.__call__()

        self.assertEqual(len(new_text), len("{{شريط بوابات|نمط=قائمة|فيزياء|كيمياء}}\n"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_one_portals_template_found_all_portals_found(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}test"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)
        pb.check_portal = MagicMock(return_value=True)
        new_text, new_summary = pb.__call__()

        self.assertEqual(len(new_text), len(text))
        self.assertEqual(text, new_text)
        self.assertEqual(new_summary, summary)

    def test_run_if_one_portals_template_found_all_portals_found_expect_one(self):
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}test"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)

        def side_effect_func(value):
            if value == "مصر":
                return False
            return True

        pb.check_portal = MagicMock(side_effect=side_effect_func)
        new_text, new_summary = pb.__call__()
        print(new_text)
        self.assertEqual(len(new_text), len("{{شريط بوابات|نمط=قائمة|فيزياء}}testtest\n"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")

    def test_run_if_one_portals_template_found_all_portals_not_found(self):
        # test
        page = unittest.mock.Mock()
        page.title.return_value = "Example Page"

        text = "test{{شريط بوابات|نمط=قائمة|مصر|فيزياء}}test"

        summary = "Test summary"
        pb = PortalsMerge(page, text, summary)

        def side_effect_func(value):
            return False

        pb.check_portal = MagicMock(side_effect=side_effect_func)
        new_text, new_summary = pb.__call__()
        print(new_text)
        self.assertEqual(len(new_text), len("testtest"))
        self.assertEqual(new_summary, "Test summary، فحص بوابات")


if __name__ == "__main__":
    unittest.main()
