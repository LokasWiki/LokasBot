import unittest
from unittest.mock import MagicMock

from tasks.copypatrol.data.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.database = Database(config={
            'host': 'localhost',
            'port': 3306,
            'username': 'user',
            'password': 'pass',
            'database': 'test_db'
        })
        self.database.conn = self.mock_conn

    def test_execute_query(self):
        # Arrange
        self.mock_cursor.fetchone.return_value = (10,)

        # Act
        result = self.database.execute_query("SELECT COUNT(*) FROM test_table")

        # Assert
        self.assertEqual(result, (10,))

    def tearDown(self):
        self.database.close()


if __name__ == '__main__':
    unittest.main()
