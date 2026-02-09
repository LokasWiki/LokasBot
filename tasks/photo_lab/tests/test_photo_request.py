"""
Unit tests for the PhotoRequest entity.
"""

import unittest

from tasks.photo_lab.domain.entities.photo_request import PhotoRequest


class TestPhotoRequest(unittest.TestCase):
    """Test cases for PhotoRequest entity."""
    
    def test_create_photo_request(self):
        """Test creating a photo request."""
        request = PhotoRequest(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        self.assertEqual(request.page_name, "Test Page")
        self.assertEqual(request.template_text, "{{طلب ورشة صور|Test Page}}")
        self.assertFalse(request.has_perspective)
        self.assertEqual(request.request_page_title, "ويكيبيديا:ورشة الصور/طلبات/Test Page")
    
    def test_request_page_title_auto_generation(self):
        """Test that request page title is auto-generated."""
        request = PhotoRequest(
            page_name="Example Article Name",
            template_text="{{طلب ورشة صور|Example Article Name}}"
        )
        
        self.assertEqual(
            request.request_page_title,
            "ويكيبيديا:ورشة الصور/طلبات/Example Article Name"
        )
    
    def test_mark_as_archivable(self):
        """Test marking a request as archivable."""
        request = PhotoRequest(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        self.assertFalse(request.is_ready_for_archive())
        
        request.mark_as_archivable()
        
        self.assertTrue(request.has_perspective)
        self.assertTrue(request.is_ready_for_archive())
    
    def test_str_representation(self):
        """Test string representation."""
        request = PhotoRequest(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        str_repr = str(request)
        self.assertIn("Test Page", str_repr)
        self.assertIn("no perspective", str_repr)
        
        request.mark_as_archivable()
        str_repr = str(request)
        self.assertIn("has perspective", str_repr)
    
    def test_repr(self):
        """Test detailed representation."""
        request = PhotoRequest(
            page_name="Test Page",
            template_text="{{طلب ورشة صور|Test Page}}"
        )
        
        repr_str = repr(request)
        self.assertIn("page_name", repr_str)
        self.assertIn("Test Page", repr_str)


if __name__ == '__main__':
    unittest.main()
