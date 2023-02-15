import unittest
from unittest.mock import MagicMock

from core.utils.regex_scanner import RequestsScanner


class TestRequestsScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = RequestsScanner()



if __name__ == "__main__":
    unittest.main()
