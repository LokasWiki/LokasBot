import unittest

from tasks.sandbox.entities.page_entity import PageEntity


class TestPageEntity(unittest.TestCase):
    def test_initialization(self):
        """
        Test the initialization of the PageEntity class.

        This test case checks if the attributes of the PageEntity object are correctly initialized
        when creating a new instance of the class. It creates a PageEntity object with the
        specified title, text, and summary values. Then, it asserts that the title, text, and
        summary attributes of the object are equal to the expected values.

        Parameters:
            self (TestPageEntity): The current test case instance.

        Returns:
            None
        """
        page = PageEntity(
            title="Test Title",
            text="Test Text",
            summary="Test Summary"
        )
        self.assertEqual(page.title, "Test Title")
        self.assertEqual(page.text, "Test Text")
        self.assertEqual(page.summary, "Test Summary")


if __name__ == "__main__":
    unittest.main()
