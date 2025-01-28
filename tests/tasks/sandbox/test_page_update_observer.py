import unittest
import os
from unittest.mock import patch
from io import StringIO

from tasks.sandbox.entities.page_entity import PageEntity
from tasks.sandbox.observers.page_update_observer import ConsoleLogger, FileLogger


class TestPageUpdateObserver(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.page = PageEntity(
            title="Test Title",
            text="Test Text",
            summary="Test Summary"
        )
        self.test_log_file = "test_updates.log"

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    @patch('sys.stdout', new_callable=StringIO)
    def test_console_logger(self, mock_stdout):
        """Test console logger output"""
        logger = ConsoleLogger()
        logger.update(self.page)
        
        output = mock_stdout.getvalue()
        self.assertIn("Test Title", output)
        self.assertIn("Test Summary", output)

    def test_file_logger(self):
        """Test file logger output"""
        logger = FileLogger(self.test_log_file)
        logger.update(self.page)
        
        self.assertTrue(os.path.exists(self.test_log_file))
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test Title", content)
            self.assertIn("Test Summary", content)

    def test_file_logger_with_unicode(self):
        """Test file logger with unicode content"""
        page = PageEntity(
            title="صفحة تجريبية",
            text="محتوى تجريبي 🌟",
            summary="تلخيص التعديل"
        )
        
        logger = FileLogger(self.test_log_file)
        logger.update(page)
        
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("صفحة تجريبية", content)
            self.assertIn("تلخيص التعديل", content)

    def test_multiple_updates_to_file(self):
        """Test multiple updates to the same log file"""
        logger = FileLogger(self.test_log_file)
        
        # First update
        logger.update(self.page)
        
        # Second update with different page
        second_page = PageEntity(
            title="Second Title",
            text="Second Text",
            summary="Second Summary"
        )
        logger.update(second_page)
        
        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Test Title", content)
            self.assertIn("Test Summary", content)
            self.assertIn("Second Title", content)
            self.assertIn("Second Summary", content)


if __name__ == "__main__":
    unittest.main() 