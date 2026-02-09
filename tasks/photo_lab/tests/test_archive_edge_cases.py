"""
Edge case tests for archive use cases.
"""

import unittest
from datetime import datetime

try:
    from tasks.photo_lab.domain.use_cases.archive_completed_requests import ArchiveCompletedRequests
    from tasks.photo_lab.domain.use_cases.manage_archives import ManageArchives
    from tasks.photo_lab.domain.use_cases.check_request_status import CheckRequestStatus
    from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
    from tasks.photo_lab.domain.entities.archive_entry import ArchivePage, ArchiveEntry
    from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository
    WIKITEXTPARSER_AVAILABLE = True
except ImportError:
    WIKITEXTPARSER_AVAILABLE = False


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestArchiveCompletedRequestsEdgeCases(unittest.TestCase):
    """Edge case tests for ArchiveCompletedRequests."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ArchiveCompletedRequests(self.mock_repo)
    
    def test_archive_empty_list(self):
        """Test archiving empty list of requests."""
        archive_page = ArchivePage(page_number=1)
        
        results = self.use_case.execute([], archive_page)
        
        self.assertEqual(len(results['archived']), 0)
        self.assertEqual(len(results['failed']), 0)
        self.assertEqual(len(results['skipped']), 0)
    
    def test_archive_all_not_ready(self):
        """Test archiving when none are ready."""
        requests = [
            PhotoRequest(page_name="Page 1", template_text="{{...}}"),
            PhotoRequest(page_name="Page 2", template_text="{{...}}")
        ]
        # Don't mark any as ready
        
        archive_page = ArchivePage(page_number=1)
        
        results = self.use_case.execute(requests, archive_page)
        
        self.assertEqual(len(results['archived']), 0)
        self.assertEqual(len(results['skipped']), 2)
    
    def test_archive_mixed_status(self):
        """Test archiving with mixed ready/not ready status."""
        requests = [
            PhotoRequest(page_name="Ready", template_text="{{...}}"),
            PhotoRequest(page_name="Not Ready", template_text="{{...}}")
        ]
        requests[0].mark_as_archivable()
        
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|Ready}}\n{{طلب ورشة صور|Not Ready}}"
        )
        
        archive_page = ArchivePage(page_number=1)
        
        results = self.use_case.execute(requests, archive_page)
        
        self.assertEqual(len(results['archived']), 1)
        self.assertEqual(len(results['skipped']), 1)
        self.assertEqual(results['archived'][0], "Ready")
    
    def test_archive_to_full_page(self):
        """Test archiving when target archive is full."""
        # Create 10 ready requests
        requests = []
        for i in range(5):
            request = PhotoRequest(
                page_name=f"Page {i}",
                template_text=f"{{{{طلب ورشة صور|Page {i}}}}}"
            )
            request.mark_as_archivable()
            requests.append(request)
        
        main_content = "\n".join([r.template_text for r in requests])
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", main_content)
        
        # Archive already has 8 entries (room for 2 more)
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/أرشيف 1",
            "\ncontent"
        )
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/أرشيف 1",
            "طلب ورشة صور",
            8
        )
        
        archive_page = ArchivePage(page_number=1)
        # Add 8 entries to match the mock
        for i in range(8):
            archive_page.add_entry(ArchiveEntry(
                page_name=f"Existing {i}",
                template_text=f"{{{{...|{i}}}}}"
            ))
        
        results = self.use_case.execute(requests, archive_page)
        
        # Should archive all 5
        self.assertEqual(len(results['archived']), 5)
    
    def test_remove_template_from_main_page(self):
        """Test that templates are correctly removed from main page."""
        request = PhotoRequest(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        request.mark_as_archivable()
        
        original_content = "Header\n{{طلب ورشة صور|Test Page}}\nFooter"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", original_content)
        
        archive_page = ArchivePage(page_number=1)
        
        self.use_case.execute([request], archive_page)
        
        # Check that main page was updated
        updated_content = self.mock_repo.pages.get("ويكيبيديا:ورشة الصور/طلبات", "")
        self.assertNotIn("{{طلب ورشة صور|Test Page}}", updated_content)
        self.assertIn("Header", updated_content)
        self.assertIn("Footer", updated_content)


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestManageArchivesEdgeCases(unittest.TestCase):
    """Edge case tests for ManageArchives."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ManageArchives(self.mock_repo)
    
    def test_get_archive_with_gap_in_numbers(self):
        """Test when archive numbers have gaps."""
        # Archives 1 and 3 exist, but not 2
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/أرشيف 1",
            "content"
        )
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/أرشيف 3",
            "content"
        )
        self.mock_repo.add_archive_page(3, "ويكيبيديا:ورشة الصور/أرشيف 3")
        
        # Make archive 3 full
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/أرشيف 3",
            "طلب ورشة صور",
            10
        )
        
        archive_page = self.use_case.get_or_create_latest_archive()
        
        # Should create archive 4 (next after 3)
        self.assertEqual(archive_page.page_number, 4)
    
    def test_add_multiple_entries_sequentially(self):
        """Test adding multiple entries one at a time."""
        archive_page = ArchivePage(page_number=1)
        
        # Add entries one by one
        for i in range(5):
            entry = ArchiveEntry(
                page_name=f"Page {i}",
                template_text=f"{{{{...|{i}}}}}"
            )
            success = self.use_case.add_entry_to_archive(archive_page, entry)
            self.assertTrue(success)
        
        self.assertEqual(archive_page.entry_count, 5)
    
    def test_archive_page_content_integrity(self):
        """Test that archive page content is correctly formed."""
        archive_page = ArchivePage(page_number=1)
        
        entry = ArchiveEntry(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        self.use_case.add_entry_to_archive(archive_page, entry)
        
        content = archive_page.get_content()
        
        # Verify header
        # self.assertIn("{{أرشيف نقاش}}", content)
        self.assertIn("{{تصفح أرشيف|1}}", content)
        self.assertIn("{{تمت الأرشفة}}", content)
        
        # Verify entry
        self.assertIn("{{طلب ورشة صور|Test Page}}", content)
    
    def test_find_latest_archive_empty_list(self):
        """Test finding latest when no archives exist."""
        latest = self.use_case.find_latest_archive_number()
        
        self.assertEqual(latest, 0)
    
    def test_find_latest_archive_single(self):
        """Test finding latest with single archive."""
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        
        latest = self.use_case.find_latest_archive_number()
        
        self.assertEqual(latest, 1)
    
    def test_find_latest_archive_multiple(self):
        """Test finding latest with multiple archives."""
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        self.mock_repo.add_archive_page(5, "ويكيبيديا:ورشة الصور/أرشيف 5")
        self.mock_repo.add_archive_page(10, "ويكيبيديا:ورشة الصور/أرشيف 10")
        
        latest = self.use_case.find_latest_archive_number()
        
        self.assertEqual(latest, 10)


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestCheckRequestStatusEdgeCases(unittest.TestCase):
    """Edge case tests for CheckRequestStatus."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = CheckRequestStatus(self.mock_repo)
    
    def test_empty_request_list(self):
        """Test with empty list."""
        results = self.use_case.execute([])
        
        self.assertEqual(len(results), 0)
    
    def test_single_request(self):
        """Test with single request."""
        request = PhotoRequest(page_name="Test", template_text="{{...}}")
        
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Test",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/Test",
            "منظور",
            1
        )
        
        results = self.use_case.execute([request])
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].has_perspective)
    
    def test_request_page_does_not_exist(self):
        """Test when request page doesn't exist."""
        request = PhotoRequest(page_name="NonExistent", template_text="{{...}}")
        
        # Don't add the page
        
        results = self.use_case.execute([request])
        
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].has_perspective)
    
    def test_multiple_perspective_templates(self):
        """Test page with multiple perspective templates."""
        request = PhotoRequest(page_name="Test", template_text="{{...}}")
        
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Test",
            "{{منظور}} {{منظور}} {{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/Test",
            "منظور",
            3
        )
        
        results = self.use_case.execute([request])
        
        self.assertTrue(results[0].has_perspective)
    
    def test_mixed_requests(self):
        """Test list with mixed ready/not ready."""
        requests = [
            PhotoRequest(page_name="Ready1", template_text="{{...}}"),
            PhotoRequest(page_name="NotReady", template_text="{{...}}"),
            PhotoRequest(page_name="Ready2", template_text="{{...}}")
        ]
        
        # Set up Ready1 and Ready2 with perspective
        for name in ["Ready1", "Ready2"]:
            self.mock_repo.add_page(
                f"ويكيبيديا:ورشة الصور/طلبات/{name}",
                "{{منظور}}"
            )
            self.mock_repo.add_template_to_page(
                f"ويكيبيديا:ورشة الصور/طلبات/{name}",
                "منظور",
                1
            )
        
        # NotReady has no perspective
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/NotReady",
            "No perspective"
        )
        
        results = self.use_case.execute(requests)
        
        self.assertTrue(results[0].has_perspective)  # Ready1
        self.assertFalse(results[1].has_perspective)  # NotReady
        self.assertTrue(results[2].has_perspective)  # Ready2
        
        archivable = self.use_case.get_archivable_requests(results)
        self.assertEqual(len(archivable), 2)


if __name__ == '__main__':
    unittest.main()
