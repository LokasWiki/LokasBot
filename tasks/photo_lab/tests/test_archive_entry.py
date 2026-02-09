"""
Unit tests for the ArchiveEntry and ArchivePage entities.
"""

import unittest
from datetime import datetime

from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage


class TestArchiveEntry(unittest.TestCase):
    """Test cases for ArchiveEntry entity."""
    
    def test_create_archive_entry(self):
        """Test creating an archive entry."""
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}",
            archive_page_number=5
        )
        
        self.assertEqual(entry.page_name, "Test Page")
        self.assertEqual(entry.template_text, "{{طلب ورشة صور|Test Page}}")
        self.assertEqual(entry.archive_page_number, 5)
        self.assertIsNotNone(entry.archived_at)
        self.assertIsInstance(entry.archived_at, datetime)
    
    def test_get_archive_page_title(self):
        """Test getting archive page title."""
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}",
            archive_page_number=42
        )
        
        title = entry.get_archive_page_title()
        self.assertEqual(title, "ويكيبيديا:ورشة الصور/أرشيف 42")
    
    def test_format_for_archive(self):
        """Test formatting for archive."""
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        formatted = entry.format_for_archive()
        self.assertIn("{{طلب ورشة صور|Test Page}}", formatted)


class TestArchivePage(unittest.TestCase):
    """Test cases for ArchivePage entity."""
    
    def test_create_archive_page(self):
        """Test creating an archive page."""
        page = ArchivePage(page_number=1)
        
        self.assertEqual(page.page_number, 1)
        self.assertEqual(page.title, "ويكيبيديا:ورشة الصور/أرشيف 1")
        self.assertEqual(page.entry_count, 0)
        self.assertEqual(page.entries, [])
    
    def test_is_full_empty(self):
        """Test is_full with empty archive."""
        page = ArchivePage(page_number=1)
        self.assertFalse(page.is_full())
    
    def test_is_full_at_limit(self):
        """Test is_full at the limit."""
        page = ArchivePage(page_number=1)
        
        # Add 10 entries
        for i in range(10):
            entry = ArchiveEntry(
                page_name=f"Page {i}",
                template_text=f"{{{{طلب ورشة صور|Page {i}}}}}"
            )
            page.add_entry(entry)
        
        self.assertTrue(page.is_full())
        self.assertEqual(page.entry_count, 10)
    
    def test_is_full_over_limit(self):
        """Test is_full over the limit."""
        page = ArchivePage(page_number=1)
        
        # Add 11 entries
        for i in range(11):
            entry = ArchiveEntry(
                page_name=f"Page {i}",
                template_text=f"{{{{طلب ورشة صور|Page {i}}}}}"
            )
            page.add_entry(entry)
        
        self.assertTrue(page.is_full())
    
    def test_add_entry(self):
        """Test adding an entry."""
        page = ArchivePage(page_number=1)
        
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        page.add_entry(entry)
        
        self.assertEqual(page.entry_count, 1)
        self.assertEqual(entry.archive_page_number, 1)
        self.assertIn(entry, page.entries)
    
    def test_get_header(self):
        """Test getting archive header."""
        page = ArchivePage(page_number=52)
        
        header = page.get_header()
        
        # self.assertIn("{{أرشيف نقاش}}", header)
        self.assertIn("{{تصفح أرشيف|52}}", header)
        self.assertIn("{{تمت الأرشفة}}", header)
    
    def test_get_content(self):
        """Test getting full content."""
        page = ArchivePage(page_number=1)
        
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        page.add_entry(entry)
        
        content = page.get_content()
        
        # self.assertIn("{{أرشيف نقاش}}", content)
        self.assertIn("{{طلب ورشة صور|Test Page}}", content)


if __name__ == '__main__':
    unittest.main()
