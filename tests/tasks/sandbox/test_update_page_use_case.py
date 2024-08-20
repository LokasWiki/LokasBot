import unittest
from unittest.mock import Mock

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.use_cases.update_page_use_case import UpdatePageUseCase


class TestUpdatePageUseCase(unittest.TestCase):
    def test_execute(self):
        """
        Test the execution of the UpdatePageUseCase.

        This test case verifies that the execute method of the UpdatePageUseCase class
        correctly calls the save_page method of the mock repository with the provided page entity.

        Parameters:
            self (TestUpdatePageUseCase): The test case instance.

        Returns:
            None

        Raises:
            AssertionError: If the save_page method of the mock repository is not called once with the provided page entity.
        """
        # Arrange
        mock_repository = Mock()
        use_case = UpdatePageUseCase(mock_repository)
        page = PageEntity(
            title="Test Title",
            text="Test Text",
            summary="Test Summary"
        )

        # Act
        use_case.execute(page)

        # Assert
        mock_repository.save_page.assert_called_once_with(page)


if __name__ == "__main__":
    unittest.main()
