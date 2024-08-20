import unittest
from unittest.mock import MagicMock

from tasks.copypatrol.data.mysql_copyright_repository import MySQLCopyrightRepository


class TestMySQLCopyrightRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.repository = MySQLCopyrightRepository(self.mock_db)

    def test_count_open_cases(self):
        # Arrange
        self.mock_db.execute_query.return_value = (5,)

        # Act
        count = self.repository.count_open_cases(lang='ar', project='wikipedia')

        # Assert
        self.assertEqual(count, 5)


if __name__ == '__main__':
    unittest.main()
