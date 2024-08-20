import unittest
from unittest.mock import MagicMock

from tasks.copypatrol.domain.use_cases.get_open_cases import GetOpenCases


class TestGetOpenCases(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock()
        self.use_case = GetOpenCases(self.mock_repository)

    def test_execute(self):
        # Arrange
        self.mock_repository.count_open_cases.return_value = 5

        # Act
        result = self.use_case.execute(lang='ar', project='wikipedia')

        # Assert
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
