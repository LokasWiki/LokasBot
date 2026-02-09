"""
Edge case tests for entities.
"""

import unittest
from datetime import datetime

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry, ArchivePage


class TestPhotoRequestEdgeCases(unittest.TestCase):
    """Edge case tests for PhotoRequest."""
    
    def test_empty_page_name(self):
        """Test with empty page name."""
        request = PhotoRequest(
            page_name="",
            template_text="{{طلب ورشة صور|}}"
        )
        self.assertEqual(request.page_name, "")
        self.assertEqual(request.request_page_title, "ويكيبيديا:ورشة الصور/طلبات/")
    
    def test_whitespace_page_name(self):
        """Test with whitespace-only page name."""
        request = PhotoRequest(
            page_name="   ",
            template_text="{{طلب ورشة صور|   }}"
        )
        self.assertEqual(request.page_name, "   ")
    
    def test_unicode_page_name(self):
        """Test with Arabic and unicode characters."""
        arabic_name = "صفحة تجريبية"
        request = PhotoRequest(
            page_name=arabic_name,
            template_text=f"{{{{طلب ورشة صور|{arabic_name}}}}}"
        )
        self.assertEqual(request.page_name, arabic_name)
        self.assertIn(arabic_name, request.request_page_title)
    
    def test_very_long_template_text(self):
        """Test with very long template text."""
        long_text = "{{طلب ورشة صور|" + "A" * 1000 + "}}"
        request = PhotoRequest(
            page_name="Test",
            template_text=long_text
        )
        self.assertEqual(request.template_text, long_text)
    
    def test_multiple_perspective_marks(self):
        """Test marking as archivable multiple times."""
        request = PhotoRequest(
            page_name="Test",
            template_text="{{...}}"
        )
        request.mark_as_archivable()
        request.mark_as_archivable()
        request.mark_as_archivable()
        
        self.assertTrue(request.has_perspective)
        self.assertTrue(request.is_ready_for_archive())
    
    def test_toggle_perspective(self):
        """Test toggling perspective status manually."""
        request = PhotoRequest(
            page_name="Test",
            template_text="{{...}}"
        )
        
        # Initially False
        self.assertFalse(request.has_perspective)
        
        # Mark as True
        request.has_perspective = True
        self.assertTrue(request.is_ready_for_archive())
        
        # Mark as False
        request.has_perspective = False
        self.assertFalse(request.is_ready_for_archive())
    
    def test_request_page_title_with_provided_value(self):
        """Test when request_page_title is explicitly provided."""
        custom_title = "Custom/Title/Here"
        request = PhotoRequest(
            page_name="Test",
            template_text="{{...}}",
            request_page_title=custom_title
        )
        self.assertEqual(request.request_page_title, custom_title)
    
    def test_repr_with_long_template(self):
        """Test repr truncates long template text."""
        long_template = "{{طلب ورشة صور|" + "X" * 100 + "}}"
        request = PhotoRequest(
            page_name="Test",
            template_text=long_template
        )
        repr_str = repr(request)
        self.assertIn("...", repr_str)
        self.assertLess(len(repr_str), 200)


class TestArchiveEntryEdgeCases(unittest.TestCase):
    """Edge case tests for ArchiveEntry."""
    
    def test_default_timestamp(self):
        """Test that default timestamp is set."""
        before = datetime.now()
        entry = ArchiveEntry(
            page_name="Test",
            template_text="{{...}}"
        )
        after = datetime.now()
        
        self.assertIsNotNone(entry.archived_at)
        self.assertTrue(before <= entry.archived_at <= after)
    
    def test_explicit_timestamp(self):
        """Test with explicit timestamp."""
        specific_time = datetime(2023, 6, 15, 10, 30, 0)
        entry = ArchiveEntry(
            page_name="Test",
            template_text="{{...}}",
            archived_at=specific_time
        )
        self.assertEqual(entry.archived_at, specific_time)
    
    def test_empty_page_name(self):
        """Test with empty page name."""
        entry = ArchiveEntry(
            page_name="",
            template_text="{{...}}"
        )
        self.assertEqual(entry.get_archive_page_title(), "ويكيبيديا:ورشة الصور/أرشيف 0")
    
    def test_custom_base_prefix(self):
        """Test with custom base prefix."""
        entry = ArchiveEntry(
            page_name="Test",
            template_text="{{...}}",
            archive_page_number=5
        )
        custom_prefix = "User:Test/Archive"
        title = entry.get_archive_page_title(custom_prefix)
        self.assertEqual(title, "User:Test/Archive 5")
    
    def test_format_for_archive_preserves_whitespace(self):
        """Test format_for_archive preserves template formatting."""
        template_with_whitespace = "  {{طلب ورشة صور|Test}}  "
        entry = ArchiveEntry(
            page_name="Test",
            template_text=template_with_whitespace
        )
        formatted = entry.format_for_archive()
        self.assertIn(template_with_whitespace.strip(), formatted)


class TestArchivePageEdgeCases(unittest.TestCase):
    """Edge case tests for ArchivePage."""
    
    def test_zero_page_number(self):
        """Test with page number 0."""
        page = ArchivePage(page_number=0)
        self.assertEqual(page.page_number, 0)
        self.assertEqual(page.title, "ويكيبيديا:ورشة الصور/أرشيف 0")
    
    def test_negative_page_number(self):
        """Test with negative page number."""
        page = ArchivePage(page_number=-1)
        self.assertEqual(page.page_number, -1)
        self.assertEqual(page.title, "ويكيبيديا:ورشة الصور/أرشيف -1")
    
    def test_large_page_number(self):
        """Test with very large page number."""
        page = ArchivePage(page_number=999999)
        self.assertEqual(page.page_number, 999999)
        self.assertEqual(page.title, "ويكيبيديا:ورشة الصور/أرشيف 999999")
    
    def test_custom_base_prefix(self):
        """Test with custom base prefix."""
        page = ArchivePage(
            page_number=1,
            base_prefix="مستخدم:اختبار/أرشيف"
        )
        self.assertEqual(page.title, "مستخدم:اختبار/أرشيف 1")
        self.assertEqual(page.get_header(), "\n{{تصفح أرشيف|1}}\n{{تمت الأرشفة}}\n\n")
    
    def test_entries_none_initialization(self):
        """Test initialization with None entries."""
        page = ArchivePage(page_number=1, entries=None)
        self.assertEqual(page.entries, [])
        self.assertEqual(page.entry_count, 0)
    
    def test_empty_entries_list(self):
        """Test with empty entries list."""
        page = ArchivePage(page_number=1, entries=[])
        self.assertEqual(page.entry_count, 0)
        self.assertFalse(page.is_full())
    
    def test_exactly_at_capacity(self):
        """Test when exactly at capacity (10 entries)."""
        page = ArchivePage(page_number=1)
        for i in range(10):
            page.add_entry(ArchiveEntry(page_name=f"Page {i}", template_text=f"{{{{...|{i}}}}}"))
        
        self.assertTrue(page.is_full())
        self.assertEqual(page.entry_count, 10)
    
    def test_one_over_capacity(self):
        """Test when one over capacity."""
        page = ArchivePage(page_number=1)
        for i in range(11):
            page.add_entry(ArchiveEntry(page_name=f"Page {i}", template_text=f"{{{{...|{i}}}}}"))
        
        self.assertTrue(page.is_full())
        self.assertEqual(page.entry_count, 11)
    
    def test_add_entry_updates_page_number(self):
        """Test that add_entry updates entry's archive_page_number."""
        page = ArchivePage(page_number=42)
        entry = ArchiveEntry(
            page_name="Test",
            template_text="{{...}}",
            archive_page_number=0
        )
        
        page.add_entry(entry)
        
        self.assertEqual(entry.archive_page_number, 42)
    
    def test_get_content_with_no_entries(self):
        """Test get_content with empty archive."""
        page = ArchivePage(page_number=1)
        content = page.get_content()
        
        # self.assertIn("{{أرشيف نقاش}}", content)
        self.assertIn("{{تصفح أرشيف|1}}", content)
        self.assertIn("{{تمت الأرشفة}}", content)
    
    def test_get_content_with_many_entries(self):
        """Test get_content with many entries."""
        page = ArchivePage(page_number=1)
        for i in range(5):
            page.add_entry(ArchiveEntry(
                page_name=f"Page {i}",
                template_text=f"{{{{طلب ورشة صور|Page {i}}}}}"
            ))
        
        content = page.get_content()
        
        for i in range(5):
            self.assertIn(f"{{{{طلب ورشة صور|Page {i}}}}}", content)
    
    def test_is_full_with_custom_max(self):
        """Test is_full with custom maximum."""
        page = ArchivePage(page_number=1)
        for i in range(5):
            page.add_entry(ArchiveEntry(page_name=f"Page {i}", template_text="{{...}}"))
        
        self.assertFalse(page.is_full(max_entries=10))
        self.assertTrue(page.is_full(max_entries=5))
        self.assertTrue(page.is_full(max_entries=3))


class TestEntityEquality(unittest.TestCase):
    """Test equality and comparison of entities."""
    
    def test_photo_request_equality(self):
        """Test PhotoRequest equality based on page_name."""
        request1 = PhotoRequest(page_name="Test", template_text="{{...}}")
        request2 = PhotoRequest(page_name="Test", template_text="{{different}}")
        request3 = PhotoRequest(page_name="Different", template_text="{{...}}")
        
        # Same page name should be equal (based on __eq__ in dataclass)
        # Note: dataclass compares all fields by default
        self.assertNotEqual(request1, request2)  # Different template_text
        self.assertNotEqual(request1, request3)  # Different page_name
    
    def test_archive_entry_equality(self):
        """Test ArchiveEntry equality."""
        from datetime import datetime
        same_time = datetime(2023, 1, 1, 12, 0, 0)
        entry1 = ArchiveEntry(page_name="Test", template_text="{{...}}", archived_at=same_time)
        entry2 = ArchiveEntry(page_name="Test", template_text="{{...}}", archived_at=same_time)
        entry3 = ArchiveEntry(page_name="Different", template_text="{{...}}", archived_at=same_time)
        
        # Same values should be equal
        self.assertEqual(entry1, entry2)
        self.assertNotEqual(entry1, entry3)
    
    def test_archive_page_equality(self):
        """Test ArchivePage equality."""
        page1 = ArchivePage(page_number=1)
        page2 = ArchivePage(page_number=1)
        page3 = ArchivePage(page_number=2)
        
        self.assertEqual(page1.page_number, page2.page_number)
        self.assertNotEqual(page1.page_number, page3.page_number)


if __name__ == '__main__':
    unittest.main()
