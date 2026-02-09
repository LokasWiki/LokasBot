"""
Tests for infrastructure layer (PywikibotWiki implementation).
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

try:
    import pywikibot
    from tasks.photo_lab.infrastructure.wiki.pywikibot_wiki import PywikibotWiki
    from tasks.photo_lab.domain.entities.archive_entry import ArchivePage, ArchiveEntry
    PYWIKIBOT_AVAILABLE = True
except ImportError:
    PYWIKIBOT_AVAILABLE = False


@unittest.skipUnless(PYWIKIBOT_AVAILABLE, "pywikibot not available")
class TestPywikibotWiki(unittest.TestCase):
    """Test cases for PywikibotWiki implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the pywikibot site
        self.mock_site = Mock()
        self.wiki = PywikibotWiki(site=self.mock_site)
    
    def test_init_with_custom_site(self):
        """Test initialization with custom site."""
        custom_site = Mock()
        wiki = PywikibotWiki(site=custom_site)
        
        self.assertEqual(wiki.site, custom_site)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot')
    def test_init_with_default_site(self, mock_pywikibot):
        """Test initialization with default site."""
        mock_site = Mock()
        mock_pywikibot.Site.return_value = mock_site
        
        wiki = PywikibotWiki()
        
        self.assertEqual(wiki.site, mock_site)
        mock_pywikibot.Site.assert_called_once()
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_get_main_requests_page_content(self, mock_page_class):
        """Test getting main page content."""
        # Setup mock
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.text = "Test content with {{طلب ورشة صور|Test}}"
        mock_page_class.return_value = mock_page
        
        # Execute
        content = self.wiki.get_main_requests_page_content()
        
        # Assert
        self.assertEqual(content, "Test content with {{طلب ورشة صور|Test}}")
        mock_page_class.assert_called_once_with(
            self.mock_site,
            "ويكيبيديا:ورشة الصور/طلبات"
        )
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_get_main_requests_page_not_exists(self, mock_page_class):
        """Test getting main page when it doesn't exist."""
        mock_page = Mock()
        mock_page.exists.return_value = False
        mock_page_class.return_value = mock_page
        
        content = self.wiki.get_main_requests_page_content()
        
        self.assertEqual(content, "")
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_update_main_requests_page(self, mock_page_class):
        """Test updating main page."""
        mock_page = Mock()
        mock_page_class.return_value = mock_page
        
        success = self.wiki.update_main_requests_page(
            "New content",
            "Test summary"
        )
        
        self.assertTrue(success)
        self.assertEqual(mock_page.text, "New content")
        mock_page.save.assert_called_once_with(
            summary="Test summary",
            minor=False
        )
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_update_main_requests_page_failure(self, mock_page_class):
        """Test update failure handling."""
        mock_page = Mock()
        mock_page.save.side_effect = Exception("Save failed")
        mock_page_class.return_value = mock_page
        
        success = self.wiki.update_main_requests_page("Content", "Summary")
        
        self.assertFalse(success)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_page_exists_true(self, mock_page_class):
        """Test page exists returns True."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page_class.return_value = mock_page
        
        exists = self.wiki.page_exists("Some Page")
        
        self.assertTrue(exists)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_page_exists_false(self, mock_page_class):
        """Test page exists returns False."""
        mock_page = Mock()
        mock_page.exists.return_value = False
        mock_page_class.return_value = mock_page
        
        exists = self.wiki.page_exists("NonExistent")
        
        self.assertFalse(exists)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.wtp')
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_has_template_true(self, mock_page_class, mock_wtp):
        """Test has_template when template exists."""
        # Setup
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.text = "{{TestTemplate}}"
        mock_page_class.return_value = mock_page
        
        mock_template = Mock()
        mock_template.name.strip.return_value = "TestTemplate"
        mock_parsed = Mock()
        mock_parsed.templates = [mock_template]
        mock_wtp.parse.return_value = mock_parsed
        
        # Execute
        has_it = self.wiki.has_template("Some Page", "TestTemplate")
        
        # Assert
        self.assertTrue(has_it)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.wtp')
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_has_template_false(self, mock_page_class, mock_wtp):
        """Test has_template when template doesn't exist."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.text = "{{OtherTemplate}}"
        mock_page_class.return_value = mock_page
        
        mock_template = Mock()
        mock_template.name.strip.return_value = "OtherTemplate"
        mock_parsed = Mock()
        mock_parsed.templates = [mock_template]
        mock_wtp.parse.return_value = mock_parsed
        
        has_it = self.wiki.has_template("Some Page", "TestTemplate")
        
        self.assertFalse(has_it)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_create_archive_page(self, mock_page_class):
        """Test creating archive page."""
        mock_page = Mock()
        mock_page.exists.return_value = False
        mock_page_class.return_value = mock_page
        
        archive_page = ArchivePage(page_number=1)
        archive_page.add_entry(ArchiveEntry(
            page_name="Test",
            template_text="{{...}}"
        ))
        
        success = self.wiki.create_archive_page(archive_page, "Create archive")
        
        self.assertTrue(success)
        mock_page.save.assert_called_once_with(
            summary="Create archive",
            minor=False
        )
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_update_archive_page_existing(self, mock_page_class):
        """Test updating existing archive page."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page_class.return_value = mock_page
        
        archive_page = ArchivePage(page_number=1)
        archive_page.add_entry(ArchiveEntry(
            page_name="Test",
            template_text="{{...}}"
        ))
        
        success = self.wiki.update_archive_page(archive_page, "Update archive")
        
        self.assertTrue(success)
        mock_page.save.assert_called_once()
    
    def test_get_all_archive_pages(self):
        """Test getting all archive pages."""
        # Create mock pages
        mock_page1 = Mock()
        mock_page1.title.return_value = "ويكيبيديا:ورشة الصور/أرشيف 1"
        
        mock_page2 = Mock()
        mock_page2.title.return_value = "ويكيبيديا:ورشة الصور/أرشيف 5"
        
        mock_page3 = Mock()
        mock_page3.title.return_value = "ويكيبيديا:ورشة الصور/أرشيف 10"
        
        self.mock_site.allpages.return_value = [mock_page1, mock_page2, mock_page3]
        
        archives = self.wiki.get_all_archive_pages()
        
        self.assertEqual(len(archives), 3)
        self.assertEqual(archives[0][0], 1)
        self.assertEqual(archives[1][0], 5)
        self.assertEqual(archives[2][0], 10)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.wtp')
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_count_templates_in_page(self, mock_page_class, mock_wtp):
        """Test counting templates."""
        mock_page = Mock()
        mock_page.text = "{{Template}} {{Template}} {{Other}}"
        mock_page_class.return_value = mock_page
        
        # Setup wtp mock
        mock_template1 = Mock()
        mock_template1.name.strip.return_value = "TargetTemplate"
        mock_template2 = Mock()
        mock_template2.name.strip.return_value = "TargetTemplate"
        mock_template3 = Mock()
        mock_template3.name.strip.return_value = "OtherTemplate"
        
        mock_parsed = Mock()
        mock_parsed.templates = [mock_template1, mock_template2, mock_template3]
        mock_wtp.parse.return_value = mock_parsed
        
        count = self.wiki.count_templates_in_page("Page", "TargetTemplate")
        
        self.assertEqual(count, 2)


@unittest.skipUnless(PYWIKIBOT_AVAILABLE, "pywikibot not available")
class TestPywikibotWikiErrorHandling(unittest.TestCase):
    """Test error handling in PywikibotWiki."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_site = Mock()
        self.wiki = PywikibotWiki(site=self.mock_site)
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_get_request_page_content_error(self, mock_page_class):
        """Test handling error when getting page content."""
        mock_page_class.side_effect = Exception("Connection error")
        
        content = self.wiki.get_request_page_content("Some Page")
        
        self.assertEqual(content, "")
    
    @patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page')
    def test_has_template_error(self, mock_page_class):
        """Test handling error when checking template."""
        mock_page = Mock()
        mock_page.text = "content"
        mock_page_class.return_value = mock_page
        
        # Simulate error in parsing
        with patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.wtp.parse') as mock_parse:
            mock_parse.side_effect = Exception("Parse error")
            
            has_it = self.wiki.has_template("Page", "Template")
            
            self.assertFalse(has_it)
    
    def test_page_exists_error(self):
        """Test handling error when checking page existence."""
        with patch('tasks.photo_lab.infrastructure.wiki.pywikibot_wiki.pywikibot.Page') as mock_page_class:
            mock_page_class.side_effect = Exception("API error")
            
            exists = self.wiki.page_exists("Some Page")
            
            self.assertFalse(exists)
    
    def test_get_all_archive_pages_error(self):
        """Test handling error when getting archive pages."""
        self.mock_site.allpages.side_effect = Exception("API error")
        
        archives = self.wiki.get_all_archive_pages()
        
        self.assertEqual(archives, [])


if __name__ == '__main__':
    unittest.main()
