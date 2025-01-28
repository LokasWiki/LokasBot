import unittest

from tasks.sandbox.entities.page_entity import PageEntity


class TestPageEntity(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.title = "Test Title"
        self.text = "Test Text"
        self.summary = "Test Summary"
        self.page = PageEntity(
            title=self.title,
            text=self.text,
            summary=self.summary
        )

    def test_initialization(self):
        """Test if PageEntity attributes are correctly initialized"""
        self.assertEqual(self.page.title, self.title)
        self.assertEqual(self.page.text, self.text)
        self.assertEqual(self.page.summary, self.summary)

    def test_empty_values(self):
        """Test initialization with empty values"""
        empty_page = PageEntity("", "", "")
        self.assertEqual(empty_page.title, "")
        self.assertEqual(empty_page.text, "")
        self.assertEqual(empty_page.summary, "")

    def test_special_characters(self):
        """Test handling of special characters"""
        special_page = PageEntity(
            title="Title with 特殊字符",
            text="Text with\nnewlines\tand\ttabs",
            summary="Summary with emoji 🚀"
        )
        self.assertEqual(special_page.title, "Title with 特殊字符")
        self.assertEqual(special_page.text, "Text with\nnewlines\tand\ttabs")
        self.assertEqual(special_page.summary, "Summary with emoji 🚀")


if __name__ == "__main__":
    unittest.main()
