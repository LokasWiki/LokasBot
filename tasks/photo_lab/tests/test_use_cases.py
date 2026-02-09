"""
Unit tests for the use cases.
"""

import unittest

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
from tasks.photo_lab.domain.entities.archive_entry import ArchivePage
from tasks.photo_lab.domain.use_cases.extract_pending_requests import ExtractPendingRequests
from tasks.photo_lab.domain.use_cases.check_request_status import CheckRequestStatus
from tasks.photo_lab.domain.use_cases.manage_archives import ManageArchives
from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository


class TestExtractPendingRequests(unittest.TestCase):
    """Test cases for ExtractPendingRequests use case."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ExtractPendingRequests(self.mock_repo)
    
    def test_extract_single_request(self):
        """Test extracting a single request."""
        content = "{{طلب ورشة صور|Test Page}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].page_name, "Test Page")
        self.assertEqual(requests[0].template_text, "{{طلب ورشة صور|Test Page}}")
    
    def test_extract_multiple_requests(self):
        """Test extracting multiple requests."""
        content = """{{طلب ورشة صور|Page One}}

Some text here.

{{طلب ورشة صور|Page Two}}

{{طلب ورشة صور|Page Three}}"""
        
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 3)
        self.assertEqual(requests[0].page_name, "Page One")
        self.assertEqual(requests[1].page_name, "Page Two")
        self.assertEqual(requests[2].page_name, "Page Three")
    
    def test_extract_no_requests(self):
        """Test extracting when no requests exist."""
        content = "This page has no requests."
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 0)
    
    def test_extract_empty_page(self):
        """Test extracting from empty page."""
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", "")
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 0)


class TestCheckRequestStatus(unittest.TestCase):
    """Test cases for CheckRequestStatus use case."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = CheckRequestStatus(self.mock_repo)
    
    def test_request_with_perspective(self):
        """Test request with perspective template."""
        requests = [
            PhotoRequest(
                page_name="Test Page",
                template_text="{{طلب ورشة صور|Test Page}}"
            )
        ]
        
        # Set up the request page with perspective template
        request_page = "ويكيبيديا:ورشة الصور/طلبات/Test Page"
        self.mock_repo.add_page(request_page, "{{منظور}} some content")
        self.mock_repo.add_template_to_page(request_page, "منظور", 1)
        
        checked_requests = self.use_case.execute(requests)
        
        self.assertTrue(checked_requests[0].has_perspective)
        self.assertTrue(checked_requests[0].is_ready_for_archive())
    
    def test_request_without_perspective(self):
        """Test request without perspective template."""
        requests = [
            PhotoRequest(
                page_name="Test Page",
                template_text="{{طلب ورشة صور|Test Page}}"
            )
        ]
        
        # Set up the request page without perspective template
        request_page = "ويكيبيديا:ورشة الصور/طلبات/Test Page"
        self.mock_repo.add_page(request_page, "some content without perspective")
        
        checked_requests = self.use_case.execute(requests)
        
        self.assertFalse(checked_requests[0].has_perspective)
        self.assertFalse(checked_requests[0].is_ready_for_archive())
    
    def test_get_archivable_requests(self):
        """Test filtering archivable requests."""
        requests = [
            PhotoRequest(page_name="Page 1", template_text="{{طلب ورشة صور|Page 1}}"),
            PhotoRequest(page_name="Page 2", template_text="{{طلب ورشة صور|Page 2}}"),
            PhotoRequest(page_name="Page 3", template_text="{{طلب ورشة صور|Page 3}}")
        ]
        
        # Mark some as archivable
        requests[0].mark_as_archivable()
        requests[2].mark_as_archivable()
        
        archivable = self.use_case.get_archivable_requests(requests)
        
        self.assertEqual(len(archivable), 2)
        self.assertEqual(archivable[0].page_name, "Page 1")
        self.assertEqual(archivable[1].page_name, "Page 3")


class TestManageArchives(unittest.TestCase):
    """Test cases for ManageArchives use case."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ManageArchives(self.mock_repo)
    
    def test_create_first_archive(self):
        """Test creating the first archive when none exist."""
        archive_page = self.use_case.get_or_create_latest_archive()
        
        self.assertEqual(archive_page.page_number, 1)
        self.assertEqual(archive_page.entry_count, 0)
    
    def test_get_existing_archive(self):
        """Test getting existing archive with room."""
        # Set up an existing archive with 5 entries
        archive_title = "ويكيبيديا:ورشة الصور/أرشيف 1"
        # self.mock_repo.add_page(archive_title, "{{أرشيف نقاش}}\n{{طلب ورشة صور|Page 1}}")
        self.mock_repo.add_page(archive_title, "\n{{طلب ورشة صور|Page 1}}")
        self.mock_repo.add_archive_page(1, archive_title)
        self.mock_repo.add_template_to_page(archive_title, "طلب ورشة صور", 5)
        
        archive_page = self.use_case.get_or_create_latest_archive()
        
        self.assertEqual(archive_page.page_number, 1)
    
    def test_create_new_when_full(self):
        """Test creating new archive when current is full."""
        # Set up a full archive (10 entries)
        archive_title = "ويكيبيديا:ورشة الصور/أرشيف 1"
        self.mock_repo.add_page(archive_title, "\ncontent")
        self.mock_repo.add_archive_page(1, archive_title)
        self.mock_repo.add_template_to_page(archive_title, "طلب ورشة صور", 10)
        
        archive_page = self.use_case.get_or_create_latest_archive()
        
        self.assertEqual(archive_page.page_number, 2)
    
    def test_add_entry_to_archive(self):
        """Test adding entry to archive."""
        archive_page = ArchivePage(page_number=1)
        
        from tasks.photo_lab.domain.entities.archive_entry import ArchiveEntry
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        success = self.use_case.add_entry_to_archive(archive_page, entry)
        
        self.assertTrue(success)
        self.assertEqual(archive_page.entry_count, 1)
    
    def test_find_latest_archive_number(self):
        """Test finding latest archive number."""
        # No archives initially
        self.assertEqual(self.use_case.find_latest_archive_number(), 0)
        
        # Add some archives
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        self.mock_repo.add_archive_page(2, "ويكيبيديا:ورشة الصور/أرشيف 2")
        self.mock_repo.add_archive_page(5, "ويكيبيديا:ورشة الصور/أرشيف 5")
        
        self.assertEqual(self.use_case.find_latest_archive_number(), 5)


if __name__ == '__main__':
    unittest.main()
