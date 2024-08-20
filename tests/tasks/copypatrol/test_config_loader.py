import unittest

from tasks.copypatrol.config.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    def test_get_db_config(self):
        # Arrange
        config_loader = ConfigLoader('tests/mock_config.ini')

        # Act
        db_config = config_loader.get_db_config()

        # Assert
        expected_config = {
            'username': 'test_user',
            'password': 'test_pass',
            'host': 'localhost',
            'port': 3306,
            'database': 'test_db'
        }
        self.assertEqual(db_config, expected_config)


if __name__ == '__main__':
    unittest.main()
