import unittest
from unittest.mock import Mock, patch

from tasks.sandbox.main import main


class TestMain(unittest.TestCase):
    @patch('tasks.sandbox.main.UpdatePageUseCase')
    @patch('tasks.sandbox.main.RepositoryFactory.create_repository')
    @patch('tasks.sandbox.main.PageEntity')
    def test_main(self, mock_page_entity, mock_create_repository, mock_use_case):
        """
        Test the main function of the sandbox.main module.

        This test verifies that:
        1. The main function creates a repository using the factory
        2. It initializes the use case with correct observers
        3. It creates and executes the page update with correct parameters
        4. It returns 0 on success
        """
        # Arrange
        mock_page_entity.return_value = Mock(
            title="ويكيبيديا:ملعب",
            text="{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->",
            summary="بوت: إفراغ الصفحة تلقائيا!"
        )
        mock_repository = Mock()
        mock_create_repository.return_value = mock_repository
        mock_use_case_instance = Mock()
        mock_use_case.return_value = mock_use_case_instance

        # Act
        result = main()

        # Assert
        self.assertEqual(result, 0)
        mock_create_repository.assert_called_once()
        mock_use_case.assert_called_once_with(mock_repository)
        mock_use_case_instance.add_observer.assert_called()
        mock_use_case_instance.set_strategy.assert_called_once()
        mock_use_case_instance.execute.assert_called_once()
        mock_page_entity.assert_called_once_with(
            title="ويكيبيديا:ملعب",
            text="{{عنوان الملعب}}\n<!-- مرحبا! خذ راحتك في تجربة مهارتك في التنسيق والتحرير أسفل هذا السطر. هذه الصفحة لتجارب التعديل ، سيتم تفريغ هذه الصفحة كل 12 ساعة. -->",
            summary="بوت: إفراغ الصفحة تلقائيا!"
        )


if __name__ == "__main__":
    unittest.main()
