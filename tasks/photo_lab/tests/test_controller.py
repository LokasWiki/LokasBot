"""
Unit and integration tests for the PhotoLabController.
"""

import unittest
from unittest.mock import Mock, patch

try:
    from tasks.photo_lab.presentation.controllers.photo_lab_controller import PhotoLabController
    from tasks.photo_lab.domain.entities.photo_request import PhotoRequest
    from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository
    WIKITEXTPARSER_AVAILABLE = True
except ImportError:
    WIKITEXTPARSER_AVAILABLE = False


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestPhotoLabController(unittest.TestCase):
    """Test cases for PhotoLabController."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.controller = PhotoLabController(self.mock_repo)
    
    def test_run_with_no_requests(self):
        """Test controller when no requests exist."""
        # Arrange
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", "")
        
        # Act
        results = self.controller.run()
        
        # Assert
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 0)
        self.assertEqual(results['archivable_requests'], 0)
        self.assertEqual(len(results['archived']), 0)
    
    def test_run_with_no_archivable_requests(self):
        """Test controller when requests exist but none are archivable."""
        # Arrange
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|Page 1}}\n{{طلب ورشة صور|Page 2}}"
        )
        
        # No perspective templates set up
        
        # Act
        results = self.controller.run()
        
        # Assert
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 2)
        self.assertEqual(results['archivable_requests'], 0)
        self.assertEqual(len(results['archived']), 0)
    
    def test_run_with_archivable_requests(self):
        """Test controller with requests ready for archiving."""
        # Arrange
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|Page 1}}\n{{طلب ورشة صور|Page 2}}"
        )
        
        # Set up Page 1 with perspective
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "منظور",
            1
        )
        
        # Act
        results = self.controller.run()
        
        # Assert
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 2)
        self.assertEqual(results['archivable_requests'], 1)
        self.assertEqual(len(results['archived']), 1)
        self.assertEqual(results['archived'][0], "Page 1")
        self.assertEqual(results['archive_page_number'], 1)
    
    def test_run_with_multiple_archives(self):
        """Test controller when existing archives are full."""
        # Arrange
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|New Page}}"
        )
        
        # Set up request with perspective
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/New Page",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/New Page",
            "منظور",
            1
        )
        
        # Set up full archive
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/أرشيف 1",
            # "{{أرشيف نقاش}}\ncontent"
        )
        self.mock_repo.add_archive_page(1, "ويكيبيديا:ورشة الصور/أرشيف 1")
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/أرشيف 1",
            "طلب ورشة صور",
            10  # Full
        )
        
        # Act
        results = self.controller.run()
        
        # Assert
        self.assertTrue(results['success'])
        self.assertEqual(results['archive_page_number'], 2)
    
    def test_run_dry_mode(self):
        """Test dry run mode."""
        # Arrange
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "{{طلب ورشة صور|Page 1}}"
        )
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            "ويكيبيديا:ورشة الصور/طلبات/Page 1",
            "منظور",
            1
        )
        
        # Act
        results = self.controller.run_dry_mode()
        
        # Assert
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 1)
        self.assertEqual(len(results['would_archive']), 1)
        self.assertEqual(results['would_archive'][0], "Page 1")
    
    def test_run_with_repository_error(self):
        """Test controller handles repository errors gracefully."""
        # Arrange - make repository raise exception
        self.mock_repo.get_main_requests_page_content = Mock(
            side_effect=Exception("Connection failed")
        )
        
        # Act
        results = self.controller.run()
        
        # Assert
        self.assertFalse(results['success'])
        self.assertEqual(len(results['errors']), 1)
        self.assertIn("Connection failed", results['errors'][0])


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestPhotoLabControllerEdgeCases(unittest.TestCase):
    """Test edge cases for PhotoLabController."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.controller = PhotoLabController(self.mock_repo)
    
    def test_very_long_page_name(self):
        """Test with very long page names."""
        long_name = "A" * 200
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            f"{{{{طلب ورشة صور|{long_name}}}}}"
        )
        self.mock_repo.add_page(
            f"ويكيبيديا:ورشة الصور/طلبات/{long_name}",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            f"ويكيبيديا:ورشة الصور/طلبات/{long_name}",
            "منظور",
            1
        )
        
        results = self.controller.run()
        
        self.assertTrue(results['success'])
        self.assertEqual(len(results['archived']), 1)
        self.assertEqual(results['archived'][0], long_name)
    
    def test_special_characters_in_page_name(self):
        """Test with special characters in page names."""
        special_name = "Page with (parentheses) & [brackets]"
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            f"{{{{طلب ورشة صور|{special_name}}}}}"
        )
        self.mock_repo.add_page(
            f"ويكيبيديا:ورشة الصور/طلبات/{special_name}",
            "{{منظور}}"
        )
        self.mock_repo.add_template_to_page(
            f"ويكيبيديا:ورشة الصور/طلبات/{special_name}",
            "منظور",
            1
        )
        
        results = self.controller.run()
        
        self.assertTrue(results['success'])
        self.assertEqual(len(results['archived']), 1)
    
    def test_many_requests(self):
        """Test with many requests."""
        # Create 50 requests
        templates = []
        for i in range(50):
            templates.append("{{" + f"طلب ورشة صور|Page {i}" + "}}")
            if i % 2 == 0:  # Half have perspective
                self.mock_repo.add_page(
                    f"ويكيبيديا:ورشة الصور/طلبات/Page {i}",
                    "{{منظور}}"
                )
                self.mock_repo.add_template_to_page(
                    f"ويكيبيديا:ورشة الصور/طلبات/Page {i}",
                    "منظور",
                    1
                )
        
        self.mock_repo.add_page(
            "ويكيبيديا:ورشة الصور/طلبات",
            "\n".join(templates)
        )
        
        results = self.controller.run()
        
        self.assertTrue(results['success'])
        self.assertEqual(results['total_requests'], 50)
        self.assertEqual(results['archivable_requests'], 25)
        self.assertEqual(len(results['archived']), 25)


if __name__ == '__main__':
    unittest.main()
