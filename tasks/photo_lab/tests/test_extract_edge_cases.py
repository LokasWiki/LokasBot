"""
Edge case tests for ExtractPendingRequests use case.
"""

import unittest

try:
    from tasks.photo_lab.domain.use_cases.extract_pending_requests import ExtractPendingRequests
    from tasks.photo_lab.tests.mock_wiki_repository import MockWikiRepository
    WIKITEXTPARSER_AVAILABLE = True
except ImportError:
    WIKITEXTPARSER_AVAILABLE = False


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestExtractPendingRequestsEdgeCases(unittest.TestCase):
    """Edge case tests for extracting requests."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ExtractPendingRequests(self.mock_repo)
    
    def test_template_with_whitespace(self):
        """Test template with extra whitespace."""
        content = "  {{طلب ورشة صور|  Page Name  }}  "
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)
        # wikitextparser should preserve whitespace in values
        self.assertEqual(requests[0].page_name, "Page Name")
    
    def test_template_with_newlines(self):
        """Test template with newlines in content."""
        content = """{{طلب ورشة صور|
Page Name
}}"""
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].page_name.strip(), "Page Name")
    
    def test_multiple_templates_same_page(self):
        """Test multiple requests for same page name."""
        content = """{{طلب ورشة صور|Same Page}}
{{طلب ورشة صور|Same Page}}
{{طلب ورشة صور|Same Page}}"""
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        # Should extract all three, even though they're duplicates
        self.assertEqual(len(requests), 3)
        for request in requests:
            self.assertEqual(request.page_name, "Same Page")
    
    def test_mixed_content(self):
        """Test page with mixed content types."""
        content = """== Heading ==

Some text here.

{{طلب ورشة صور|Page 1}}

More text with [[link]] and ''italics''.

{{Infobox|param=value}}

{{طلب ورشة صور|Page 2}}

* List item 1
* List item 2

{{طلب ورشة صور|Page 3}}"""
        
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 3)
        self.assertEqual(requests[0].page_name, "Page 1")
        self.assertEqual(requests[1].page_name, "Page 2")
        self.assertEqual(requests[2].page_name, "Page 3")
    
    def test_template_with_named_parameters(self):
        """Test template with named parameters."""
        # The implementation now handles named parameters too
        content = "{{طلب ورشة صور|name=Page Name}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        # Implementation now extracts value from named parameters
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].page_name, "Page Name")
    
    def test_empty_template_arguments(self):
        """Test template with empty argument."""
        content = "{{طلب ورشة صور|}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        if len(requests) > 0:
            self.assertEqual(requests[0].page_name, "")
    
    def test_template_without_arguments(self):
        """Test template without any arguments."""
        content = "{{طلب ورشة صور}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        # Should be skipped as there are no arguments
        self.assertEqual(len(requests), 0)
    
    def test_similar_template_names(self):
        """Test with similar but different template names."""
        content = """{{طلب ورشة صور|Valid Page}}
{{طلب ورشة صور أخرى|Invalid Page}}
{{طلب ورشة|Another Invalid}}
{{طلب ورشة صور/فرعي|Also Invalid}}"""
        
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        # Should only extract the exact match
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].page_name, "Valid Page")
    
    def test_unicode_page_names(self):
        """Test with various unicode characters in page names."""
        content = """{{طلب ورشة صور|صفحة عربية}}
{{طلب ورشة صور|Página española}}
{{طلب ورشة صور|中文页面}}
{{طلب ورشة صور|Русская страница}}
{{طلب ورشة صور|Page avec accents: éèà}}"""
        
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 5)
        self.assertEqual(requests[0].page_name, "صفحة عربية")
        self.assertEqual(requests[1].page_name, "Página española")
        self.assertEqual(requests[2].page_name, "中文页面")
        self.assertEqual(requests[3].page_name, "Русская страница")
        self.assertEqual(requests[4].page_name, "Page avec accents: éèà")
    
    def test_page_with_only_other_templates(self):
        """Test page with templates but no request templates."""
        content = """{{Infobox|name=Test}}
{{Stub}}
{{Cleanup}}
{{Citation needed}}"""
        
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 0)
    
    def test_very_long_page_content(self):
        """Test with very long page content."""
        # Create a long content with many requests
        templates = []
        for i in range(100):
            templates.append(f"{{{{طلب ورشة صور|Page {i}}}}}")
            templates.append("Some text here...")
        
        content = "\n".join(templates)
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 100)
    
    def test_nested_templates(self):
        """Test with nested templates."""
        content = "{{طلب ورشة صور|{{PAGENAME}}}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        # Should still extract, though the page name might include template markup
        self.assertEqual(len(requests), 1)
    
    def test_html_entities_in_content(self):
        """Test with HTML entities in content."""
        content = "{{طلب ورشة صور|Page & Name}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", content)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)


@unittest.skipUnless(WIKITEXTPARSER_AVAILABLE, "wikitextparser not available")
class TestExtractRequestParsing(unittest.TestCase):
    """Tests for request parsing details."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_repo = MockWikiRepository()
        self.use_case = ExtractPendingRequests(self.mock_repo)
    
    def test_preserves_full_template_text(self):
        """Test that full template text is preserved exactly."""
        template = "{{طلب ورشة صور|Test Page}}"
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", template)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].template_text, template)
    
    def test_preserves_multiline_template(self):
        """Test preservation of multiline template text."""
        template = """{{طلب ورشة صور|
Page Name
|param=value
}}"""
        self.mock_repo.add_page("ويكيبيديا:ورشة الصور/طلبات", template)
        
        requests = self.use_case.execute()
        
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].template_text, template)


if __name__ == '__main__':
    unittest.main()
