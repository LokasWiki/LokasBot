import unittest
from unittest.mock import Mock, patch

from tasks.sandbox.main import main


class TestMain(unittest.TestCase):
    @patch('tasks.sandbox.main.UpdatePageUseCase')
    @patch('tasks.sandbox.main.PywikibotPageRepository')
    @patch('tasks.sandbox.main.PageEntity')
    def test_main(self, mock_page_entity, mock_repository, mock_use_case):
        """
        Test the main function of the sandbox.main module.

        This function tests the main function of the sandbox.main module by mocking the dependencies and
        verifying that the function returns 0 and that the necessary methods are called.

        Parameters:
            self (TestMain): The test case instance.
            mock_page_entity (Mock): A mock object for the PageEntity class.
            mock_repository (Mock): A mock object for the PywikibotPageRepository class.
            mock_use_case (Mock): A mock object for the UpdatePageUseCase class.

        Returns:
            None

        Raises:
            AssertionError: If the result of the main function is not equal to 0 or if the necessary methods
                            are not called.

        """
        # Arrange
        mock_page_entity.return_value = mock_page_entity
        mock_use_case_instance = Mock()
        mock_use_case.return_value = mock_use_case_instance

        # Act
        result = main()

        # Assert
        self.assertEqual(result, 0)
        mock_use_case_instance.execute.assert_called_once()
        mock_page_entity.assert_called_once_with(
            title="ويكيبيديا:ملعب",
            text="{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->",
            summary="بوت: إفراغ الصفحة تلقائيا!"
        )


if __name__ == "__main__":
    unittest.main()
